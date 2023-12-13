# Gordian Envelope Extension: Symmetric Encryption

## BCR-2023-004

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022<br/>
Revised: Aug 15, 2023

## Abstract

This document extends the Gordian Envelope Base Specification to add the `encrypted` case arm, which supports symmetric encryption.

## Introduction

This document extends the [Gordian Envelope Base Specification](https://datatracker.ietf.org/doc/draft-mcnally-envelope/) to add the `encrypted` case arm used to represent an Envelope that has been encrypted using a symmetric key. The scheme defined herein supports [IETF-ChaCha20-Poly1305](https://datatracker.ietf.org/doc/html/rfc7539).

Like elision, which is supported by the Envelope Base Specification, encryption is a reversible transformation of an Envelope that does not alter its unique digest. And since Envelope is a recursively nested structure of Envelopes in a Merkle-like digest tree, any of these nested envelopes can be elided or encrypted without disturbing the tree, hence preserving constructs like signatures.

This basic encryption can be further extended to support public key encryption (including encryption to multiple recipients) and social backup and recovery using [Sharded Secret Key Reconstruction (SSKR)](bcr-2020-011-sskr.md).

## Format Specification

This section is normative, and specifies an additional case arm for the `envelope` type: `encrypted`. It also specifies that assertions may be encrypted by adding the `encrypted-assertion` case to Envelope's `assertion-element` type.

The formal language used is the [Concise Data Definition Language (CDDL)](https://datatracker.ietf.org/doc/html/rfc8610). The top-level specification of Gordian Envelope with this extension added is:

```
envelope = #6.200(envelope-content)
envelope-content = (
    leaf / elided / node / assertion / wrapped /
    encrypted
)

assertion-element = (
    assertion / elided-assertion /
    encrypted-assertion
)

encrypted-assertion = encrypted     ; MUST represent an assertion
```

The format for `encrypted` is defined by [UR Type Definition for Encrypted Messages](bcr-2022-001-encrypted-message.md), including the CBOR tag `#6.40002`. In this specification, the optional fourth array element `aad` is REQUIRED, and MUST contain the CBOR-encoded tagged digest of the envelope. `tagged-digest` is defined in [BCR-2021-002](bcr-2021-002-digest.md).

```
encrypted = #6.40002([ ciphertext, nonce, auth, aad ])

ciphertext = bytes
nonce = bytes .size 12
auth = bytes .size 16

aad = tagged-digest
```

The `encrypted` case can be discriminated from other Envelope case arms by the fact that it is the only one that is tagged using `#6.40002`.

## Declaring the Digest

This section is normative.

The `encrypted` case directly declares the encrypted envelope's digest as the fourth element of its array, `aad`. The `tagged-digest` encoded therein MUST match the actual digest of the Envelope that has been encrypted. Decrypting an envelope MUST be validated by matching the decrypted Envelope's actual computed digest to the one declared, and the decryption operation MUST reject the result if the digests do not match.

**Example**

```
$ KEY=`envelope generate key`
$ ENVELOPE=`envelope subject "Hello"`

$ envelope format --diag $ENVELOPE

200(   / envelope /
   24("Hello")   / leaf /
)

$ envelope digest --hex $ENVELOPE

4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b

$ ENCRYPTED_ENVELOPE=`envelope encrypt --key $KEY $ENVELOPE`
$ envelope format --diag $ENCRYPTED_ENVELOPE

200(   / envelope /
   40002(   / encrypted /
      [
         h'dadeecba53db714445c0',
         h'3cda0648bcb07f0f8b4da2be',
         h'912a35829bab21219c0e7974f6f8b2cc',
         h'd99c4158204d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b'
      ]
   )
)

$ envelope digest --hex $ENCRYPTED_ENVELOPE

4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b
```

Notice that the digest of the unencrypted and encrypted Envelopes both match. This is because the fourth array element of the encrypted Envelope is the encoded CBOR for `tagged-digest`:

```
40001(h'4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b')
```

## Reference Implementations

This section is informative.

Both the [Swift Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/BCSwiftEnvelope) and the [Rust Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/bc-envelope-rust) support this extension.

## Future Proofing

To support this extension, future extensions to the encrypted message used herein and defined in [UR Type Definition for Encrypted Messages](bcr-2022-001-encrypted-message.md) may support other encryption constructs. To work with this specification, they MUST support an equivalent of the `aad` field afforded by the original IETF-ChaCha20-Poly1305 construct so that the digest of the encrypted Envelope can be declared.

## Security Considerations

Generally, this document inherits the security considerations of the cryptographic construct it uses: [IETF-ChaCha20-Poly1305](https://datatracker.ietf.org/doc/html/rfc7539).

## IANA Considerations

This document makes no requests of IANA.
