# Anchor Predicates

## BCR-2026-004

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for anchoring assertions to cryptographic event logs in Gordian Envelopes. These predicates enable independent attestation that an assertion exists, providing verifiable proof of existence and ordering without implying consent or approval.

These predicates are proposed for the **core registry** (codepoints 87-93), as they represent fundamental cryptographic infrastructure for envelopes.

## Status: Core Registry Proposal

This BCR proposes additions to the **Blockchain Commons Core Registry** (codepoints 0-99) as defined in [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

### Placement Rationale

The proposed codepoints (87-93) follow the XID Privileges range (70-86), which ends with `Revoke` (86). This placement is logical because:
- Anchoring is cryptographic infrastructure, like XID operations
- Both anchoring and revocation deal with assertion state management
- The 87-100 range is currently unassigned

### Request for Community Review

We invite feedback on:
- Whether these predicates belong in the core registry
- Whether the proposed codepoint assignments are appropriate
- Any conflicts with existing or planned predicates
- Suggested refinements to predicate definitions

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### Problem Statement

Assertions in Gordian Envelopes may need independent attestation that they exist at a particular point in time. This is distinct from:
- **Signing** — which implies consent or authorship
- **Witnessing** (human) — which implies observation of events

Cryptographic event logs (as in Certificate Transparency, Key Transparency, and CEL) provide **append-only** structures where independent parties can attest to having observed an assertion, without implying approval.

### Why Anchoring Matters

Anchoring provides **proof of existence and ordering** without requiring trust in the asserter:

1. **Certificate Transparency** — Public logs prove certificates existed at a point in time, enabling detection of misissued certificates even after the fact
2. **Key Transparency** — Append-only logs of key bindings prevent silent key replacement attacks
3. **Software Transparency** — Binary hashes in logs prove what code was distributed, enabling detection of supply chain attacks

In all cases, the value comes from the log's **append-only, publicly auditable nature**. Once an assertion is anchored, it cannot be removed or altered — the log provides permanent evidence that the assertion existed.

### Use Cases

**Timestamp Authority**: An independent service anchors assertions to prove they existed before a certain time — useful for intellectual property, contract precedence, or regulatory compliance.

**Multi-Party Attestation**: Multiple log operators anchor the same assertion (quorum), providing resilience against any single operator being compromised or unavailable.

**Audit Trails**: Anchoring creates tamper-evident records of assertions for compliance, legal discovery, or forensic analysis.

**Revocation Detection**: Anchoring enables detection of attempts to silently replace assertions — the original anchor remains in the log even after revocation or update.

### Terminology Distinction

The term "witness" is overloaded:
- **Fair Witness** (human attestation) — a neutral party observing and attesting to facts
- **Cryptographic witness** — an entity anchoring assertions to a log

This BCR uses **anchor** terminology to avoid confusion with human witnessing concepts.

### Solution

This specification defines predicates for cryptographic log anchoring:

| Predicate | Purpose |
|-----------|---------|
| `anchoredBy` | Who anchored the assertion |
| `anchors` | What assertion is anchored |
| `anchoredAt` | When it was anchored |
| `anchorDigest` | Cryptographic binding |
| `anchorLog` | Which log contains the anchor |

Optional extensions for multi-anchor scenarios:
| Predicate | Purpose |
|-----------|---------|
| `anchorQuorum` | Minimum anchors required |
| `anchorIndex` | Position in log |

### Conceptual Foundation

These predicates are **Envelope-native vocabulary** for expressing anchoring relationships within Gordian Envelopes, which uses concepts inspired by:
- [Cryptographic Event Logs (CEL)](https://digitalbazaar.github.io/cel-spec/)
- Certificate Transparency (RFC 6962)
- Key Transparency systems

> **Note**: This is not a bridge format or interoperability specification for CT/CEL. Round-trip conversion to/from external log formats would require a separate specification.

## Terminology

**Anchor**: A cryptographic attestation that an assertion exists in a log, without implying consent or approval.

**Anchor Assertion**: An envelope asserting that another assertion has been anchored to a log.

**Event Log**: An append-only, cryptographically verifiable data structure (e.g., Merkle tree).

**Checkpoint**: A signed summary of log state at a point in time.

## Proposed Known Value Assignments

All proposed codepoints are in the **Core Registry** range (0-99).

### Anchor Predicates (87-93)

---

#### 87: `anchoredBy`

**Type**: property
**Definition**: Identifies the entity that anchored an assertion to a cryptographic event log.
**Domain**: Any assertion
**Range**: XID, DID, or URI identifying the anchoring entity
**Usage**: Declares which entity provided the anchor attestation.

```
    Digest(my-assertion) [
        'anchoredBy': XID(log-operator)
        'anchoredAt': 2026-02-02T12:00:00Z
    ]
```

**Notes**:
- Anchoring is attestation of existence, not consent or approval
- Multiple `anchoredBy` assertions may exist for the same assertion (different anchors)

---

#### 88: `anchors`

**Type**: property
**Definition**: References the assertion that is being anchored.
**Domain**: Anchor assertion
**Range**: Digest or URI of the anchored assertion
**Usage**: Establishes an explicit, verifiable link between an anchor assertion and the assertion it attests to.

```
    Digest(anchor-assertion) [
        'anchors': Digest(original-assertion)
        'anchoredBy': XID(log-operator)
        'anchorDigest': Digest(abc123...)
    ]
```

---

#### 89: `anchoredAt`

**Type**: property
**Definition**: The time at which the assertion was anchored to the log.
**Domain**: Anchor assertion
**Range**: xsd:dateTime (ISO 8601)
**Usage**: Supports temporal ordering, auditability, and equivocation detection.

**Notes**:
- This is when the anchor was created, not when the original assertion was created
- Use `date` (16) or `validFrom` (21) for the original assertion's timestamp

---

#### 90: `anchorDigest`

**Type**: property
**Definition**: A cryptographic digest of the canonical form of the assertion being anchored.
**Domain**: Anchor assertion
**Range**: Digest
**Usage**: Cryptographically binds the anchor to a specific assertion representation.

```
    Digest(anchor-assertion) [
        'anchors': Digest(original-assertion)
        'anchorDigest': Digest(e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855)
    ]
```

**Notes**:
- Enables verification that the anchored content hasn't changed
- Uses the native Envelope `Digest` type for type safety
- Should use the canonical envelope digest

---

#### 91: `anchorLog`

**Type**: property
**Definition**: Identifies the cryptographic event log in which the assertion was anchored.
**Domain**: Anchor assertion
**Range**: URI identifying the log
**Usage**: Enables cross-log comparison and detection of inconsistent log views.

```
    Digest(anchor-assertion) [
        'anchors': Digest(original-assertion)
        'anchorLog': "https://log.example.com/v1"
    ]
```

---

#### 92: `anchorQuorum`

**Type**: property
**Definition**: Specifies the minimum number of distinct anchors required for an assertion to satisfy anchoring requirements.
**Domain**: Any assertion
**Range**: Integer or policy expression
**Usage**: Expresses governance or trust thresholds independently of verification.

```
    Digest(high-value-assertion) [
        'anchorQuorum': 3
    ]
```

**Notes**:
- This is a policy declaration, not a verification mechanism
- Verification of quorum satisfaction is application-specific

---

#### 93: `anchorIndex`

**Type**: property
**Definition**: The index or position of the anchored assertion in the log.
**Domain**: Anchor assertion
**Range**: Integer
**Usage**: Supports detection of log equivocation and inconsistent ordering claims.

```
    Digest(anchor-assertion) [
        'anchors': Digest(original-assertion)
        'anchorLog': "https://log.example.com/v1"
        'anchorIndex': 12345
    ]
```

---

## Usage Patterns

### Basic Anchoring

```
    Digest(anchor-assertion) [
        'anchors': Digest(original-document)
        'anchoredBy': XID(transparency-log)
        'anchoredAt': 2026-02-02T12:00:00Z
        'anchorDigest': Digest(...)
        'anchorLog': "https://log.example.com/v1"
    ]
```

### Multiple Anchors (Quorum)

```
    Digest(important-assertion) [
        'anchorQuorum': 2
    ]

// Anchor 1
    Digest(anchor-1) [
        'anchors': Digest(important-assertion)
        'anchoredBy': XID(log-operator-a)
    ]

// Anchor 2
    Digest(anchor-2) [
        'anchors': Digest(important-assertion)
        'anchoredBy': XID(log-operator-b)
    ]
```

### Anchor Updates

When an assertion is revoked or updated, a new anchor entry is created:

```
Digest(update-anchor) [
    'anchors': Digest(updated-assertion)
    'anchoredBy': XID(log-operator)
]
```

> **Important**: This creates a **new** anchor entry in the log. The original anchor remains permanently in the append-only log — it is not modified or deleted. This is how Certificate Transparency handles certificate revocation: the original certificate's log entry persists, but a newer entry indicates the update.

## Relationship to Other Predicates

### Core Registry

| Codepoint | Predicate | Relationship |
|-----------|-----------|--------------|
| 21 | `validFrom` | Use for assertion validity, not anchor time |
| 22 | `validUntil` | Use for assertion expiry |
| 86 | `Revoke` | XID key revocation (different from assertion supersession) |

### BCR-2026-005 (General Assertions)

| Predicate | Usage with Anchors |
|-----------|-------------------|
| `revocationReason` | Why an anchor was revoked |

## Security Considerations

### Anchoring vs. Signing

Anchoring attests to **existence**, not **approval**. An anchor assertion means "I observed this assertion in my log view" — it does not mean "I agree with this assertion" or "I authorize this assertion."

### Log Trust

Relying parties must evaluate:
- Whether they trust the log operator (`anchoredBy`)
- Whether the log itself is trustworthy (`anchorLog`)
- Whether sufficient anchors exist (`anchorQuorum`)

### Equivocation Detection

The `anchorIndex` predicate supports detection of log equivocation — where a log operator presents different views to different parties. Cross-log comparison using `anchorLog` and `anchorIndex` can reveal inconsistencies.

### Hash Binding

The `anchorDigest` provides cryptographic binding between the anchor and the anchored content. Verifiers should confirm that the hash matches the canonical form of the referenced assertion.

## Open Questions

### Relationship to Provenance Marks

[BCR-2025-001: Provenance Marks](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2025-001-provenance-mark.md) provides a powerful mechanism for **self-sovereign, permissionless provenance** through forward-commit chains. Provenance Marks:

- Require no external infrastructure — they are self-proving
- Enable permissionless operation — no log operators needed
- Use forward commits to establish temporal ordering
- Create cryptographic chains within a document series

Anchor predicates address a **different use case**: external attestation by independent parties. They are useful when:

- Third-party attestation is required (regulatory, compliance)
- Cross-organization verification is needed
- Independent witnesses add trust beyond self-attestation
- Integration with existing transparency log infrastructure is desired

| Aspect | Provenance Marks | Anchor Predicates |
|--------|------------------|-------------------|
| Infrastructure | None required (self-sovereign) | Requires log operators |
| Permission model | Permissionless | Depends on log access |
| Proof type | Forward-commit chain | External attestation |
| Trust model | Self-proving sequence | Independent witnesses |
| Primary use | Document series integrity | Cross-party attestation |

**These mechanisms are independent**: Anchor predicates can be used without Provenance Marks, and Provenance Marks work without external anchoring. They may also be **complementary** — external anchors could potentially strengthen Provenance Mark chains for high-assurance scenarios.

**Questions for community review:**

1. When both mechanisms are used together, what is the recommended pattern?
2. Should external anchors reference Provenance Mark chain hashes, or individual assertions?
3. Are there use cases where one mechanism clearly subsumes the other?

We invite feedback on how these specifications should interoperate. See also the [Provenance Mark developer documentation](https://developer.blockchaincommons.com/provemark/).

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [Cryptographic Event Logs (CEL)](https://github.com/w3c-ccg/cel-spec)
- [Certificate Transparency (RFC 6962)](https://datatracker.ietf.org/doc/html/rfc6962)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)
- [BCR-2025-001: Provenance Marks](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2025-001-provenance-mark.md)

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — `revocationReason` for anchor revocations
- **BCR-2026-007: Principal Authority Predicates** — Authority relationships

---

*BCR-2026-004: Anchor Predicates*
*Draft - February 2, 2026*
