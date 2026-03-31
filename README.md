# agent-skill-scanner

> Last updated: 2026-03-31

Scan agent skill files for security vulnerabilities. 22 detection rules across prompt injection, capability escalation, data exfiltration, encoded payloads, and composition risks.

Built for [OpenClaw](https://github.com/openclaw) and Model Context Protocol (MCP) skill files. Generic SAST tools (semgrep, CodeQL) produce zero detections on these formats because they lack rules for markdown-embedded code and YAML skill definitions. This scanner fills that gap.

## Install

```bash
pip install agent-skill-scanner
```

## Usage

Scan a directory of skill files:

```bash
agent-skill-scan scan --path ./skills/
```

Example output:

```
Skill                                    Findings Severity
--------------------------------------------------------------
anti-injection-skill                            9 CRITICAL
askhuman                                        3 CRITICAL
azure-devops                                    1 HIGH
curl-http                                       3 CRITICAL
deploy-agent                                    0 CLEAN
--------------------------------------------------------------
TOTAL                                          16

Scanned 5 skills, 16 findings.

Findings by category:
  prompt_injection: 6
  capability_escalation: 5
  data_exfiltration: 3
  encoded_payload: 2
```

### Options

```bash
agent-skill-scan scan --path ./skills/ --output json    # JSON output for CI
agent-skill-scan scan --path ./skills/ --quiet          # Exit code only (0=clean, 1=findings)
agent-skill-scan scan --path ./skills/ --min-severity HIGH  # Filter by severity
agent-skill-scan scan --path ./skill.md                 # Scan a single file
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | No HIGH or CRITICAL findings |
| 1 | HIGH or CRITICAL findings detected |

## What it detects

22 rules across 5 categories:

| Category | Rules | Examples |
|----------|-------|---------|
| **Prompt injection** | 5 | System prompt override, role hijacking, instruction injection |
| **Capability escalation** | 5 | Privilege escalation commands, shell spawning, persistence mechanisms |
| **Data exfiltration** | 4 | Credential access, environment variable reads, outbound data transfer |
| **Encoded payloads** | 4 | Base64 encoded commands, hex payloads, obfuscated strings |
| **Composition risks** | 4 | Unrestricted tool chaining, cross-skill data flow, trust boundary violations |

## How it works

The scanner parses agent skill files (SKILL.md, MCP tool definitions, YAML configs with `name:`/`description:` frontmatter) and runs pattern-based detection against code blocks, full text, and structured fields. Rules are defined in YAML and can be extended.

## Research

This scanner was built from findings in the [agent-skill-scanner research project](https://github.com/rexcoleman/agent-skill-scanner/blob/master/FINDINGS.md). The core finding: generic SAST tools produce zero detections on agent skill files (McNemar chi2=9.09, p=0.003). The gap is structural — no existing rules target markdown/YAML skill formats.

## Limitations

- Pattern-based detection only — no semantic analysis or LLM-powered reasoning
- Designed for OpenClaw SKILL.md and MCP tool definitions — may miss formats from other agent frameworks
- Rules cover known attack patterns from published research, not zero-days
- False positives possible on skills that legitimately use system commands

## Also available as a GitHub Action

Add agent-skill-scanner to your CI pipeline:

```yaml
- uses: rexcoleman/agent-skill-scan-action@v1
  with:
    path: './skills/'
```

See [agent-skill-scan-action](https://github.com/rexcoleman/agent-skill-scan-action) for full documentation.

## Also available as an MCP server

Use agent-skill-scanner in Claude Code:

See [agent-skill-scan-mcp](https://github.com/rexcoleman/agent-skill-scan-mcp) for setup instructions.

## License

[MIT](LICENSE) — Rex Coleman, 2026

More research at [rexcoleman.dev](https://rexcoleman.dev).
