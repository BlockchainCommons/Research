# CBOR Encodings for Cryptographic Keys and Signatures

## BCR-2024-005

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: February 26, 2024

---

## Abstract

This document specifies the Concise Data Definition Language (CDDL) representations for cryptographic keys and signatures serialized in Concise Binary Object Representation (CBOR). It aims to provide a standardized and interoperable format for representing various types of cryptographic keys, including symmetric keys, asymmetric private and public keys, and signatures, across different cryptographic algorithms. The document assigns a CBOR tag to each key and signature type, and defines the structure of their CBOR representations, including flexible representation of metadata. It also specifies a key capabilities and permissions model.

## Table of Contents

- [Introduction](#introduction)
    - [Goals](#goals)
    - [Prior Work](#prior-work)
    - [Reference Implementation](#reference-implementation)
- [Key Capabilities](#key-capabilities)
- [CBOR Tags](#cbor-tags)
- [CDDL Definitions](#cddl-definitions)
    - [Symmetric Keys](#symmetric-keys)
        - [ietfchacha20poly1305-key](#ietfchacha20poly1305-key)
        - [AES Keys](#aes-keys)
        - [Serpent](#serpent)
        - [Twofish](#twofish)
    - [Asymmetric Keys](#asymmetric-keys)
        - [RSA Keys](#rsa-keys)
        - [SecP256k1 Keys](#secp256k1-keys)
        - [NIST ECDSA Keys](#nist-ecdsa-keys)
        - [Curve25519 Keys](#curve25519-keys)
        - [Ed25519 Keys](#ed25519-keys)
        - [Ristretto255 Keys](#ristretto255-keys)
        - [X25519 Keys](#x25519-keys)
        - [X448 Keys](#x448-keys)
        - [Ed448 Keys](#ed448-keys)
    - [Post-Quantum Cryptography (PQC) Keys](#post-quantum-cryptography-pqc-keys)
        - [NTRU Keys](#ntru-keys)
        - [Kyber Keys](#kyber-keys)
        - [SIKE Keys](#sike-keys)
        - [Dilithium Keys](#dilithium-keys)
        - [Falcon Keys](#falcon-keys)
        - [PQ3 Keys](#pq3-keys)
    - [HMAC Secrets](#hmac-secrets)

## Introduction

Cryptographic keys and signatures are fundamental components of modern security systems, enabling secure communication, authentication, and data integrity. With the advent of diverse cryptographic algorithms and the increasing need for interoperability between different systems and protocols, there arises a necessity for a standardized format for representing cryptographic keys and signatures. This document addresses this need by defining a set of CDDL specifications for the serialization of cryptographic keys and signatures in CBOR.

### Goals

- Create a comprehensive and consistent set of CBOR encoding specifications for cryptographic keys and signatures.
- Support a wide range of cryptographic algorithms and key types, including emerging post-quantum cryptographic algorithms.
- Provide a framework for understanding and assigning key capabilities and permissions.
- Ensure compatibility with existing standards and protocols, such as SSH and OpenPGP.
- Design structures that support minimal encoding of keys and signatures, while also allowing for additional metadata.
- Assign CBOR tags to each key type and signature type to ensure unambiguous identification and interoperability.
- Become even more useful when used in conjunction with Gordian Envelope.

All definitions in this document are compatible with CBOR [Common Deterministic Encoding (CDE)](https://datatracker.ietf.org/doc/draft-ietf-cbor-cde/) and [Gordian Deterministic CBOR (dCBOR)](https://datatracker.ietf.org/doc/draft-mcnally-deterministic-cbor/), which is an even stricter profile of CDE. The definitions are written in [Concise Data Definition Language (CDDL)](https://datatracker.ietf.org/doc/html/rfc8610)

The CBOR tag identifies both the type of key or signature and the parameters it uses. Thus if a key type comes in multiple sizes, each size will have its own tag.

### Prior Work

Several other BCR documents address the CBOR serialization of keys, signatures, and encrypted messages including:

- [BCR-2020-007: UR Type Definition for Hierarchical Deterministic (HD) Keys](./bcr-2020-007-hdkey.md)
- [BCR-2020-008: UR Type Definition for Elliptic Curve (EC) Keys](./bcr-2020-008-eckey.md)
- [BCR-2022-001: UR Type Definition for Encrypted Messages](./bcr-2022-001-encrypted-message.md)
- [BCR-2023-011: UR Type Definitions for Public Key Cryptography](./bcr-2023-011-public-key-crypto.md)

Some of the definitions in the present work may partially overlap with definitions in these prior works. In an effort to re-imagine CBOR definitions for keys and signatures comprehensively and from scratch, the present document was produced *de novo*, and no effort has so far been made to align it with the prior work. It is the author's opinion that the present work may present an opportunity to define "version 2" of the existing keys, ensuring backward compatibility while providing a more forward-looking framework.

### Reference Implementation

A reference implementation in Swift is a work in progress.

## Key Capabilities

"Key Capabilities" describes the functional attributes and operations supported by various cryptographic key types. Capabilities are distinct from permissions, which are the subset of capabilities that are allowed for a given key. For example, a key may have the capability to sign, but not the permission to sign.

| Capability | Definition |
|---|---|
| `agreement` | Private keys of this type afford producing a shared secret with another public key. |
| `auth`      | Public keys of this type afford authenticating an entity. |
| `derive`    | Private keys of this type afford deriving a range of other keys. |
| `encrypt`   | Public and symmetric keys of this type afford encryption. Private and symmetric keys of this type afford decryption. |
| `public`    | Private keys of this type afford deriving a characteristic public key. |
| `sign`      | Private keys of this type afford signing. Public keys of this type afford verification. |
| `wrap`      | Private and symmetric keys of this type afford wrapping other keys, typically symmetric keys for key exchange. Public and symmetric keys of this type afford unwrapping other keys. |

## CBOR Tags

These tags will be registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

Symmetric keys are in the 404xx range, except for legacy tag assignments.

| UR type(s)                                    | CBOR Tag | Capabilities    | Notes                    |
| :-------------------------------------------- | :------- | :-------------- | :----------------------- |
| `ur:ietfchacha20poly1305-key`, `crypto-key`   | #6.40023 | encrypt, wrap   | Legacy tag assignment    |
| `ur:aes128-key`                               | #6.40400 | encrypt, wrap   |                          |
| `ur:aes256-key`                               | #6.40401 | encrypt, wrap   |                          |
| `ur:serpent`                                  | #6.40402 | encrypt, wrap   |                          |
| `ur:twofish`                                  | #6.40403 | encrypt, wrap   |                          |

Asymmetric private keys are in the 405xx range and are even.

| UR type                           | CBOR Tag | Capabilities                           |
| :-------------------------------- | :------- | :--------------------------------------|
| `ur:rsa2048-private`              | #6.40500 | public, encrypt, sign, auth, wrap      |
| `ur:rsa4096-private`              | #6.40502 | public, encrypt, sign, auth, wrap      |
| `ur:secp256k1-ecdsa-private`      | #6.40504 | public, sign, auth, derive             |
| `ur:secp256k1-schnorr-private`    | #6.40506 | public, sign, auth                     |
| `ur:ecdsa_nistp256-private`       | #6.40508 | public, sign, auth, agreement, derive  |
| `ur:ecdsa_nistp384-private`       | #6.40510 | public, sign, auth, agreement, derive  |
| `ur:ecdsa_nistp521-private`       | #6.40512 | public, sign, auth, agreement, derive  |
| `ur:curve25519-private`           | #6.40514 | public, agreement                      |
| `ur:ed25519-private`              | #6.40516 | public, sign, auth                     |
| `ur:ristretto255-private`         | #6.40518 | public, sign, auth, agreement          |
| `ur:x25519-private`               | #6.40520 | public, agreement                      |
| `ur:x448-private`                 | #6.40522 | public, agreement                      |
| `ur:ed448-private`                | #6.40524 | public, sign, agreement                |
| `ur:ntru-hrss701-private`         | #6.40536 | public, encrypt, auth, wrap            |
| `ur:ntru-hps2048509-private`      | #6.40538 | public, encrypt, auth, wrap            |
| `ur:ntru-hps2048677-private`      | #6.40540 | public, encrypt, auth, wrap            |
| `ur:ntru-hps4096821-private`      | #6.40542 | public, encrypt, auth, wrap            |
| `ur:kyber512-private`             | #6.40544 | public, encrypt, agreement, wrap       |
| `ur:kyber768-private`             | #6.40546 | public, encrypt, agreement, wrap       |
| `ur:kyber1024-private`            | #6.40548 | public, encrypt, agreement, wrap       |
| `ur:sike-p434-private`            | #6.40550 | public, agreement                      |
| `ur:sike-p503-private`            | #6.40552 | public, agreement                      |
| `ur:sike-p610-private`            | #6.40554 | public, agreement                      |
| `ur:sike-p751-private`            | #6.40556 | public, agreement                      |
| `ur:dilithium2-private`           | #6.40558 | public, sign, auth                     |
| `ur:dilithium3-private`           | #6.40560 | public, sign, auth                     |
| `ur:dilithium5-private`           | #6.40562 | public, sign, auth                     |
| `ur:falcon512-private`            | #6.40564 | public, sign, auth                     |
| `ur:falcon1024-private`           | #6.40566 | public, sign, auth                     |
| `ur:pq3-private`                  | #6.40568 | public, sign, auth, agreement          |

Asymmetric public keys are in the 405xx range and are odd, being one greater than the corresponding private key.

| UR type                       | CBOR Tag |
| :---------------------------- | :------- |
| `ur:rsa2048-public`           | #6.40501 |
| `ur:rsa4096-public`           | #6.40503 |
| `ur:secp256k1-ecdsa-public`   | #6.40505 |
| `ur:secp256k1-schnorr-public` | #6.40507 |
| `ur:ecdsa_nistp256-public`    | #6.40509 |
| `ur:ecdsa_nistp384-public`    | #6.40511 |
| `ur:ecdsa_nistp521-public`    | #6.40513 |
| `ur:curve25519-public`        | #6.40515 |
| `ur:ed25519-public`           | #6.40517 |
| `ur:ristretto255-public`      | #6.40519 |
| `ur:x25519-public`            | #6.40521 |
| `ur:x448-public`              | #6.40523 |
| `ur:ed448-public`             | #6.40525 |
| `ur:ntru-hrss701-public`      | #6.40537 |
| `ur:ntru-hps2048509-public`   | #6.40539 |
| `ur:ntru-hps2048677-public`   | #6.40541 |
| `ur:ntru-hps4096821-public`   | #6.40543 |
| `ur:kyber512-public`          | #6.40545 |
| `ur:kyber768-public`          | #6.40547 |
| `ur:kyber1024-public`         | #6.40549 |
| `ur:sike-p434-public`         | #6.40551 |
| `ur:sike-p503-public`         | #6.40553 |
| `ur:sike-p610-public`         | #6.40555 |
| `ur:sike-p751-public`         | #6.40557 |
| `ur:dilithium2-public`        | #6.40559 |
| `ur:dilithium3-public`        | #6.40561 |
| `ur:dilithium5-public`        | #6.40563 |
| `ur:falcon512-public`         | #6.40565 |
| `ur:falcon1024-public`        | #6.40567 |
| `ur:pq3-public`               | #6.40569 |

Signatures are in the 406xx range.

| UR type                           | CBOR Tag |
| :-------------------------------- | :------- |
| `ur:secp256k1-signature`          | #6.40601 |
| `ur:secp256k1-schnorr-signature`  | #6.40602 |
| `ur:rsa2048-signature`            | #6.40603 |
| `ur:rsa4096-signature`            | #6.40604 |
| `ur:ecdsa_nistp256-signature`     | #6.40605 |
| `ur:ecdsa_nistp384-signature`     | #6.40606 |
| `ur:ecdsa_nistp521-signature`     | #6.40607 |
| `ur:ed25519-signature`            | #6.40608 |
| `ur:ristretto255-signature`       | #6.40609 |
| `ur:ed448-signature`              | #6.40610 |
| `ur:dilithium2-signature`         | #6.40611 |
| `ur:dilithium3-signature`         | #6.40612 |
| `ur:dilithium5-signature`         | #6.40613 |
| `ur:falcon512-signature`          | #6.40614 |
| `ur:falcon1024-signature`         | #6.40615 |
| `ur:pq3-signature`                | #6.40616 |

HMAC secrets are in the 407xx range.

| UR type                   | CBOR Tag |
| :------------------------ | :------- |
| `hmac-sha1-secret`        | #6.40700 |
| `hmac-sha256-secret`      | #6.40701 |
| `hmac-sha512-secret`      | #6.40702 |

SSH text keys are in the 408xx range.

| UR type                   | CBOR Tag |
| :------------------------ | :------- |
| `ssh-private`             | #6.40800 |
| `ssh-public`              | #6.40801 |
| `ssh-signature`           | #6.40802 |
| `ssh-certificate`         | #6.40803 |

## CDDL Definitions

The CBOR tags defined above correspond to the following CDDL constant definitions each prefixed by `tag-`, e.g.:

```cddl
tag-ietfchacha20poly1305-key = #6.40400
; ...
```

Constants for key capabilities and permissions are defined as follows:

```cddl
agreement = 1
auth = 2
derive = 3
encrypt = 4
public = 5
sign = 6
wrap = 7

capability = agreement / auth / derive / encrypt / public / sign / wrap

key-permissions = [ +capability ]
```

Map keys that identify various metadata fields shared by various definitions are defined as constants:

```cddl
key = 1             ; The key material (key-type-bare)
comment = 2         ; A comment about the key (text)
checknum = 3        ; A check number for the key (uint32)
permissions = 4     ; The permissions for the key (key-permissions)
; more possible fields

key-metadata = (
    ? comment: text .default "", ; A comment about the key
    ? permissions: key-permissions,
    ; more possible fields that may apply to all keys
)

key-metadata-private = (
    key-metadata,
    ? checknum: uint32, ; A check number for the private key (required for full SSH round-trip compatibility)
    ; more possible fields that apply only to private keys
)

key-metadata-public = (
    key-metadata
    ; more possible fields that apply only to public keys
)
```

The serialization structure of the key definitions in this document is a CBOR dictionary with a required field and zero or more optional fields.

```cddl
key-type = tag-key-type({
    key: bstr, ; specific to the key type
    ? key-metadata
    ; more possible fields that apply only to the key type
})
```

Likewise, the serialization structure of the signature definitions in this document is a CBOR dictionary with a required field and zero or more optional fields.

```cddl
signature = 1          ; The signature
hash-algorithm = 2     ; The hash algorithm used to create the signature (string compatible with SSH signatures)
namespace = 3          ; The namespace of the signature (string compatible with SSH signatures)
public-key = 4         ; The public key used to create the signature (compatible with SSH)
; more possible fields

signature-metadata = (
    ? hash-algorithm: string, ; required for SSH compatibility
    ? namespace: string, ; required for SSH compatibility
    ? public-key: key-type-public, ; specific to the signature type, required for SSH compatibility
    ; more possible fields
)
```

```cddl
signature-type = tag-signature-type({
    signature: bstr, ; specific to the signature type
    ? signature-metadata
})
```

Keys that do not specify a `permissions` field are understood to have the same permissions as they key type's capabilities; in other words, they are as general-purpose as the key type allows.

### Symmetric Keys

#### ietfchacha20poly1305-key

The `ietfchacha20poly1305-key` consists only of the key material, which is the essential component for cryptographic operations. It is defined as a byte string (`bstr`) and must have a size of 32 bytes, matching the size requirement for ChaCha20-Poly1305 keys.

```cddl
ietfchacha20poly1305-key = tag-ietfchacha20poly1305-key({
    key: bstr .size 32,
    ? key-metadata
})
```

#### AES Keys

##### aes128-key

The `aes128-key` represents a symmetric key used in AES-128 encryption. This key must be exactly 16 bytes in length.

```cddl
aes128-key = tag-aes128-key({
    key: bstr .size 16,
    ? key-metadata
})
```

##### aes256-key

The `aes256-key` represents a symmetric key for AES-256 encryption. This key must be exactly 32 bytes in length.

```cddl
aes256-key = tag-aes256-key({
    key: bstr .size 32,
    ? key-metadata
})
```

#### Serpent

The `serpent` key type is used for the Serpent block cipher. The key must be exactly 32 bytes in length.

```cddl
serpent-key = tag-serpent-key({
    key: bstr .size 32,
    ? key-metadata
})
```

#### Twofish

The `twofish` key type is used for the Twofish block cipher. The key must be exactly 32 bytes in length.

```cddl
twofish-key = tag-twofish-key({
    key: bstr .size 32,
    ? key-metadata
})
```

### Asymmetric Keys

#### RSA Keys

- **modulus (`n`)**: The product of two primes, a fundamental part of both the public and private keys.
- **publicExponent (`e`)**: A small integer, commonly 65537, used in the public key for encryption and verification.
- **privateExponent (`d`)**: The multiplicative inverse of `e` modulo `(p-1)*(q-1)`, used in the private key for decryption and signing.
- **prime1 (`p`)** and **prime2 (`q`)**: The two prime numbers whose product is the modulus `n`. These are kept secret as part of the private key.
- **coefficient (`qi`)**: The Chinese Remainder Theorem coefficient, which is the multiplicative inverse of `q` modulo `p`. This is used in the CRT optimization for RSA operations.

##### rsa2048-private

```cddl
rsa2048-private = tag-rsa2048-private({
    key: [
        n: bstr .size 256,     ; modulus (256 bytes)
        e: bstr .size(3..),    ; public exponent (3 bytes, variable)
        d: bstr .size 256,     ; private exponent (256 bytes)
        p: bstr .size 128,     ; prime 1 (128 bytes)
        q: bstr .size 128,     ; prime 2 (128 bytes)
        qi: bstr .size 128      ; coefficient (128 bytes)
    ],
    ? key-metadata-private
})
```

##### rsa2048-public

```cddl
rsa2048-public = tag-rsa2048-public({
    key: [
        e: bstr .size(3..),    ; public exponent (3 bytes, variable)
        n: bstr .size 256      ; modulus (256 bytes)
    ],
    ? key-metadata-public
})
```

##### rsa2048-signature

```cddl
rsa2048-signature = tag-rsa2048-signature({
    signature: bstr .size 256,
    ? signature-metadata
})
```

##### rsa4096-private

```cddl
rsa4096-private = tag-rsa4096-private({
    key: [
        bstr .size 512,     ; n: modulus (512 bytes)
        bstr .size(3..),    ; e: public exponent (3 bytes, variable)
        bstr .size 512,     ; d: private exponent (512 bytes)
        bstr .size 256,     ; p: prime 1 (256 bytes)
        bstr .size 256,     ; q: prime 2 (256 bytes)
        bstr .size 256      ; qi: coefficient (256 bytes)
    ],
    ? key-metadata-private
})
```

##### rsa4096-public

```cddl
rsa4096-public = tag-rsa4096-public({
    key: [
        bstr .size(3..),    ; e: public exponent (3 bytes, variable)
        bstr .size 512      ; n: modulus (512 bytes)
    ],
    ? key-metadata-public
})
```

##### rsa4096-signature

```cddl
rsa4096-signature = tag-rsa4096-signature({
    signature: bstr .size 512,
    ? signature-metadata
})
```

#### SecP256k1 Keys

##### secp256k1-ecdsa-private

A `secp256k1-ecdsa-private` is defined as a 32-byte string, which represents the private key data in the secp256k1 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
secp256k1-ecdsa-private = secp256k1-ecdsa-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### secp256k1-ecdsa-public

A `secp256k1-ecdsa-public` can be represented in both compressed (33 bytes) and uncompressed (65 bytes) forms. The first byte indicates whether the key is compressed or uncompressed: `0x02` or `0x03` for compressed keys, and `0x04` for uncompressed keys. The remaining bytes represent the coordinate(s) of the public key on the secp256k1 curve.

```cddl
secp256k1-ecdsa-public = tag-secp256k1-ecdsa-public({
    key: secp256k1-ecdsa-public-compressed / secp256k1-ecdsa-public-uncompressed,
    ? key-metadata-public
})

secp256k1-ecdsa-public-compressed = bstr .size 33
secp256k1-ecdsa-public-uncompressed = bstr .size 65
```

##### secp256k1-signature

```cddl
secp256k1-signature = tag-secp256k1-signature({
    signature: bstr .size 64,
    ? signature-metadata
})
```

##### secp256k1-schnorr-private

A `secp256k1-schnorr-private` is defined as a 32-byte string, which represents the private key data in the secp256k1 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
secp256k1-schnorr-private = tag-secp256k1-schnorr-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### secp256k1-schnorr-public

A `secp256k1-schnorr-public` is an x-only public key, which is a 32-byte string that represents the x-coordinate of the public key on the secp256k1 curve.

```cddl
secp256k1-schnorr-public = tag-secp256k1-schnorr-public({
    key: bstr .size 32,
    ? key-metadata-public
})
```

##### secp256k1-schnorr-signature

```cddl
secp256k1-schnorr-signature = tag-secp256k1-schnorr-signature({
    key: bstr .size 64,
    ? signature-metadata
})
```

#### NIST ECDSA Keys

The following keys are used in the NIST elliptic curve digital signature algorithm (ECDSA) with the P-256, P-384, and P-521 curves.

##### ecdsa_nistp256-private

A `ecdsa_nistp256-private` is defined as a 32-byte string, which represents the private key data in the P-256 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ecdsa_nistp256-private = tag-ecdsa_nistp256-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### ecdsa_nistp256-public

A `ecdsa_nistp256-public` can be represented in both compressed (33 bytes) and uncompressed (65 bytes) forms. The first byte indicates whether the key is compressed or uncompressed: `0x02` or `0x03` for compressed keys, and `0x04` for uncompressed keys. The remaining bytes represent the coordinate(s) of the public key on the P-256 curve.

```cddl
ecdsa_nistp256-public = tag-ecdsa_nistp256-public({
    key: ecdsa_nistp256-public-compressed / ecdsa_nistp256-public-uncompressed,
    ? key-metadata-public
})

ecdsa_nistp256-public-compressed = bstr .size 33
ecdsa_nistp256-public-uncompressed = bstr .size 65
```

##### ecdsa_nistp256-signature

```cddl
ecdsa_nistp256-signature = tag-ecdsa_nistp256-signature({
    signature: bstr .size 64,
    ? signature-metadata
})
```

##### ecdsa_nistp384-private

A `ecdsa_nistp384-private` is defined as a 48-byte string, which represents the private key data in the P-384 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ecdsa_nistp384-private = tag-ecdsa_nistp384-private({
    key: bstr .size 48,
    ? key-metadata-private
})
```

##### ecdsa_nistp384-public

A `ecdsa_nistp384-public` can be represented in both compressed and uncompressed forms. The first byte indicates whether the key is compressed or uncompressed: `0x02` or `0x03` for compressed keys, and `0x04` for uncompressed keys. The remaining bytes represent the coordinate(s) of the public key on the P-384 curve.

```cddl
ecdsa_nistp384-public = tag-ecdsa_nistp384-public({
    key: ecdsa_nistp384-public-compressed / ecdsa_nistp384-public-uncompressed,
    ? key-metadata-public
})

ecdsa_nistp384-public-compressed = bstr .size 49
ecdsa_nistp384-public-uncompressed = bstr .size 97
```

##### ecdsa_nistp384-signature

```cddl
ecdsa_nistp384-signature = tag-ecdsa_nistp384-signature({
    signature: bstr .size 96,
    ? signature-metadata
})
```

##### ecdsa_nistp521-private

A `ecdsa_nistp521-private` is defined as a 66-byte string, which represents the private key data in the P-521 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ecdsa_nistp521-private = tag-ecdsa_nistp521-private({
    key: bstr .size 66,
    ? key-metadata-private
})
```

##### ecdsa_nistp521-public

A `ecdsa_nistp521-public` can be represented in both compressed and uncompressed forms. The first byte indicates whether the key is compressed or uncompressed: `0x02` or `0x03` for compressed keys, and `0x04` for uncompressed keys. The remaining bytes represent the coordinate(s) of the public key on the P-521 curve.

```cddl
ecdsa_nistp521-public = tag-ecdsa_nistp521-public({
    key: ecdsa_nistp521-public-compressed / ecdsa_nistp521-public-uncompressed,
    ? key-metadata-public
})

ecdsa_nistp521-public-compressed = bstr .size 67
ecdsa_nistp521-public-uncompressed = bstr .size 133
```

##### ecdsa_nistp521-signature

```cddl
ecdsa_nistp521-signature = tag-ecdsa_nistp521-signature({
    signature: bstr .size 132,
    ? signature-metadata
})
```

#### Curve25519 Keys

Curve25519 keys are used for Diffie-Hellman key exchange.

##### curve25519-private

A `curve25519-private` is defined as a 32-byte string, which represents the private key data in the Curve25519 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
curve25519-private = tag-curve25519-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### curve25519-public

A `curve25519-public` is defined as a 32-byte string, which represents the public key data in the Curve25519 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
curve25519-public = tag-curve25519-public({
    key: bstr .size 32,
    ? key-metadata-public
})
```

#### Ed25519 Keys

##### ed25519-private

An `ed25519-private` is defined as a 32-byte string, which represents the private key data in the Ed25519 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ed25519-private = tag-ed25519-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### ed25519-public

An `ed25519-public` is defined as a 32-byte string, which represents the public key data in the Ed25519 elliptic curve cryptography. This key is used for verifying signatures made with the corresponding private key.

```cddl
ed25519-public = tag-ed25519-public({
    key: bstr .size 32,
    ? key-metadata-public
})
```

##### ed25519-signature

```cddl
ed25519-signature = tag-ed25519-signature({
    signature: bstr .size 64,
    ? signature-metadata
})
```

#### Ristretto255 Keys

##### ristretto255-private

A `ristretto255-private` is defined as a 32-byte string, which represents the private key data in the Ristretto255 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ristretto255-private = tag-ristretto255-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### ristretto255-public

A `ristretto255-public` is defined as a 32-byte string, which represents the public key data in the Ristretto255 elliptic curve cryptography. This key is used for verifying signatures made with the corresponding private key.

```cddl
ristretto255-public = tag-ristretto255-public({
    key: bstr .size 32,
    ? key-metadata-public
})
```

##### ristretto255-signature

```cddl
ristretto255-signature = tag-ristretto255-signature({
    signature: bstr .size 64,
    ? signature-metadata
})
```

#### X25519 Keys

##### x25519-private

An `x25519-private` is defined as a 32-byte string, which represents the private key data in the X25519 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
x25519-private = tag-x25519-private({
    key: bstr .size 32,
    ? key-metadata-private
})
```

##### x25519-public

An `x25519-public` is defined as a 32-byte string, which represents the public key data in the X25519 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
x25519-public = tag-x25519-public({
    key: bstr .size 32,
    ? key-metadata-public
})
```

#### X448 Keys

X448 keys are used for Diffie-Hellman key exchange.

##### x448-private

An `x448-private` is defined as a 56-byte string, which represents the private key data in the X448 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
x448-private = tag-x448-private({
    key: bstr .size 56,
    ? key-metadata-private
})
```

##### x448-public

An `x448-public` is defined as a 56-byte string, which represents the public key data in the X448 elliptic curve cryptography for Diffie-Hellman key exchange.

```cddl
x448-public = tag-x448-public({
    key: bstr .size 56,
    ? key-metadata-public
})
```

#### Ed448 Keys

Ed448 keys are used for digital signatures.

##### ed448-private

An `ed448-private` is defined as a 57-byte string, which represents the private key data in the Ed448 elliptic curve cryptography. This key is used for signing transactions and messages.

```cddl
ed448-private = tag-ed448-private({
    key: bstr .size 57,
    ? key-metadata-private
})
```

##### ed448-public

An `ed448-public` is defined as a 57-byte string, which represents the public key data in the Ed448 elliptic curve cryptography. This key is used for verifying signatures made with the corresponding private key.

```cddl
ed448-public = tag-ed448-public({
    key: bstr .size 57,
    ? key-metadata-public
})
```

##### ed448-signature

```cddl
ed448-signature = tag-ed448-signature({
    signature: bstr .size 114,
    ? signature-metadata
})
```

### Post-Quantum Cryptography (PQC) Keys

It's essential to note that these key sizes are subject to change as the algorithms evolve, especially under the scrutiny of the standardization process by organizations like NIST. The final, standardized versions of these algorithms could have different parameters (and thus different key sizes) based on the latest cryptographic research, security analyses, and performance considerations.

All the data sizes listed are speculative. To ensure accuracy and compliance with the latest standards, it will be crucial to check these sizes against the latest specifications and implementations from authoritative sources, such as the NIST Post-Quantum Cryptography Standardization project and/or the official documentation of each algorithm.

#### NTRU Keys

NTRU is a lattice-based cryptographic system that supports both encryption and digital signatures. It stands out for its efficiency and security against quantum computer attacks, making it a robust choice for securing data in a post-quantum world. NTRU's security is based on the hardness of the shortest vector problem (SVP) in lattice cryptography, offering fast operations and relatively small key sizes compared to other post-quantum candidates.

NTRUSign, the primary NTRU-based signature scheme, has a well-known security vulnerability that can allow attackers to forge signatures. This means someone without genuine access to the private key could potentially create signatures that would be accepted and verified with the corresponding public key. This is why we do not assign the `sign` capability to NTRU keys.

##### ntru-hrss701-private

The private key for NTRU HRSS701.

```cddl
ntru-hrss701-private = tag-ntru-hrss701-private({
    key: bstr .size 1450,
    ? key-metadata-private
})
```

##### ntru-hrss701-public

The public key for NTRU HRSS701.

```cddl
ntru-hrss701-public = tag-ntru-hrss701-public({
    key: bstr .size 1138,
    ? key-metadata-public
})
```

##### ntru-hps2048509-private

The private key for NTRU HPS2048509.

```cddl
ntru-hps2048509-private = tag-ntru-hps2048509-private({
    key: bstr .size 1230,
    ? key-metadata-private
})
```

##### ntru-hps2048509-public

The public key for NTRU HPS2048509.

```cddl
ntru-hps2048509-public = tag-ntru-hps2048509-public({
    key: bstr .size 930,
    ? key-metadata-public
})
```

##### ntru-hps2048677-private

The private key for NTRU HPS2048677.

```cddl
ntru-hps2048677-private = tag-ntru-hps2048677-private({
    key: bstr .size 1234,
    ? key-metadata-private
})
```

##### ntru-hps2048677-public

The public key for NTRU HPS2048677.

```cddl
ntru-hps2048677-public = tag-ntru-hps2048677-public({
    key: bstr .size 934,
    ? key-metadata-public
})
```

##### ntru-hps4096821-private

The private key for NTRU HPS4096821.

```cddl
ntru-hps4096821-private = tag-ntru-hps4096821-private({
    key: bstr .size 2062,
    ? key-metadata-private
})
```

##### ntru-hps4096821-public

The public key for NTRU HPS4096821.

```cddl
ntru-hps4096821-public = tag-ntru-hps4096821-public({
    key: bstr .size 1230,
    ? key-metadata-public
})
```

#### Kyber Keys

Kyber is a key encapsulation mechanism (KEM) that is part of the lattice-based cryptographic family, designed to secure communications against quantum computer attacks. It is known for its efficiency in terms of both computational overhead and key size, making it practical for real-world applications. Kyber is selected for standardization by the NIST Post-Quantum Cryptography project, highlighting its security and efficiency.

##### kyber512-private-key

```cddl
kyber512-private-key = tag-kyber512-private-key({
    key: bstr .size 1632,
    ? key-metadata-private
})
```

##### kyber512-public-key

```cddl
kyber512-public-key = tag-kyber512-public-key({
    key: bstr .size 800,
    ? key-metadata-public
})
```

##### kyber768-private-key

```cddl
kyber768-private-key = tag-kyber768-private-key({
    key: bstr .size 2400,
    ? key-metadata-private
})
```

##### kyber768-public-key

```cddl
kyber768-public-key = tag-kyber768-public-key({
    key: bstr .size 1184,
    ? key-metadata-public
})
```

##### kyber1024-private-key

```cddl
kyber1024-private-key = tag-kyber1024-private-key({
    key: bstr .size 3168,
    ? key-metadata-private
})
```

##### kyber1024-public-key

```cddl
kyber1024-public-key = tag-kyber1024-public-key({
    key: bstr .size 1568,
    ? key-metadata-public
})
```

#### SIKE Keys

SIKE (Supersingular Isogeny Key Encapsulation) is a post-quantum cryptographic algorithm. It is based on the difficulty of computing isogenies between supersingular elliptic curves, a problem believed to be resistant to quantum computer attacks. SIKE is distinctive for its novel approach to cryptography, offering a unique alternative to other post-quantum methods with relatively small message sizes, though it generally incurs higher computational costs.

##### sike-p434-private

```cddl
sike-p434-private = tag-sike-p434-private({
    key: bstr .size 374,
    ? key-metadata-private
})
```

##### sike-p434-public

```cddl
sike-p434-public = tag-sike-p434-public({
    key: bstr .size 330,
    ? key-metadata-public
})
```

##### sike-p503-private

```cddl
sike-p503-private = tag-sike-p503-private({
    key: bstr .size 434,
    ? key-metadata-private
})
```

##### sike-p503-public

```cddl
sike-p503-public = tag-sike-p503-public({
    key: bstr .size 378,
    ? key-metadata-public
})
```

##### sike-p610-private

```cddl
sike-p610-private = tag-sike-p610-private({
    key: bstr .size 524,
    ? key-metadata-private
})
```

##### sike-p610-public

```cddl
sike-p610-public = tag-sike-p610-public({
    key: bstr .size 462,
    ? key-metadata-public
})
```

##### sike-p751-private

```cddl
sike-p751-private = tag-sike-p751-private({
    key: bstr .size 564,
    ? key-metadata-private
})
```

##### sike-p751-public

```cddl
sike-p751-public = tag-sike-p751-public({
    key: bstr .size 496,
    ? key-metadata-public
})
```

#### CRYSTALS-Dilithium Keys

CRYSTALS-Dilithium is a digital signature scheme designed to resist attacks from quantum computers. It leverages the mathematical hardness of problems within modular lattices to achieve its security. Dilithium offers various security levels, allowing it to be tailored for different application requirements.

##### dilithium2-private

```cddl
dilithium2-private = tag-dilithium2-private({
    key: bstr .size 2528,
    ? key-metadata-private
})
```

##### dilithium2-public

```cddl
dilithium2-public = tag-dilithium2-public({
    key: bstr .size 1312,
    ? key-metadata-public
})
```

##### dilithium2-signature

```cddl
dilithium2-signature = tag-dilithium2-signature({
    signature: bstr .size 2420,
    ? signature-metadata
})
```

##### dilithium3-private

```cddl
dilithium3-private = tag-dilithium3-private({
    key: bstr .size 4000,
    ? key-metadata-private
})
```

##### dilithium3-public

```cddl
dilithium3-public = tag-dilithium3-public({
    key: bstr .size 1952,
    ? key-metadata-public
})
```

##### dilithium3-signature

```cddl
dilithium3-signature = tag-dilithium3-signature({
    signature: bstr .size 3293,
    ? signature-metadata
})
```

##### dilithium5-private

```cddl
dilithium5-private = tag-dilithium5-private({
    key: bstr .size 4864,
    ? key-metadata-private
})
```

##### dilithium5-public

```cddl
dilithium5-public = tag-dilithium5-public({
    key: bstr .size 2592,
    ? key-metadata-public
})
```

##### dilithium5-signature

```cddl
dilithium5-signature = tag-dilithium5-signature({
    signature: bstr .size 4595,
    ? signature-metadata
})
```

#### FALCON Keys

FALCON is a digital signature scheme designed for security in a post-quantum world. It's known for generating exceptionally compact signatures, making it well-suited for scenarios where storage or bandwidth is limited. FALCON's security is based on the hardness of problems related to NTRU lattices.

##### falcon512-private

```cddl
falcon512-private = tag-falcon512-private({
    key: bstr .size 1281,
    ? key-metadata-private
})
```

##### falcon512-public

```cddl
falcon512-public = tag-falcon512-public({
    key: bstr .size 897,
    ? key-metadata-public
})
```

##### falcon512-signature

```cddl
falcon512-signature = tag-falcon512-signature({
    signature: bstr .size 666,
    ? signature-metadata
})
```

##### falcon1024-private

```cddl
falcon1024-private = tag-falcon1024-private({
    key: bstr .size 2305,
    ? key-metadata-private
})
```

##### falcon1024-public

```cddl
falcon1024-public = tag-falcon1024-public({
    key: bstr .size 1793,
    ? key-metadata-public
})
```

##### falcon1024-signature

```cddl
falcon1024-signature = tag-falcon1024-signature({
    signature: bstr .size 1280,
    ? signature-metadata
})
```

#### PQ3 Keys

Apple's new post-quantum cryptographic protocol is called PQ3. Apple announced PQ3 in February 2024 as a significant upgrade to iMessage's cryptographic security. PQ3 is a combination of new post-quantum algorithms and current Elliptic Curve algorithms. Apple claims that PQ3 has the "strongest security properties of any at-scale messaging protocol in the world".

This format is speculative.

##### pq3-private

```cddl
pq3-private = tag-pq3-private({
    key: [
        kyber1024-private,
        ecdsa_nistp256-private
    ],
    ? key-metadata-private
})
```

##### pq3-public

```cddl
pq3-public = tag-pq3-public({
    key: [
        kyber1024-public,
        ecdsa_nistp256-public
    ],
    ? key-metadata-public
})
```

##### pq3-signature

```cddl
pq3-signature = tag-pq3-signature({
    signature: bstr .size TBD,
    ? signature-metadata
})
```

### HMAC Secrets

#### HMAC-SHA1 Secret

The `hmac-sha1-secret` is defined as a byte string (`bstr`) and can have a variable length depending on the underlying hash function used, but should be at least 20 bytes for HMAC-SHA1.

```cddl
hmac-sha1-secret = tag-hmac-sha1-secret(
    bstr .size(20..)
)
```

#### HMAC-SHA256 Secret

The `hmac-sha256-secret` is defined as a byte string (`bstr`) and can have a variable length depending on the underlying hash function used, but should be at least 32 bytes for HMAC-SHA256.

```cddl
hmac-sha256-secret = tag-hmac-sha256-secret(
    bstr .size(32..)
)
```

#### HMAC-SHA512 Secret

The `hmac-sha512-secret` is defined as a byte string (`bstr`) and can have a variable length depending on the underlying hash function used, but should be at least 64 bytes for HMAC-SHA512.

```cddl
hmac-sha512-secret = tag-hmac-sha512-secret(
    bstr .size(64..)
)
```
