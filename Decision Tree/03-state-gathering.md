# 3. State Gathering Phase

## Overview

Before any framework application, executives must complete the **State Assessment Matrix**. This three-dimensional assessment ensures we understand the decision context before selecting a framework.

**Key Principle:** State before solution. Never apply a framework without first gathering context.

## Prerequisite: Problem Discovery

The Decision Tree assumes that a **Problem Statement** has already been developed through the **Problem Discovery Framework**. Problems should be discovered, prioritized through the EB-25 methodology, and crystallized into formal Problem Statements before entering the State Gathering phase.

**If you do not have a formal Problem Statement:**
1. Go to the **Problem Discovery** framework (see `../Problem Discovery/`)
2. Apply the EB-25 prioritization methodology
3. Complete Problem Identification to construct a solution-agnostic Problem Statement
4. Draft and finalize an RFC for the proposed solution
5. Return to the Decision Tree with the Problem Statement and RFC(s)

**Why This Prerequisite:**
- Prevents solution-first thinking
- Ensures executive time is spent on high-impact problems
- Provides structured solution options (RFCs) for evaluation
- Streamlines the decision-making process

## The Three-Dimensional Assessment

### Dimension A: Alignment Check

Alignment ensures cofounders agree on the problem statement before discussing solutions. 

#### Alignment Questions

| Question                                              | Assessment | Threshold          |
| ----------------------------------------------------- | ---------- | ------------------ |
| Are both cofounders aligned on the problem statement? | Yes/No     | Must be YES        |
| Do we share the same success metrics?                 | Yes/No     | Must be YES        |
| Are there hidden assumptions or unstated constraints? | Documented | Must be documented |
| Is this a values conflict or a tactical disagreement? | Identified | Must be identified |

#### Exit Conditions

- **If YES to all:** Proceed to Risk Assessment
- **If NO to any:** Use Alignment Resolution Protocol (see [06-special-protocols.md](./06-special-protocols.md))  

#### Common Alignment Issues

**Issue 1: Problem vs Solution Confusion**

- Symptom: Cofounders arguing about different problems
- Solution: Separate problem statement from solution discussion
- Protocol: Alignment Resolution Protocol

**Issue 2: Hidden Assumptions**

- Symptom: Agreement on surface, disagreement on details
- Solution: Explicitly document all assumptions
- Protocol: ASOFF framework with assumption tracking

**Issue 3: Values vs Tactical**

- Symptom: Fundamental disagreement on what matters
- Solution: Explicit values discussion before tactical discussion
- Protocol: STOP Protocol for values-based decisions

### Dimension B: Risk Assessment

Risk assessment quantifies the potential impact if the decision goes wrong.

#### Risk Categories

| Risk Category                | Low (1)                               | Medium (2)  | High (3)    | Critical (4) |
| ---------------------------- | ------------------------------------- | ----------- | ----------- | ------------ |
| **Financial impact**   | <$10K | $10K-$100K | $100K-$1M | >$1M |             |             |              |
| **Timeline impact**    | <1 week                               | 1-4 weeks   | 1-3 months  | >3 months    |
| **Team morale impact** | Minimal                               | Noticeable  | Significant | Severe       |
| **Customer impact**    | None                                  | Minor       | Moderate    | Major        |
| **Strategic impact**   | Tactical                              | Operational | Strategic   | Existential  |

#### Risk Score Calculation

Sum the scores across all five categories:

```
Risk Score = Financial + Timeline + Team + Customer + Strategic
```

**Risk Categories:**

- **Score 5-8:** Low-risk decision
- **Score 9-12:** Medium-risk decision
- **Score 13-16:** High-risk decision
- **Score 17-20:** Critical-risk decision

#### Risk Mitigation Considerations

For each risk domain, document:

1. **Probability:** How likely is this risk to materialize? (Low/Medium/High)
2. **Impact:** If it materializes, what's the severity? (Low/Medium/High)
3. **Mitigation:** What can we do to prevent or reduce this risk?
4. **Contingency:** If the risk materializes, what's our backup plan?

#### Example Risk Assessment

```
Decision: Hire first senior engineer

Financial: $150K salary + benefits = Medium (2)
Timeline: 3-4 month hiring process = Medium (2)
Team: High impact on team dynamics = High (3)
Customer: Indirect impact through better product = Low (1)
Strategic: Critical for product execution = High (3)

Risk Score: 2 + 2 + 3 + 1 + 3 = 11 (Medium Risk)
```

### Dimension C: Reversibility Check

Reversibility assesses how easy it is to undo the decision if needed.

#### Reversibility Factors

| Reversibility Factor                                   | Assessment     |
| ------------------------------------------------------ | -------------- |
| Can this decision be undone within 30 days?            | Yes/No         |
| What is the cost of reversal?                          | $ estimate     |
| What is the time cost of reversal?                     | Duration       |
| Are there irreversible commitments (contracts, hires)? | List           |
| Is this a one-way door or two-way door decision?       | Classification |

#### Reversibility Classification

**Type I (Two-way door):**

- Easily reversible
- Low cost (<$10K)
- Short time (<1 week)
- No irreversible commitments
- **Example:** Changing a software library, adjusting pricing slightly

**Type II (One-way door moderate):**

- Reversible with significant cost
- Medium cost ($10K-$100K)
- Medium time (1-4 weeks)
- Some commitments may need unwinding
- **Example:** Hiring a contractor, signing a 3-month office lease

**Type III (One-way door significant):**

- Difficult to reverse
- High cost ($100K-$1M)
- Long time (1-3 months)
- Significant commitments to unwind
- **Example:** Hiring a full-time employee, signing a 1-year contract

**Type IV (One-way door critical):**

- Nearly impossible to reverse
- Very high cost (>$1M)
- Very long time (>3 months)
- Major commitments
- **Example:** Raising capital, major product pivot, merger/acquisition

#### Reversibility Assessment Tips

**Tip 1: Consider Soft Costs**

- Reversal isn't just money - it's also reputation, team morale, customer trust
- Document soft costs alongside financial costs

**Tip 2: Consider Partial Reversal**

- Sometimes full reversal isn't possible, but partial mitigation is
- Document what partial reversal looks like

**Tip 3: Consider Opportunity Cost**

- Time spent reversing is time not spent on other priorities
- Include opportunity cost in reversal assessment

## Decision Context Card

Complete the Decision Context Card after state assessment. Use the template in [`./templates/decision-context-card.md`](./templates/decision-context-card.md).

### Card Structure

```markdown
## Decision Context Card

**Decision ID:** [AUTO-GENERATED: YYYY-MM-DD-SEQ]
**Date:** [DATE]
**Initiator:** [NAME]
**Decision Title:** [BRIEF TITLE]

### Alignment Status
- Problem Statement Alignment: [YES/NO/PARTIAL]
- Success Metric Alignment: [YES/NO/PARTIAL]
- Values vs Tactical: [VALUES/TACTICAL/BOTH]
- Alignment Notes: [FREE TEXT]

### Risk Assessment
- Risk Score: [X/20]
- Risk Category: [LOW/MEDIUM/HIGH/CRITICAL]
- Primary Risk Domains: [LIST]
- Risk Mitigation Considerations: [FREE TEXT]

### Reversibility Assessment
- Reversibility Type: [TYPE I/II/III/IV]
- Reversal Cost: [$ ESTIMATE]
- Reversal Time: [DURATION]
- Irreversible Commitments: [LIST/NONE]

### Preliminary Framework Recommendation
- Suggested Framework: [FRAMEWORK NAME]
- Rationale: [FREE TEXT]
```

## State Assessment Best Practices

### Practice 1: Independent Assessment First

Each cofounder should complete the state assessment independently before comparing notes.

**Why:**

- Prevents anchoring bias
- Reveals different perspectives
- Identifies blind spots
- Ensures thorough consideration

### Practice 2: Time Box the Assessment

State assessment should take 15-30 minutes for most decisions.

**Why:**

- Prevents over-analysis
- Forces prioritization
- Maintains momentum
- Respects cofounder time

### Practice 3: Document Disagreements

If cofounders disagree on state assessment, document the disagreement.

**Why:**

- Makes differences explicit
- Enables later resolution
- Provides audit trail
- Supports learning

### Practice 4: Use Data When Possible

Base assessments on objective data rather than gut feel.

**Why:**

- Reduces bias
- Enables comparison
- Supports justification
- Improves accuracy

## Common State Assessment Pitfalls

### Pitfall 1: Skipping to Solution

**Symptom:** Cofounders start discussing solutions before completing state assessment.

**Solution:** Enforce the process. No framework selection until state assessment is complete.

### Pitfall 2: Optimism Bias

**Symptom:** Underestimating risk or overestimating reversibility.

**Solution:** Use reference points from past decisions. Consider worst-case scenarios explicitly.

### Pitfall 3: Alignment Assumption

**Symptom:** Assuming alignment without verifying.

**Solution:** Explicitly answer alignment questions. Don't assume shared understanding.

### Pitfall 4: Vague Assessments

**Symptom:** Using terms like "significant" or "moderate" without definition.

**Solution:** Use the provided scoring matrices. Be specific with numbers and timeframes.

## State Assessment Examples

### Example 1: Low-Risk, Type I Decision

**Decision:** Switch from AWS to GCP for a non-critical service

**Alignment:**

- Problem statement: YES (both agree current service is expensive)
- Success metrics: YES (both agree cost reduction is goal)
- Values vs tactical: TACTICAL

**Risk Assessment:**

- Financial: $5K migration cost = Low (1)
- Timeline: 3 days = Low (1)
- Team: Minimal impact = Low (1)
- Customer: No impact = Low (1)
- Strategic: Tactical = Low (1)
- **Risk Score: 5 (Low Risk)**

**Reversibility:**

- Can undo in 30 days: YES
- Reversal cost: $5K
- Reversal time: 3 days
- Irreversible commitments: None
- **Type: Type I**

**Framework Recommendation:** 5-Minute Rule or ICE

### Example 2: Medium-Risk, Type II Decision

**Decision:** Hire first marketing lead

**Alignment:**

- Problem statement: YES (both agree need marketing expertise)
- Success metrics: PARTIAL (disagree on specific metrics)
- Values vs tactical: BOTH

**Risk Assessment:**

- Financial: $120K salary = Medium (2)
- Timeline: 2-3 months = Medium (2)
- Team: Noticeable impact = Medium (2)
- Customer: Minor impact = Low (1)
- Strategic: Operational = Medium (2)
- **Risk Score: 9 (Medium Risk)**

**Reversibility:**

- Can undo in 30 days: NO
- Reversal cost: $30K (severance + recruiting)
- Reversal time: 2-3 months
- Irreversible commitments: Employment contract
- **Type: Type II**

**Framework Recommendation:** ASOFF (due to partial alignment)

### Example 3: High-Risk, Type IV Decision

**Decision: Raise Series A funding**

**Alignment:**

- Problem statement: YES (both agree need capital)
- Success metrics: YES (both agree valuation and terms)
- Values vs tactical: VALUES (control vs growth)

**Risk Assessment:**

- Financial: $5M raise = Critical (4)
- Timeline: 4-6 months = High (3)
- Team: Significant impact = High (3)
- Customer: Moderate impact = Medium (2)
- Strategic: Existential = Critical (4)
- **Risk Score: 16 (High Risk)**

**Reversibility:**

- Can undo in 30 days: NO
- Reversal cost: Impossible
- Reversal time: Impossible
- Irreversible commitments: Investor contracts, board seats
- **Type: Type IV**

**Framework Recommendation:** STOP Protocol

## Next Steps

After completing the Decision Context Card:

1. **If alignment issues exist:** Use Alignment Resolution Protocol (see [06-special-protocols.md](./06-special-protocols.md))
2. **If alignment achieved:** Proceed to Framework Selection (see [04-framework-selection.md](./04-framework-selection.md))

---

**Next: [04-framework-selection.md](./04-framework-selection.md)**
