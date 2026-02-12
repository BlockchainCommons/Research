# Signing Event Assertions

## BCR-2026-XXX

**© 2026 Blockchain Commons**

Authors: Christopher Allen, Wolf McNally, Shannon Appelcline<br/>
Date: February 5, 2026

---

## Abstract

A cryptographic signature proves a key signed content. It does not prove who holds the key, when signing occurred, or what the signature means. This BCR defines predicates for **signer identity binding** — linking signatures to identity documents (XIDs/DIDs) — using the pattern from BCR-2024-009.

For signature metadata (time, place, role, commitment, policy), see BCR-2026-XXX Signature Qualifiers.

## Status: Draft

## Introduction

### What Signatures Prove

A signature proves exactly one thing:

> **The private key for a specific public key produced this signature over this content.**

A signature does not prove who holds the key, whether the key was compromised or delegated, when signing occurred, why it happened, or that the signer agreed to anything.

```
{
    Digest(contract)
} 'signed': Signature
```

This proves the key signed. It does not prove Alice controls that key, that she is CEO, or that she signed for Acme Corp.

### The Problem

Alice signing personally and Alice signing as CEO for Acme Corp produce identical signatures. The difference is what Alice attests about her signing act. To express this in Gordian Envelope:

1. Predicates linking signatures to identity (XIDs)
2. Predicates expressing representation
3. A pattern binding assertions to signatures

### Solution

This BCR defines two predicates for **signer identity binding**:

- `signer` (800) — links signature to signer's identity document
- `signedOnBehalfOf` (801) — identifies who the signer represents

Two patterns bind assertions to signatures:
- **Signature-with-assertions** — signer's own assertions (primary)
- **Wrapped signing** — third-party assertions

### Relationship to Signature Qualifiers

This BCR and BCR-2026-XXX Signature Qualifiers are complementary:

| BCR | Focus | Predicates |
|-----|-------|------------|
| **This BCR** | Signer identity binding | `signer`, `signedOnBehalfOf` |
| Signature Qualifiers | Signature metadata | `sig:signerRole`, `sig:commitment`, `sig:signingTime`, etc. |

Signature Qualifiers derives from XAdES, an international standard we do not control. XAdES handles identity via `SigningCertificate` (X.509-specific). This BCR fills the gap for identity-agnostic systems using XIDs and DIDs.

## Binding Assertions to Signatures

### The Problem

Assertions alongside a signature aren't cryptographically bound:

```
// WRONG: Anyone could add these assertions
{
    Digest(contract)
} [
    'signed': Signature
    'signer': XID(alice)
]
```

### Pattern 1: Signature-with-Assertions

For a signer's own assertions, use the pattern from BCR-2024-009: make the Signature the subject, add assertions, wrap, sign.

```
{
    Digest(contract)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
            'signedOnBehalfOf': XID(acme-corp)
            'sig:signerRole': '' [
                'isA': 'sig:Role'
                'sig:roleName': "CEO"
            ]
            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Approved'
            ]
        ]
    } ['signed': Signature]
]
```

The inner signature covers content. The outer signature binds assertions to the inner signature. Both must verify against the same key.

### Pattern 2: Wrapped Signing

For third-party assertions (timestamps, notarization), wrap the signed content, add assertions, sign:

```
{
    {
        Digest(contract)
    } [
        'signed': {
            Signature ['signer': XID(alice)]
        } ['signed': Signature]
    ]
    [
        'anchoredAt': 2026-02-04T12:00:00Z
        'anchoredBy': XID(timestamp-authority)
    ]
} [
    'signed': {
        Signature [
            'signer': XID(timestamp-authority)
            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Attested'
            ]
        ]
    } ['signed': Signature]
]
```

The third party's signature binds their assertions about the already-signed content.

### When to Use Each

| Pattern | Who Asserts | About What |
|---------|-------------|------------|
| Signature-with-assertions | Signer | Their signing act |
| Wrapped signing | Third party | Signed content |

Examples of wrapped signing: timestamp authorities, notaries, witnesses, endorsers.

### Dates vs Timestamps

A date in signing assertions is a claim, not proof. For provable timestamps, a third party must counter-sign — they couldn't sign content that didn't exist.

## Multi-Party Signatures

### Parallel Signatures

Multiple parties independently signing the same content:

```
{
    Digest(contract)
} [
    'signed': {
        Signature [
            'signer': XID(alice)
            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Approved'
            ]
        ]
    } ['signed': Signature]
    'signed': {
        Signature [
            'signer': XID(bob)
            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Approved'
            ]
        ]
    } ['signed': Signature]
]
```

### Counter-Signatures

A party signing over another's signed content:

```
{
    {
        Digest(contract)
    } [
        'signed': {
            Signature ['signer': XID(alice)]
        } ['signed': Signature]
    ]
} [
    'signed': {
        Signature [
            'signer': XID(bob)
            'sig:commitment': '' [
                'isA': 'sig:Commitment'
                'sig:commitmentType': 'sig:Witnessed'
            ]
        ]
    } ['signed': Signature]
]
```

Bob's signature covers Alice's complete signed envelope.

## Terminology

**Assertion**: Envelope term for a predicate-object pair. 

**Attestation**: The act of declaring facts. Signers *attest*; attestations are expressed as *assertions*.

**Signing Event**: A key producing a signature over content.

**Signing Event Assertions**: Assertions on a Signature subject — who signed, representing whom, in what capacity, for what purpose.

## Known Value Assignments

Proposed for the Reserved range (256-999) per BCR-2023-002.

### 800: `signer`

Links a signature to a document identifying the signer.

**Subject**: Signature<br/>
**Object**: Identity document (XID, DID, or URI)

```
Signature [
    'signer': XID(alice)
]
```

A signature proves a key signed; `signer` links to identity. Useful in all scenarios, but required when signature schemes (EdDSA, BBS+, Longfellow) don't embed the public key or allow its recovery from the signature.

Within the Gordian ecosystem (XIDs, Clubs, GSTP), `signer` references an XID or Club. Gordian Envelope also supports DIDs and other URIs.

**Distinction from `sig:signerRole`**: This predicate's object is an **identity document**. The `sig:signerRole` predicate's object is a **role description**. Both may appear on the same signature:

```
Signature [
    'signer': XID(alice)                    // WHO signed (identity)
    'sig:signerRole': '' [                  // WHAT capacity (role)
        'isA': 'sig:Role'
        'sig:roleName': "CEO"
    ]
]
```

### 801: `signedOnBehalfOf`

Optional. Identifies who the signer represents.

**Subject**: Signature<br/>
**Object**: Identity document (XID, DID, or URI) of the represented entity

```
Signature [
    'signer': XID(alice)
    'signedOnBehalfOf': XID(acme-corp)
]
```

Only include when acting for another party. This is a claim, not fact — evaluation requires checking delegation authority (see BCR-2026-XXX Principal Authority).

**Note**: This predicate expresses representation without requiring any specific authority framework. A signer may represent another entity without formal delegation (e.g., a family member acting for an incapacitated person).

## Security Considerations

### Cryptographic Verification Requirements

For signature-with-assertions pattern, verifiers MUST:

1. Verify the outer signature (on wrapped signature-with-assertions)
2. Verify the inner signature (on content)
3. Confirm both signatures use the **same public key**

If both signatures are valid but use different keys, the envelope has been tampered with — someone added assertions to another party's signature.

For wrapped signing (third-party assertions), different keys are expected — the third party's key signs the outer envelope.

### Claims vs Proof

Signing event assertions are claims by the signer, not proof. Relying parties must evaluate to affirm that:
- The XID resolves to the claimed identity
- All claims (role, representation) are plausible
- Check delegation chains if `signedOnBehalfOf` is present

### Elision

When `signer` is elided, signatures remain valid but identity is hidden. This enables selective disclosure while preserving cryptographic verification.

### Implementation

For API guidance and reference implementation, see [BCR-2024-009](bcr-2024-009-signature-metadata.md).

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2024-009: Signatures with Metadata](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-009-signature-metadata.md)
- [BCR-2026-XXX: Signature Qualifiers](bcr-2026-xxx-signature-qualifiers.md)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-003-envelope.md)
- [BBS Signature Scheme](https://identity.foundation/bbs-signature/draft-irtf-cfrg-bbs-signatures.html)
- [Longfellow ZK Scheme](https://datatracker.ietf.org/doc/html/draft-google-cfrg-libzk-01)

## Related BCRs

- BCR-2026-XXX: General Assertion Predicates
- BCR-2026-XXX: Principal Authority Predicates
- BCR-2026-XXX: Signature Qualifiers — complementary; provides `sig:signerRole`, `sig:commitment`, `sig:signingTime`, etc.

---

*BCR-2026-XXX: Signing Event Assertions*
*Draft — February 5, 2026*
