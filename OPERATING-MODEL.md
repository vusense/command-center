# Command Center — Operating Model

This document records **how Vusense will use** the Executive Decision Framework in this repository. It resolves the open threads from the framework review without replacing the framework docs themselves.

## Recommended direction (v1.0)

| Thread | Decision | Rationale |
| ------ | -------- | --------- |
| **Adoption** | **Mandatory two-gate flow** for all executive decisions (cofounder sign-off). Defined exceptions only (see below). | Preserves audit trail and problem-first discipline. |
| **Operationalize** | **Markdown + Git in this repo** is the system of record. Filled templates live under [`decisions/`](./decisions/) (see naming below). | Matches Obsidian vault; versioned; investor-ready. |
| **Harden docs** | Gap fixes in framework docs + this model (emergency path, RFC options rule, root index, Technical Stack bridge). | Reduces ambiguity before first live decision. |
| **Technical Stack bridge** | Platform/architecture decisions **must** enter via Problem Discovery when they meet executive-decision criteria ([`Technical Stack/00-decision-integration.md`](./Technical Stack/00-decision-integration.md)). | Keeps product context and decision process linked. |
| **Tooling** | **Phase 2** — no custom app in v1.0. Optional: Obsidian Dataview, git hooks, or Linear labels later. | Process proof before automation. |

## Who must use the gates

| Role | Gate 1 (Problem Discovery) | Gate 2 (Decision Tree) |
| ---- | -------------------------- | ------------------------ |
| Cofounders / executives | Required for sign-off decisions | Required |
| CTO (technical exec decisions) | Required when decision meets criteria in Technical Stack integration doc | Required |
| Engineering leads | May draft RFCs and problem captures; do not bypass finalized handoff | N/A without exec sign-off |
| Board / advisors | Input via RFC review or escalation; not day-to-day backlog owners | Escalation path only |

**Board visibility:** Completed decisions are copied or linked from [`decisions/`](./decisions/) into quarterly board packs (see Decision Tree [`08-documentation-due-diligence.md`](./Decision%20Tree/08-documentation-due-diligence.md)).

## Exceptions (bypass or compress Gate 1)

Full criteria: [`Problem Discovery/07-emergency-and-expedited.md`](./Problem%20Discovery/07-emergency-and-expedited.md).

| Situation | Gate 1 | Gate 2 |
| --------- | ------ | ------ |
| Standard executive decision | Full EB-25 → Problem Statement → RFC | Full meta-framework |
| **Expedited** (urgent, important, &lt;48h) | Compressed identification + single RFC with ≥3 options | Full or Emergency per risk |
| **Emergency** (&lt;4h harm if delayed) | Retroactive Problem Statement within 24h | Emergency Protocol; retroactive RFC within 48h if missing |

Bypass without retroactive documentation is **not permitted** for investor-facing or Type III/IV decisions.

## Operating rhythm

| Cadence | Activity | Owner |
| ------- | -------- | ----- |
| **Continuous** | Symptom capture to EB-25 raw backlog | Anyone |
| **Weekly** | EB-25 hygiene: promote/demote Top 5, enforce 25-item cap | CTO or designated exec |
| **Per Top-5 item** | Problem Identification + RFC lifecycle | Problem owner (exec sponsor) |
| **On handoff** | State Gathering within 5 business days | Cofounders |
| **Quarterly** | Framework review + success metrics check | Executive team |

## Artifact storage and naming

All live decision artifacts go under **`decisions/`**:

```
decisions/
  backlog/           # Active eb-25-backlog copies (optional symlink to template)
  problems/          # problem-statement-{id}.md
  rfcs/              # rfc-{id}.md (one file per RFC)
  active/            # In-flight decision context cards + framework worksheets
  register/          # Snapshots or exports of decision-register rows
  retrospections/    # Completed retrospection templates
```

**ID convention:** `YYYY-MM-DD-short-slug` (e.g. `2026-05-21-sdk-platform`).

Templates in `Problem Discovery/templates/` and `Decision Tree/templates/` remain **blank masters**; never edit masters in place for a live decision—copy into `decisions/`.

## Framework health metrics (lightweight v1.0)

Track quarterly in a single markdown table at [`decisions/register/framework-health.md`](./decisions/register/framework-health.md) (create on first use):

- EB-25 backlog count (target ≤25)
- Top 5 items with finalized RFCs ready for handoff
- Decisions completed in register vs bypassed without documentation
- Retrospection completion rate for mandatory frameworks
- Average days from RFC finalize to Decision Register entry

## Tooling roadmap (Phase 2 — not in scope now)

- Obsidian Dataview dashboards over `decisions/`
- PR-based RFC review for engineering-heavy RFCs
- Optional integration: RFC structure aligns with ADR-style records

## Related documents

- [README.md](./README.md) — repository index
- [Problem Discovery/](./Problem%20Discovery/) — Gate 1
- [Decision Tree/](./Decision%20Tree/) — Gate 2
- [Technical Stack/00-decision-integration.md](./Technical%20Stack/00-decision-integration.md) — when technical work enters the gates
- [examples/exemplar-sdk-platform.md](./examples/exemplar-sdk-platform.md) — golden-path pilot walkthrough

---

**Version:** 1.0 | **Date:** 2026-05-21 | **Next review:** Quarterly with framework docs
