# Exemplar: Mobile SDK Platform Strategy

**Decision ID:** `2026-05-21-sdk-platform`  
**Status:** PILOT / EXAMPLE (not a recorded executive decision)  
**Purpose:** Golden-path walkthrough of Gate 1 → Gate 2 using real Vusense context from [Technical Stack/01-overview.md](../Technical%20Stack/01-overview.md).

---

## Gate 1 — Problem Discovery

### 1. EB-25 capture

**Symptom (raw backlog entry):**

> Engineering friction: two native codebases (`sdk-ios`, `sdk-android`) will duplicate secure capture, Enclave/Keystore integration, and ProofMode bundle logic. Onboarding for mobile engineers is slower than web. No customer blocker yet, but roadmap assumes both platforms in Q3.

**Eisenhower:** Important, Not Urgent → **Next 20** initially.

**Promotion to Top 5:** Promoted when Q3 SDK milestone added to roadmap; demoted “Office lease renewal research” to Next 20.

---

### 2. Problem identification (solution-agnostic)

**Problem ID:** `2026-05-21-sdk-platform`

| Field | Content |
| ----- | ------- |
| **Context** | Vusense edge attestation requires tamper-resistant capture and hardware-backed signing on iOS and Android ([02-architecture.md](../Technical%20Stack/02-architecture.md)). |
| **Friction** | Maintaining two native SDKs doubles implementation and test cost for identical trust guarantees; drift risk against `shared-protocol` / `attestation_schema.json`. |
| **Impact** | Slower feature parity across platforms; higher defect rate at trust boundaries; delayed enterprise pilots needing both stores. |
| **Constraints** | Must preserve Secure Enclave / Hardware Keystore usage; ProofMode compatibility; cannot weaken first-pass engine rules. |
| **Success criteria** | (1) Both platforms ship same attestation semantics within one release train. (2) ≤1.2× engineering effort vs single-platform baseline for next major feature. (3) No regression in jailbreak/root detection posture. |

**5 Whys (abbreviated):**

1. Why duplicate work? — Two repos (`sdk-ios`, `sdk-android`).
2. Why two repos? — Native stacks chosen for maximum hardware API access.
3. Why is duplication painful now? — Shared schema and identical edge flow mean most features are parallel copies.
4. Why not unify? — Unclear if cross-platform framework meets crypto/sensor requirements.
5. Root problem? — **We lack a decided platform strategy for the edge layer that balances trust requirements with delivery speed.**

---

### 3. RFC (single file, three options)

**RFC ID:** `rfc-2026-05-21-sdk-platform-a`  
**Status:** FINALIZED (example)

This exemplar uses **one RFC with three options** (satisfies handoff + ASOFF; see [Problem Discovery/05-rfc-methodology.md](../Problem%20Discovery/05-rfc-methodology.md)).

#### Option A — Dual native SDKs (status quo)

- **Pros:** Maximum control; best-documented HSM APIs; aligns with current repo plan.
- **Cons:** 2× feature cost; schema drift risk; slower hiring (need both skill sets).
- **Cost:** ~2 FTE-mobile ongoing | **Timeline:** Ongoing parallel workstreams

#### Option B — React Native + Expo with native modules

- **Pros:** Single product codebase; shared UI/demo; Expo C++ module path noted in overview.
- **Cons:** Bridge complexity for crypto; Expo release cadence risk; may need thin native shims per platform anyway.
- **Cost:** ~1.3 FTE-mobile + 0.5 FTE spike | **Timeline:** 6–8 week spike + migration

#### Option C — Kotlin Multiplatform / shared core + thin native shells

- **Pros:** Shared business logic; native UI/sensor layers remain thin.
- **Cons:** Smaller hiring pool; tooling maturity; still two store pipelines.
- **Cost:** ~1.5 FTE-mobile + 0.3 FTE spike | **Timeline:** 8–10 week spike

**Trade-offs documented:** Option B highest schedule risk for crypto; Option C medium risk; Option A lowest technical risk, highest ongoing cost.

---

### 4. Handoff checklist

- [x] Top 5 EB-25  
- [x] Solution-agnostic Problem Statement  
- [x] Finalized RFC with ≥3 options  
- [x] Objections captured as trade-offs  

→ Proceed to **Decision Tree / State Gathering**.

---

## Gate 2 — Decision Tree

### 1. Decision priority

| Question | Answer |
| -------- | ------ |
| Executive decision required now? | **Yes** — blocks repo creation and hiring profile |
| Can this wait a quarter? | **No** — Q3 milestone dependency |

### 2. Alignment check

| Question | Answer |
| -------- | ------ |
| Aligned on problem statement? | **Yes** (example) |
| Shared success metrics? | **Yes** — criteria from Problem Statement |
| Hidden assumptions documented? | **Yes** — e.g. “both app stores required v1” |
| Values vs tactical? | **Tactical** (delivery vs trust trade-off, not mission pivot) |

*Note:* Handoff does **not** guarantee alignment on **which option** — only on the problem. Option selection may still require ASOFF debate.

### 3. Risk assessment (illustrative)

| Category | Score | Rationale |
| -------- | ----- | --------- |
| Financial | 2 | Spike + redirect &lt;$100K |
| Timeline | 3 | 6–10 week critical path to Q3 |
| Team | 2 | Skill mix change |
| Customer | 2 | Pilot timing if slip |
| Strategic | 3 | Edge layer is core product |
| **Total** | **12** | **Medium risk** |

### 4. Reversibility

**Type II** — switching platform after 2–3 months of implementation costs $50K–$150K and 4–8 weeks (moderate one-way door).

### 5. Framework selection

| Input | Output |
| ----- | ------ |
| Alignment on problem: Yes | — |
| Risk 12, Type II, partial alignment on option possible | **ASOFF** |

### 6. ASOFF application (sketch)

| Step | Example action |
| ---- | -------------- |
| **Assess** | Import Problem Statement + link `rfc-2026-05-21-sdk-platform-a` |
| **Stake** | Cofounder A favors Option A; Cofounder B favors Option B with spike exit criteria |
| **Options** | Map Option A/B/C from RFC §5 into ASOFF Option 1/2/3 fields |
| **Filter** | Score against success criteria + trust constraints |
| **Finalize** | e.g. “Option B with 4-week spike; abort to A if Enclave parity not proven” |

Use template: [Decision Tree/templates/asoff-worksheet.md](../Decision%20Tree/templates/asoff-worksheet.md) in `decisions/active/`.

### 7. Record and retrospect

- Enter row in [decision-register.md](../Decision%20Tree/templates/decision-register.md) under `decisions/register/`
- **Retrospection:** Recommended after 90 days (did spike meet success criteria?)

---

## Outcome (example only)

> **Illustrative decision:** Run 4-week technical spike on Option B; parallel maintain Option A for one release if spike fails. Update `01-overview.md` and repo list after register entry.

Do not treat this outcome as an approved company decision.

---

## Files to create for a real run

| Artifact | Path |
| -------- | ---- |
| EB-25 backlog | `decisions/backlog/eb-25.md` |
| Problem Statement | `decisions/problems/2026-05-21-sdk-platform.md` |
| RFC | `decisions/rfcs/rfc-2026-05-21-sdk-platform-a.md` |
| Decision Context Card | `decisions/active/2026-05-21-sdk-platform-context.md` |
| ASOFF worksheet | `decisions/active/2026-05-21-sdk-platform-asoff.md` |

---

**See also:** [Technical Stack/00-decision-integration.md](../Technical%20Stack/00-decision-integration.md) | [OPERATING-MODEL.md](../OPERATING-MODEL.md)
