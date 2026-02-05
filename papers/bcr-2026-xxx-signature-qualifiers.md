````markdown
# Signature Qualifiers for Gordian Envelope

This document defines an interoperable, XAdES-inspired vocabulary for signature metadata carried using the technique defined in [BCR-2024-009](bcr-2024-009-signature-metadata.md).

## BCR-2026-XXX DRAFT

**© 2026 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: February 4, 2026

---

## Abstract

[BCR-2024-009](bcr-2024-009-signature-metadata.md) defines a structural method for attaching immutable metadata to signatures in Gordian Envelope by creating a “signature metadata envelope” and signing it with the same key used for the payload signature. However, the metadata fields in that BCR are illustrative, not interoperable.

This document proposes a small, focused set of **Signature Qualifiers**: standardized predicates and object structures designed specifically for Gordian Envelope’s semantic system and (most importantly) for use inside Envelope signature metadata. The design is inspired by the high-value parts of XAdES “qualifying properties” (e.g., signing time, policy binding, commitment semantics, role/place, signed-object description, countersignatures), but avoids XAdES elements that are tightly bound to X.509/PKI long-term validation plumbing.

---

## Status of This Document

📙 This document is research and a proposed specification. It defines a vocabulary intended to be stable and interoperable, but it does not yet have a reference implementation.

---

## Terminology

This BCR uses the following terms consistently:

- **Signature target**: the exact digest value that the signature commits to (declared using `sig:Target`).
- **Signed envelope**: the target is a digest of a Gordian Envelope (`sig:EnvelopeSemanticDigest` or `sig:EnvelopeStructuralDigest`).
- **Signed object**: any object referenced in metadata, including envelopes, detached byte sequences, or externally-resolved artifacts (declared using `sig:SignedObject`). `sig:SignedObject` is descriptive; it does not define the cryptographic binding unless it includes (or is tied to) the signature target digest.
- **Signed presentation**: the concrete, possibly-obscured representation of the signed envelope at signing time (some nodes may be elided/encrypted/compressed).

---

## Background

### Gordian Envelope signatures with metadata

In [BCR-2024-009](bcr-2024-009-signature-metadata.md), we define a canonical pattern for making signature metadata immutable:

1. Sign the signed object’s digest to produce an inner `Signature` object.
2. Create a **signature metadata envelope** whose subject is that inner `Signature`, and add metadata as assertions on it.
3. Wrap and sign the signature metadata envelope with the **same private key**.
4. Attach the resulting signed signature-metadata envelope as the object of the signed object’s `'signed'` assertion (when the signed object is an envelope), or otherwise associate it by application-defined means.

This document does **not** change that structure. It defines interoperable metadata **inside** step (2).

### Unit and “deliberate emptiness”

[BCR-2026-001](bcr-2026-001-unit.md) defines **Unit** (`''`, Known Value 0) as *deliberate emptiness*: a position that carries **zero informational content** and **must not** be replaced with any other value. In Gordian Envelope, Unit enables envelopes whose meaning is conveyed entirely by their assertions, without requiring a subject identifier such as a DID or XID.

This is directly relevant here: most qualifier objects (policy bindings, role claims, place descriptors, etc.) are *record-like values* scoped to a single signature metadata envelope. They usually do not represent independently-identified entities. Therefore their subject should normally be **Unit**.

### References

[BCR-2024-011](bcr-2024-011-reference.md) defines `Reference` (CBOR tag `#6.40025`, UR type `ur:reference`) as a 32-byte globally unique reference to an object (the "referent"). References are intentionally **not typed**: the context in which they appear must allow the referent to be resolved (e.g., locally within a document, or globally via a registry or index).

This BCR uses `Reference` whenever it needs a compact, globally unique pointer to a signed object or related artifact, without embedding the object itself. When the referent type is not otherwise clear, this BCR pairs `Reference` with explicit qualifiers (e.g., `sig:targetType`, `sig:mediaType`) to disambiguate interpretation.

### Salted Values and decorrelation

[BCR-2023-017](bcr-2023-017-salt.md) defines `salt` (CBOR tag `#6.40018`, UR type `ur:salt`). [BCR-2026-004](bcr-2026-004-salted-value.md) defines the **Salted Value** pattern that uses Unit as the subject and carries the underlying value as:

```envelope
'' [
    'salt': Salt(<random-data>)
    'value': "Indiana"
]
```

This BCR permits Salted Values for certain small enumerated fields (e.g., region/locality) where elision may be expected and decorrelation is desirable. Where concealment is desired, presentations SHOULD elide the entire Salted Value wrapper (see [BCR-2026-004](bcr-2026-004-salted-value.md)).

### XAdES as inspiration

XAdES defines “qualifying properties” that add durable meaning and auditability to signatures (who/when/why/under what policy/what objects/what roles/what place/etc.), including a split between properties that are signed versus unsigned.

Gordian Envelope already provides a mechanism for binding metadata immutably to a signature (by signing the metadata envelope itself). The missing piece is an interoperable vocabulary that different implementers can rely on.

---

## Goals

1. **Interoperability:** Two independent implementers should produce signature metadata that can be recognized and understood without out-of-band agreement.
2. **Envelope-native:** Everything is expressed as Envelope assertions; complex metadata is represented as typed sub-envelopes that can be selectively disclosed or elided.
3. **Determinism-friendly:** Predicates SHOULD be expressed as Known Values when feasible.
4. **Policy & intent first:** Prioritize the signature semantics that matter most in real-world verification and audits:
   - *when* the signer claims to have signed
   - *what commitment* the signature represents
   - *what policy* the signature is bound to
   - *what object(s)* are being signed (especially for detached objects and referenced artifacts)
   - role/place context (when needed)
   - countersignature/endorsement support
   - an Envelope-native attestation of which signed-envelope nodes were obscured in the signed presentation
5. **Practical privacy:** Support common metadata that can be partially disclosed and decorrelated when needed, especially for small enumerated fields.

---

## Non-Goals (Out of Scope)

This BCR intentionally does **not** standardize the XAdES family’s PKI-heavy long-term validation material:

- certificate chain embedding
- OCSP/CRL and revocation values
- archival timestamp renewal structures

Those may be addressed by a future Envelope profile if needed.

---

## Methodology

We extracted the parts of XAdES that are broadly useful independent of XMLDSIG and PKI plumbing:

- `SigningTime`
- `DataObjectFormat` (for signed objects)
- `CommitmentTypeIndication`
- `SignaturePolicyIdentifier` / `SignaturePolicyStore`
- `SignerRole` / `SignatureProductionPlace`
- `CounterSignature`

We then mapped them into Envelope’s assertion model and the signature-metadata structure from [BCR-2024-009](bcr-2024-009-signature-metadata.md), incorporating the subject guidance from [BCR-2026-001](bcr-2026-001-unit.md):

- Most qualifier objects are *typed record values* and SHOULD use **Unit** as subject.
- Only use ARIDs (or other identifying subjects) when a qualifier object must be referenced independently across contexts.

For small enumerated fields where elision may be expected and decorrelation is desirable, we adopt **Salted Values** per [BCR-2026-004](bcr-2026-004-salted-value.md). If you anticipate needing decorrelatable elision later, you MUST choose Salted Values at creation time; you cannot “add salt later” without changing the signed metadata.

We also add one Envelope-native qualifier:

- **Obscured-nodes claim (`sig:obscured`):** a lexicographically-sorted array of **semantic digests** identifying which nodes in a signed envelope were obscured *in the signed presentation* (elided, encrypted, or compressed) at signing time.

---

## The Signature Qualifiers Profile

### Overview

Signature Qualifiers are assertions intended to appear inside the **signature metadata envelope** defined in [BCR-2024-009](bcr-2024-009-signature-metadata.md).

For example:

```envelope
Signature [
    'sig:signingTime': 2026-02-04T19:52:00Z
    'sig:signaturePolicy': '' [ ... ]
    'sig:commitment': '' [ ... ]
    ...
]
```

These assertions are then made immutable by the surrounding construction:

```envelope
{ Signature [ ...qualifiers... ] } [ 'signed': Signature ]
```

### Namespacing

All terms defined by this BCR use the prefix:

- `sig:` — “Signature Qualifiers (Envelope-native)”

In Envelope notation this is typically shown using known values as predicates:

- `'sig:signingTime'`
- `'sig:signaturePolicy'`
- etc.

### Canonical subject guidance for qualifier objects

Unless otherwise specified, all typed qualifier objects in this BCR:

- SHOULD use **Unit** (`''`) as their subject, per [BCR-2026-001](bcr-2026-001-unit.md).
- MUST NOT use Unit to mean “unknown” or “missing”; Unit means “this position carries no informational content and must not be replaced.”

**When to use a non-Unit subject (exceptional):**

A producer MAY use an [ARID](bcr-2022-002-arid.md) (or other identifying subject) for a typed qualifier object only when at least one of the following is true:

- the qualifier must be referenced multiple times from different places
- the qualifier must be referenced externally by identifier
- the qualifier represents an independently-identified entity rather than a record-like value

Even in these cases, producers SHOULD consider using a digest-based identity (e.g., envelope Digest or Reference) rather than a fresh ARID, when the semantics are “the immutable object with this exact digest.” ARIDs are used when there is no correlation between the value of the ARID and the referent object, which makes them useful when the referent is mutable (i.e., may change over time.)

---

## Known Value Assignments

### Reserved code point range

This BCR proposes reserving the code point range:

- **1600–1699** for Signature Qualifiers (`sig:`), including predicates, types, and controlled vocabularies.

This range is intended for inclusion in the “community, specification required” registry (see [BCR-2023-002](bcr-2023-002-known-value.md)).

### Assignments

#### Predicates (1600–1619)

| Code Point | Term                     | Kind      | Description                                                                         |
|-----------:|--------------------------|-----------|-------------------------------------------------------------------------------------|
|       1600 | `sig:profile`            | predicate | Declares the Signature Qualifiers profile identifier/version used by the metadata.  |
|       1601 | `sig:signingTime`        | predicate | Claimed time of signing.                                                            |
|       1602 | `sig:signerRole`         | predicate | Claimed signer role/capacity (`sig:Role`).                                          |
|       1603 | `sig:signingPlace`       | predicate | Claimed production place/jurisdiction (`sig:Place`).                                |
|       1604 | `sig:commitment`         | predicate | Commitment semantics (`sig:Commitment`).                                            |
|       1605 | `sig:signaturePolicy`    | predicate | Policy binding (`sig:Policy`).                                                      |
|       1606 | `sig:signedObject`       | predicate | Description of a signed object (`sig:SignedObject`), repeatable.                    |
|       1607 | `sig:target`             | predicate | Declares the signature target (`sig:Target`).                                       |
|       1608 | `sig:countersignatureOf` | predicate | Identifies what signature (or signature digest) is being countersigned.             |
|       1609 | `sig:endorsement`        | predicate | Explains countersignature intent (`sig:Endorsement`).                               |
|       1610 | `sig:obscured`           | predicate | Sorted array of semantic digests of signed-envelope nodes obscured in the signed presentation. |

#### Field predicates used inside typed qualifier objects (1620–1659)

| Code Point | Term                      | Kind      | Description                                                                                         |
|-----------:|---------------------------|-----------|-----------------------------------------------------------------------------------------------------|
|       1620 | `sig:policyId`            | predicate | Policy identifier (URI/string).                                                                     |
|       1621 | `sig:policyDigest`        | predicate | Digest of the policy bytes (commitment to exact policy text).                                       |
|       1622 | `sig:policyURI`           | predicate | Retrieval URI for the policy (optional convenience).                                                |
|       1623 | `sig:policyName`          | predicate | Human name for policy.                                                                              |
|       1624 | `sig:policyVersion`       | predicate | Human version label.                                                                                |
|       1625 | `sig:commitmentType`      | predicate | Controlled commitment type (see enum below).                                                        |
|       1626 | `sig:commitmentStatement` | predicate | Human statement describing commitment.                                                              |
|       1627 | `sig:appliesTo`           | predicate | Reference/digest indicating which object(s) the claim applies to.                                   |
|       1628 | `sig:roleName`            | predicate | Human role name.                                                                                    |
|       1629 | `sig:roleAuthority`       | predicate | Reference to authority defining/assigning the role.                                                 |
|       1630 | `sig:roleEvidence`        | predicate | Reference/digest to evidence backing the role claim (optional).                                     |
|       1631 | `sig:country`             | predicate | Country code (e.g., ISO 3166-1 alpha-2).                                                            |
|       1632 | `sig:region`              | predicate | Region/state/province (string; optionally a Salted Value per [BCR-2026-004](bcr-2026-004-salted-value.md)). |
|       1633 | `sig:locality`            | predicate | Locality/city (string; optionally a Salted Value per [BCR-2026-004](bcr-2026-004-salted-value.md)).        |
|       1634 | `sig:timeZone`            | predicate | Time zone identifier (IANA TZ database string).                                                     |
|       1635 | `sig:objectRef`           | predicate | Reference (`ur:reference`, CBOR tag `#6.40025`) or digest identifying an object.                    |
|       1636 | `sig:mediaType`           | predicate | Media type (e.g., `application/pdf`).                                                               |
|       1637 | `sig:encoding`            | predicate | Encoding label (e.g., `binary`, `base64`).                                                          |
|       1638 | `sig:displayName`         | predicate | Human label for the object.                                                                         |
|       1639 | `sig:language`            | predicate | Language tag (BCP 47 string).                                                                       |
|       1640 | `sig:targetType`          | predicate | Controlled digest type for `sig:Target` and for digest-valued `sig:objectRef` (see enum below).     |

#### Types (1650–1669)

| Code Point | Term               | Kind | Description                                                       |
|-----------:|--------------------|------|-------------------------------------------------------------------|
|       1650 | `sig:Policy`       | type | Typed envelope describing a signature policy binding.             |
|       1651 | `sig:Commitment`   | type | Typed envelope describing commitment semantics.                   |
|       1652 | `sig:Role`         | type | Typed envelope describing signer role/capacity.                   |
|       1653 | `sig:Place`        | type | Typed envelope describing signing place/jurisdiction.             |
|       1654 | `sig:SignedObject` | type | Typed envelope describing a signed object (descriptive).          |
|       1655 | `sig:Target`       | type | Typed envelope declaring the signature target (cryptographic).    |
|       1656 | `sig:Endorsement`  | type | Typed envelope describing countersignature endorsement semantics. |

#### Commitment type controlled vocabulary (1670–1679)

| Code Point | Term            | Kind | Description                      |
|-----------:|-----------------|------|----------------------------------|
|       1670 | `sig:Authored`  | enum | “I authored this.”               |
|       1671 | `sig:Approved`  | enum | “I approve this.”                |
|       1672 | `sig:Witnessed` | enum | “I witnessed this.”              |
|       1673 | `sig:Reviewed`  | enum | “I reviewed this.”               |
|       1674 | `sig:Notarized` | enum | “I notarize this.”               |
|       1675 | `sig:Certified` | enum | “I certify this.”                |
|       1676 | `sig:Attested`  | enum | “I attest this is true/correct.” |

#### Target type controlled vocabulary (1680–1689)

| Code Point | Term                           | Kind | Description                                                                 |
|-----------:|--------------------------------|------|-----------------------------------------------------------------------------|
|       1680 | `sig:EnvelopeSemanticDigest`   | enum | Target is the semantic digest of a Gordian Envelope (default).              |
|       1681 | `sig:EnvelopeStructuralDigest` | enum | Target is the structural digest of a Gordian Envelope.                      |
|       1682 | `sig:DetachedBytesDigest`      | enum | Target is a digest of detached bytes (non-Envelope object).                 |

`sig:EnvelopeSemanticDigest` is the default and most common target type. The semantic digest is stable across elision, encryption, and compression — a signature over a semantic digest remains valid regardless of how the envelope is later obscured or revealed.

`sig:EnvelopeStructuralDigest` is used only when the signer intends the signature to be invalidated if the signed envelope's obscuration state changes. Because the structural digest incorporates whether each node is elided, encrypted, or compressed, any change to the envelope's disclosure — revealing an elided assertion, decrypting an encrypted one, or decompressing a compressed one — will change the structural digest and invalidate the signature. This is appropriate when the signer wants to lock down a specific presentation of the envelope. When validating such a signature, the envelope's structural digest must be used, not its semantic digest.

`sig:DetachedBytesDigest` is used when signing objects that are not Gordian Envelopes, such as files, binary artifacts, or other opaque byte sequences.

---

## Object Specifications

All typed qualifier objects in this section are shown with **Unit** (`''`) as their subject, per [BCR-2026-001](bcr-2026-001-unit.md). This is the RECOMMENDED form for signature metadata.

### `sig:Policy`

A policy binds a signature to a specific ruleset. A verifier MAY require a specific policy digest or policy identifier to accept a signature.

```envelope
'' [
    'isA': 'sig:Policy'
    'sig:policyId': "urn:example:policy:acme-signing-policy:v3"
    'sig:policyDigest': Digest(<sha256>)
    'sig:policyURI': "https://example.com/policies/acme-signing-policy-v3"
    'sig:policyName': "Acme Signing Policy"
    'sig:policyVersion': "3.0"
]
```

### `sig:Commitment`

Commitment describes what the signer means by signing.

```envelope
'' [
    'isA': 'sig:Commitment'
    'sig:commitmentType': 'sig:Approved'
    'sig:commitmentStatement': "Approved for release."
    'sig:appliesTo': Reference(<ref>)     // or Digest(...)
]
```

### `sig:Role`

Role describes the signer’s claimed capacity and optionally the authority/evidence for that claim.

```envelope
'' [
    'isA': 'sig:Role'
    'sig:roleName': "Release Manager"
    'sig:roleAuthority': Reference(<ref>)            // optional
    'sig:roleEvidence': Reference(<ref>)             // or Digest(...), optional
]
```

> `sig:roleAuthority` and `sig:roleEvidence` are optional because many deployments will not have a portable credentialing framework; the goal is to allow structured claims without forcing a PKI-style model.

### `sig:Place`

Place is intentionally coarse-grained and disclosure-friendly.

Fields such as `sig:region` and `sig:locality` are sometimes drawn from small enumerable sets and may be elided. To support decorrelation in those cases, producers MAY encode those fields as **Salted Values** per [BCR-2026-004](bcr-2026-004-salted-value.md). If you anticipate needing decorrelatable elision, you MUST choose Salted Values when constructing the signed metadata.

Plain-string form:

```envelope
'' [
    'isA': 'sig:Place'
    'sig:country': "US"
    'sig:region': "ID"
    'sig:locality': "Eagle"
    'sig:timeZone': "America/Boise"
]
```

Decorrelatable form (recommended when region/locality may be elided):

```envelope
'' [
    'isA': 'sig:Place'
    'sig:country': "US"

    'sig:region': '' [
        'salt': Salt(<random-bytes>)
        'value': "ID"
    ]

    'sig:locality': '' [
        'salt': Salt(<random-bytes>)
        'value': "Eagle"
    ]

    'sig:timeZone': "America/Boise"
]
```

### `sig:Target`

`sig:Target` declares the **signature target**, i.e., the digest value that the signature commits to. It is the normative binding between a signature and what is signed.

A `sig:Target` MUST use a `Digest` in `sig:objectRef`. `Reference` is not permitted as a signature target because it does not cryptographically bind to the referent.

```envelope
'' [
    'isA': 'sig:Target'
    'sig:targetType': 'sig:EnvelopeSemanticDigest'
    'sig:objectRef': Digest(<envelope-semantic-digest>)
]
```

### `sig:obscured`

The `sig:obscured` assertion records which nodes in a **signed envelope** were obscured in the **signed presentation** — i.e., elided, encrypted, or compressed at signing time.

This qualifier applies **only** when the signature target is a signed envelope (`sig:EnvelopeSemanticDigest` or `sig:EnvelopeStructuralDigest`). It MUST NOT be used when the signature target is `sig:DetachedBytesDigest`.

The object is a CBOR array of `Digest` values, lexicographically sorted. Each digest identifies a node (or subtree root) in the signed envelope that was obscured in the signed presentation.

#### Digest type

The `sig:obscured` array MUST contain **semantic digests** of the obscured nodes.

This ensures the claim remains checkable against the same signed envelope even if the envelope’s obscuration state changes later (e.g., if an elided node is later revealed). In other words, `sig:obscured` complements signatures over `sig:EnvelopeSemanticDigest`.

#### Minimality and redundancy

To maximize interoperability and keep the list compact:

- Producers SHOULD include only **maximal obscured subtree roots**.
- Producers MUST NOT include both an obscured node and any of its descendants in the array.
- Producers MUST NOT include duplicate digests.

This makes `sig:obscured` a set of “roots of obscured regions” in the signed envelope.

#### Ordering

The digest array MUST be lexicographically sorted using Envelope/dCBOR’s existing digest-sorting rules: compare the **tagged CBOR-encoded byte strings** of the `Digest` values.

#### Relationship to `sig:targetType`

- If the signature target is `sig:EnvelopeSemanticDigest`, `sig:obscured` is the signer’s objective statement about what the signed presentation hid at signing time, and remains meaningful even if later disclosure changes.
- If the signature target is `sig:EnvelopeStructuralDigest`, `sig:obscured` is generally redundant (because the structural digest already commits to obscuration state), but may still be included as an index. In that case, it SHOULD correspond to the obscuration state of the signed presentation.

#### Interpretation

- **`'sig:obscured': []`** (empty array) — the signer attests that the signed presentation contained no obscured nodes.
- **`'sig:obscured': [ Digest(<root>) ]`** where the digest is the signed envelope’s semantic digest — the signer attests they signed a presentation where the entire signed envelope was obscured.
- **`'sig:obscured': [ Digest(<a>), Digest(<b>), ... ]`** — the signer attests that the listed subtrees were obscured in the signed presentation, and (by omission) that other subtrees were not obscured.

A verifier who holds the full (unobscured) signed envelope can check each digest against the envelope’s digest tree to confirm that the listed nodes exist and to understand exactly which content the signed presentation obscured.

> `sig:obscured` is an objective claim about the signed presentation’s obscuration state, not about the signer’s private knowledge.

**Example — signer attests the signed presentation hid nothing:**

```envelope
Signature [
    'sig:signingTime': 2026-02-04T19:52:00Z
    'sig:obscured': []
]
```

**Example — signer attests they signed a fully obscured envelope:**

```envelope
Signature [
    'sig:signingTime': 2026-02-04T19:52:00Z
    'sig:obscured': [
        Digest(71274df1)
    ]
]
```

**Example — two subtrees were obscured at signing time:**

```envelope
Signature [
    'sig:signingTime': 2026-02-04T19:52:00Z
    'sig:obscured': [
        Digest(3a7c8f2d)
        Digest(b4e1a8c0)
    ]
]
```

**Guidance:**

- Producers SHOULD include `sig:obscured` whenever the signed presentation contains any obscured nodes.
- Producers MAY include `'sig:obscured': []` to explicitly attest that nothing was obscured, though omitting the assertion entirely is also valid.
- Verifiers SHOULD treat the absence of `sig:obscured` as "unknown" — the signer made no claim about obscuration.

### `sig:SignedObject`

`sig:SignedObject` describes a **signed object** relevant to the signature (including the signed envelope itself, detached byte sequences, or referenced artifacts). It is descriptive metadata; it does not define the cryptographic binding unless it includes (or is explicitly tied to) the signature target digest.

If `sig:objectRef` is a `Reference`, the referent type is resolved from context; producers SHOULD include enough context for resolution, such as `sig:mediaType`, `sig:displayName`, `sig:language`, and domain-specific qualifiers.

If `sig:objectRef` is a `Digest`, `sig:targetType` SHOULD be provided to specify what that digest means (`sig:EnvelopeSemanticDigest`, `sig:EnvelopeStructuralDigest`, or `sig:DetachedBytesDigest`).

```envelope
'' [
    'isA': 'sig:SignedObject'
    'sig:objectRef': Reference(<ref>)              // or Digest(...)
    'sig:targetType': 'sig:DetachedBytesDigest'    // only when sig:objectRef is Digest(...)
    'sig:mediaType': "application/pdf"
    'sig:encoding': "binary"
    'sig:displayName': "Contract.pdf"
    'sig:language': "en-US"
]
```

### `sig:Endorsement`

Endorsement explains countersignature intent.

```envelope
'' [
    'isA': 'sig:Endorsement'
    'sig:commitmentType': 'sig:Witnessed'
    'sig:commitmentStatement': "Witnessed Alice’s approval."
    'sig:appliesTo': Digest(<signature-digest>)   // or Reference(...)
]
```

---

## Requirements for Use in Signature Metadata

1. Signature Qualifiers MUST be placed inside the signature metadata envelope defined in [BCR-2024-009](bcr-2024-009-signature-metadata.md) if they are intended to be immutable.
2. Producers SHOULD encode typed qualifier objects with **Unit** (`''`) as their subject, per [BCR-2026-001](bcr-2026-001-unit.md), unless they have a specific need for a referencable subject.
3. Producers SHOULD use `Reference` (per [BCR-2024-011](bcr-2024-011-reference.md)) when they need a compact globally unique pointer to a referent; when the referent type is not otherwise clear, they SHOULD provide disambiguation (e.g., via `sig:mediaType`, `sig:displayName`, or other qualifiers).
4. Producers MAY represent small enumerated values as **Salted Values** per [BCR-2026-004](bcr-2026-004-salted-value.md) when those values may be elided and decorrelation is desirable. This is particularly relevant for `sig:region` and `sig:locality`.
5. When Salted Values are used and the value is to be concealed, presentations SHOULD elide the entire Salted Value wrapper (see [BCR-2026-004](bcr-2026-004-salted-value.md)).
6. `sig:Target` MUST use a `Digest` in `sig:objectRef`. `Reference` MUST NOT be used as a signature target.
7. `sig:obscured` MUST be used only when the signature target type is `sig:EnvelopeSemanticDigest` or `sig:EnvelopeStructuralDigest`. It MUST NOT be used when the signature target type is `sig:DetachedBytesDigest`.
8. Producers SHOULD include `sig:obscured` whenever the signed presentation contains any obscured nodes. If present, the array:
   - MUST contain semantic digests,
   - MUST be lexicographically sorted by the tagged CBOR-encoded digest bytes,
   - SHOULD contain only maximal obscured subtree roots, and
   - MUST NOT include redundant ancestor/descendant digests.
9. Verifiers that understand this BCR SHOULD:
   - verify both the payload signature and the metadata signature as defined in [BCR-2024-009](bcr-2024-009-signature-metadata.md)
   - interpret Signature Qualifier predicates and typed objects according to this BCR
10. A verifier MAY ignore Signature Qualifiers it does not recognize.
11. Producers SHOULD include `'sig:profile'` to allow future evolution.

Example profile declaration:

```envelope
'sig:profile': "sig:SQ-1"
```

---

## Examples

### Example 1: Approval signature with explicit “nothing obscured” claim

```envelope
{
    "Release Artifact" [
        'isA': "SoftwareRelease"
        'version': "1.2.3"
        "artifact": Reference(<ref>)
    ]
} [
    'signed': {
        Signature(<alice-key>) [
            'sig:profile': "sig:SQ-1"
            'sig:signingTime': 2026-02-04T19:52:00Z
            'sig:obscured': []

            'sig:signaturePolicy': '' [
                'isA': 'sig:Policy'
                'sig:policyId': "urn:example:policy:release-approval:v1"
                'sig:policyDigest': Digest(<sha256>)
            ]

            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Approved'
                'sig:commitmentStatement': "Approved for public release."
                'sig:appliesTo': Reference(<ref>)
            ]

            'sig:signerRole': '' [
                'isA': 'sig:Role'
                'sig:roleName': "Release Manager"
            ]

            'sig:signingPlace': '' [
                'isA': 'sig:Place'
                'sig:country': "US"
                'sig:region': "ID"
                'sig:timeZone': "America/Boise"
            ]

            'sig:signedObject': '' [
                'isA': 'sig:SignedObject'
                'sig:objectRef': Reference(<ref>)
                'sig:mediaType': "application/octet-stream"
                'sig:displayName': "release-1.2.3.tgz"
            ]
        ]
    } [ 'signed': Signature(<alice-key>) ]
]
```

### Example 2: Signature made over an obscured signed-envelope presentation

Here the signer attests that two subtrees were obscured in the signed presentation:

```envelope
Signature(<alice-key>) [
    'sig:profile': "sig:SQ-1"
    'sig:signingTime': 2026-02-04T19:52:00Z
    'sig:obscured': [
        Digest(3a7c8f2d)
        Digest(b4e1a8c0)
    ]
]
```

### Example 3: Holder-based elision of sensitive place fields with decorrelation

If the signature metadata was created with Salted Values for region/locality, a holder can elide those assertions without leaking correlatable digests for common small values.

Original (created by signer):

```envelope
'sig:signingPlace': '' [
    'isA': 'sig:Place'
    'sig:country': "US"

    'sig:region': '' [
        'salt': Salt(<random-bytes>)
        'value': "ID"
    ]

    'sig:locality': '' [
        'salt': Salt(<random-bytes>)
        'value': "Eagle"
    ]

    'sig:timeZone': "America/Boise"
]
```

Redacted presentation (by holder):

```envelope
'sig:signingPlace': '' [
    'isA': 'sig:Place'
    'sig:country': "US"
    ELIDED(2)    // elide the region and locality assertions (each uses a Salted Value wrapper)
    'sig:timeZone': "America/Boise"
]
```

---

## Security Considerations

1. **Metadata immutability:** These qualifiers are intended to be immutable only when used inside the signed signature-metadata structure of [BCR-2024-009](bcr-2024-009-signature-metadata.md).
2. **Subject injection / identity pollution:** Using fresh UUIDs or ARIDs as subjects for record-like qualifier objects can create accidental claims of independent identity and can frustrate comparison/deduplication. Defaulting to **Unit** avoids this and correctly signals “meaning is entirely in the assertions” as defined in [BCR-2026-001](bcr-2026-001-unit.md).
3. **Reference type ambiguity:** `Reference` values (per [BCR-2024-011](bcr-2024-011-reference.md)) do not carry type information. Producers SHOULD provide sufficient context to resolve a reference.
4. **Correlation and dictionary attacks on elided small fields:** Elided digests of small enumerable values (e.g., state codes, common localities) can be correlated or brute-forced. Where these values may be elided, producers SHOULD consider Salted Values per [BCR-2026-004](bcr-2026-004-salted-value.md), and presentations that conceal the value SHOULD elide the wrapper.
5. **Obscured claim semantics:** `sig:obscured` is an objective claim about the signed presentation’s obscuration state, not about the signer’s private knowledge. It is defined only for signed envelopes, not detached-byte targets.
6. **Policy substitution:** If a policy URI is used without a policy digest, policy substitution attacks become possible. Implementers SHOULD include `sig:policyDigest` whenever policy meaning matters.

---

## Future Work

- Standardize common `sig:profile` identifiers and evolution rules.
- Define an optional profile for long-term validation material (timestamps, validation evidence) if Envelope deployments require it.
- Align `sig:roleAuthority` and `sig:roleEvidence` with identity/credential work as it matures, while preserving the value-like default representation.

---

## References

### Internal (BCR)

- [BCR-2022-002: ARID: Apparently Random Identifier](bcr-2022-002-arid.md)
- [BCR-2023-002: Known Values](bcr-2023-002-known-value.md)
- [BCR-2023-017: UR Type Definition for Random Salt](bcr-2023-017-salt.md)
- [BCR-2024-009: Signatures with Metadata in Gordian Envelope](bcr-2024-009-signature-metadata.md)
- [BCR-2024-011: References](bcr-2024-011-reference.md)
- [BCR-2026-001: Unit: The Known Value for Deliberate Emptiness](bcr-2026-001-unit.md)
- [BCR-2026-004: Envelope Salted Values](bcr-2026-004-salted-value.md)

### External

- W3C Note: XML Advanced Electronic Signatures (XAdES): https://www.w3.org/TR/XAdES/
- ETSI EN 319 132-1 V1.3.1: XAdES digital signatures (baseline signatures): https://www.etsi.org/deliver/etsi_en/319100_319199/31913201/01.03.01_60/en_31913201v010301p.pdf
````
