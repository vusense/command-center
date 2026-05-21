# 5. RFC (Request for Comments) Methodology

## Overview

With a crystallized Problem Statement in hand, we now connect the problem to potential solutions using the **RFC (Request for Comments)** methodology. An RFC is a formal proposal for a solution, opened for peer review before any decision is made.

## Why RFCs?

* Decouples the person from the idea.
* Allows asynchronous, thoughtful critique.
* Forces solution providers to think deeply about trade-offs.

## The RFC Lifecycle

### 1. Draft

The author drafts the RFC proposing a solution to the formalized Problem Statement. The RFC outlines the proposed architecture/approach, costs, and known trade-offs.

### 2. Review (Comment Period)

The RFC is published to relevant stakeholders. Reviewers leave comments, ask clarifying questions, and point out edge cases.
*Reviewers are critiquing the proposal, not the person.*

### 3. Iterate

The author updates the RFC based on feedback. This may involve adding mitigation strategies for identified risks or pivoting the approach entirely.

### 4. Finalize

Once the comment period ends (typically 3-5 days) and the author has addressed the major critiques, the RFC is marked as "Finalized".
*Note: Finalized does not mean "Approved". It means it is ready for an executive decision.*

## Multiple RFCs vs multiple options in one RFC

| Pattern | Description |
| ------- | ------------- |
| **One RFC, ≥3 options** | Preferred default. Document options A / B / C (and optional “do nothing”) in §5 *Alternatives Considered* or §2 *Detailed Design*. Satisfies ASOFF without multiple files. |
| **Multiple RFCs** | Use when sponsors disagree on architecture enough that a single doc would be misleading. Each RFC should reference the same Problem Statement ID. |

**Handoff minimum:** ≥3 evaluable options across the package (see [06-handoff-to-decision.md](./06-handoff-to-decision.md#options-rule)).

**Emergency / expedited:** A single RFC may be finalized quickly if it lists ≥3 options with trade-offs; full multi-day review may follow after the decision (see [07-emergency-and-expedited.md](./07-emergency-and-expedited.md)).

*Complete the RFC using the template in `./templates/rfc.md`.*

---

**Next: [06-handoff-to-decision.md](./06-handoff-to-decision.md)**
