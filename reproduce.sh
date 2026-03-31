#!/usr/bin/env bash
# reproduce.sh — Reproduce all experiments for agent-skill-scanner
# Usage: bash reproduce.sh [--skip-download]
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=== Agent Skill Security Scanner — Reproduce ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%S%z)"
echo ""

# Verify lock_commit
grep -q "lock_commit.*TO BE SET\|lock_commit.*PENDING" EXPERIMENTAL_DESIGN.md && echo "FAIL: lock_commit not set" && exit 1
echo "PASS: lock_commit verified"

# Install
pip install -e ".[dev]" -q
echo "PASS: skill-scanner installed"

# E0: Sanity validation
echo ""
echo "--- E0: Sanity Validation ---"
python -m pytest tests/ -v
echo "PASS: E0 complete"

# Download skills (skip if already present)
if [ ! -d "data/curated/skills" ] || [ "$(ls data/curated/skills/*.md 2>/dev/null | wc -l)" -lt 40 ]; then
    if [ "${1:-}" != "--skip-download" ]; then
        echo ""
        echo "--- Downloading curated skills ---"
        python scripts/download_skills.py
    else
        echo "SKIP: --skip-download flag set"
    fi
fi

# E1: Comparison pipeline
echo ""
echo "--- E1: Scanner Comparison ---"
python scripts/run_comparison.py \
    --skills-dir data/curated/skills \
    --skip-vt \
    --output outputs/experiments/comparison_with_semgrep.json

echo ""
echo "--- E1: Official Skills ---"
python3 -c "
from skill_scanner.cli import scan_path
from pathlib import Path
import json

results = scan_path(Path.home() / 'openclaw' / 'skills')
output = [r.to_dict() for r in results]
with open('outputs/experiments/official_skills_comparison.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f'Official: {len(results)} skills, {sum(r.finding_count for r in results)} findings')
"

# Generate figures
echo ""
echo "--- Generating figures ---"
python scripts/generate_figures.py 2>/dev/null || echo "WARN: figure generation skipped (matplotlib not installed)"

echo ""
echo "=== Reproduction complete ==="
echo "Results in: outputs/experiments/"
