"""Parse OpenClaw SKILL.md files into structured representations."""

import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SkillFile:
    """Parsed representation of an OpenClaw SKILL.md file."""

    path: Path
    name: str = ""
    description: str = ""
    raw_frontmatter: str = ""
    frontmatter: dict = field(default_factory=dict)
    body: str = ""
    required_bins: list = field(default_factory=list)
    required_env: list = field(default_factory=list)
    install_packages: list = field(default_factory=list)
    code_blocks: list = field(default_factory=list)
    urls: list = field(default_factory=list)

    @property
    def full_text(self) -> str:
        return self.raw_frontmatter + "\n" + self.body


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CODE_BLOCK_RE = re.compile(r"```(?:\w+)?\s*\n(.*?)```", re.DOTALL)
URL_RE = re.compile(
    r"https?://[^\s\)\]\}>\"'`]+",
)


def parse_skill_file(path: Path) -> SkillFile:
    """Parse a SKILL.md file into a SkillFile object."""
    text = path.read_text(encoding="utf-8", errors="replace")
    skill = SkillFile(path=path)

    # Extract YAML frontmatter
    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        skill.raw_frontmatter = fm_match.group(1)
        skill.body = text[fm_match.end() :]
        _parse_frontmatter(skill)
    else:
        skill.body = text

    # Extract code blocks
    skill.code_blocks = CODE_BLOCK_RE.findall(text)

    # Extract URLs
    skill.urls = URL_RE.findall(text)

    return skill


def _parse_frontmatter(skill: SkillFile) -> None:
    """Parse frontmatter — handles both YAML and JSON-in-YAML formats."""
    raw = skill.raw_frontmatter

    # Extract name
    name_match = re.search(r"^name:\s*(.+)$", raw, re.MULTILINE)
    if name_match:
        skill.name = name_match.group(1).strip().strip("\"'")

    # Extract description
    desc_match = re.search(r"^description:\s*(.+)$", raw, re.MULTILINE)
    if desc_match:
        skill.description = desc_match.group(1).strip().strip("\"'")

    # Try to parse the metadata block — OpenClaw uses JSON-in-YAML
    metadata_match = re.search(
        r"metadata:\s*\n\s*(\{.*?\})\s*$", raw, re.DOTALL | re.MULTILINE
    )
    if metadata_match:
        try:
            # Clean JSON (remove trailing commas, fix formatting)
            json_str = metadata_match.group(1)
            # Remove trailing commas before } or ]
            json_str = re.sub(r",\s*([}\]])", r"\1", json_str)
            metadata = json.loads(json_str)
            skill.frontmatter = metadata
            _extract_openclaw_metadata(skill, metadata)
        except json.JSONDecodeError:
            pass

    # Fallback: try simple YAML-style parsing for requires
    if not skill.required_bins:
        bins_match = re.search(
            r'"?bins"?\s*:\s*\[([^\]]+)\]', raw
        )
        if bins_match:
            skill.required_bins = [
                b.strip().strip("\"'") for b in bins_match.group(1).split(",")
            ]

        any_bins_match = re.search(
            r'"?anyBins"?\s*:\s*\[([^\]]+)\]', raw
        )
        if any_bins_match:
            skill.required_bins.extend(
                b.strip().strip("\"'") for b in any_bins_match.group(1).split(",")
            )

    if not skill.required_env:
        env_match = re.search(
            r'"?env"?\s*:\s*\[([^\]]+)\]', raw
        )
        if env_match:
            skill.required_env = [
                e.strip().strip("\"'") for e in env_match.group(1).split(",")
            ]


def _extract_openclaw_metadata(skill: SkillFile, metadata: dict) -> None:
    """Extract structured fields from OpenClaw metadata."""
    oc = metadata.get("openclaw", {})
    requires = oc.get("requires", {})

    skill.required_bins = requires.get("bins", [])
    if "anyBins" in requires:
        skill.required_bins.extend(requires["anyBins"])
    skill.required_env = requires.get("env", [])

    for installer in oc.get("install", []):
        pkg = installer.get("package") or installer.get("formula", "")
        if pkg:
            skill.install_packages.append(pkg)
