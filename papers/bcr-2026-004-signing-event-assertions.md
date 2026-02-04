# Signing Event Assertions

## BCR-2026-004

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 4, 2026

---

## Abstract

In Gordian Envelope, the `signed` predicate is purely cryptographic — it proves that a specific private key was used to sign specific content. Nothing more. A signature alone doesn't prove who possesses the key, when signing occurred, or what the signature means.

To express these facts about a signing event, signers must explicitly attest them using predicates bound to the signature. This BCR:

1. **Establishes the mental model** — signatures prove keys signed, not identity or intent
2. **Documents two signing patterns** — signature-with-assertions (primary) and wrapped signing (for third-party assertions)
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

3. **Two signing patterns** for cryptographically binding assertions:
   - **Signature-with-assertions** (primary) — signer's own assertions about their signing act
   - **Wrapped signing** — third-party assertions about already-signed content

## Binding Assertions to Signatures

### Problem: Assertions Must Be Bound to Signatures

Simply adding assertions alongside a signature doesn't cryptographically bind them:

```
// WRONG: Assertions not bound to signature
{
    Digest(contract)
} [
    'signed': Signature
    'signer': XID(alice)           // Not signed!
    'signedOnBehalfOf': XID(acme)  // Anyone could add this
]
```

These assertions could be added or modified by anyone after Alice signed.

### Pattern 1: Signature-with-Assertions (Primary)

For a signer's own assertions about their signing act, use the signature-with-assertions pattern from [BCR-2024-009](bcr-2024-009-signature-metadata.md):

1. **Sign the content**: Produce a Signature
2. **Create assertion envelope**: Make the Signature the subject, add assertions
3. **Sign the assertion envelope**: Bind assertions to the signature
4. **Attach to content**: Use the signed assertion envelope as the `'signed'` object

```
{
    Digest(contract)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
            'xades:ClaimedRole': "Chief Executive Officer"
            'xades:CommitmentType': "approval"
        ]
    } [
        'signed': Signature
    ]
]
```

The Signature object carries its own assertions, wrapped and signed. This is a self-contained unit: "Alice's signature, with Alice's assertions about that signature, bound together."

**Verification**: Both signatures must verify against the same public key. The inner signature covers the content; the outer signature covers the assertion envelope.

**Key separation**: Alice may use different keys from her XID — one for signing content, another for signing the assertion envelope. Both must be Alice's keys. The `signer` predicate points to the XID where key purposes are documented.

### Pattern 2: Wrapped Signing (Third-Party Assertions)

When a **third party** needs to add assertions to already-signed content — such as a timestamp authority, notary, or witness — use wrapped signing:

1. **Start with signed content**: Content already signed by original signer
2. **Wrap**: Make the signed content the subject of a new envelope
3. **Add third-party assertions**: Attach assertions about the signed content
4. **Sign**: Third party signs, binding their assertions

```
{
    // Alice's signed content (using Pattern 1)
    {
        Digest(contract)
    } [
        'signed': {
            Signature [
                'signer': XID(alice)
            ]
        } ['signed': Signature]
    ]
    [
        // Timestamp authority's assertions about Alice's signed content
        'anchoredAt': 2026-02-04T12:00:00Z
        'anchoredBy': XID(timestamp-authority)
    ]
} [
    'signed': {
        Signature [
            'signer': XID(timestamp-authority)
            'xades:CommitmentType': "timestamp"
        ]
    } ['signed': Signature]
]
```

The timestamp authority wraps Alice's signed content, adds timestamp assertions, and signs. The TSA's assertions are about Alice's content, not about the TSA's own signing act.

### When to Use Each Pattern

| Pattern | Use When | Who Asserts | About What |
|---------|----------|-------------|------------|
| Signature-with-assertions | Signer's own claims | The signer | Their signing act |
| Wrapped signing | Third-party claims | Another party | The signed content |

**Examples of wrapped signing**:
- Timestamp authority adds `anchoredAt` to prove when content existed
- Notary adds witnessing assertions to signed documents
- Endorser adds endorsement to someone else's signed work
- Fair witness adds observation assertions

**Do not use wrapped signing** for a signer's own assertions about their signing — use signature-with-assertions instead.

### What Belongs in Signing Event Assertions

Signing event assertions (on the Signature object) should contain **only the signer's own claims about their signing act**:

| Signing Event Assertions | Does NOT Belong |
|---------------------------|-----------------|
| `signer` — who I am | Third-party role certifications |
| `signedOnBehalfOf` — who I represent (if applicable) | Third-party authority assertions |
| `xades:ClaimedRole` — my claimed capacity (if applicable) | Endorsements of the signer |
| `xades:CommitmentType` — what this signature means (if applicable) | Credentials about the signer |

Third-party assertions belong elsewhere:
- **About the signer** (certifying role, endorsing authority): In the signer's XID document
- **About the signed content** (timestamps, notarization): Using the wrapped signing pattern

This separation ensures:
1. Signing event assertions are always self-asserted by the signer
2. Third-party identity assertions are discoverable via the XID reference
3. Third-party content assertions use a distinct structural pattern
4. Relying parties can distinguish self-asserted vs. third-party claims by structure

### Dates Are Not Timestamps

A signer can include a date in their signing event assertions — this is acceptable and sometimes useful. But it's critical to understand: **a date is not a timestamp**.

A date in signing event assertions is a **self-asserted claim**, not a proof. The signer claims "I signed this on February 4, 2026" — but the only thing the signature actually proves is that the key signed the content. The date is just another assertion.

For **provable timestamps**, you need a third-party timestamp authority to counter-sign the envelope. The timestamp authority's signature proves the content existed at a specific time — because the authority couldn't have signed something that didn't exist yet.

This is the same mental model issue: people assume a date inside a signed envelope proves when it was signed. It doesn't. Only a counter-signature from a trusted timestamp authority provides that proof.

**Note**: Lifecycle predicates like `validFrom` and `validUntil` belong in the main assertion (see BCR-2026-005), not in the signing event assertions. A signing event records facts about the act of signing; validity periods are properties of the content being signed.

Timestamp authority patterns (similar to RFC 3161 TSA or blockchain anchoring) are outside the scope of this BCR. See BCR-2026-011 (Anchor Predicates) for cryptographic event log assertion patterns.

## Multi-Party Signatures

### Parallel Signatures (Independent Signers)

When multiple parties independently sign the same content, each adds their signature-with-assertions:

```
{
    Digest(contract)
} [
    // Alice's signature with her assertions
    'signed': {
        Signature [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
            'xades:ClaimedRole': "CEO"
            'xades:CommitmentType': "approval"
        ]
    } ['signed': Signature]

    // Bob's signature with his assertions
    'signed': {
        Signature [
            'signer': XID(bob)
            'signedOnBehalfOf': XID(widgets-inc)
            'xades:ClaimedRole': "Authorized Representative"
            'xades:CommitmentType': "approval"
        ]
    } ['signed': Signature]
]
```

Each signature is independent. Alice and Bob both signed the contract; neither signed over the other's signature.

### Counter-Signatures (Sequential Signing)

When a party signs **over** another's signed content — witnessing, notarizing, or approving — use wrapped signing:

```
{
    // Alice's signed content
    {
        Digest(contract)
    } [
        'signed': {
            Signature [
                'signer': XID(alice)
                'xades:CommitmentType': "approval"
            ]
        } ['signed': Signature]
    ]
} [
    // Bob counter-signs Alice's signed content
    'signed': {
        Signature [
            'signer': XID(bob)
            'xades:CommitmentType': "witness"
        ]
    } ['signed': Signature]
]
```

Bob's signature covers Alice's complete signed envelope. This proves Bob witnessed Alice's signature — he couldn't have signed something that didn't exist.

## Terminology

**Assertion vs Attestation**: In Gordian Envelope, *assertion* is the technical term for a predicate-object pair attached to a subject — this is Envelope vocabulary. *Attestation* refers to the act of formally declaring or testifying to facts — this is general vocabulary. In this BCR: the signer *attests* to facts about the signing event; these attestations are expressed as *assertions* in the Envelope structure.

**Signing Event**: The act of a private key producing a signature over specific content. The cryptographic operation itself — distinct from any claims about who performed it or why.

**Signing Event Assertions**: The Envelope assertions containing the signer's attestations about the signing event — who they are (`signer`), who they represent (`signedOnBehalfOf`), in what capacity (`xades:ClaimedRole`), and the signature's purpose (`xades:CommitmentType`). These are self-asserted claims, not cryptographic proofs.

**Signature-with-Assertions Pattern**: The technique of making a Signature the subject of an envelope, adding assertions, wrapping, and signing again. Binds the signer's own assertions to their signature. See [BCR-2024-009](bcr-2024-009-signature-metadata.md).

**Wrapped Signing Pattern**: The technique of wrapping already-signed content, adding assertions, and signing. Used when a third party adds assertions about signed content (timestamps, notarization, witnessing).

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
**Domain**: Signing event assertions (on the Signature subject)
**Range**: Identity reference (may be ELIDED for privacy)
**Usage**: Establishes who made the signature, as opposed to which key made it.

```
{
    Digest(document)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
        ]
    } ['signed': Signature]
]
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
**Domain**: Signing event assertions (on the Signature subject)
**Range**: Identity reference
**Usage**: Indicates the signer is acting for another entity.

```
{
    Digest(vendor-contract)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
        ]
    } ['signed': Signature]
]
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
Signature [
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
Signature [
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
    Digest(contract)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
            'xades:ClaimedRole': "CEO"
            'xades:CommitmentType': "approval"
        ]
    } ['signed': Signature]
]
```

### Minimal Signature with Identity Only

```
{
    Digest(document)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
        ]
    } ['signed': Signature]
]
```

### Privacy-Preserving with Elided Signer

```
{
    Digest(document)
} [
    'signed': {
        Signature [
            'signer': ELIDED
            'xades:CommitmentType': "witness"
        ]
    } ['signed': Signature]
]
```

The signature structure is preserved, the commitment type is visible, but the signer identity is elided.

## Relationship to Other Specifications

### BCR-2024-009: Signatures with Metadata

This BCR defines the vocabulary for signing event assertions using the structural pattern established in [BCR-2024-009](bcr-2024-009-signature-metadata.md). BCR-2024-009 defined the technique of attaching metadata to signatures; this BCR specifies the predicates to use.

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
- Verify both signatures cryptographically (inner on content, outer on assertion envelope)
- Confirm both signatures use the same public key (for self-asserted assertions)
- Resolve the XID reference to confirm identity
- Evaluate whether the claimed role and representation are plausible
- Verify authority claims using BCR-2026-006 predicates if needed

### Signature-with-Assertions Integrity

For self-asserted signing event assertions, both signatures must verify against the same key. If they use different keys:
- For **signature-with-assertions**: This is a verification failure — someone tampered with the assertion envelope
- For **wrapped signing**: This is expected — the wrapper is a different party (TSA, notary, etc.)

### Elision and Assertions

When `signer` is elided:
- Both signatures remain cryptographically valid
- The signing key may still be visible (in the Signature)
- The identity behind the key is hidden
- Other assertions (role, commitment) may remain visible

This enables privacy-preserving signatures where identity is disclosed selectively.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2024-009: Signatures with Metadata](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-009-signature-metadata.md) — Structural pattern for signature-with-assertions
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
