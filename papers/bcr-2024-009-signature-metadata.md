# Signatures with Metadata in Gordian Envelope

## BCR-2024-009

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 7, 2024

### Introduction

In this document, we extend that concept to include metadata in the signature. This allows the signer to include additional information about the signed subject, such as the signer's identity, the date of the signature, and the purpose of the signature.

### Signing the Envelope Subject

In [BCR-2023-013](bcr-2023-013-envelope-crypto.md), we explained how to digitally sign the subject of a [Gordian Envelope](bcr-2024-003-envelope.md).

This involves signing the hash of the subject envelope, then adding an assertion to it, like this:

```
"Subject" [
    'signed': Signature
]
```

It's important to note that if the subject has assertions that also need signing:

```
"Subject" [
    "assertion1": "value1"
    "assertion2": "value2"
]
```

Then adding a signature assertion to the subject envelope is not sufficient, because the subject *only* is signed.

```
"Subject" [                // This is signed
    "assertion1": "value1" // This is not signed
    "assertion2": "value2" // This is not signed
    'signed': Signature
]
```

To cover the other assertions, the entire envelope must be signed by wrapping it first, making the entire envelope, including its assertions, the subject:

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
} [
    'signed': Signature
]
```

### Signature Metadata

Now that we can sign a payload envelope, the question arises as to where to put additional metadata about the signature, such as the signer's identity, the date of the signature, and the purpose of the signature.

We could add these to the payload envelope as assertions before we wrap it to be signed:

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
        "signer": "Alice"
        "date": 2024-12-07
        "purpose": "Proof of Identity"
    ]
} [
    'signed': Signature
]
```

But this would violate a preferred separation of concerns where the payload envelope is only about the payload, and the signature metadata is separate. Failing to separate these concerns becomes critical when an envelope may have multiple signatures, each with its own metadata.

Alternatively, we could add our metadata after signing the envelope:

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
} [
    'signed': Signature
    "signer": "Alice"
    "date": 2024-12-07
    "purpose": "Proof of Identity"
]
```

But then we're back to having assertions that are not signed, leaving them *mutable*. This is a problem because the metadata could be changed after the signature is applied, leaving the signature valid, but the metadata incorrect.

### Signature with Metadata

To solve this, we introduce a standard for adding signatures with metadata. This solution leverages the recursive nature of Gordian Envelope to create a signature envelope that includes the metadata, and then signs *that* envelope with the same private key used to sign the payload.

### Step 1

Wrap the payload envelope and produce a `Signature` object as usual, but don't yet add it as an assertion:

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
}
```

```
Signature
```

### Step 2

Create an envelope with the payload `Signature` as its subject, and add the metadata as assertions on this subject:

```
Signature [
    "signer": "Alice"
    "date": 2024-12-07
    "purpose": "Proof of Identity"
]
```

### Step 3

Wrap this signature metadata envelope and then sign *it* with the *same* private key used to sign the payload:

```
{
    Signature [
        "signer": "Alice"
        "date": 2024-12-07
        "purpose": "Proof of Identity"
    ]
} [
    'signed': Signature
]
```

### Step 4:

Use this signed signature metadata envelope as the object of the `'signed'` assertion on the wrapped payload envelope, in the same position as a `Signature` object that includes no metadata:

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
} [
    'signed': {
        Signature [
            "signer": "Alice"
            "date": 2024-12-07
            "purpose": "Proof of Identity"
        ]
    } [
        'signed': Signature
    ]
]
```

Signing the metadata and the payload signature with the same private key that signed the payload ensures that the metadata is immutable with the same level of security as the payload itself.

## Verification

To verify the signature, the verifier MUST verify both signatures against the sender's public key. The outer signature verifies the metadata envelope, and the inner signature verifies the payload envelope. Both signatures MUST be valid against the same public key for the overall signature to be considered valid. In addition, the outer signature MUST be the only assertion on the signature metadata envelope, and MUST NOT have additional assertions itself. (Note that the metadata assertions themselves may be arbirarily complex.)

The basic Envelope API for verifying signatures does not need to change at all: whether or not a signature carries metadata is transparent to the verifier who does not need the metadata.

Th extended Envelope API for verifying signatures provides affordances for verifying the envelope and returning the metadata, if desired. This metadata is returned as the `Signature` with metadata envelope, which may be inspected further:

```
Signature [
    "signer": "Alice"
    "date": 2024-12-07
    "purpose": "Proof of Identity"
]
```

## Multiple Signatures

Because of the cleanly separated concerns, it is easy to add multiple signatures with metadata to an envelope. Each signature with metadata stands alone, and the payload envelope is signed by each of them.

### Without Metadata

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
} [
    'signed': Signature
    'signed': Signature
]
```

### With Metadata

```
{
    "Subject" [
        "assertion1": "value1"
        "assertion2": "value2"
    ]
} [
    'signed': {
        Signature [
            "signer": "Alice"
            "date": 2024-12-07
            "purpose": "Proof of Identity"
        ]
    } [
        'signed': Signature
    ]
    'signed': {
        Signature [
            "signer": "Bob"
            "date": 2024-12-08
            "purpose": "Witness"
        ]
    } [
        'signed': Signature
    ]
]
```

## Reference Implementation

The reference implementation for signatures with metadata is in the [`bc-envelope` Rust crate](https://crates.io/crates/bc-envelope), or on GitHub at [BlockchainCommons/bc-envelope-rust](https://github.com/blockchaincommons/bc-envelope-rust/).

The basic signing and verification API remains unchanged, while the extended signing API provides affordances for working with the metadata.

The unit tests in the reference implementation demonstrate how to sign with metadata, and verify signatures returning metadata if any.

## Future Work

This paper lays out the format for adding metadata to signatures in Gordian Envelopes. However, the metadata examples given in this paper are intended to be illustrative, not normative. While there is no intent to limit what developers may add as metadata using this technique, future work will include developing standards for interoperable metadata, including dates, signer identity, and signing purpose.
