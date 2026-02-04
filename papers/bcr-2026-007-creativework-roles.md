# CreativeWork Role Predicates

## BCR-2026-007

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for creative contribution roles in Gordian Envelopes. These 14 roles describe what kind of contribution an entity made to a creative work — Author, Editor, Architect, Designer, and others — independent of whether the contributor is human, AI, or a hybrid team.

This vocabulary is derived from the CreativeWork contributor roles vocabulary (to be published at [attestation.info](https://attestation.info)) and designed to work with Schema.org's Role pattern while remaining interoperable with CRediT, ONIX, MARC, and EBUCore.

This BCR complements:
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md) — lifecycle management
- [BCR-2026-006: Principal Authority Predicates](bcr-2026-006-principal-authority.md) — authority relationships

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
- Whether these role definitions are clear and complete
- Whether the 1000-1999 range is appropriate for this vocabulary
- Whether the CRediT/ONIX/MARC mappings are accurate
- Any missing roles that belong in this creative contribution vocabulary
- Suggested refinements to role definitions

### Open Questions

**Q1: Is `niso-credit:Conceptualization` equivalent to "ConceptOriginator"?**

NISO CRediT defines Conceptualization as: "Ideas; formulation or evolution of overarching research goals and aims."

This BCR's ConceptOriginator is defined as: "Originated the core idea, premise, or conceptual foundation of the CreativeWork."

These may differ in:
- **Scope**: CRediT is scholarly research-focused; ConceptOriginator applies to all creative works
- **Emphasis**: CRediT includes "evolution" of goals; ConceptOriginator emphasizes "origination"

Should we use `niso-credit:Conceptualization` (2400) directly, define a distinct `ConceptOriginator` (1065), or document both with clear distinction?

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### Problem Statement

Existing role vocabularies tend to be:
- **Domain-specific** — CRediT for scholarly publishing, ONIX for book trade
- **Medium-specific** — text-only, audiovisual-only
- **Conflating multiple axes** — mixing authorship with implementation

Creative works increasingly span text, code, media, and data in a single work. A cross-creative, medium-agnostic role vocabulary is needed.

### Solution

This specification defines 14 roles that:
- Separate ideation, expression, design, execution, review, and lifecycle
- Work equally for code, standards, books, films, datasets, and hybrid works
- Are orthogonal to agent type (human, AI, tool, or hybrid team)
- Map to existing standards without duplicating them

### Scope Boundary

This BCR defines **creative contribution roles** — what kind of work was done.

**Not in scope:**
- Authority relationships (who directed whom) — see [BCR-2026-006](bcr-2026-006-principal-authority.md)
- Lifecycle roles (distribution, stewardship) — see BCR-2026-008
- Social roles (community shepherding, facilitation)
- Domain-specific scholarly roles (funding acquisition, investigation)

### Agent Type Orthogonality

Role definitions describe *what* is being done, not *who or what* does it. Any role can be filled by:
- Humans
- AI systems
- Tools
- Hybrid teams

The same role vocabulary applies regardless of agent type. Attribution quality should be consistent whether the Author is a human writer or an AI system.

## Terminology

**Role**: A type of contribution to a creative work, describing what was done.

**CreativeWork**: Any work of authorship — text, code, music, visual composition, data, or hybrid.

**Known Value**: A registered predicate identifier in the Gordian Envelope system. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Specifications

### BCR-2026-005: General Assertion Predicates

| Codepoint | Predicate | Usage with Roles |
|-----------|-----------|------------------|
| 1002 | `processDisclosure` | Describes how the work was produced |

### BCR-2026-006: Principal Authority Predicates

| Codepoint | Predicate | Usage with Roles |
|-----------|-----------|------------------|
| 1040 | `principalAuthority` | Who directed the work |
| 1041 | `assertsDelegationFrom` | Agent claims delegation |

### Schema.org Predicates

| Codepoint | Predicate | Usage with Roles |
|-----------|-----------|------------------|
| 11227 | `schema:contributor` | Links work to contributor with role assertions |
| 12151 | `schema:roleName` | Assigns role type to contributor |

These predicates use the [Schema.org Known Values Registry](https://github.com/BlockchainCommons/Research/blob/master/known-value-assignments/markdown/10000_schema_registry.md) for structural patterns.

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### CreativeWork Roles (1060-1073)

---

#### `schema:author` (11063)

**Type**: property (Schema.org)
**Definition**: Created the primary expressive content of the CreativeWork.
**Includes**: Text, code, music, visual composition, or other expressive media.
**CRediT mapping**: Writing – Original Draft, Software
**MARC mapping**: aut (Author)

```
    Digest(document) [
        'schema:author': XID(writer)
    ]
```

> **Note**: Use the existing Schema.org predicate `schema:author` (11063) rather than defining a new role value.

---

#### `schema:editor` (11369)

**Type**: property (Schema.org)
**Definition**: Refined, revised, or shaped existing content for quality, clarity, or coherence.
**CRediT mapping**: Writing – Review & Editing
**MARC mapping**: edt (Editor)

```
    Digest(document) [
        'schema:editor': XID(editor)
    ]
```

> **Note**: Use the existing Schema.org predicate `schema:editor` (11369) rather than defining a new role value.

---

#### 1062: `Architect`

**Type**: role
**Definition**: Designed the high-level structural organization and governing principles of the CreativeWork.
**Notes**: A specialization of Designer focused on formal structure rather than aesthetic presentation.
**CRediT mapping**: Methodology (partial)

---

#### 1063: `Designer`

**Type**: role
**Definition**: Shaped the aesthetic, visual, or experiential presentation of the CreativeWork.
**CRediT mapping**: Visualization
**ONIX mapping**: A12 (Book designer)

---

#### 1064: `Manager`

**Type**: role
**Definition**: Coordinated, administered, or oversaw the production process.
**CRediT mapping**: Project Administration, Supervision
**MARC mapping**: ppm (Project manager)

---

#### `niso-credit:Conceptualization` (2400)

**Type**: value (NISO CRediT)
**Definition**: Originated the core idea, premise, or conceptual foundation of the CreativeWork.
**Notes**: Captures ideation prior to expressive creation. Distinct from authorship and implementation.

```
    Digest(document) [
        'schema:contributor': {
            XID(ideator) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
    ]
```

> **Note**: Use the existing NISO CRediT role value `niso-credit:Conceptualization` (2400) rather than defining a new `ConceptOriginator` value.

---

#### 1066: `Documenter`

**Type**: role
**Definition**: Created documentation, specifications, or explanatory materials for the CreativeWork.
**Notes**: Distinct from Author — Documenter creates materials *about* the work, not the work itself.

---

#### 1067: `TechnicalProducer`

**Type**: role
**Definition**: Implemented the technical realization of the CreativeWork.
**Notes**: Answers "how the work is made to function or exist." For audiovisual, this includes recording, mixing, mastering.
**EBUCore mapping**: Technical producer

---

#### 1068: `Curator`

**Type**: role
**Definition**: Selected and organized materials or works into a coherent whole.
**CRediT mapping**: Data Curation (partial)
**MARC mapping**: cur (Curator)

---

#### 1069: `Reviewer`

**Type**: role
**Definition**: Evaluated, critiqued, or assessed the CreativeWork.
**CRediT mapping**: Validation (partial)
**MARC mapping**: rev (Reviewer)

---

#### 1070: `Maintainer`

**Type**: role
**Definition**: Provides ongoing care, updates, or stewardship of the CreativeWork after initial creation.
**Notes**: Technical maintenance focus. For broader stewardship of ideas, see BCR-2026-006.

---

#### 1071: `MaterialContributor`

**Type**: role
**Definition**: Supplied reusable materials incorporated into the CreativeWork.
**Includes**: Assets, libraries, datasets, samples, or other materials.
**CRediT mapping**: Resources

---

#### 1072: `Performer`

**Type**: role
**Definition**: Performed, presented, or enacted the CreativeWork.
**Includes**: Musicians, actors, speakers, demonstrators.
**MARC mapping**: prf (Performer)
**EBUCore mapping**: Performer

---

#### 1073: `IntellectualContributor`

**Type**: role
**Definition**: Contributed ideas or guidance without authorship or editorial ownership.
**Notes**: Advisory input, consultation, or expertise that shaped the work without direct creation.
**CRediT mapping**: (no direct equivalent — CRediT focuses on direct contributions)

---

## Standard Mappings

### CRediT Taxonomy Mapping

CRediT (Contributor Roles Taxonomy) is registered in the Known Values registry at codepoints 2400-2413. See [NISO CRediT Registry](https://github.com/BlockchainCommons/Research/blob/master/known-value-assignments/markdown/2400_niso_credit_registry.md).

| CRediT Role | Codepoint | CreativeWork Role | Notes |
|-------------|-----------|-------------------|-------|
| Conceptualization | 2400 | ConceptOriginator | Direct mapping |
| Data Curation | 2401 | Curator | Partial — CRediT includes data cleaning |
| Formal Analysis | 2402 | — | Scholarly-specific, out of scope |
| Funding Acquisition | 2403 | — | Scholarly-specific, out of scope |
| Investigation | 2404 | — | Scholarly-specific, out of scope |
| Methodology | 2405 | Architect | Partial — methodology design |
| Project Administration | 2406 | Manager | Direct mapping |
| Resources | 2407 | MaterialContributor | Direct mapping |
| Software | 2408 | Author | Code is expressive content |
| Supervision | 2409 | Manager | Combined with administration |
| Validation | 2410 | Reviewer | Partial — validation is a form of review |
| Visualization | 2411 | Designer | Direct mapping |
| Writing – Original Draft | 2412 | Author | Direct mapping |
| Writing – Review & Editing | 2413 | Editor | Direct mapping |

### ONIX/MARC/EBUCore Mappings

Detailed mappings to publishing and media standards are available in the attestation.info documentation (when published). Key correspondences:

| CreativeWork Role | MARC Relator | ONIX Code |
|-------------------|--------------|-----------|
| Author | aut | A01 |
| Editor | edt | B01 |
| Designer | — | A12 |
| Performer | prf | — |
| Curator | cur | — |

## Usage Patterns

### Basic Role Attribution

Use direct predicates where Schema.org provides them:

```
    Digest(blog-post) [
        'schema:author': XID(alice)
        'schema:editor': XID(bob)
    ]
```

### Multiple Roles

A single contributor may hold multiple roles. Use direct predicates where available, Role pattern for others:

```
    Digest(software-project) [
        'schema:author': XID(developer)
        'schema:contributor': {
            XID(developer) [
                'schema:roleName': 'Architect'
                'schema:roleName': 'Documenter'
            ]
        }
    ]
```

### Roles with Principal Authority

Combining roles with authority predicates from BCR-2026-006:

```
    Digest(ai-generated-document) [
        'principalAuthority': XID(human-director)
        'schema:author': XID(claude-ai)
        'schema:editor': XID(human-director)
        'schema:contributor': {
            XID(human-director) [
                'schema:roleName': 'niso-credit:Conceptualization'
            ]
        }
        'schema:contributor': {
            XID(claude-ai) [
                'assertsDelegationFrom': XID(human-director)
            ]
        }
        'processDisclosure': "Drafted by Claude under human direction and review."
    ]
```

### AI as Contributor

AI systems receive the same role vocabulary as human contributors:

```
    Digest(code-module) [
        'schema:author': "Claude Sonnet 4.5"
        'schema:editor': XID(developer)
        'schema:contributor': {
            XID(developer) [
                'schema:roleName': 'Reviewer'
            ]
        }
    ]
```

## Roles Not Included

The following roles are intentionally excluded from this BCR:

| Role | Reason | Where Covered |
|------|--------|---------------|
| Distribution | Lifecycle role, not creative contribution | BCR-2026-008 |
| Stewardship | Lifecycle role, not creative contribution | BCR-2026-008 |
| Commissioning | May overlap with ConceptOriginator | BCR-2026-008 (under review) |
| Community Shepherding | Social role, not creative contribution | Out of scope |
| Funding Acquisition | Scholarly-specific | Out of scope |
| Investigation | Scholarly-specific | Out of scope |
| Formal Analysis | Scholarly-specific | Out of scope |

## Security Considerations

### Role Claims Are Assertions

Role attributions are claims by the asserter. Relying parties must:
- Verify the identity of the contributor
- Evaluate whether to trust the role claim
- Consider the authority context (who made the attribution)

### Role vs. Authority

Having a role (e.g., Author) does not imply authority over the work. Authority relationships are expressed through BCR-2026-006 predicates (`principalAuthority`, `assertsDelegationFrom`).

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [BCR-2026-006: Principal Authority Predicates](bcr-2026-006-principal-authority.md)
- [attestation.info](https://attestation.info) — Source vocabulary (planned)
- [CRediT Taxonomy](https://credit.niso.org/) — ANSI/NISO Z39.104-2022
- [NISO CRediT Known Values Registry](https://github.com/BlockchainCommons/Research/blob/master/known-value-assignments/markdown/2400_niso_credit_registry.md) — Codepoints 2400-2413
- [MARC Relator Codes](https://www.loc.gov/marc/relators/)
- [ONIX Code Lists](https://www.editeur.org/14/Code-Lists/)

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Lifecycle management
- **BCR-2026-006: Principal Authority Predicates** — Authority relationships
- **BCR-2026-008: Lifecycle Role Predicates** — Distribution, Stewardship

---

*BCR-2026-007: CreativeWork Role Predicates*
*Draft - February 2, 2026*
