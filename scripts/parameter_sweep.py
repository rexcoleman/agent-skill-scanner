"""Parameter sensitivity sweep per EXPERIMENTAL_DESIGN.md §10.

Sweeps:
1. Pattern matching: exact only vs fuzzy (simulated via rule subsets)
2. Minimum skill body length filter: 0, 50, 100, 200 chars
3. Detection category subsets (ablation): remove one category at a time
"""

import json
import copy
from pathlib import Path

from skill_scanner.parser import parse_skill_file
from skill_scanner.engine import DetectionEngine, Category
from skill_scanner.rules import load_rules_from_yaml
from skill_scanner.cli import find_skill_files

RULES_DIR = Path("rules")
SKILLS_DIR = Path("data/curated/skills")


def sweep_body_length(skill_files, engine):
    """Sweep minimum body length filter."""
    thresholds = [0, 50, 100, 200]
    results = {}

    for threshold in thresholds:
        total_findings = 0
        skills_flagged = 0
        for sf in skill_files:
            skill = parse_skill_file(sf)
            if len(skill.body.strip()) < threshold:
                continue
            result = engine.scan(skill)
            total_findings += result.finding_count
            if result.finding_count > 0:
                skills_flagged += 1

        results[threshold] = {
            "min_body_length": threshold,
            "skills_scanned": sum(1 for sf in skill_files if len(parse_skill_file(sf).body.strip()) >= threshold),
            "total_findings": total_findings,
            "skills_flagged": skills_flagged,
        }

    return results


def sweep_category_ablation(skill_files, all_rules):
    """Remove one detection category at a time and measure impact."""
    categories = list(Category)
    results = {}

    # Full detection (baseline)
    engine = DetectionEngine()
    engine.load_rules(all_rules)
    baseline_findings = 0
    baseline_flagged = 0
    for sf in skill_files:
        skill = parse_skill_file(sf)
        result = engine.scan(skill)
        baseline_findings += result.finding_count
        if result.finding_count > 0:
            baseline_flagged += 1

    results["baseline"] = {
        "removed": "none",
        "total_findings": baseline_findings,
        "skills_flagged": baseline_flagged,
    }

    # Ablate each category
    for cat in categories:
        ablated_rules = [r for r in all_rules if r.category != cat]
        engine = DetectionEngine()
        engine.load_rules(ablated_rules)

        total_findings = 0
        skills_flagged = 0
        for sf in skill_files:
            skill = parse_skill_file(sf)
            result = engine.scan(skill)
            total_findings += result.finding_count
            if result.finding_count > 0:
                skills_flagged += 1

        drop = baseline_findings - total_findings
        results[cat.value] = {
            "removed": cat.value,
            "rules_removed": sum(1 for r in all_rules if r.category == cat),
            "total_findings": total_findings,
            "skills_flagged": skills_flagged,
            "findings_drop": drop,
            "drop_pct": round(drop / baseline_findings * 100, 1) if baseline_findings > 0 else 0,
        }

    return results


def sweep_rule_subsets(skill_files, all_rules):
    """Test with different rule subset sizes (simulates pattern library depth)."""
    results = {}
    n_rules = len(all_rules)

    for pct in [25, 50, 75, 100]:
        n = max(1, int(n_rules * pct / 100))
        subset = all_rules[:n]
        engine = DetectionEngine()
        engine.load_rules(subset)

        total_findings = 0
        skills_flagged = 0
        for sf in skill_files:
            skill = parse_skill_file(sf)
            result = engine.scan(skill)
            total_findings += result.finding_count
            if result.finding_count > 0:
                skills_flagged += 1

        results[f"{pct}pct"] = {
            "rule_pct": pct,
            "n_rules": n,
            "total_findings": total_findings,
            "skills_flagged": skills_flagged,
        }

    return results


def main():
    skill_files = find_skill_files(SKILLS_DIR)
    all_rules = load_rules_from_yaml(RULES_DIR)

    engine = DetectionEngine()
    engine.load_rules(all_rules)

    print("=== Parameter Sensitivity Sweep ===\n")

    # 1. Body length threshold
    print("1. Minimum body length filter")
    body_results = sweep_body_length(skill_files, engine)
    for k, v in body_results.items():
        print(f"   threshold={k:>3}: {v['skills_scanned']} skills, {v['total_findings']} findings, {v['skills_flagged']} flagged")
    print()

    # 2. Category ablation
    print("2. Category ablation (remove one at a time)")
    ablation_results = sweep_category_ablation(skill_files, all_rules)
    for k, v in ablation_results.items():
        if k == "baseline":
            print(f"   baseline:              {v['total_findings']} findings, {v['skills_flagged']} flagged")
        else:
            print(f"   remove {k:25}: {v['total_findings']} findings ({v['drop_pct']:+.1f}% drop), {v['skills_flagged']} flagged")
    print()

    # 3. Rule subset size
    print("3. Rule library size sweep")
    subset_results = sweep_rule_subsets(skill_files, all_rules)
    for k, v in subset_results.items():
        print(f"   {v['rule_pct']}% rules ({v['n_rules']:>2}): {v['total_findings']} findings, {v['skills_flagged']} flagged")
    print()

    # Robustness assessment
    print("4. Robustness Assessment")
    # Check if findings are stable across body length thresholds
    findings_range = [v["total_findings"] for v in body_results.values()]
    body_robust = max(findings_range) - min(findings_range) <= 5
    print(f"   Body length: {'ROBUST' if body_robust else 'SENSITIVE'} (range: {min(findings_range)}-{max(findings_range)})")

    # Check which category removal has biggest impact
    max_drop_cat = max(
        [(k, v["drop_pct"]) for k, v in ablation_results.items() if k != "baseline"],
        key=lambda x: x[1]
    )
    print(f"   Most impactful category: {max_drop_cat[0]} ({max_drop_cat[1]}% of findings)")

    # Check if 50% rules still catches most findings
    half_findings = subset_results["50pct"]["total_findings"]
    full_findings = subset_results["100pct"]["total_findings"]
    rule_robust = half_findings >= full_findings * 0.6
    print(f"   Rule library: {'ROBUST' if rule_robust else 'SENSITIVE'} (50% rules catches {half_findings}/{full_findings})")

    # Save all results
    output = {
        "body_length_sweep": body_results,
        "category_ablation": ablation_results,
        "rule_subset_sweep": subset_results,
        "robustness": {
            "body_length_robust": body_robust,
            "most_impactful_category": max_drop_cat[0],
            "most_impactful_drop_pct": max_drop_cat[1],
            "rule_library_robust": rule_robust,
        },
    }
    out_path = Path("outputs/experiments/parameter_sweep.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
