# HYPOTHESIS REGISTRY

<!-- version: 1.0 -->
<!-- created: 2026-03-31 -->

> **Authority hierarchy:** OpenClaw docs + VirusTotal API docs (Tier 1) > Prior art papers (Tier 2) > SE-146 playbook (Tier 3) > This document (Contract)
> **Conflict rule:** When a higher-tier document and this contract disagree, the higher tier wins. Flag the conflict in the DECISION_LOG.
> **Upstream:** DATA_CONTRACT (skill corpus), EXPERIMENTAL_DESIGN (design decisions)
> **Downstream:** EXPERIMENT_CONTRACT (experiment design), FINDINGS (hypothesis resolution narratives)

## Pre-Registration Lock

**Lock commit (lock_commit):** `6aa582c`
**Lock date:** 2026-03-31

> **Temporal gate (LL-74):** All hypotheses must be committed and locked before any experimental results are generated. Any experiment output with a git timestamp before the lock commit is invalid.

---

## 1) Pre-Registration Protocol

Hypotheses MUST be written **before** Phase 1 experiments begin.

**Gate:** >= 3 hypotheses registered and committed to version control before any experiment script is executed.

**Enforcement:**
- The hypothesis registry file MUST have a git commit timestamp earlier than any experiment output file.
- Adding hypotheses after seeing results is an academic integrity violation.
- Amendments to existing hypotheses MUST be tracked via `CONTRACT_CHANGE` commits with justification.

---

## 2) Hypothesis Format

Each hypothesis includes: hypothesis_id, statement, falsification_criterion, metric, resolution, evidence.

---

## 3) Registry Table

| hypothesis_id | statement | falsification_criterion | metric | resolution | evidence |
|---------------|-----------|------------------------|--------|------------|----------|
| H-1 | Purpose-built skill-scanner detects >20% more security threats in OpenClaw SKILL.md files than VirusTotal file scan API, measured on an identical 100-skill corpus. | Skill-scanner detection rate is <= VirusTotal detection rate + 20pp on the 100-skill corpus. | `(skill_scanner_detections - vt_detections) / total_union_detections > 0.20` | PENDING | — |
| H-2 | The detection rate gap between skill-scanner and VirusTotal concentrates in semantic threat categories (prompt injection, capability escalation) rather than payload-based categories (encoded payloads, data exfiltration). | Gap in semantic categories is <= gap in payload-based categories. | `G(semantic) > G(payload)` where `G(c) = \|D_ss(c) \ D_vt(c)\| / \|D_ss(c) ∪ D_vt(c)\|` | PENDING | — |
| H-3 | Generic static analysis (semgrep with default + security rulesets) detects <10% of agent-specific threats that the purpose-built scanner catches. | semgrep detects >=10% of the threats that skill-scanner catches. | `\|D_semgrep ∩ D_ss\| / \|D_ss\| < 0.10` | PENDING | — |
| H-4 | VirusTotal's Code Insight (LLM-based analysis) does NOT close the detection gap for prompt injection patterns in SKILL.md files. | VT Code Insight flags >80% of prompt injection patterns that skill-scanner catches. | `\|D_vt_codeinsight(injection) ∩ D_ss(injection)\| / \|D_ss(injection)\| < 0.80` | PENDING | — |
| H-5 (exploratory) | There is no significant positive correlation between OpenClaw skill popularity (install count or star count) and vulnerability rate. | Significant positive correlation exists (p < 0.05, r > 0.3). | Pearson/Spearman correlation between popularity metric and per-skill vulnerability count. | PENDING | — |

---

## 4) Resolution Protocol

| Resolution | Criteria |
|------------|----------|
| **SUPPORTED** | Metric meets or exceeds the stated threshold across all specified conditions |
| **REFUTED** | Metric falls below the stated threshold |
| **INCONCLUSIVE** | Ambiguous results, insufficient data, or metric within noise margin (+/-1 std of threshold) |

**Resolution rules:**
- Every hypothesis MUST be resolved before Phase 3 begins.
- The `evidence` field MUST reference a specific output file path and the exact metric value.
- INCONCLUSIVE resolutions MUST include a brief explanation.
- Resolutions are final once committed.

---

## 5) Acceptance Criteria

- [x] >= 3 hypotheses registered before Phase 1
- [x] All hypotheses follow the required format (all 6 fields populated)
- [ ] All hypotheses resolved (no PENDING status at project end)
- [ ] Every resolution includes an evidence reference to a specific output file
- [ ] No hypothesis was added after experiment results were observed (verified by git timestamps)
- [ ] Resolution narrative for each hypothesis included in FINDINGS.md

---

## 6) Surprise Detection Criteria

Pre-registered surprises that would warrant investigation if observed:

| Surprise | Detection Condition | Follow-up |
|----------|-------------------|-----------|
| VT Code Insight already catches most injection | H-4 REFUTED (VT catches >80% of injection) | Investigate Code Insight methodology; test on increasingly subtle injection |
| Popularity correlates with vulnerability | H-5 REFUTED (r > 0.3, p < 0.05) | Investigate causal mechanism — more contributors = more attack surface? Or more scrutiny? |
| semgrep catches more than expected | H-3 REFUTED (semgrep >10% overlap) | Identify which semgrep rules match; these are not agent-specific threats |
| Scanner has HIGH false positive rate | >30% of scanner findings are false positives per manual review | Refine pattern library; report FPR prominently in findings |
