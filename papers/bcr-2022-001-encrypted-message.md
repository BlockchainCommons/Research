# UR Type Definition for Encrypted Messages

## BCR-2022-001

**© 2022 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Mar 15, 2022<br/>
Revised: Aug 12, 2023

---

## Introduction

This paper addresses the need for a way to encrypt messages using best practices and encode them using [CBOR](https://cbor.io/) and [URs](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md). It specifies a general "encrypted message" structure and a specific encoding based on ChaCha20-Poly1305 Authenticated Encryption as specified in [RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439).

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type          | CBOR Tag |
| :--------------- | :------- |
| ur:encrypted     | #6.40002 |
| ur:crypto-key    | #6.40023 |
| ur:encrypted-key | #6.40027 |

These tags have been registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

### Related Work

The [COSE specification](https://datatracker.ietf.org/doc/draft-ietf-cose-rfc8152bis-struct/) specifies a highly general structure for the encryption and signing of messages in CBOR. There is also a need for an alternative that is simpler, more specific, more compact, and more opinionated about best practices, while still allowing for extensibility and able to serve as a component of larger structures.

## The ChaCha20-Poly1305-IETF Cipher

The [IETF variant of the ChaCha20-Poly1305](https://datatracker.ietf.org/doc/html/rfc8439) construction can encrypt a practically unlimited number of messages, but individual messages cannot exceed 64*(2^32)-64 bytes (approximately 256 GiB).

To encrypt a message, the sender provides a 32-byte symmetric key and a 12-byte nonce. The nonce is sent as part of the message, but the key is kept secret between the sender and recipient. The ChaCha20 stream cipher is used for encryption and decryption, and as part of the construction, a 16-byte authentication tag is generated using Poly1305, and is used to verify message integrity. An "additional authenticated data" field can also be provided, which is not encrypted, but it is included in the message authentication step. This field is often used to send metadata about the encrypted portion of the message. In all, the fields used and the names this document refers to them by are:

* `plaintext`: [Any length] The unencrypted message.
* `ciphertext`: [Same length as `plaintext`] The encrypted message.
* `aad`: [Any length] Additional Authenticated Data
* `key`: [32 bytes] The symmetric key.
* `nonce` [12 bytes] The nonce, which must not be repeated for the same key.
* `auth` [16 bytes] The authentication tag.

## CDDL for Encrypted Message

The following specification is written in [Concise Data Definition Language (CDDL)](https://tools.ietf.org/html/rfc8610).

When used embedded in another CBOR structure, this structure MUST be tagged `#6.40002`. When used as the top-level object of a UR, it MUST NOT be tagged.

The general format for a Encrypted Message is a CBOR array with either 3 or 4 elements. The `aad` element is optional, but if it is present it MUST NOT be empty.

```
encrypted = [ ciphertext, nonce, auth, ? aad ];

ciphertext = bytes
nonce = bytes .size 12
auth = bytes .size 16
aad = bytes
```

### Example/Test Vector

* Test Vector from [Section 2.8.2 of RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439#section-2.8.2):

plaintext: `4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e`

plaintext as UTF-8: `Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it.`

aad: `50515253c0c1c2c3c4c5c6c7`

key: `808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f`

nonce: `070000004041424344454647`

ciphertext: `d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116`

* In the CBOR diagnostic notation, with `#6.40002` tag:

```
40002( / encrypted /
   [
      h'd31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d6
        3dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b36
        92ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc
        3ff4def08e4b7a9de576d26586cec64b6116', / ciphertext /
      h'070000004041424344454647', / nonce /
      h'1ae10b594f09e26a7e902ecbd0600691', / auth /
      h'50515253c0c1c2c3c4c5c6c7' / aad /
   ]
)
```

* Encoded as binary using [CBOR Playground](https://cbor.me):

```
d9 9c42                                 # tag(40002) encrypted
   84                                   # array(4)
      58 72                             # bytes(114) ciphertext
         d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116
      4c                                # bytes(12)
         070000004041424344454647       # "....@ABCDEFG"
      50                                # bytes(16) auth
         1ae10b594f09e26a7e902ecbd0600691
      4c                                # bytes(12) aad
         50515253c0c1c2c3c4c5c6c7       #
```

* As a hex string:

```
d99c42845872d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b61164c070000004041424344454647501ae10b594f09e26a7e902ecbd06006914c50515253c0c1c2c3c4c5c6c7
```

* The structure above, as a UR:

NOTE: URs do not use CBOR tags for the top-level object. The type of the object is provided by the type field of the UR schema, in this case `encrypted`:

```
ur:encrypted/lrhdjptecylgeeiemnhnuykglnperfguwskbsaoxpmwegydtjtayzeptvoreosenwyidtbfsrnoxhylkptiobglfzszointnmojplucyjsuebknnambddtahtbonrpkbsnfrenmoutrylbdpktlulkmkaxplvldeascwhdzsqddkvezstbkpmwgolplalufdehtsrffhwkuewtmngrknntvwkotdihlntoswgrhscmgsataeaeaefzfpfwfxfyfefgflgdcyvybdhkgwasvoimkbmhdmsbtihnammegsgdgygmgurtsesasrssskswstcfnbpdct
```

### Security Considerations

The security considerations for this type are the same as that for the cryptographic construction defined in [RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439).

## Future Proofing

The `#6.40002` tag is intended to be extensible to other symmetric encryption constructs, if and when the need arises. The only requirement is that later constructs are distinguishable from the one defined herein, for example by inserting a distinguishing integer as the first element of the array.

## Symmetric Encryption Key

The `#6.40023` tag is used to represent a symmetric encryption key. It is a byte string of 32 bytes, which is the size of the key used in the ChaCha20-Poly1305-IETF cipher.

```cddl
crypto-key = bytes .size 32
```

## Encrypted Key

The `#6.40027` tag is used to represent a key that has been encrypted using a derivation function. It is a profile of `EncryptedMessage` which MUST contain the CBOR serialization of a `KeyDerivation` structure in the message's Additional Authenticated Data (AAD) field:

```cddl
EncryptedKey = #6.40027(EncryptedMessage)   ; TAG_ENCRYPTED_KEY

EncryptedMessage =
    #6.40002([                              ; TAG_ENCRYPTED
        ciphertext: bstr,
        nonce: bstr,
        auth: bstr,
        aad: bstr .cbor KeyDerivation       ; This MUST be present in an `EncryptedKey`
    ])
```

So the full serialization will have two nested tags: the outer one representing `EncryptedKey` and the inner one representing `EncryptedMessage`:

```cddl
#6.40027( #6.40002( ... ) )
```

Currently four key derivation methods are supported:

```cddl
KeyDerivationMethod = HKDF / PBKDF2 / Scrypt / Argon2id

HKDF = 0
PBKDF2 = 1
Scrypt = 2
Argon2id = 3
```

The above constants are used to identify the key derivation method in the `KeyDerivation` structure, which is an array of the form:

```cddl
[<KeyDerivationMethod>, Salt, <other parameters>]
```

The actual parameter arrays being:

```cddl
KeyDerivation = HKDFParams / PBKDF2Params / ScryptParams / Argon2idParams

HKDFParams = [HKDF, Salt, HashType]
PBKDF2Params = [PBKDF2, Salt, iterations: uint, HashType]
ScryptParams = [Scrypt, Salt, log_n: uint, r: uint, p: uint]
Argon2idParams = [Argon2id, Salt]

HashType = SHA256 / SHA512

SHA256 = 0
SHA512 = 1
```

The `Salt` type is defined in [BCR-2023-017](bcr-2023-017-salt.md).

### IANA Considerations

This document requests that [IANA](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml) reserve the following tag:

| Tag   | Data Item    | Semantics                                                          |
| :---- | :----------- | :----------------------------------------------------------------- |
| 40002 | array        | ur:encrypted, IETF ChaCha20-Poly1305 (RFC8439) encrypted message   |
| 40023 | byte string  | ur:crypto-key, Cryptographic key used for symmetric encryption     |
| 40027 | tagged array | ur:encrypted-key, Content key encrypted with a derivation function |
