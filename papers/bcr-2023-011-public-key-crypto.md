# UR Type Definitions for Public Key Cryptography

## BCR-2023-011

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 9, 2023<br/>
Revised: December 9, 2023

## Introduction

Public key cryptography is a fundamental building block of secure systems. This document defines a set of UR types for encrypting and signing data using public key cryptography.

The encryption primitives are based on [X25519 key agreement](https://datatracker.ietf.org/doc/html/rfc7748), and the signature primitives are based on [BIP-340 Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) and [ECDSA-25519-doublesha256](https://en.bitcoin.it/wiki/BIP_0137).

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type                  | CBOR Tag |
| :----------------------- | :------- |
| ur:agreement-private-key | #6.40010 |
| ur:agreement-public-key  | #6.40011 |
| ur:crypto-prvkeys        | #6.40013 |
| ur:crypto-prvkey-base    | #6.40016 |
| ur:crypto-pubkeys        | #6.40017 |
| ur:crypto-sealed         | #6.40019 |
| ur:signature             | #6.40020 |
| ur:signing-private-key   | #6.40021 |
| ur:signing-public-key    | #6.40022 |

These tags have been registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

## Agreement Private Key `ur:agreement-private-key`

A Curve25519 private key used for [X25519 key agreement](https://datatracker.ietf.org/doc/html/rfc7748). See `private-key-base` for how to derive agreement keys from the base key material.

### CDDL

```
agreement-private-key = #6.40010(bytes .size 32)
```

## Agreement Public Key `ur:agreement-public-key`

A Curve25519 public key used for [X25519 key agreement](https://datatracker.ietf.org/doc/html/rfc7748).

### CDDL

```
agreement-public-key = #6.40011(bytes .size 32)
```

## Private Key Base `ur:crypto-prvkey-base`

Holds cryptographic key material that may be of any length, but it is RECOMMENDED that it be at least 32 bytes in length. It can produce all the private and public keys needed to use this suite. It is usually only serialized for purposes of backup.

### CDDL

```
crypto-prvkey-base = #6.40016(key-material)
key-material = bytes
```

### Derivations

* `signing-private-key`: [HKDF](https://www.rfc-editor.org/rfc/rfc6234) with salt: `signing`.
* `agreement-private-key`: [HKDF](https://www.rfc-editor.org/rfc/rfc6234) with salt: `agreement`.
* `signing-private-key`: [RFC-7748 X25519](https://datatracker.ietf.org/doc/html/rfc7748).
* `signing-public-key`:
    * [BIP-340 Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) x-only public key, or
    * [ECDSA-25519-doublesha256](https://en.bitcoin.it/wiki/BIP_0137) public key.

## PublicKeys `ur:crypto-pubkeys`

Holds the public keys of an identifiable entity, and can be made public. It is not simply called a "public key" because it holds at least _two_ public keys: one for signing and another for encryption. The `signing-public-key` may specifically be for verifying Schnorr or ECDSA signatures.

### CDDL

A `crypto-pubkeys` is a two-element array with the first element being the `signing-public-key` and the second being the `agreement-public-key`.

```
crypto-pubkeys = #6.40017([signing-public-key, agreement-public-key])
```

## Sealed Message `ur:crypto-sealed`

A message that has been one-way encrypted to a particular `agreement-public-key`, and may be used to implement anonymous-sender and multi-recipient public key encryption.

An ephemeral sender agreement key pair generated at encryption time, and the ephemeral sender's public key is included, enabling the recipient to decrypt the message without identifying the real sender. The ephemeral private key is discarded.

The `encrypted` type is defined in [BCR-2022-001](bcr-2022-001-encrypted-message.md).

### SealedMessage: CDDL

```
crypto-sealed = #6.40019([encrypted, ephemeral-public-key])
ephemeral-public-key = agreement-public-key
```

## Signature

A cryptographic signature. It has two variants:

* A [BIP-340 Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) signature.
* An [ECDSA-25519-doublesha256](https://en.bitcoin.it/wiki/BIP_0137) signature.

### CDDL

A `signature` has two variants. The Schnorr variant is preferred. Schnorr signatures may include tag data of arbitrary length.

If the `signature-variant-schnorr` is selected and has no tag, it will appear directly as a byte string of length 64. If it includes tag data, it will appear as a two-element array where the first element is the signature and the second element is the tag. The second form MUST NOT be used if the tag data is empty.

If the `signature-variant-ecdsa` is selected, it will appear as a two-element array where the first element is `1` and the second element is a byte string of length 64.

```
signature = #6.40020(signature-variant-schnorr / signature-variant-ecdsa)

signature-variant-schnorr = signature-schnorr / signature-schnorr-tagged
signature-schnorr = bytes .size 64
signature-schnorr-tagged = [signature-schnorr, schnorr-tag]
schnorr-tag = bytes .size ne 0

signature-variant-ecdsa = [ 1, signature-ecdsa ]
signature-ecdsa = bytes .size 64
```

## SigningPrivateKey

A private key for creating [BIP-340 Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) or [ECDSA-25519-doublesha256](https://en.bitcoin.it/wiki/BIP_0137) signatures. See `private-key-base` for how to derive signing keys from the base key material.

### CDDL

```
private-signing-key = #6.40021(bytes .size 32)
```

## SigningPublicKey

A public key for verifying signatures. It has two variants:

* An x-only public key for verifying [BIP-340 Schnorr](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) signatures.
* An ECDSA public key [ECDSA-25519-doublesha256](https://en.bitcoin.it/wiki/BIP_0137) signatures.

### SigningPublicKey: CDDL

A signing public key has two variants: Schnorr or ECDSA. The Schnorr variant is preferred, so it appears as a byte string of length 32. If ECDSA is selected, it appears as a 2-element array where the first element is `1` and the second element is the compressed ECDSA key as a byte string of length 33.

```
signing-public-key = #6.40022(key-variant-schnorr / key-variant-ecdsa)

key-variant-schnorr = key-schnorr
key-schnorr = bytes .size 32

key-variant-ecdsa = [1, key-ecdsa]
key-ecdsa = bytes .size 33
```
