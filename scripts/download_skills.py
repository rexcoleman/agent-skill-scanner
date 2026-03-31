"""Download skill files from GitHub for the benchmark corpus."""

import json
import time
import urllib.request
import urllib.error
from pathlib import Path


def download_curated_skills(
    manifest_path: Path,
    output_dir: Path,
    delay: float = 0.5,
) -> dict:
    """Download SKILL.md files for curated skills from GitHub."""
    with open(manifest_path) as f:
        manifest = json.load(f)

    output_dir.mkdir(parents=True, exist_ok=True)
    results = {"downloaded": 0, "failed": 0, "skipped": 0, "details": []}

    for skill in manifest:
        url = skill.get("github_raw_url")
        if not url:
            results["skipped"] += 1
            results["details"].append({
                "skill_name": skill["skill_name"],
                "status": "skipped",
                "reason": "no github_raw_url",
            })
            continue

        out_file = output_dir / f"{skill['skill_name']}.md"
        if out_file.exists():
            results["downloaded"] += 1
            results["details"].append({
                "skill_name": skill["skill_name"],
                "status": "cached",
            })
            continue

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="replace")

            out_file.write_text(content)
            results["downloaded"] += 1
            results["details"].append({
                "skill_name": skill["skill_name"],
                "status": "downloaded",
                "size": len(content),
            })
            print(f"  OK: {skill['skill_name']} ({len(content)} bytes)")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            results["failed"] += 1
            results["details"].append({
                "skill_name": skill["skill_name"],
                "status": "failed",
                "error": str(e),
            })
            print(f"  FAIL: {skill['skill_name']}: {e}")

        time.sleep(delay)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("data/curated/sample_manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("data/curated/skills"))
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    print(f"Downloading skills from manifest: {args.manifest}")
    results = download_curated_skills(args.manifest, args.output, args.delay)
    print(f"\nDone: {results['downloaded']} downloaded, {results['failed']} failed, {results['skipped']} skipped")

    summary_path = args.output.parent / "download_results.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {summary_path}")
