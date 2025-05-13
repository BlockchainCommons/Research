# UR Type Definition for Post-Quantum Cryptographic Structures

## BCR-2025-003

**© 2025 Blockchain Commons**

Author: Wolf McNally\
Date: April 25, 2025

## Introduction

This document defines a set of CBOR tags and [Uniform Resource (UR) types](./bcr-2020-005-ur.md) for post-quantum cryptographic structures implementing ML-KEM and ML-DSA. These tags and types are intended to be used in conjunction with the Concise Binary Object Representation (CBOR) format, which is a data serialization format designed for small code size and small message size.

## About ML-KEM and ML-DSA

ML‑KEM (“Module‑Lattice Key‑Encapsulation Mechanism”) and ML‑DSA (“Module‑Lattice Digital Signature Algorithm”) are NIST’s post‑quantum standards for key exchange and signatures. Both descend from the CRYSTALS competition winners—Kyber and Dilithium respectively—but they are *not drop‑in replacements* for those schemes.

## UR Types and CBOR Tags

This document defines the following [UR types](./bcr-2020-006-urtypes.md) along with their corresponding CBOR tags, which have been assigned in the [IANA Concise Binary Object Representation (CBOR) Tags registry](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

| UR type                | CBOR Tag   |
| :--------------------- | :--------- |
| `ur:mlkem-private-key` | `#6.40100` |
| `ur:mlkem-public-key`  | `#6.40101` |
| `ur:mlkem-ciphertext`  | `#6.40102` |
| `ur:mldsa-private-key` | `#6.40103` |
| `ur:mldsa-public-key`  | `#6.40104` |
| `ur:mldsa-signature`   | `#6.40105` |

## CDDL Definitions

This section provides the [CDDL](https://datatracker.ietf.org/doc/html/rfc8610) definitions for the CBOR tags defined above.

Our reference for the key sizes and other parameters is the [`pqcrypto-mlkem`](https://crates.io/crates/pqcrypto-mlkem) and [`pqcrypto-mldsa`](https://crates.io/crates/pqcrypto-mldsa) crates, which are part of the [PQClean](https://github.com/pqclean/pqclean/) project.

Our general architecture is for the CBOR tag to identify the type of object, and then the first element of the tuple to identify the level of security. The second element of the tuple is a binary string of a fixed size, which contains the actual key, ciphertext, or signature.

The [bc-components](https://crates.io/crates/bc-components) crate contains reference implementations of these schemas.

```cddl
mlkem-level = 512 / 768 / 1024

mlkem-tuple<$L, $S> = (
  $L .within mlkem-level,
  bstr .size $S
)

mlkem-private-key = #6.40100([
    mlkem-tuple<512, 1632> //
    mlkem-tuple<768, 2400> //
    mlkem-tuple<1024, 3168>
])

mlkem-public-key = #6.40101([
    mlkem-tuple<512, 800> //
    mlkem-tuple<768, 1184> //
    mlkem-tuple<1024, 1568>
])

mlkem-ciphertext = #6.40102([
    mlkem-tuple<512, 768> //
    mlkem-tuple<768, 1088> //
    mlkem-tuple<1024, 1568>
])

mldsa-level = 2 / 3 / 5

mldsa-tuple<$L, $S> = (
  $L .within mldsa-level,
  bstr .size $S
)

mldsa-private-key = #6.40103([
    mldsa-tuple<2, 2560> //
    mldsa-tuple<3, 4032> //
    mldsa-tuple<5, 4896>
])

mldsa-public-key = #6.40104([
    mldsa-tuple<2, 1312> //
    mldsa-tuple<3, 1952> //
    mldsa-tuple<5, 2592>
])

mldsa-signature = #6.40105([
    mldsa-tuple<2, 2420> //
    mldsa-tuple<3, 3309> //
    mldsa-tuple<5, 4627>
])
```
