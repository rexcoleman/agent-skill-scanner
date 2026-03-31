"""Generate figures for FINDINGS and blog post."""

import json
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not installed. Generating text-based figures only.")


OUTPUT_DIR = Path("outputs/figures")


def load_results():
    """Load comparison results."""
    with open("outputs/experiments/comparison_with_semgrep.json") as f:
        curated = json.load(f)
    return curated


def generate_detection_gap_chart(results):
    """Bar chart: skill-scanner vs semgrep detection counts."""
    ss_count = sum(r["skill_scanner"]["finding_count"] for r in results)
    sg_count = sum(r.get("semgrep", {}).get("findings", 0) for r in results)

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(["skill-scanner\n(purpose-built)", "semgrep\n(generic SAST)"],
                      [ss_count, sg_count],
                      color=["#2563eb", "#94a3b8"], edgecolor="black", linewidth=0.5)
        ax.set_ylabel("Total Findings (45 curated skills)", fontsize=12)
        ax.set_title("Detection Gap: Purpose-Built vs Generic SAST\non Agent Skill Files", fontsize=14)
        ax.bar_label(bars, fontsize=14, fontweight="bold")
        ax.set_ylim(0, max(ss_count, 1) * 1.2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "detection_gap.png", dpi=150)
        plt.close()
        print(f"  Saved: {OUTPUT_DIR}/detection_gap.png")
    else:
        print(f"  skill-scanner: {ss_count} findings")
        print(f"  semgrep:       {sg_count} findings")
        print(f"  Gap: {ss_count - sg_count} ({100 if sg_count == 0 else round((ss_count-sg_count)/ss_count*100)}%)")


def generate_category_breakdown(results):
    """Horizontal bar chart: findings by detection category."""
    categories = {}
    for r in results:
        for f in r["skill_scanner"].get("findings", []):
            cat = f["category"]
            categories[cat] = categories.get(cat, 0) + 1

    if not categories:
        return

    cats = sorted(categories.items(), key=lambda x: x[1])
    labels = [c[0].replace("_", " ").title() for c in cats]
    values = [c[1] for c in cats]

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = {
            "Data Exfiltration": "#ef4444",
            "Prompt Injection": "#f59e0b",
            "Capability Escalation": "#8b5cf6",
            "Encoded Payload": "#06b6d4",
            "Composition Risk": "#22c55e",
        }
        bar_colors = [colors.get(l, "#94a3b8") for l in labels]
        bars = ax.barh(labels, values, color=bar_colors, edgecolor="black", linewidth=0.5)
        ax.set_xlabel("Number of Findings", fontsize=12)
        ax.set_title("Findings by Detection Category\n(45 curated OpenClaw skills)", fontsize=14)
        ax.bar_label(bars, fontsize=12, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "category_breakdown.png", dpi=150)
        plt.close()
        print(f"  Saved: {OUTPUT_DIR}/category_breakdown.png")
    else:
        for l, v in zip(labels, values):
            print(f"  {l}: {v}")


def generate_fp_analysis(results):
    """Stacked bar: true concerns vs likely FPs in curated skills."""
    true_concern = 0
    likely_fp = 0

    for r in results:
        for f in r["skill_scanner"].get("findings", []):
            # Heuristic: EXFIL on curated skills with legitimate service URLs are likely FPs
            # CAP and INJ findings are more likely genuine
            if f["category"] in ("prompt_injection", "capability_escalation", "encoded_payload"):
                true_concern += 1
            elif f["category"] == "data_exfiltration":
                likely_fp += 1
            else:
                likely_fp += 1

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.bar(["skill-scanner\nfindings"], [true_concern], label="Likely genuine concern",
               color="#ef4444", edgecolor="black", linewidth=0.5)
        ax.bar(["skill-scanner\nfindings"], [likely_fp], bottom=[true_concern],
               label="Likely false positive\n(legitimate API calls)",
               color="#fbbf24", edgecolor="black", linewidth=0.5)
        ax.set_ylabel("Number of Findings", fontsize=12)
        ax.set_title("The FP Boundary Problem\nin Agent Skill Scanning", fontsize=14)
        ax.legend(loc="upper right")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "fp_boundary.png", dpi=150)
        plt.close()
        print(f"  Saved: {OUTPUT_DIR}/fp_boundary.png")
    else:
        print(f"  Likely genuine: {true_concern}")
        print(f"  Likely FP (API calls): {likely_fp}")
        print(f"  Total: {true_concern + likely_fp}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = load_results()

    print("Generating figures...")
    generate_detection_gap_chart(results)
    generate_category_breakdown(results)
    generate_fp_analysis(results)
    print("Done.")


if __name__ == "__main__":
    main()
