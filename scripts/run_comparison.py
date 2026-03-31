"""Run the multi-scanner comparison pipeline.

For each skill in the corpus:
1. Run skill-scanner (our tool)
2. Run semgrep (generic SAST baseline)
3. Run VirusTotal (if API key available)
4. Collect and aggregate results
"""

import json
import os
import subprocess
import hashlib
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from skill_scanner.cli import scan_path
from skill_scanner.engine import ScanResult


def run_skill_scanner(skill_path: Path) -> dict:
    """Run our scanner on a skill file."""
    results = scan_path(skill_path)
    if results:
        return results[0].to_dict()
    return {"error": "no results"}


def run_semgrep(skill_path: Path) -> dict:
    """Run semgrep with generic rules on a skill file."""
    try:
        result = subprocess.run(
            [
                "semgrep", "scan",
                "--config", "auto",
                "--json",
                "--quiet",
                str(skill_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode in (0, 1):  # 0=clean, 1=findings
            try:
                data = json.loads(result.stdout)
                return {
                    "findings": len(data.get("results", [])),
                    "results": data.get("results", [])[:20],  # Cap at 20
                    "errors": len(data.get("errors", [])),
                }
            except json.JSONDecodeError:
                return {"findings": 0, "raw": result.stdout[:500]}
        return {"error": f"semgrep exit {result.returncode}", "stderr": result.stderr[:500]}
    except FileNotFoundError:
        return {"error": "semgrep not installed"}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}


def run_virustotal(skill_path: Path, api_key: Optional[str] = None) -> dict:
    """Submit a skill file to VirusTotal for scanning."""
    if not api_key:
        api_key = os.environ.get("VT_API_KEY")
    if not api_key:
        return {"error": "no VT_API_KEY"}

    content = skill_path.read_bytes()
    file_hash = hashlib.sha256(content).hexdigest()

    # First check if already scanned
    try:
        req = urllib.request.Request(
            f"https://www.virustotal.com/api/v3/files/{file_hash}",
            headers={"x-apikey": api_key},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            return {
                "sha256": file_hash,
                "cached": True,
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "undetected": stats.get("undetected", 0),
                "harmless": stats.get("harmless", 0),
                "total_engines": sum(stats.values()),
            }
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return {"error": f"VT lookup failed: {e.code}"}

    # Upload file for scanning
    boundary = "----FormBoundary" + hashlib.md5(content[:100]).hexdigest()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{skill_path.name}"\r\n'
        f"Content-Type: text/markdown\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()

    try:
        req = urllib.request.Request(
            "https://www.virustotal.com/api/v3/files",
            data=body,
            headers={
                "x-apikey": api_key,
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            analysis_id = data.get("data", {}).get("id", "")

        # Poll for results (VT takes a few seconds)
        for _ in range(10):
            time.sleep(15)
            req = urllib.request.Request(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers={"x-apikey": api_key},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                status = data.get("data", {}).get("attributes", {}).get("status")
                if status == "completed":
                    stats = data["data"]["attributes"].get("stats", {})
                    return {
                        "sha256": file_hash,
                        "cached": False,
                        "malicious": stats.get("malicious", 0),
                        "suspicious": stats.get("suspicious", 0),
                        "undetected": stats.get("undetected", 0),
                        "harmless": stats.get("harmless", 0),
                        "total_engines": sum(stats.values()),
                    }

        return {"error": "VT analysis timed out", "analysis_id": analysis_id}
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return {"error": f"VT upload failed: {e}"}


def run_comparison(
    skills_dir: Path,
    output_path: Path,
    vt_api_key: Optional[str] = None,
    skip_vt: bool = False,
    skip_semgrep: bool = False,
) -> list[dict]:
    """Run all scanners on all skills in a directory."""
    skill_files = sorted(skills_dir.glob("*.md"))
    results = []

    for i, skill_path in enumerate(skill_files):
        print(f"[{i+1}/{len(skill_files)}] Scanning: {skill_path.name}")
        entry = {
            "skill_name": skill_path.stem,
            "skill_path": str(skill_path),
            "skill_scanner": run_skill_scanner(skill_path),
        }

        if not skip_semgrep:
            entry["semgrep"] = run_semgrep(skill_path)

        if not skip_vt:
            entry["virustotal"] = run_virustotal(skill_path, vt_api_key)
            time.sleep(15)  # VT rate limit: 4 requests/min on free tier
        else:
            entry["virustotal"] = {"skipped": True}

        results.append(entry)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    return results


def summarize_results(results: list[dict]) -> dict:
    """Generate summary statistics from comparison results."""
    summary = {
        "total_skills": len(results),
        "skill_scanner": {"total_findings": 0, "skills_with_findings": 0, "by_category": {}},
        "semgrep": {"total_findings": 0, "skills_with_findings": 0},
        "virustotal": {"total_detections": 0, "skills_with_detections": 0},
    }

    for r in results:
        # Skill scanner
        ss = r.get("skill_scanner", {})
        fc = ss.get("finding_count", 0)
        summary["skill_scanner"]["total_findings"] += fc
        if fc > 0:
            summary["skill_scanner"]["skills_with_findings"] += 1
        for f in ss.get("findings", []):
            cat = f.get("category", "unknown")
            summary["skill_scanner"]["by_category"][cat] = (
                summary["skill_scanner"]["by_category"].get(cat, 0) + 1
            )

        # Semgrep
        sg = r.get("semgrep", {})
        sg_fc = sg.get("findings", 0)
        summary["semgrep"]["total_findings"] += sg_fc
        if sg_fc > 0:
            summary["semgrep"]["skills_with_findings"] += 1

        # VirusTotal
        vt = r.get("virustotal", {})
        vt_mal = vt.get("malicious", 0) + vt.get("suspicious", 0)
        summary["virustotal"]["total_detections"] += vt_mal
        if vt_mal > 0:
            summary["virustotal"]["skills_with_detections"] += 1

    return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run multi-scanner comparison")
    parser.add_argument("--skills-dir", type=Path, required=True, help="Directory of skill .md files")
    parser.add_argument("--output", type=Path, default=Path("outputs/experiments/comparison_results.json"))
    parser.add_argument("--skip-vt", action="store_true", help="Skip VirusTotal (no API key)")
    parser.add_argument("--skip-semgrep", action="store_true", help="Skip semgrep")
    args = parser.parse_args()

    results = run_comparison(
        args.skills_dir,
        args.output,
        skip_vt=args.skip_vt,
        skip_semgrep=args.skip_semgrep,
    )

    summary = summarize_results(results)
    summary_path = args.output.parent / "comparison_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults: {args.output}")
    print(f"Summary: {summary_path}")
    print(json.dumps(summary, indent=2))
