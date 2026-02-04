# Signing Event Assertions

## BCR-2026-004

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 4, 2026

---

## Abstract

In Gordian Envelope, the `signed` predicate is purely cryptographic — it proves that a specific private key was used to sign specific content. Nothing more. A signature alone doesn't prove who possesses the key, when signing occurred, or what the signature means.

To express these facts about a signing event, signers must explicitly attest them using predicates bound to the signature via the double-signing pattern. This BCR:

1. **Establishes the mental model** — signatures prove keys signed, not identity or intent
2. **Documents the double-signing pattern** — how to cryptographically bind assertions to signatures
3. **Defines two novel predicates** — `signer` (300) links to the signer's identity; `signedOnBehalfOf` (301) optionally identifies another XID the signer represents
4. **References XAdES standards** — `xades:ClaimedRole` and `xades:CommitmentType` for additional assertion types

## Status: Draft

## Introduction

### Signed Proves Key, Not Identity

In Gordian Envelope, the `signed` predicate is a **purely cryptographic operation**. A cryptographic signature proves exactly one thing:

> **The private key corresponding to a specific public key was used to produce this signature over this specific content.**

That's it. Given the public key and the content, anyone can verify this mathematical relationship. If the content changes by even one bit, verification fails. If a different private key signed, verification fails.

A signature does **not** prove:
- **Who** possesses or possessed the private key
- **Whether** the key has been compromised, shared, or delegated
- **When** the signing operation occurred
- **Why** the signing happened or what it means
- **That** the signer read, understood, or agreed to the content

```
{
    Digest(contract)
} 'signed': Signature(key-abc123)
```

This proves the private key for `abc123` signed the contract digest. It does not prove Alice controls that key, that Alice is CEO, that Alice signed on behalf of Acme Corp, or even that Alice has ever seen the contract.

### Identical Signatures Can Mean Different Things

Compare two scenarios:

**Scenario A**: Alice's personal key signs a document. The signature proves the key signed.

**Scenario B**: Alice, as CEO, signs a contract on behalf of Acme Corp as approval.

Both produce cryptographically identical signatures. The difference is what the signer attests — who Alice is, what role she's acting in, and what her signature means.

To express these assertions in Gordian Envelope, we need:
1. Explicit predicates linking signatures to identity documents (XIDs)
2. Predicates expressing representation relationships
3. A pattern for cryptographically binding assertions to signatures

### Solution

This specification defines:

1. **Two novel predicates** for signing event assertions:
   - `signer` — Links a signature to the signer's XID document
   - `signedOnBehalfOf` — (Optional) Identifies another XID that the signer represents

2. **References to XAdES standards** for additional assertion types:
   - `xades:ClaimedRole` — The capacity in which the signer is acting
   - `xades:CommitmentType` — The purpose or meaning of the signature

3. **The double-signing pattern** for cryptographically binding assertions to signatures

## The Double-Signing Pattern

### Problem: Assertions Must Be Bound to Signatures

Simply adding assertions alongside a signature doesn't cryptographically bind them:

```
// WRONG: Assertions not bound to signature
{
    Digest(contract)
} 'signed': Signature(alice)
  'signer': XID(alice)           // Not signed!
  'signedOnBehalfOf': XID(acme)  // Anyone could add this
```

These assertions could be added or modified by anyone after Alice signed.

### Solution: Wrap and Sign Twice

The double-signing pattern solves this:

1. **Inner wrap and sign**: Sign the content
2. **Add assertions**: Attach signing event assertions to the inner signed envelope
3. **Outer wrap and sign**: Sign again, binding the assertions

```
{
    {
        Digest(contract)
    } 'signed': Signature(alice)
    [
        'signer': XID(alice)
        'signedOnBehalfOf': XID(acme-corp)
        'xades:ClaimedRole': "Chief Executive Officer"
        'xades:CommitmentType': "approval"
    ]
} 'signed': Signature(alice)
```

Now the outer signature cryptographically binds Alice's identity, representation, role, and commitment type to her inner signature on the contract.

### Inner Signs Content, Outer Binds Assertions

The inner signature proves: "This key signed this content."

The outer signature proves: "This key asserts these assertions about that signature."

Typically both signatures use the same key — Alice making assertions about her own signature. But they need not be the same:

- **Same key**: Self-asserted assertions. Alice claims her own identity, role, and intent.
- **Different key**: May be key separation or third-party assertion:
  - **By purpose**: Alice uses distinct keys for different operations — one authorized only for git commits, another for contract signing, another for routine approvals
  - **By device**: Alice uses distinct keys on different devices — phone, laptop, hardware token — each with its own authorization scope
  - **Third-party**: A different identity is attesting facts about Alice's signature. If this is a formal counter-signature (notary, witness, approver), see the Counter-Signatures section below. If not a counter-signature, third-party assertions are generally not recommended — the signer should make their own assertions. Exception: hardware assertions where a secure element attests security properties of the signing operation.

  The `signer` predicate points to the XID where key purposes and devices are documented, allowing relying parties to determine which case applies.

### What Belongs in Signing Event Assertions

The signing event assertions should contain **only the signer's own claims about the signing event**:

| Signing Event Assertions | Does NOT Belong |
|---------------------------|-----------------|
| `signer` — who I am | Third-party role certifications |
| `signedOnBehalfOf` — who I represent (if applicable) | Third-party authority assertions |
| `xades:ClaimedRole` — my claimed capacity (if applicable) | Endorsements of the signer |
| `xades:CommitmentType` — what this signature means (if applicable) | Credentials about the signer |

Third-party assertions about the signer (certifying their role, endorsing their authority, etc.) belong in the **signer's XID document**, not in the signing event assertions. The `signer` predicate points to where those third-party assertions live.

This separation ensures:
1. Signing event assertions contain only self-asserted claims about the signing event
2. Third-party assertions are discoverable via the XID reference
3. Relying parties know which claims are self-asserted vs. third-party certified

### Dates Are Not Timestamps

A signer can include a date in their signing event assertions — this is acceptable and sometimes useful. But it's critical to understand: **a date is not a timestamp**.

A date in signing event assertions is a **self-asserted claim**, not a proof. The signer claims "I signed this on February 4, 2026" — but the only thing the signature actually proves is that the key signed the content. The date is just another assertion.

For **provable timestamps**, you need a third-party timestamp authority to counter-sign the envelope. The timestamp authority's signature proves the content existed at a specific time — because the authority couldn't have signed something that didn't exist yet.

This is the same mental model issue: people assume a date inside a signed envelope proves when it was signed. It doesn't. Only a counter-signature from a trusted timestamp authority provides that proof.

**Note**: Lifecycle predicates like `validFrom` and `validUntil` belong in the main assertion (see BCR-2026-005), not in the signing event assertions. A signing event records facts about the act of signing; validity periods are properties of the content being signed.

Timestamp authority patterns (similar to RFC 3161 TSA or blockchain anchoring) are outside the scope of this BCR. See BCR-2026-011 (Anchor Predicates) for cryptographic event log assertion patterns.

## Counter-Signatures (Multi-Party)

When multiple parties sign with assertions, each applies the double-signing pattern:

```
{
    // Alice's double-signed envelope
    {
        {
            Digest(contract)
        } 'signed': Signature(alice)
        [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
            'xades:ClaimedRole': "CEO"
            'xades:CommitmentType': "approval"
        ]
    } 'signed': Signature(alice)

    // Bob's assertions (counter-signature)
    [
        'signer': XID(bob)
        'signedOnBehalfOf': XID(widgets-inc)
        'xades:ClaimedRole': "Authorized Representative"
        'xades:CommitmentType': "approval"
    ]
} 'signed': Signature(bob)
```

Bob's outer signature binds his assertions to his counter-signature on Alice's already-signed envelope.

## Terminology

**Assertion vs Attestation**: In Gordian Envelope, *assertion* is the technical term for a predicate-object pair attached to a subject — this is Envelope vocabulary. *Attestation* refers to the act of formally declaring or testifying to facts — this is general vocabulary. In this BCR: the signer *attests* to facts about the signing event; these attestations are expressed as *assertions* in the Envelope structure.

**Signing Event**: The act of a private key producing a signature over specific content. The cryptographic operation itself — distinct from any claims about who performed it or why.

**Signing Event Assertions**: The Envelope assertions containing the signer's attestations about the signing event — who they are (`signer`), who they represent (`signedOnBehalfOf`), in what capacity (`xades:ClaimedRole`), and the signature's purpose (`xades:CommitmentType`). These are self-asserted claims, not cryptographic proofs.

**Double-Signing Pattern**: The technique of wrapping and signing twice to cryptographically bind assertions to an inner signature. The inner signature proves the key signed; the outer signature proves the key asserts the assertions.

**XID Document**: An eXtensible IDentifier document containing identity information, key bindings, key purposes, and other assertions about an identity.

**XAdES**: XML Advanced Electronic Signatures, an ETSI standard defining signature properties including claimed roles and commitment types.

## Proposed Known Value Assignments

This BCR proposes additions to the **Reserved** range (256-999) as defined in [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

The proposed codepoints (300-301) are placed above the compact 2-byte range (0-255) to preserve those precious codepoints for the most fundamental predicates. Signing event assertions are important but not as frequent as core predicates, and 3-byte encoding is acceptable for assertions that appear once per signature.

### Signing Event Assertions (300-301)

---

#### 300: `signer`

**Type**: property
**Definition**: Links a signature to a document identifying the signer.
**Domain**: Signing event assertions (on inner signed envelope)
**Range**: Identity reference (may be ELIDED for privacy)
**Usage**: Establishes who made the signature, as opposed to which key made it.

```
{
    {
        Digest(document)
    } 'signed': Signature(key-abc123)
    [
        'signer': XID(alice)
    ]
} 'signed': Signature(key-abc123)
```

**Notes**:
- A signature proves a key signed; `signer` links to the identity behind the key
- The identity reference can be elided while preserving the assertion structure
- **Why `signer` is necessary**: Not all signature schemes embed the public key in the signature or allow key recovery:
  - **EdDSA/Ed25519**: Public key cannot be recovered from signature (hashed in Fiat-Shamir transform)
  - **BBS+**: Zero-knowledge proofs are unlinkable — verifiers cannot determine which key/signature created the proof
  - **Longfellow and similar ZK schemes**: Designed specifically to hide signer identity from the cryptographic artifact

  In these schemes, there is no public key to "look up" from the signature alone. The `signer` predicate provides the necessary link to identity that the cryptographic signature cannot.
- **Gordian ecosystem**: Within XIDs, Clubs, and GSTP, this predicate references an XID or Club
- **Broader use**: Gordian Envelope supports other identity reference formats (URIs, DIDs, etc.) for interoperability with external systems

---

#### 301: `signedOnBehalfOf`

**Type**: property
**Definition**: (Optional) Identifies another entity that the signer represents when making this signature.
**Domain**: Signing event assertions (on inner signed envelope)
**Range**: Identity reference
**Usage**: Indicates the signer is acting for another entity.

```
{
    {
        Digest(vendor-contract)
    } 'signed': Signature(alice-key)
    [
        'signer': XID(alice)
        'signedOnBehalfOf': XID(acme-corp)
    ]
} 'signed': Signature(alice-key)
```

**Notes**:
- **Optional** — Only include when the signer is acting on behalf of another party (e.g., employee signing for company, agent signing for principal). Omit when signing in personal capacity.
- This is a claim by the signer — verification requires checking delegation authority
- For authority chain documentation, see BCR-2026-006's `conferredBy` and `conferralChain` predicates
- Common in corporate, legal, and organizational contexts
- **Gordian ecosystem**: Within XIDs, Clubs, and GSTP, this predicate references an XID or Club
- **Broader use**: Gordian Envelope supports other identity reference formats (URIs, DIDs, etc.) for interoperability with external systems

---

## Referenced Standards

This BCR references predicates from the XAdES standard for signature properties that are not novel to Gordian Envelope.

### xades:ClaimedRole

**Standard**: ETSI TS 101 903 (XAdES)
**Definition**: The capacity or role in which the signer is acting, as claimed by the signer.
**Range**: Text describing the role (e.g., "CEO", "Legal Representative", "Witness")
**Usage**: Describes the function the signer is performing.

```
[
    'signer': XID(alice)
    'xades:ClaimedRole': "Chief Executive Officer"
]
```

**Notes**:
- This is a claimed role, not a certified role — it is self-asserted
- For certified roles backed by certificate chains, see XAdES CertifiedRoles
- Gordian Envelope supports text values; implementations may use Known Values for common roles

### xades:CommitmentType

**Standard**: ETSI TS 101 903 (XAdES)
**Definition**: The purpose or meaning of the signature — what the signer is committing to.
**Range**: Text or identifier describing the commitment type
**Usage**: Distinguishes different signature purposes (approval, acknowledgment, witness, etc.)

```
[
    'signer': XID(alice)
    'xades:CommitmentType': "approval"
]
```

**Notes**:
- Gordian Envelope does not limit values to XAdES OID constants
- Common values include: "approval", "acknowledgment", "witness", "receipt", "origin"
- For XAdES OID interoperability, see Appendix A

---

## Usage Patterns

### Complete Signature with Assertions

```
{
    {
        Digest(contract)
    } 'signed': Signature(alice-key)
    [
        'signer': XID(alice)
        'signedOnBehalfOf': XID(acme-corp)
        'xades:ClaimedRole': "CEO"
        'xades:CommitmentType': "approval"
    ]
} 'signed': Signature(alice-key)
```

### Minimal Signature with Identity Only

```
{
    {
        Digest(document)
    } 'signed': Signature(alice-key)
    [
        'signer': XID(alice)
    ]
} 'signed': Signature(alice-key)
```

### Privacy-Preserving with Elided Signer

```
{
    {
        Digest(document)
    } 'signed': Signature(...)
    [
        'signer': ELIDED
        'xades:CommitmentType': "witness"
    ]
} 'signed': Signature(...)
```

The signature structure is preserved, the commitment type is visible, but the signer identity is elided.

## Relationship to Other Specifications

### Double-Signing Pattern

This BCR formally documents the double-signing pattern for signing event assertions. While the technique of wrapping and signing twice has been used informally in Gordian Envelope examples, this specification establishes the best practices and defines the predicates for expressing signing event assertions.

### BCR-2026-006: Principal Authority Predicates

| Concern | BCR | Question Answered |
|---------|-----|-------------------|
| **Signing Event Assertions** | This BCR (004) | "What are the facts about this signing event?" |
| **Principal Authority** | BCR-2026-006 | "Who directed and takes responsibility for this work?" |

A document may have:
- `principalAuthority` identifying who directed the work
- Signing event assertion predicates indicating who signed and how

Both may be present. Neither implies the other.

### XID Key Operations

| Codepoint | Predicate | Purpose |
|-----------|-----------|---------|
| 63 | `delegate` | Grants cryptographic signing privileges to another key |
| 300 | `signer` | Links a signature to an identity (XID document) |
| 301 | `signedOnBehalfOf` | Indicates representation relationship |

`delegate` is a key-level operation (key A can sign for key B). `signer` and `signedOnBehalfOf` are identity-level operations (person Alice signed for organization Acme).

## Security Considerations

### Assertions Are Self-Asserted

The predicates in this BCR express **claims by the signer**. Relying parties must:
- Verify the signature cryptographically
- Resolve the XID reference to confirm identity
- Evaluate whether the claimed role and representation are plausible
- Verify authority claims using BCR-2026-006 predicates if needed

### Double-Signing Integrity

Both signatures should use the same key. If the outer signature uses a different key:
- It becomes a counter-signature (third-party assertion about the inner signature)
- The assertions become that third party's claims about the signer
- This may be intentional (notarization) or a verification failure

### Elision and Assertions

When `signer` is elided:
- The signature remains cryptographically valid
- The signing key is visible (in the Signature)
- The identity behind the key is hidden
- Other assertions (role, commitment) may remain visible

This enables privacy-preserving signatures where identity is disclosed selectively.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [ETSI TS 101 903: XAdES](https://www.etsi.org/deliver/etsi_ts/101900_101999/101903/01.04.02_60/ts_101903v010402p.pdf)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)
- [The BBS Signature Scheme (IETF Draft)](https://identity.foundation/bbs-signature/draft-irtf-cfrg-bbs-signatures.html) — Zero-knowledge proofs with unlinkable signatures
- [The Longfellow Zero-knowledge Scheme (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-google-cfrg-libzk-01) — Privacy-preserving credential verification

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Lifecycle predicates (`validFrom`, `validUntil`)
- **BCR-2026-006: Principal Authority Predicates** — Authority relationships (`conferredBy`, `conferralChain`)

---

## Appendix A: XAdES Commitment Type OIDs

For systems requiring XAdES interoperability, the following OID values are defined by ETSI TS 101 903:

| Commitment Type | OID |
|-----------------|-----|
| Proof of origin | 1.2.840.113549.1.9.16.6.1 |
| Proof of receipt | 1.2.840.113549.1.9.16.6.2 |
| Proof of delivery | 1.2.840.113549.1.9.16.6.3 |
| Proof of sender | 1.2.840.113549.1.9.16.6.4 |
| Proof of approval | 1.2.840.113549.1.9.16.6.5 |
| Proof of creation | 1.2.840.113549.1.9.16.6.6 |

Gordian Envelope implementations may use these OIDs or equivalent text values. The `xades:CommitmentType` predicate is not limited to these values.

---

*BCR-2026-004: Signing Event Assertions*
*Draft - February 4, 2026*
