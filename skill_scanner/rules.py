"""Load detection rules from YAML configuration files."""

import yaml
from pathlib import Path

from .engine import Rule, Category, Severity


def load_rules_from_yaml(rules_dir: Path) -> list[Rule]:
    """Load all YAML rule files from a directory."""
    rules = []
    for yaml_file in sorted(rules_dir.glob("*.yaml")):
        rules.extend(_parse_rule_file(yaml_file))
    return rules


def _parse_rule_file(path: Path) -> list[Rule]:
    """Parse a single YAML rule file."""
    with open(path) as f:
        data = yaml.safe_load(f)

    if not data or "rules" not in data:
        return []

    rules = []
    for entry in data["rules"]:
        try:
            rule = Rule(
                rule_id=entry["id"],
                category=Category(entry["category"]),
                severity=Severity(entry["severity"]),
                title=entry["title"],
                description=entry["description"],
                patterns=entry.get("patterns", []),
                target=entry.get("target", "body"),
                condition=entry.get("condition", "any"),
            )
            rules.append(rule)
        except (KeyError, ValueError) as e:
            print(f"Warning: skipping malformed rule in {path}: {e}")

    return rules
