# 7. Emergency and Expedited Paths

## Overview

The standard Problem Discovery flow (EB-25 → identification → RFC → handoff) assumes **days, not hours**. Real incidents still require executive action. This document defines **when Gate 1 may be compressed or completed retroactively**, and how that connects to the Decision Tree **Emergency Protocol**.

**Key principle:** Speed is allowed; **documentation debt is not forgiven** for high-stakes decisions.

## When to use which path

| Path | Time pressure | Gate 1 | Gate 2 | Retroactive docs |
| ---- | ------------- | ------ | ------ | ---------------- |
| **Standard** | None | Full | Full | N/A |
| **Expedited** | Important + urgent; decision needed within ~48h | Compressed (below) | Per state assessment; Emergency only if &lt;4h | Problem Statement within 24h; RFC finalized within 48h |
| **Emergency** | Material harm if delayed &gt;4h | Minimal capture + retroactive full Gate 1 | [Emergency Protocol](../02-decision-tree/06-special-protocols.md) | Problem Statement within 24h; RFC or post-hoc options doc within 48h |

## Expedited Problem Discovery

### Eligibility

All must be true:

- Problem is **Important** on the Eisenhower matrix (would enter EB-25 if time allowed)
- Delay beyond 48h causes measurable harm (customer, security, legal, or existential)
- Executive sponsor approves expedited label in writing (Slack/email OK; copy into backlog notes)

### Compressed steps

1. **EB-25:** Log item; may temporarily exceed Top 5 only for this item with explicit demotion of lowest Top-5 item documented in backlog notes
2. **Problem Identification:** 30–60 minute session; solution-agnostic Problem Statement required **before** executive decision when possible
3. **RFC:** **One** finalized RFC that includes **≥3 distinct options** in §5 Alternatives Considered (or §2 as sub-options A/B/C) — satisfies ASOFF option count without three separate files
4. **Handoff:** Proceed to Decision Tree when Problem Statement exists and RFC is Draft/Finalized with options documented

### Not eligible for expedited

- Type IV / STOP-level strategic pivots (use standard or Emergency with full STOP)
- Problems that are Not Important (delegate or delete)
- Avoid-list items resurfacing without Eisenhower re-qualification

## Emergency Problem Discovery

### Eligibility

Aligns with Decision Tree Emergency Protocol:

- Decision required within **4 hours**
- Delay causes **significant harm**
- No time for standard or expedited RFC review window

### Minimum before decision (15 minutes)

Capture in backlog or incident note:

- Symptom and timestamp
- Who is affected
- Provisional problem statement (may include solution language — **must be rewritten** within 24h)
- Why standard/expedited path was impossible

### After decision (mandatory)

| Artifact | Deadline |
| -------- | -------- |
| Solution-agnostic Problem Statement | 24 hours |
| RFC **or** emergency options memo (≥3 options, trade-offs, risks) | 48 hours |
| Decision Context Card + framework worksheet | Per Emergency Protocol (24h) |
| Retrospection | 48 hours |

Add row to Decision Register marking `EMERGENCY` and linking retroactive Problem Discovery artifacts.

## EB-25 during crisis

- **Do not** grow backlog above 25 during emergency; log to incident channel first, formalize into EB-25 during retroactive window
- After resolution, **reconcile** Top 5 within one weekly hygiene cycle

## Symmetry with Decision Tree

| Decision Tree | Problem Discovery |
| ------------- | ----------------- |
| Emergency Protocol (&lt;4h) | Emergency path (this doc) |
| Alignment Resolution | If problem statement disputed retroactively, run Alignment Resolution before closing register |
| STOP / Type IV | Standard Gate 1 only — no expedited/emergency skip |

## Navigation

- **Previous:** [06-handoff-to-decision.md](./06-handoff-to-decision.md)
- **Operating Model:** [../../README.md#operating-model](../../README.md#operating-model)
- **Decision Tree emergency:** [../02-decision-tree/06-special-protocols.md](../02-decision-tree/06-special-protocols.md)

---

**Next:** Return to [Gate 1 README](./README.md), [repository hub](../../README.md), or [03-problem-discovery.md](./03-problem-discovery.md)
