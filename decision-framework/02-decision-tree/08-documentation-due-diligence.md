# 8. Documentation and Investor Due Diligence

## Overview

This document establishes documentation standards for the decision meta-framework. Proper documentation ensures auditability, supports investor due diligence, and enables continuous improvement.

**Key Principle:** If it's not documented, it didn't happen. Documentation is not optional.

## Decision Register

### Purpose

The Decision Register is the master record of all executive decisions. It provides:

- Complete history of executive decisions
- Pattern analysis capability
- Investor due diligence support
- Audit trail for governance

### Register Structure

| Decision ID | Date | Title | Framework | Risk Level | Reversibility | Outcome | Status |
|-------------|------|-------|-----------|------------|---------------|---------|--------|
| YYYY-MM-DD-001 | 2026-05-18 | Hire first engineer | ASOFF | Medium | Type II | Successful | Complete |
| YYYY-MM-DD-002 | 2026-05-20 | Pivot to B2B focus | STOP | Critical | Type IV | In Progress | Active |
| YYYY-MM-DD-003 | 2026-05-25 | Switch CRM tool | 5-Minute Rule | Low | Type I | Successful | Complete |

### Register Maintenance

**Update Frequency:**
- Add new decisions immediately after framework application
- Update outcomes as decisions are implemented
- Archive completed decisions quarterly

**Access Control:**
- Executives: Read/write access
- Board: Read access
- Advisors: Read access (if granted)
- Employees: No access

**Storage:**
- Version-controlled repository
- Secure location with access logging
- Regular backups
- Immutable records (no editing after sign-off)

**Template:** [`./templates/decision-register.md`](./templates/decision-register.md)

### Decision ID Format

**Format:** YYYY-MM-DD-SEQ

**Example:** 2026-05-18-001

**Rules:**
- YYYY: Four-digit year
- MM: Two-digit month
- DD: Two-digit day
- SEQ: Three-digit sequence number (resets daily)

## Investor Due Diligence Package

### Package Purpose

When investors request due diligence, provide a comprehensive package that demonstrates:

- Structured decision-making process
- Executive team maturity
- Governance capabilities
- Risk management approach

### Package Contents

#### 1. Executive Summary (1-2 pages)

**Contents:**
- Overview of decision meta-framework
- Key principles and philosophy
- Framework selection approach
- Documentation standards
- Recent decision highlights

**Purpose:** Provide high-level understanding for investors.

#### 2. Framework Documentation (this document set)

**Contents:**
- Complete framework documentation
- Framework descriptions and selection logic
- Process documentation
- Governance structure

**Purpose:** Demonstrate systematic approach to decision-making.

#### 3. Sample Decision Records (3-5 representative decisions)

**Selection Criteria:**
- Include different framework types
- Include different risk levels
- Include different outcomes (success and learning)
- Include recent decisions (last 6 months)

**Redaction:**
- Remove sensitive commercial information
- Remove personal cofounder disagreements
- Retain framework application and outcomes
- Preserve process integrity

**Purpose:** Provide concrete examples of framework application.

#### 4. Decision Register (sanitized)

**Contents:**
- Complete decision register
- All decisions with framework, risk, reversibility
- Outcomes and status
- Sanitized to remove sensitive information

**Redaction:**
- Remove specific financial amounts
- Remove customer names
- Remove sensitive strategic details
- Retain decision types and outcomes

**Purpose:** Demonstrate decision-making patterns and history.

#### 5. Retrospection Summary (last 12 months)

**Contents:**
- Summary of all retrospections
- Framework performance metrics
- Process improvements implemented
- Lessons learned

**Redaction:**
- Remove specific decision details
- Retain aggregate metrics and insights
- Remove cofounder-specific feedback

**Purpose:** Demonstrate continuous improvement capability.

#### 6. Framework Performance Metrics (last 12 months)

**Contents:**
- Framework usage statistics
- Decision success rates
- Cofounder satisfaction scores
- Time investment accuracy

**Purpose:** Demonstrate framework effectiveness.

### Package Assembly

**Timeline:** 5-7 business days

**Process:**
1. Identify decisions for sample records
2. Redact sensitive information
3. Assemble executive summary
4. Review package for completeness
5. Both cofounders approve package
6. Deliver to investors

**Quality Checklist:**
- [ ] All 6 components included
- [ ] Redaction complete and consistent
- [ ] Executive summary clear and concise
- [ ] Sample decisions representative
- [ ] Decision register sanitized
- [ ] Retrospection summary comprehensive
- [ ] Performance metrics accurate
- [ ] Both cofounders approved

### Redaction Policy

**What to Redact:**
- Specific financial amounts (use ranges)
- Customer names and details
- Sensitive strategic information
- Personal cofounder disagreements
- Proprietary technology details
- Competitive intelligence

**What to Retain:**
- Framework application process
- Decision types and categories
- Risk and reversibility assessments
- Framework selection rationale
- Outcomes and lessons learned
- Process improvements

**Redaction Standard:**
- Redaction must be consistent across all documents
- Redaction must preserve process integrity
- Redaction must not obscure framework effectiveness
- Redaction must be approved by both cofounders

## Audit Trail Requirements

### For Type III/IV Decisions

**Minimum Documentation:**

1. **Decision Context Card**
   - Alignment assessment
   - Risk assessment
   - Reversibility assessment
   - Framework recommendation

2. **Framework Application Template**
   - Complete framework template
   - All sections filled
   - Sign-off from both cofounders

3. **Sign-off**
   - Explicit agreement or dissent
   - Date and signature
   - Comments if applicable

4. **Retrospection** (if mandatory)
   - Complete retrospection template
   - Action items
   - Framework adjustments

5. **Escalation Documentation** (if applicable)
   - Escalation trigger
   - External input received
   - Final resolution

### For Type I/II Decisions

**Minimum Documentation:**

1. **Decision Context Card**
   - Basic state assessment
   - Framework recommendation

2. **Framework Application Template**
   - Complete framework template
   - Sign-off from both cofounders

3. **Decision Register Entry**
   - Decision ID, date, title
   - Framework used
   - Outcome and status

### Storage Requirements

**Version Control:**
- All documents in version-controlled repository
- Immutable after sign-off
- Version history retained

**Security:**
- Secure storage with access logging
- Encryption at rest
- Regular backups
- Access limited to authorized personnel

**Retention:**
- Permanent retention (company lifetime)
- No document deletion
- Archive old decisions quarterly

**Backup:**
- Daily automated backups
- Off-site backup storage
- Backup restoration testing
- Backup access logging

## Documentation Standards

### File Naming Conventions

**Decision Records:**
- Format: `DECISION-[ID]-[TITLE].md`
- Example: `DECISION-2026-05-18-001-hire-first-engineer.md`

**Retrospections:**
- Format: `RETRO-[ID]-[DATE].md`
- Example: `RETRO-2026-05-18-001-2026-05-25.md`

**Framework Applications:**
- Format: `FRAMEWORK-[FRAMEWORK]-[ID].md`
- Example: `FRAMEWORK-ASOFF-2026-05-18-001.md`

### Document Structure

**Standard Header:**
```markdown
# [Document Title]

**Decision ID:** [ID]
**Date:** [DATE]
**Framework:** [FRAMEWORK]
**Status:** [STATUS]
```

**Standard Footer:**
```markdown
---

**Document Control**
- Created: [DATE]
- Last Modified: [DATE]
- Version: [X.X]
- Author: [NAME]

**Sign-off**
- Cofounder A: [NAME/SIGNATURE] - [DATE]
- Cofounder B: [NAME/SIGNATURE] - [DATE]
```

### Documentation Quality

**Clarity:**
- Use clear, concise language
- Avoid jargon when possible
- Define acronyms on first use
- Use consistent terminology

**Completeness:**
- Fill all template sections
- No blank fields
- Explain "N/A" responses
- Provide rationale for decisions

**Accuracy:**
- Ensure data is correct
- Verify calculations
- Cross-reference related documents
- Update documents when information changes

**Consistency:**
- Use consistent formatting
- Use consistent terminology
- Follow templates exactly
- Maintain version control

## Common Documentation Mistakes

### Mistake 1: Incomplete Templates

**Symptom:** Leaving sections blank or incomplete.

**Solution:** Use templates as checklists. Complete all sections. Use "N/A" with explanation if not applicable.

### Mistake 2: No Version Control

**Symptom:** Documents edited without version history.

**Solution:** Use version-controlled repository. Never edit signed documents without creating new version.

### Mistake 3: Poor Redaction

**Symptom:** Inconsistent or incomplete redaction for due diligence.

**Solution:** Establish clear redaction policy. Apply consistently. Have both cofounders review.

### Mistake 4: No Backup

**Symptom:** Documents stored in single location with no backup.

**Solution:** Implement automated backups with off-site storage. Test restoration regularly.

### Mistake 5: Access Control Issues

**Symptom:** Documents accessible to unauthorized personnel.

**Solution:** Implement access control with logging. Review access permissions regularly.

## Documentation Quality Checklist

Before considering documentation complete:

- [ ] All template sections completed
- [ ] Sign-off obtained from both cofounders
- [ ] Document stored in version-controlled repository
- [ ] Document backed up
- [ ] Access control configured
- [ ] Decision register updated
- [ ] Naming conventions followed
- [ ] Standard header and footer included

## Next Steps

After documentation:

1. **Store documents** in secure, version-controlled repository
2. **Update Decision Register** with new decision
3. **Schedule retrospection** if required
4. **Archive old documents** quarterly

---

**Next: [09-training-onboarding.md](./09-training-onboarding.md)**
