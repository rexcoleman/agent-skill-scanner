"""E0 Sanity Validation Tests — must pass before E1 experiments."""

import json
import pytest
from pathlib import Path

from skill_scanner.parser import parse_skill_file
from skill_scanner.engine import DetectionEngine, Category, Severity
from skill_scanner.rules import load_rules_from_yaml
from skill_scanner.cli import scan_path

RULES_DIR = Path(__file__).parent.parent / "rules"
SYNTHETIC_DIR = Path(__file__).parent.parent / "data" / "synthetic"


@pytest.fixture
def engine():
    eng = DetectionEngine()
    rules = load_rules_from_yaml(RULES_DIR)
    eng.load_rules(rules)
    return eng


# ── E0a: Positive control ──────────────────────────────────────


class TestE0aPositiveControl:
    """Scanner MUST detect known-malicious patterns in synthetic malicious skill."""

    def test_positive_control_has_findings(self):
        results = scan_path(SYNTHETIC_DIR / "e0a_positive_control.md")
        assert len(results) == 1
        r = results[0]
        assert r.finding_count > 0, "Positive control must produce findings"

    def test_detects_prompt_injection(self):
        results = scan_path(SYNTHETIC_DIR / "e0a_positive_control.md")
        categories = {f.category for f in results[0].findings}
        assert Category.PROMPT_INJECTION in categories, "Must detect prompt injection"

    def test_detects_data_exfiltration(self):
        results = scan_path(SYNTHETIC_DIR / "e0a_positive_control.md")
        categories = {f.category for f in results[0].findings}
        assert Category.DATA_EXFILTRATION in categories, "Must detect data exfiltration"

    def test_detects_capability_escalation(self):
        results = scan_path(SYNTHETIC_DIR / "e0a_positive_control.md")
        categories = {f.category for f in results[0].findings}
        assert Category.CAPABILITY_ESCALATION in categories, "Must detect capability escalation"

    def test_max_severity_is_critical(self):
        results = scan_path(SYNTHETIC_DIR / "e0a_positive_control.md")
        assert results[0].max_severity == Severity.CRITICAL


# ── E0b: Negative control ──────────────────────────────────────


class TestE0bNegativeControl:
    """Scanner must NOT false-positive on a clean skill."""

    def test_negative_control_clean(self):
        results = scan_path(SYNTHETIC_DIR / "e0b_negative_control.md")
        assert len(results) == 1
        r = results[0]
        # Allow INFO findings; no HIGH or CRITICAL
        high_findings = [
            f for f in r.findings if f.severity in (Severity.CRITICAL, Severity.HIGH)
        ]
        assert len(high_findings) == 0, (
            f"Clean skill should have no HIGH/CRITICAL findings, got: "
            f"{[(f.rule_id, f.evidence[:60]) for f in high_findings]}"
        )

    def test_official_skills_low_fp_rate(self):
        """Official OpenClaw skills should have a low false positive rate."""
        official_dir = Path.home() / "openclaw" / "skills"
        if not official_dir.exists():
            pytest.skip("OpenClaw repo not cloned")

        results = scan_path(official_dir)
        total_skills = len(results)
        skills_with_critical = sum(
            1 for r in results
            if any(f.severity == Severity.CRITICAL for f in r.findings)
        )
        # Accept up to 15% FP rate on official skills for CRITICAL findings
        fp_rate = skills_with_critical / total_skills if total_skills > 0 else 0
        assert fp_rate <= 0.15, (
            f"FP rate {fp_rate:.1%} exceeds 15% threshold on official skills. "
            f"Skills with CRITICAL: {skills_with_critical}/{total_skills}"
        )


# ── E0c: Dose-response ─────────────────────────────────────────


class TestE0cDoseResponse:
    """Detection should correlate with injection sophistication."""

    LEVELS = [
        ("e0c_level1_obvious.md", "obvious"),
        ("e0c_level2_moderate.md", "moderate"),
        ("e0c_level3_subtle.md", "subtle"),
        ("e0c_level4_stealthy.md", "stealthy"),
        ("e0c_level5_advanced.md", "advanced"),
    ]

    def test_all_levels_detected(self):
        """Scanner should find SOMETHING at every sophistication level."""
        for filename, label in self.LEVELS:
            results = scan_path(SYNTHETIC_DIR / filename)
            assert len(results) == 1
            assert results[0].finding_count > 0, (
                f"Level '{label}' ({filename}) produced 0 findings — "
                f"scanner fails to detect at this sophistication level"
            )

    def test_obvious_has_most_findings(self):
        """Most obvious injection should produce the most findings."""
        counts = []
        for filename, label in self.LEVELS:
            results = scan_path(SYNTHETIC_DIR / filename)
            counts.append((label, results[0].finding_count))

        obvious_count = counts[0][1]
        # Level 1 should have >= as many findings as any other level
        for label, count in counts[1:]:
            assert obvious_count >= count, (
                f"Obvious level ({obvious_count} findings) should have >= "
                f"{label} level ({count} findings)"
            )

    def test_severity_trend(self):
        """More sophisticated attacks should still be detected but may have lower max severity."""
        severities = []
        severity_rank = {
            Severity.CRITICAL: 4, Severity.HIGH: 3,
            Severity.MEDIUM: 2, Severity.LOW: 1, Severity.INFO: 0,
        }
        for filename, label in self.LEVELS:
            results = scan_path(SYNTHETIC_DIR / filename)
            max_sev = results[0].max_severity
            rank = severity_rank.get(max_sev, -1) if max_sev else -1
            severities.append((label, rank, max_sev))

        # At minimum, level 1 should be CRITICAL/HIGH
        assert severities[0][1] >= 3, (
            f"Obvious injection should be HIGH or CRITICAL, got {severities[0][2]}"
        )


# ── Parser tests ────────────────────────────────────────────────


class TestParser:
    """Verify SKILL.md parsing handles real OpenClaw format."""

    def test_parse_positive_control(self):
        skill = parse_skill_file(SYNTHETIC_DIR / "e0a_positive_control.md")
        assert skill.name == "totally-legit-helper"
        assert "curl" in skill.required_bins
        assert "nc" in skill.required_bins
        assert "sudo" in skill.required_bins
        assert len(skill.code_blocks) > 0
        assert len(skill.urls) > 0

    def test_parse_negative_control(self):
        skill = parse_skill_file(SYNTHETIC_DIR / "e0b_negative_control.md")
        assert skill.name == "file-organizer"
        assert "mkdir" in skill.required_bins
        assert "mv" in skill.required_bins

    def test_parse_official_skill(self):
        """Parse a real OpenClaw official skill."""
        github_skill = Path.home() / "openclaw" / "skills" / "github" / "SKILL.md"
        if not github_skill.exists():
            pytest.skip("OpenClaw repo not cloned")
        skill = parse_skill_file(github_skill)
        assert skill.name == "github"
        assert "gh" in skill.required_bins


# ── Rule loading tests ──────────────────────────────────────────


class TestRuleLoading:
    """Verify rules load correctly from YAML."""

    def test_load_all_rules(self):
        rules = load_rules_from_yaml(RULES_DIR)
        assert len(rules) > 0, "No rules loaded"

    def test_all_categories_covered(self):
        rules = load_rules_from_yaml(RULES_DIR)
        categories = {r.category for r in rules}
        expected = {
            Category.PROMPT_INJECTION,
            Category.DATA_EXFILTRATION,
            Category.CAPABILITY_ESCALATION,
            Category.ENCODED_PAYLOAD,
            Category.COMPOSITION_RISK,
        }
        assert categories == expected, f"Missing categories: {expected - categories}"

    def test_rule_ids_unique(self):
        rules = load_rules_from_yaml(RULES_DIR)
        ids = [r.rule_id for r in rules]
        assert len(ids) == len(set(ids)), f"Duplicate rule IDs: {[x for x in ids if ids.count(x) > 1]}"
