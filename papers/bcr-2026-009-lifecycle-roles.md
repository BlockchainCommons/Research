# Lifecycle Role Predicates

## BCR-2026-009

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for lifecycle roles in Gordian Envelopes. These roles describe contributions that occur before or after the creative act itself — commissioning what should exist, distributing the finished work, and stewarding it over time.

These lifecycle roles complement the creative contribution roles in [BCR-2026-008: CreativeWork Role Predicates](bcr-2026-008-creativework-roles.md), which focus on what happens *during* creation.

## Status: Pre-Registration Proposal

📙 **Research** — This BCR proposes new Known Values and is seeking community review.

### Registration Intent

We propose registering these predicates in the **Community Assigned (specification required)** range (1000-1999) as defined in [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

This range is currently unassigned. We are seeking **rough consensus** from the Gordian developer community before claiming these codepoints. If the community determines these predicates:
- Do not merit the 1000-1999 range, or
- Should use different codepoint assignments

We will register in the **Community Assigned (first come-first served)** range (100000+) instead.

### Request for Community Review

We invite feedback on:
- Whether these lifecycle roles are distinct from creative roles
- Whether the 1000-1999 range is appropriate for this vocabulary
- Whether Commissioning belongs here or overlaps with ConceptOriginator
- Any missing lifecycle roles
- Suggested refinements to role definitions

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### Problem Statement

Creative contribution vocabularies (CRediT, the CreativeWork roles vocabulary) focus on what happens during creation — writing, editing, designing, reviewing. But creative works have lifecycles that extend beyond the creative act:

- **Before**: Someone decides what should exist (commissioning)
- **After**: Someone makes it available (distribution) and cares for it over time (stewardship)

These lifecycle roles are often conflated with creative roles or authority relationships, but they represent distinct contributions.

### Solution

This specification defines three lifecycle roles:

1. **`Commissioner`** — Decided what should exist
2. **`Distributor`** — Makes the work available
3. **`Steward`** — Provides long-term care for the work and its ideas

### Scope Boundary

This BCR defines **lifecycle roles** — contributions before and after the creative act.

**Not in scope:**
- Creative contribution roles (Author, Editor, etc.) — see [BCR-2026-008: CreativeWork Role Predicates](bcr-2026-008-creativework-roles.md)
- Authority relationships — see [BCR-2026-007: Principal Authority Predicates](bcr-2026-007-principal-authority.md)
- Social roles (community shepherding, facilitation) — see Roles Not Included

### Relationship to Other BCRs

| BCR | Focus | Lifecycle Phase |
|-----|-------|-----------------|
| BCR-2026-007 | Authority relationships | Overlays all phases |
| BCR-2026-008 | Creative contribution | During creation |
| **BCR-2026-009** | **Lifecycle roles** | **Before and after creation** |

## Terminology

**Lifecycle Role**: A type of contribution that occurs before or after the creative act itself.

**Commissioning**: The decision that a work should exist, including scope and purpose.

**Distribution**: Making a work available to its intended audience.

**Stewardship**: Long-term care for a work, its ideas, and any community around it.

**Known Value**: A registered predicate identifier in the Gordian Envelope system. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### Lifecycle Roles (1100-1102)

---

#### 1100: `Commissioner`

**Type**: role
**Definition**: Decided that the CreativeWork should exist and defined its scope or purpose.
**Phase**: Before creation
**Distinction from ConceptOriginator**: ConceptOriginator provides the core *idea*; Commissioner makes the *decision* to create and may define requirements without providing the concept.

```
    Digest(commissioned-report) [
        'schema:author': XID(researcher)
        'schema:contributor': {
            XID(foundation) [
                'schema:roleName': 'Commissioner'
            ]
        }
        'schema:contributor': {
            XID(researcher) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
    ]
```

**Examples**:
- A foundation commissions a research report (Commissioner) while researchers develop the approach (Conceptualization)
- A client commissions software (Commissioner) while developers design the architecture (Architect)
- A publisher commissions a book on a topic (Commissioner) while the author provides the unique perspective (ConceptOriginator)

**Notes**:
- Commissioner often overlaps with `principalAuthority` but they are distinct: Commissioner is a role (what they did), while `principalAuthority` is a relationship (who directs)
- A work may have no Commissioner (self-initiated) or multiple Commissioners (collaborative initiative)

---

#### 1101: `Distributor`

**Type**: role
**Definition**: Makes the CreativeWork available to its intended audience.
**Phase**: After creation
**Distinction from Publisher**: Traditional "publisher" conflates multiple roles (commissioning, editing, distribution, responsibility). Distributor isolates the distribution function.

```
    Digest(open-source-project) [
        'schema:author': XID(maintainer)
        'schema:contributor': {
            XID(maintainer) [
                'schema:roleName': 'Steward'
            ]
        }
        'schema:contributor': {
            XID(package-registry) [
                'schema:roleName': 'Distributor'
            ]
        }
    ]
```

**Examples**:
- npm, PyPI, or crates.io distributing software packages
- Archive.org preserving and distributing digital works
- A bookstore or library making physical works available
- A website hosting and serving content

**Notes**:
- Distribution without responsibility: A Distributor may make work available without taking responsibility for its content (see BCR-2026-005 for `principalAuthority`)
- Multiple distributors: A work may have many distributors across different channels

---

#### 1102: `Steward`

**Type**: role
**Definition**: Provides long-term care for the CreativeWork, its ideas, and any community around it.
**Phase**: After creation (ongoing)
**Distinction from Maintainer**: Maintainer (BCR-2026-006) focuses on technical updates; Steward encompasses broader care including ideas, community, and legacy.

```
    Digest(community-project) [
        'schema:author': XID(original-author)
        'schema:contributor': {
            XID(original-author) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
        'schema:contributor': {
            XID(foundation) [
                'schema:roleName': 'Steward'
            ]
        }
    ]
```

**Examples**:
- A foundation stewarding an open-source project after the original author steps back
- An archive preserving and contextualizing historical works
- A standards body maintaining a specification and its community
- Ward Cunningham's stewardship of the wiki concept and community

**Notes**:
- Stewardship may include but is not limited to: maintaining relevance, responding to community needs, preserving access, updating context, managing succession
- Steward implies ongoing relationship; for one-time care, Maintainer may be more appropriate

---

## Usage Patterns

### Commissioned Work

```
    Digest(research-report) [
        'principalAuthority': XID(foundation)
        'schema:author': XID(research-team)
        'schema:contributor': {
            XID(foundation) [
                'schema:roleName': 'Commissioner'
            ]
        }
        'schema:contributor': {
            XID(research-team) [
                'assertsDelegationFrom': XID(foundation)
            ]
        }
    ]
```

### Full Lifecycle Attribution

```
    Digest(open-standard) [
        'schema:author': XID(working-group)
        'schema:contributor': {
            XID(standards-body) [
                'schema:roleName': 'Commissioner'
                'schema:roleName': 'Steward'
            ]
        }
        'schema:contributor': {
            XID(working-group) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
        'schema:contributor': {
            XID(website) [
                'schema:roleName': 'Distributor'
            ]
        }
    ]
```

### Stewardship Succession

```
    Digest(legacy-project) [
        'schema:author': XID(original-creator)
        'schema:contributor': {
            XID(original-creator) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
        'schema:contributor': {
            XID(new-foundation) [
                'schema:roleName': 'Steward'
            ]
        }
        'processDisclosure': "Stewardship transferred to New Foundation in 2025."
    ]
```

## Roles Not Included

The following roles are intentionally excluded from this BCR:

| Role | Reason | Notes |
|------|--------|-------|
| **Community Shepherding** | Social role, not lifecycle | Nurturing human relationships is valuable but distinct from work lifecycle |
| **Facilitator** | Social role, not lifecycle | Enabling collaboration is process, not lifecycle contribution |
| **Publisher** | Conflated term | Decomposes into Commissioner + Editor + Distributor + Steward |
| **Sponsor** | Financial role | Funding is important but distinct from lifecycle roles; may be added in future BCR |

### Why Not Community Shepherding?

Community shepherding — nurturing human relationships around a work — is valuable but operates on a different axis than lifecycle roles:

- **Lifecycle roles** are about the work itself (commissioning, distributing, stewarding the work)
- **Community roles** are about people (facilitating discussion, resolving conflicts, welcoming newcomers)

Community roles may warrant their own BCR focused on social/collaborative contributions, but they don't belong in a lifecycle vocabulary.

## Security Considerations

### Role Claims Are Assertions

Lifecycle role attributions are claims by the asserter. Relying parties should evaluate:
- Who made the attribution
- Whether the claimed role is plausible
- Whether confirmation from the role-holder exists

### Commissioner vs. Principal Authority

Having the Commissioner role does not automatically confer `principalAuthority`. A Commissioner may:
- Initiate a work without directing its creation
- Define scope without taking responsibility for content
- Fund creation without editorial control

Authority relationships should be expressed explicitly through BCR-2026-007.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [BCR-2026-007: Principal Authority Predicates](bcr-2026-007-principal-authority.md)
- [BCR-2026-008: CreativeWork Role Predicates](bcr-2026-008-creativework-roles.md)
- [Schema.org Known Values Registry](https://github.com/BlockchainCommons/Research/blob/master/known-value-assignments/markdown/10000_schema_registry.md) — `schema:contributor` (11227), `schema:roleName` (12151)
- [RAA Framework](https://github.com/peterkaminski/raa-framework) — Role analysis informing this BCR

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Lifecycle management for assertions
- **BCR-2026-007: Principal Authority Predicates** — Authority relationships
- **BCR-2026-008: CreativeWork Role Predicates** — Creative contribution roles

---

*BCR-2026-009: Lifecycle Role Predicates*
*Draft - February 2, 2026*
