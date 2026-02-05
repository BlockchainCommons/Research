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

## Background

### Gordian Envelope signatures with metadata

In [BCR-2024-009](bcr-2024-009-signature-metadata.md), we define a canonical pattern for making signature metadata immutable:

1. Sign the payload envelope’s digest to produce an inner `Signature` object.
2. Create a **signature metadata envelope** whose subject is that inner `Signature`, and add metadata as assertions on it.
3. Wrap and sign the signature metadata envelope with the **same private key**.
4. Attach the resulting signed signature-metadata envelope as the object of the payload’s `'signed'` assertion.

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
   - *what object(s)* are being signed (especially for attachments or detached objects)
   - role/place context (when needed)
   - countersignature/endorsement support
   - an Envelope-specific “what did the signer actually see?” claim to reduce misrepresentation after elision
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

For small enumerated fields where elision may be expected and decorrelation is desirable, we adopt **Salted Values** per [BCR-2026-004](bcr-2026-004-salted-value.md).

We also add one Envelope-specific qualifier:

- **Visibility claim:** what portion(s) the signer asserts were visible at signing time, to reduce the chance that later disclosure/elision can be used to misrepresent what was endorsed.

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
|       1607 | `sig:target`             | predicate | Declares the intended signature target (`sig:Target`).                              |
|       1608 | `sig:countersignatureOf` | predicate | Identifies what signature (or signature digest) is being countersigned.             |
|       1609 | `sig:endorsement`        | predicate | Explains countersignature intent (`sig:Endorsement`).                               |
|       1610 | `sig:visibility`         | predicate | Signer visibility claim (`sig:Visibility`).                                         |

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
|       1640 | `sig:targetType`          | predicate | Controlled target/reference type (see enum below).                                                  |
|       1641 | `sig:visibilityType`      | predicate | Controlled visibility type (see enum below).                                                        |

#### Types (1650–1669)

| Code Point | Term               | Kind | Description                                                       |
|-----------:|--------------------|------|-------------------------------------------------------------------|
|       1650 | `sig:Policy`       | type | Typed envelope describing a signature policy binding.             |
|       1651 | `sig:Commitment`   | type | Typed envelope describing commitment semantics.                   |
|       1652 | `sig:Role`         | type | Typed envelope describing signer role/capacity.                   |
|       1653 | `sig:Place`        | type | Typed envelope describing signing place/jurisdiction.             |
|       1654 | `sig:SignedObject` | type | Typed envelope describing a signed object.                        |
|       1655 | `sig:Target`       | type | Typed envelope declaring the intended signature target.           |
|       1656 | `sig:Endorsement`  | type | Typed envelope describing countersignature endorsement semantics. |
|       1657 | `sig:Visibility`   | type | Typed envelope describing signer visibility claim.                |

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

#### Visibility type controlled vocabulary (1680–1689)

| Code Point | Term                   | Kind | Description                                                                  |
|-----------:|------------------------|------|------------------------------------------------------------------------------|
|       1680 | `sig:FullContentSeen`  | enum | Signer claims they saw the full unelided plaintext content.                  |
|       1681 | `sig:DigestOnly`       | enum | Signer claims they only validated digests/commitments, not full plaintext.   |
|       1682 | `sig:DisclosedDigests` | enum | Signer claims they saw a specific disclosed subset (identified by digests).  |

#### Target type controlled vocabulary (1690–1699)

| Code Point | Term                           | Kind | Description                                                                 |
|-----------:|--------------------------------|------|-----------------------------------------------------------------------------|
|       1690 | `sig:EnvelopeSemanticDigest`   | enum | Target is the semantic digest of a Gordian Envelope.                        |
|       1691 | `sig:EnvelopeStructuralDigest` | enum | Target is the structural digest of a Gordian Envelope.                      |
|       1692 | `sig:DetachedBytesDigest`      | enum | Target is a digest of detached bytes.                                       |
|       1693 | `sig:Reference`                | enum | Target is a `Reference` (`ur:reference`, CBOR tag `#6.40025`) per [BCR-2024-011](bcr-2024-011-reference.md). |

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

Fields such as `sig:region` and `sig:locality` are sometimes drawn from small enumerable sets and may be elided. To support decorrelation in those cases, producers MAY encode those fields as **Salted Values** per [BCR-2026-004](bcr-2026-004-salted-value.md).

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

### `sig:SignedObject`

SignedObject describes an object that is signed or intended to be covered by the signature, especially when it is a detached object or an attachment.

If `sig:objectRef` is a `Reference`, the referent type is resolved from context; producers SHOULD include enough context for resolution, such as `sig:tar
