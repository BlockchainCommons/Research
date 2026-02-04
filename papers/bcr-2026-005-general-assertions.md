# General Assertion Predicates

## BCR-2026-005

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for general-purpose assertion lifecycle management in Gordian Envelopes. These predicates handle versioning, revocation, disclosure, and transparency — concerns that apply across all assertion types.

This BCR is intentionally minimal. It provides foundational predicates that domain-specific BCRs (Principal Authority, CreativeWork Roles, Fair Witness, Peer Endorsement) can reference without duplication.

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
- Whether these predicates fill genuine gaps in the Known Value registry
- Whether the 1000-1999 range is appropriate for this vocabulary
- Any conflicts or overlaps with existing ontologies
- Suggested refinements to predicate definitions

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### Problem Statement

Assertions in Gordian Envelopes need lifecycle management: they can be updated, superseded, or revoked. They may carry disclosure about how they were produced. Currently, these common needs are addressed ad-hoc in each domain-specific vocabulary, leading to inconsistency and duplication.

### Solution

This specification defines six predicates for assertion lifecycle and transparency:

**Lifecycle predicates:**
1. **`supersedes`** — Links a new assertion to the one it replaces
2. **`revocationReason`** — Documents why an assertion was revoked
3. **`processDisclosure`** — Narrative about how the assertion was produced

**Transparency predicates:**
4. **`disclosedBias`** — Potential biases the attestor discloses
5. **`disclosedLimitations`** — Limitations on the attestor's knowledge or perspective
6. **`assertionLimitations`** — Scope or constraints of the assertion itself

These predicates complement existing core predicates `validFrom` (21) and `validUntil` (22), which this BCR references but does not redefine.

### Scope Boundary

This BCR defines **lifecycle and disclosure predicates**, not contribution types or roles. Predicates describing *what kind* of contribution was made (Author, Editor, etc.) belong in domain-specific BCRs such as the CreativeWork Roles BCR.

### Design Principles

These principles guide predicate design across this BCR suite:

1. **Clarity over brevity** — Names should be immediately understandable; Known Value encoding size is constant regardless of name length
2. **Consistency within categories** — Similar predicates follow similar naming patterns (e.g., `delegation*` prefix)
3. **Reusability across contexts** — Generic predicates (like those in this BCR) work outside their primary category
4. **Collision avoidance** — Avoid terms heavily used in other ontologies (see Collision Analysis below)
5. **Self-documenting** — Names hint at expected value types
6. **Defer to standards** — When a predicate is semantically equivalent to an existing standard (Schema.org, Dublin Core, VC), reference that standard rather than creating a duplicate
7. **Agent type orthogonality** — Definitions describe *what* is being done, not *who or what* does it; any role can be filled by humans, AI systems, tools, or hybrid teams

### Collision Analysis

The following terms were evaluated for collision risk with major ontologies:

| Term | Collision Risk | Resolution |
|------|----------------|------------|
| `domain` | rdfs:domain, Schema.org | Avoided — use specific terms |
| `role` | Schema.org Role type | Avoided — use context-specific predicates |
| `context` | JSON-LD @context | Avoided — use specific terms |
| `bias` | General term | `disclosedBias` — prefixed for clarity |
| `limitations` | General term | `disclosedLimitations`, `assertionLimitations` — prefixed |

## Terminology

**Assertion**: A signed statement in a Gordian Envelope expressing a claim about something.

**Supersession**: The replacement of one assertion with a newer version, where the newer version is authoritative.

**Revocation**: The explicit withdrawal of an assertion, distinct from expiration (reaching `validUntil`) or supersession (replacement with new content).

**Known Value**: A registered predicate identifier in the Gordian Envelope system, encoded as a numeric codepoint for efficient representation. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Core Predicates

This BCR uses the following predicates from the core registry. These are **not redefined** here — implementers should use the existing core codepoints.

| Codepoint | Predicate | Usage in This Context |
|-----------|-----------|----------------------|
| 21 | `validFrom` | When the assertion becomes effective |
| 22 | `validUntil` | When the assertion expires |

### Time Bounds Semantics

The `validFrom` and `validUntil` predicates apply to **the assertion itself**, not necessarily to the underlying relationship being asserted.

For example, if Alice asserts "I delegate signing authority to Bob" with `validFrom: 2026-02-01` and `validUntil: 2026-12-31`:
- The **assertion** is valid during that period
- The **delegation relationship** may have different temporal bounds defined by external policy or law
- Relying parties should interpret time bounds as "this assertion is authoritative during this period," not as legal terms of the underlying relationship

### Distinction from XID Predicates

The core registry includes predicates for cryptographic key operations:

| Codepoint | Predicate | Purpose |
|-----------|-----------|---------|
| 63 | `delegate` | Grants cryptographic signing privileges to another key |
| 86 | `Revoke` | Revokes cryptographic key permissions |

These XID predicates manage **key-level privileges** — who can sign on behalf of which keys. The predicates in this BCR manage **assertion-level semantics** — how assertions relate to each other over time.

The two concerns are orthogonal:
- A key may have `delegate` privileges without any authority assertions
- An authority assertion may exist without granting `delegate` key privileges
- Both may be used together when delegation includes signing rights

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### General Assertions (1000-1005)

---

#### 1000: `supersedes`

**Type**: property
**Definition**: References an earlier assertion that this assertion replaces.
**Domain**: Any assertion
**Range**: Digest or URI of the superseded assertion
**Usage**: Creates an explicit version chain for assertions.

```
    Digest(new-delegation-v2) [
        'supersedes': Digest(old-delegation-v1)
        'validFrom': 2026-02-01
    ]
```

**Notes**:
- The superseding assertion should be signed by an entity authorized to update the original
- Supersession is distinct from revocation — supersession provides new content, revocation withdraws without replacement

---

#### 1001: `revocationReason`

**Type**: property
**Definition**: Documents why an assertion was revoked.
**Domain**: Revocation assertion
**Range**: Text or Known Value for reason category
**Usage**: Distinguishes revocation causes (key compromise, error, withdrawal of consent, etc.)

```
    Digest(revocation) [
        'supersedes': Digest(original-assertion)
        'revocationReason': "Key compromise suspected"
    ]
```

**Notes**:
- This predicate is optional — revocation can occur without stating a reason
- The reason is for human understanding; automated systems should rely on the presence of supersession

---

#### 1002: `processDisclosure`

**Type**: property
**Definition**: Narrative disclosure about how the assertion or work was produced.
**Domain**: Any assertion or creative work
**Range**: Text
**Usage**: Provides context about production methods, tools used, or collaboration involved.

```
    Digest(document) [
        'processDisclosure': "Drafted with AI assistance using Claude. Human author reviewed, edited, and approved final content."
    ]
```

**Notes**:
- This predicate captures the *how* of production, not the *who* (which is handled by role predicates in other BCRs)
- Useful for AI-assisted content, tool-generated outputs, collaborative works, or any situation where production process matters

---

#### 1003: `disclosedBias`

**Type**: property
**Definition**: Potential biases the attestor discloses about their perspective or relationship to the subject.
**Domain**: Any assertion
**Range**: Text
**Usage**: Enables attestors to proactively disclose factors that might affect interpretation of their assertion.

```
    Digest(endorsement) [
        'disclosedBias': "I have a professional relationship with the subject. We have collaborated on three projects."
    ]
```

**Notes**:
- Self-reported disclosure — relying parties should treat as a claim, not verified fact
- Absence of `disclosedBias` does not mean absence of bias
- Useful for endorsements, reviews, recommendations, and any evaluative assertion
- Domain-specific BCRs (Fair Witness, Peer Endorsement) reference this predicate rather than defining their own

---

#### 1004: `disclosedLimitations`

**Type**: property
**Definition**: Known limitations on the attestor's knowledge, perspective, or ability to evaluate.
**Domain**: Any assertion
**Range**: Text
**Usage**: Enables attestors to acknowledge gaps in their knowledge or constraints on their perspective.

```
    Digest(skill-endorsement) [
        'disclosedLimitations': "I observed their work on frontend components only. I cannot speak to their backend or infrastructure skills."
    ]
```

**Notes**:
- Complements `disclosedBias` — bias is about perspective, limitations is about scope of knowledge
- Particularly important for endorsements and attestations where partial observation is common
- Encourages epistemic humility in assertions

---

#### 1005: `assertionLimitations`

**Type**: property
**Definition**: Scope or constraints of the assertion itself, independent of the attestor's limitations.
**Domain**: Any assertion
**Range**: Text
**Usage**: Documents what the assertion does and does not claim, establishing its boundaries.

```
    Digest(competency-assertion) [
        'assertionLimitations': "This assertion covers demonstrated skill as of the observation date. It does not predict future performance or guarantee results."
    ]
```

**Notes**:
- Different from `disclosedLimitations`: attestor limitations are about the person making the claim; assertion limitations are about the claim itself
- Helps prevent over-interpretation of assertions
- Useful for any assertion that might be misunderstood as broader than intended

---

## Usage Patterns

### Signature as Acceptance

When an assertion requires acceptance by multiple parties (such as a delegation that binds both principal and agent), the signature pattern handles acceptance:

- **Single signature**: The signer accepts the assertion's terms
- **Multi-signature**: All signers accept; the assertion is effective when all required signatures are present

This BCR does not define an `acceptance` predicate because signing already carries acceptance semantics. External policy or law may impose additional acceptance requirements beyond cryptographic signature.

**Important**: Signature represents **cryptographic assent** — evidence that a key holder signed. It does not establish temporal acceptance ("when did they agree?") or legal acceptance ("is this binding?"). Those determinations depend on external policy, jurisdiction, and context.

### Third-Party Revocation

When an entity other than the original signer needs to revoke an assertion:

1. The third party creates a new assertion with `supersedes` pointing to the original
2. The new assertion may include `revocationReason`
3. Relying parties must determine whether the third party has authority to revoke

This BCR does not define who may revoke — that is a policy decision. It provides the vocabulary to express that revocation occurred and why.

### Version Chains

Multiple supersessions create a version chain:

```
v1 (original)
  ← superseded by v2
    ← superseded by v3 (current)
```

Relying parties should follow the chain to find the current authoritative assertion. An assertion with no incoming `supersedes` reference and no outgoing supersession is current.

## Security Considerations

### Supersession Authority

Systems consuming these predicates must verify that the entity creating a superseding assertion has authority to do so. The predicate structure does not enforce authorization — it only expresses the relationship.

### Revocation Timing

The `validFrom` on a revocation indicates when the revocation becomes effective, not when the original assertion was compromised. For key compromise scenarios, the actual compromise time may be unknown or earlier than the revocation.

### Disclosure Integrity

The `processDisclosure`, `disclosedBias`, `disclosedLimitations`, and `assertionLimitations` predicates contain self-reported information. Relying parties should treat these as claims by the signer, not as verified fact.

### Transparency Predicate Interpretation

The presence of transparency predicates (`disclosedBias`, `disclosedLimitations`, `assertionLimitations`) indicates the attestor made an effort at disclosure. However:
- Absence of these predicates does not indicate absence of bias or limitations
- Disclosed limitations may be incomplete
- Transparency predicates do not validate the assertion itself

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)

## Related BCRs

This BCR provides foundational predicates used by:

- **BCR-2026-006: Signature Context Predicates** — Signing capacity and delegation
- **BCR-2026-007: Principal Authority Predicates** — Authority relationships (principal, delegation, scope)
- **BCR-2026-008: CreativeWork Role Predicates** — Contribution roles (Author, Editor, etc.)
- **BCR-2026-010: Fair Witness Predicates** — Neutral observer attestations (references `disclosedBias`, `disclosedLimitations`)
- **BCR-2026-011: Peer Endorsement Predicates** — Peer-to-peer trust building (references transparency predicates)

---

*BCR-2026-005: General Assertion Predicates*
*Draft - February 2, 2026*
