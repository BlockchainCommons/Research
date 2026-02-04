# Signature Context Predicates

## BCR-2026-006

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for expressing the context and capacity in which signatures are made in Gordian Envelopes. These predicates apply to ALL signature types — self-attestations, peer endorsements, and binding agreements — enabling clear expression of signing role, authority conferral, and authority chains.

This BCR depends on [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md) for lifecycle management.

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

When an entity signs an assertion in a Gordian Envelope, the signature captures *that* the signature was made, but not:
- **In what capacity** the signer is acting
- **On whose behalf** the signer may be acting
- **What chain of authority** authorizes the signature

These questions apply to ALL signature types:
- **Self-attestations** — claims about oneself
- **Peer endorsements** — claims about others
- **Binding agreements** — bilateral contracts where both parties sign

Without vocabulary to express signature context, relying parties cannot evaluate the authority behind a signature.

### Why "Signature Context" Not "Endorsement Authority"

Earlier drafts named this concern "Endorsement Authority," but [XID-Quickstart Tutorial 09](https://github.com/BlockchainCommons/XID-Quickstart) clarifies that self-attestation, peer endorsement, and binding agreement are DIFFERENT signature types. The predicates in this BCR apply to ALL of them, not just endorsements.

"Signature Context" accurately describes what these predicates capture: the context and capacity in which any signature is made.

### Solution

This specification defines four predicates for signature context:

1. **`signingAs`** — The capacity or role in which the signer is acting
2. **`onBehalfOf`** — The party the signer represents (if any)
3. **`conferredBy`** — Who granted the signer's authority
4. **`conferralChain`** — The full chain of authority conferral (for multi-hop)

### Relationship to Principal Authority

This BCR and [BCR-2026-007: Principal Authority Predicates](bcr-2026-007-principal-authority.md) address related but distinct concerns:

| Concern | BCR | Question Answered |
|---------|-----|-------------------|
| **Signature Context** | This BCR (006) | "In what capacity is this signature made?" |
| **Principal Authority** | BCR-2026-007 | "Who directs and takes responsibility for this work?" |

**Signature Context** is about the signature itself — role, conferral, authority chain.

**Principal Authority** is about the work — who directed it, whose judgment shaped it, who stands behind it.

A document may have:
- `principalAuthority` identifying who directed the work
- `signingAs` on signatures indicating the capacity of each signer

Both may be present. Neither implies the other.

## Terminology

**Signature Context**: The capacity, role, and authority chain under which a signature is made.

**Signing Capacity**: The role or function in which a signer acts (e.g., "CEO", "Legal Representative", "Witness").

**Conferral**: The grant of authority from one party to another to act or sign on their behalf. This term is used instead of "delegation" to distinguish from cryptographic delegation (XID `delegate` predicate) which grants cryptographic signing privileges.

**Conferral Chain**: A sequence of authority conferrals from an original authority to the current signer.

**Known Value**: A registered predicate identifier in the Gordian Envelope system. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Specifications

### BCR-2026-005: General Assertion Predicates

| Codepoint | Predicate | Usage in This Context |
|-----------|-----------|----------------------|
| 1000 | `supersedes` | Updating authority conferral assertions |
| 1001 | `revocationReason` | Documenting why authority was revoked |
| 21 | `validFrom` | When signing authority becomes effective |
| 22 | `validUntil` | When signing authority expires |

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### Signature Context (1020-1023)

---

#### 1020: `signingAs`

**Type**: property
**Definition**: The capacity or role in which the signer is acting.
**Domain**: Signature or signed assertion
**Range**: Text or Known Value for role
**Usage**: Clarifies the function the signer is performing.

```
{
    Digest(corporate-agreement) [
        'signed': {
            XID(alice) [
                'signingAs': "Chief Executive Officer"
            ]
        }
    ]
}
```

**Notes**:
- Applies to any signature type (attestation, endorsement, agreement)
- Does not grant authority — only describes claimed capacity
- Relying parties must evaluate whether the claimed capacity is valid

---

#### 1021: `onBehalfOf`

**Type**: property
**Definition**: The party the signer represents when making this signature.
**Domain**: Signature or signed assertion
**Range**: XID, DID, or identifier of the represented party
**Usage**: Indicates the signer is acting for another entity.

```
{
    Digest(vendor-contract) [
        'signed': {
            XID(legal-counsel) [
                'signingAs': "Legal Representative"
                'onBehalfOf': XID(acme-corp)
            ]
        }
    ]
}
```

**Notes**:
- The signer asserts they have authority to represent the named party
- Does not itself prove authority — see `conferredBy` for authority chain
- Common in corporate, legal, and organizational contexts

---

#### 1022: `conferredBy`

**Type**: property
**Definition**: The entity that granted the signer's authority to sign.
**Domain**: Signature context
**Range**: XID, DID, or identifier of the conferring party
**Usage**: Documents the immediate source of signing authority.

```
{
    Digest(approval-document) [
        'signed': {
            XID(department-head) [
                'signingAs': "Authorized Approver"
                'conferredBy': XID(cfo)
            ]
        }
    ]
}
```

**Notes**:
- For single-hop authority conferral, `conferredBy` is sufficient
- For multi-hop conferral, use `conferralChain`
- The conferral may be standing (ongoing) or contextual (one-time)
- "Conferral" is used instead of "delegation" to distinguish from cryptographic delegation (XID `delegate` predicate)

---

#### 1023: `conferralChain`

**Type**: property
**Definition**: The full chain of authority conferral from original authority to current signer.
**Domain**: Signature context
**Range**: Ordered list of XIDs/DIDs representing the conferral path
**Usage**: Documents multi-hop authority conferral for complex authority structures.

```
{
    Digest(field-authorization) [
        'signed': {
            XID(field-agent) [
                'signingAs': "Field Representative"
                'conferralChain': [XID(board), XID(ceo), XID(regional-director)]
            ]
        }
    ]
}
```

**Notes**:
- Chain is ordered from original authority to immediate conferrer
- The signer is implicitly at the end of the chain
- Use for audit trails and authority verification
- Simpler cases can use `conferredBy` alone

---

## Usage Patterns

### Self-Attestation with Capacity

A person signing a claim about themselves, in a specific capacity:

```
{
    Digest(skill-claim) [
        'subject': XID(alice)
        'hasSkill': "Rust programming"
        'signed': {
            XID(alice) [
                'signingAs': "Individual"
            ]
        }
    ]
}
```

### Peer Endorsement with Capacity

Someone endorsing another person, in a professional capacity:

```
{
    Digest(endorsement) [
        'subject': XID(bob)
        'endorses': "Project management skills"
        'signed': {
            XID(alice) [
                'signingAs': "Former Supervisor"
                'disclosedBias': "Worked together for 3 years"
            ]
        }
    ]
}
```

### Corporate Agreement

A binding agreement signed by representatives:

```
{
    Digest(service-agreement) [
        'parties': [XID(acme-corp), XID(widgets-inc)]
        'terms': Digest(agreement-terms)
        'signed': {
            XID(alice) [
                'signingAs': "CEO"
                'onBehalfOf': XID(acme-corp)
            ]
        }
        'signed': {
            XID(bob) [
                'signingAs': "Authorized Representative"
                'onBehalfOf': XID(widgets-inc)
                'conferredBy': XID(widgets-ceo)
            ]
        }
    ]
}
```

### Multi-Hop Authority Conferral

Field authorization with full audit trail:

```
{
    Digest(emergency-authorization) [
        'authorizes': "Emergency procurement up to $50,000"
        'signed': {
            XID(field-manager) [
                'signingAs': "Emergency Coordinator"
                'onBehalfOf': XID(corporation)
                'conferralChain': [XID(board), XID(ceo), XID(coo), XID(regional-vp)]
            ]
        }
    ]
}
```

### Combined with Principal Authority

Using both Signature Context and Principal Authority predicates:

```
{
    Digest(ai-generated-report) [
        'principalAuthority': XID(research-director)
        'processDisclosure': "Generated by AI under human direction"
        'signed': {
            XID(research-director) [
                'signingAs': "Principal Investigator"
                'onBehalfOf': XID(research-institute)
            ]
        }
    ]
}
```

## Security Considerations

### Signature Context Claims Are Assertions

The predicates in this BCR express **claims by the signer**. Relying parties must:
- Verify the signer's identity
- Evaluate whether the claimed capacity (`signingAs`) is plausible
- Verify the conferral chain if authority is claimed
- Consider the context and stakes of the assertion

### Authority Conferral Verification

The presence of `conferredBy` or `conferralChain` does not prove valid authority conferral. Verification requires:
- Checking that each conferrer had authority to confer
- Confirming the conferral was active at signing time
- Validating any scope or constraint limitations

### Capacity vs. Authority

`signingAs` describes claimed capacity, not granted authority. A signature claiming `signingAs: "CEO"` does not prove the signer is a CEO. External verification is required for high-stakes contexts.

### Chain Integrity

For `conferralChain`, each link should be independently verifiable. A broken or unverifiable link invalidates the claimed authority from that point forward.

## Open Questions

### Q1: Integration with BCR-2024-009 Signature Metadata

[BCR-2024-009](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-009-signature-metadata.md) defines a pattern for attaching metadata to signatures using double-signing: the outer signature signs both the original content and the metadata on the inner Signature object.

**Question**: Should the signature context predicates in this BCR (`signingAs`, `onBehalfOf`, `conferredBy`, `conferralChain`) be applied:

1. **As assertions on the signer XID** (as shown in current examples) — simpler but metadata is separate from signature
2. **As metadata on the Signature object** (per BCR-2024-009) — cryptographically bound but requires double-signing
3. **Either pattern depending on use case** — with guidance on when to use each

We invite community feedback on the recommended integration pattern. See [GitHub issue #158](https://github.com/BlockchainCommons/Research/issues/158) for discussion.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2024-009: Signature Metadata](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-009-signature-metadata.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [XID-Quickstart Tutorial 09: Binding Agreements](https://github.com/BlockchainCommons/XID-Quickstart)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)

## Related BCRs

- **BCR-2024-009: Signature Metadata** — Established pattern for attaching metadata to signatures using double-signing. Signature context predicates should be applied using this pattern.
- **BCR-2026-005: General Assertion Predicates** — Lifecycle predicates used by this BCR
- **BCR-2026-007: Principal Authority Predicates** — Authority over work (complementary; uses matching `conferral*` terminology)

---

*BCR-2026-006: Signature Context Predicates*
*Draft - February 2, 2026*
