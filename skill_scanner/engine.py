"""Detection engine — runs rules against parsed skill files."""

import re
import base64
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from .parser import SkillFile


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Category(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    CAPABILITY_ESCALATION = "capability_escalation"
    DATA_EXFILTRATION = "data_exfiltration"
    ENCODED_PAYLOAD = "encoded_payload"
    COMPOSITION_RISK = "composition_risk"


@dataclass
class Finding:
    """A single security finding in a skill file."""

    rule_id: str
    category: Category
    severity: Severity
    title: str
    description: str
    evidence: str
    line_number: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence[:200],  # Truncate long evidence
            "line_number": self.line_number,
        }


@dataclass
class ScanResult:
    """Complete scan result for a skill file."""

    skill_path: str
    skill_name: str
    findings: list = field(default_factory=list)
    error: Optional[str] = None

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    @property
    def max_severity(self) -> Optional[Severity]:
        if not self.findings:
            return None
        severity_order = [
            Severity.CRITICAL,
            Severity.HIGH,
            Severity.MEDIUM,
            Severity.LOW,
            Severity.INFO,
        ]
        for s in severity_order:
            if any(f.severity == s for f in self.findings):
                return s
        return None

    def to_dict(self) -> dict:
        return {
            "skill_path": self.skill_path,
            "skill_name": self.skill_name,
            "finding_count": self.finding_count,
            "max_severity": self.max_severity.value if self.max_severity else None,
            "findings": [f.to_dict() for f in self.findings],
            "error": self.error,
        }


@dataclass
class Rule:
    """A detection rule loaded from YAML config."""

    rule_id: str
    category: Category
    severity: Severity
    title: str
    description: str
    patterns: list = field(default_factory=list)  # Regex patterns
    target: str = "body"  # "body", "frontmatter", "full_text", "code_blocks", "urls"
    condition: str = "any"  # "any" (OR) or "all" (AND)


class DetectionEngine:
    """Runs detection rules against parsed skill files."""

    def __init__(self):
        self.rules: list[Rule] = []
        self._compiled: dict[str, list[re.Pattern]] = {}

    def load_rules(self, rules: list[Rule]) -> None:
        self.rules = rules
        self._compiled = {}
        for rule in rules:
            self._compiled[rule.rule_id] = [
                re.compile(p, re.IGNORECASE | re.DOTALL) for p in rule.patterns
            ]

    def scan(self, skill: SkillFile) -> ScanResult:
        """Scan a skill file against all loaded rules."""
        result = ScanResult(
            skill_path=str(skill.path),
            skill_name=skill.name or skill.path.stem,
        )

        for rule in self.rules:
            findings = self._check_rule(rule, skill)
            result.findings.extend(findings)

        # Run built-in detectors (not pattern-based)
        result.findings.extend(self._detect_encoded_payloads(skill))
        result.findings.extend(self._detect_capability_escalation(skill))

        return result

    def _get_target_text(self, rule: Rule, skill: SkillFile) -> str:
        if rule.target == "body":
            return skill.body
        elif rule.target == "frontmatter":
            return skill.raw_frontmatter
        elif rule.target == "full_text":
            return skill.full_text
        elif rule.target == "code_blocks":
            return "\n".join(skill.code_blocks)
        elif rule.target == "urls":
            return "\n".join(skill.urls)
        return skill.full_text

    def _check_rule(self, rule: Rule, skill: SkillFile) -> list[Finding]:
        """Check a single rule against a skill file."""
        target_text = self._get_target_text(rule, skill)
        if not target_text:
            return []

        compiled_patterns = self._compiled[rule.rule_id]
        matches = []

        for pattern in compiled_patterns:
            for match in pattern.finditer(target_text):
                matches.append(match)

        if rule.condition == "all" and len(matches) < len(compiled_patterns):
            return []

        if not matches:
            return []

        findings = []
        seen_evidence = set()
        for match in matches:
            evidence = match.group(0)[:200]
            if evidence in seen_evidence:
                continue
            seen_evidence.add(evidence)

            line_number = target_text[: match.start()].count("\n") + 1
            findings.append(
                Finding(
                    rule_id=rule.rule_id,
                    category=rule.category,
                    severity=rule.severity,
                    title=rule.title,
                    description=rule.description,
                    evidence=evidence,
                    line_number=line_number,
                )
            )

        return findings

    def _detect_encoded_payloads(self, skill: SkillFile) -> list[Finding]:
        """Detect base64-encoded content that decodes to suspicious strings."""
        findings = []
        b64_pattern = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")
        suspicious_decoded = [
            "http", "curl", "wget", "eval", "exec", "import os",
            "subprocess", "socket", "/bin/sh", "/bin/bash",
            "ignore previous", "system prompt", "<script",
        ]

        for match in b64_pattern.finditer(skill.full_text):
            candidate = match.group(0)
            try:
                decoded = base64.b64decode(candidate).decode("utf-8", errors="replace")
                for sus in suspicious_decoded:
                    if sus.lower() in decoded.lower():
                        findings.append(
                            Finding(
                                rule_id="ENC-001",
                                category=Category.ENCODED_PAYLOAD,
                                severity=Severity.HIGH,
                                title="Base64-encoded suspicious content",
                                description=f"Base64 string decodes to content containing '{sus}'",
                                evidence=f"Encoded: {candidate[:60]}... Decoded contains: {sus}",
                                line_number=skill.full_text[: match.start()].count("\n") + 1,
                            )
                        )
                        break
            except Exception:
                continue

        return findings

    def _detect_capability_escalation(self, skill: SkillFile) -> list[Finding]:
        """Detect skills requesting capabilities beyond their stated scope."""
        findings = []

        # Check if skill requests dangerous bins not implied by its description
        dangerous_bins = {
            "sudo", "su", "docker", "kubectl", "ssh", "scp",
            "aws", "gcloud", "az", "terraform",
            "rm", "dd", "mkfs", "fdisk",
            "nc", "ncat", "netcat", "nmap", "tcpdump",
        }

        requested_dangerous = set(skill.required_bins) & dangerous_bins
        if requested_dangerous:
            # Check if the skill description justifies these capabilities
            desc_lower = (skill.description + " " + skill.name).lower()
            unjustified = []
            for bin_name in requested_dangerous:
                # Simple heuristic: if the binary name or its domain isn't
                # mentioned in the description, it may be escalation
                related_terms = {
                    "sudo": ["root", "admin", "elevated", "privilege", "sudo"],
                    "docker": ["container", "docker", "image"],
                    "kubectl": ["kubernetes", "k8s", "cluster", "kubectl"],
                    "ssh": ["remote", "ssh", "server"],
                    "aws": ["aws", "amazon", "cloud", "s3"],
                    "gcloud": ["google", "gcp", "cloud"],
                    "terraform": ["terraform", "infrastructure", "iac"],
                    "nc": ["network", "netcat", "socket", "listen"],
                    "nmap": ["scan", "port", "network", "nmap"],
                }
                terms = related_terms.get(bin_name, [bin_name])
                if not any(t in desc_lower for t in terms):
                    unjustified.append(bin_name)

            if unjustified:
                findings.append(
                    Finding(
                        rule_id="CAP-010",
                        category=Category.CAPABILITY_ESCALATION,
                        severity=Severity.HIGH,
                        title="Skill requests dangerous binaries not justified by description",
                        description=f"Skill requests {unjustified} but description doesn't mention related functionality",
                        evidence=f"Required bins: {skill.required_bins}, Unjustified: {unjustified}",
                    )
                )

        return findings
