"""CLI entry point for skill-scanner."""

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_skill_file
from .engine import DetectionEngine, ScanResult, Severity
from .rules import load_rules_from_yaml


DEFAULT_RULES_DIR = Path(__file__).parent / "rules"


def find_skill_files(path: Path) -> list[Path]:
    """Find all SKILL.md files under a directory, or treat path as a single file."""
    if path.is_file():
        return [path]

    skill_files = list(path.rglob("SKILL.md"))
    # Also match .md files that look like skill definitions
    for md_file in path.rglob("*.md"):
        if md_file.name != "SKILL.md" and md_file not in skill_files:
            # Check if it has frontmatter with name/description
            try:
                head = md_file.read_text(encoding="utf-8", errors="replace")[:500]
                if head.startswith("---") and ("name:" in head or "description:" in head):
                    skill_files.append(md_file)
            except OSError:
                continue

    return sorted(skill_files)


def scan_path(
    path: Path,
    rules_dir: Path = DEFAULT_RULES_DIR,
) -> list[ScanResult]:
    """Scan a path (file or directory) and return results."""
    engine = DetectionEngine()
    rules = load_rules_from_yaml(rules_dir)
    engine.load_rules(rules)

    skill_files = find_skill_files(path)
    results = []

    for skill_path in skill_files:
        try:
            skill = parse_skill_file(skill_path)
            result = engine.scan(skill)
        except Exception as e:
            result = ScanResult(
                skill_path=str(skill_path),
                skill_name=skill_path.stem,
                error=str(e),
            )
        results.append(result)

    return results


def format_table(results: list[ScanResult]) -> str:
    """Format results as a human-readable table."""
    lines = []
    lines.append(f"{'Skill':<40} {'Findings':>8} {'Severity':<10}")
    lines.append("-" * 62)

    for r in results:
        severity = r.max_severity.value if r.max_severity else "CLEAN"
        lines.append(f"{r.skill_name:<40} {r.finding_count:>8} {severity:<10}")

    total_findings = sum(r.finding_count for r in results)
    lines.append("-" * 62)
    lines.append(f"{'TOTAL':<40} {total_findings:>8}")
    lines.append(f"\nScanned {len(results)} skills, {total_findings} findings.")

    # Summary by category
    category_counts: dict[str, int] = {}
    for r in results:
        for f in r.findings:
            cat = f.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

    if category_counts:
        lines.append("\nFindings by category:")
        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {cat}: {count}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        prog="skill-scanner",
        description="Detect security threats in agent skill files",
    )
    subparsers = parser.add_subparsers(dest="command")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan skill files for security issues")
    scan_parser.add_argument("--path", "-p", type=Path, required=True, help="Path to skill file or directory")
    scan_parser.add_argument("--rules", "-r", type=Path, default=DEFAULT_RULES_DIR, help="Path to rules directory")
    scan_parser.add_argument("--output", "-o", choices=["json", "table"], default="table", help="Output format")
    scan_parser.add_argument("--min-severity", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"], default="INFO", help="Minimum severity to report")
    scan_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output, exit code only (0=clean, 1=findings)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "scan":
        results = scan_path(args.path, args.rules)

        # Filter by min severity
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
        min_idx = severity_order.index(args.min_severity)
        for r in results:
            r.findings = [
                f for f in r.findings
                if severity_order.index(f.severity.value) <= min_idx
            ]

        if not args.quiet:
            if args.output == "json":
                print(json.dumps([r.to_dict() for r in results], indent=2))
            else:
                print(format_table(results))

        # Exit code: 1 if any HIGH or CRITICAL findings
        if any(
            f.severity in (Severity.CRITICAL, Severity.HIGH)
            for r in results
            for f in r.findings
        ):
            sys.exit(1)


if __name__ == "__main__":
    main()
