# Signature Context Predicates

## BCR-2026-006

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for expressing the context and capacity in which signatures are made in Gordian Envelopes. These predicates apply to ALL signature types — self-attestations, peer endorsements, and binding agreements — enabling clear expression of signing role, delegation, and authority chains.

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
- **What chain of delegation** authorizes the signature

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
3. **`delegatedBy`** — Who granted the signer's authority
4. **`delegationChain`** — The full chain of delegation (for multi-hop)

### Relationship to Principal Authority

This BCR and [BCR-2026-007: Principal Authority Predicates](bcr-2026-007-principal-authority.md) address related but distinct concerns:

| Concern | BCR | Question Answered |
|---------|-----|-------------------|
| **Signature Context** | This BCR (006) | "In what capacity is this signature made?" |
| **Principal Authority** | BCR-2026-007 | "Who directs and takes responsibility for this work?" |

**Signature Context** is about the signature itself — role, delegation, authority chain.

**Principal Authority** is about the work — who directed it, whose judgment shaped it, who stands behind it.

A document may have:
- `principalAuthority` identifying who directed the work
- `signingAs` on signatures indicating the capacity of each signer

Both may be present. Neither implies the other.

## Terminology

**Signature Context**: The capacity, role, and authority chain under which a signature is made.

**Signing Capacity**: The role or function in which a signer acts (e.g., "CEO", "Legal Representative", "Witness").

**Delegation**: Authorization from one party to another to sign on their behalf.

**Delegation Chain**: A sequence of delegations from an original authority to the current signer.

**Known Value**: A registered predicate identifier in the Gordian Envelope system. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Specifications

### BCR-2026-005: General Assertion Predicates

| Codepoint | Predicate | Usage in This Context |
|-----------|-----------|----------------------|
| 1000 | `supersedes` | Updating delegation assertions |
| 1001 | `revocationReason` | Documenting why delegation was revoked |
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
    CID(corporate-agreement) [
        'signature': {
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
    CID(vendor-contract) [
        'signature': {
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
- Does not itself prove authority — see `delegatedBy` for authority chain
- Common in corporate, legal, and organizational contexts

---

#### 1022: `delegatedBy`

**Type**: property
**Definition**: The entity that granted the signer's authority to sign.
**Domain**: Signature context
**Range**: XID, DID, or identifier of the delegating party
**Usage**: Documents the immediate source of signing authority.

```
{
    CID(approval-document) [
        'signature': {
            XID(department-head) [
                'signingAs': "Authorized Approver"
                'delegatedBy': XID(cfo)
            ]
        }
    ]
}
```

**Notes**:
- For single-hop delegation, `delegatedBy` is sufficient
- For multi-hop delegation, use `delegationChain`
- The delegation may be standing (ongoing) or contextual (one-time)

---

#### 1023: `delegationChain`

**Type**: property
**Definition**: The full chain of delegation from original authority to current signer.
**Domain**: Signature context
**Range**: Ordered list of XIDs/DIDs representing the delegation path
**Usage**: Documents multi-hop delegation for complex authority structures.

```
{
    CID(field-authorization) [
        'signature': {
            XID(field-agent) [
                'signingAs': "Field Representative"
                'delegationChain': [XID(board), XID(ceo), XID(regional-director)]
            ]
        }
    ]
}
```

**Notes**:
- Chain is ordered from original authority to immediate delegator
- The signer is implicitly at the end of the chain
- Use for audit trails and authority verification
- Simpler cases can use `delegatedBy` alone

---

## Usage Patterns

### Self-Attestation with Capacity

A person signing a claim about themselves, in a specific capacity:

```
{
    CID(skill-claim) [
        'subject': XID(alice)
        'hasSkill': "Rust programming"
        'signature': {
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
    CID(endorsement) [
        'subject': XID(bob)
        'endorses': "Project management skills"
        'signature': {
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
    CID(service-agreement) [
        'parties': [XID(acme-corp), XID(widgets-inc)]
        'terms': CID(agreement-terms)
        'signature': {
            XID(alice) [
                'signingAs': "CEO"
                'onBehalfOf': XID(acme-corp)
            ]
        }
        'signature': {
            XID(bob) [
                'signingAs': "Authorized Representative"
                'onBehalfOf': XID(widgets-inc)
                'delegatedBy': XID(widgets-ceo)
            ]
        }
    ]
}
```

### Multi-Hop Delegation

Field authorization with full audit trail:

```
{
    CID(emergency-authorization) [
        'authorizes': "Emergency procurement up to $50,000"
        'signature': {
            XID(field-manager) [
                'signingAs': "Emergency Coordinator"
                'onBehalfOf': XID(corporation)
                'delegationChain': [XID(board), XID(ceo), XID(coo), XID(regional-vp)]
            ]
        }
    ]
}
```

### Combined with Principal Authority

Using both Signature Context and Principal Authority predicates:

```
{
    CID(ai-generated-report) [
        'principalAuthority': XID(research-director)
        'processDisclosure': "Generated by AI under human direction"
        'signature': {
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
- Verify the delegation chain if authority is claimed
- Consider the context and stakes of the assertion

### Delegation Verification

The presence of `delegatedBy` or `delegationChain` does not prove valid delegation. Verification requires:
- Checking that each delegator had authority to delegate
- Confirming the delegation was active at signing time
- Validating any scope or constraint limitations

### Capacity vs. Authority

`signingAs` describes claimed capacity, not granted authority. A signature claiming `signingAs: "CEO"` does not prove the signer is a CEO. External verification is required for high-stakes contexts.

### Chain Integrity

For `delegationChain`, each link should be independently verifiable. A broken or unverifiable link invalidates the claimed authority from that point forward.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [XID-Quickstart Tutorial 09: Binding Agreements](https://github.com/BlockchainCommons/XID-Quickstart)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Lifecycle predicates used by this BCR
- **BCR-2026-007: Principal Authority Predicates** — Authority over work (complementary concern)

---

*BCR-2026-006: Signature Context Predicates*
*Draft - February 2, 2026*
