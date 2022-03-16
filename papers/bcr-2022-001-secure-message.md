# UR Type Definition for Secure Messages

## BCR-2022-001

**© 2022 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Mar 15, 2022

---

## Introduction

This paper addresses the need for a way to encrypt messages using best practices and encode them using [CBOR](https://cbor.io/) and [URs](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md). It specifies a general "secure message" structure and a specific encoding based on ChaCha20-Poly1305 Authenticated Encryption as specified in [RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439).

This specification defines a type `crypto-msg` (CBOR tag `#6.48`).

⚠️ WARNING: As of the date of this publication the tag `#6.48` is unallocated in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml). Blockchain Commons is applying for this number to be assigned to the CBOR specification herein, but because it is in a range that is open to other applications, it may change. So for now, the `#6.48` tag MUST be understood as provisional and subject to change by all implementors.

### Related Work

The [COSE specification](https://datatracker.ietf.org/doc/draft-ietf-cose-rfc8152bis-struct/) specifies a highly general structure for the encryption and signing of messages in CBOR. There is also a need for an alternative that is simpler, more specific, more compact, and more opinionated about best practices, while still allowing for extensibility and able to serve as a component of larger structures.

## The ChaCha20-Poly1305-IETF Cipher

The [IETF variant of the ChaCha20-Poly1305](https://datatracker.ietf.org/doc/html/rfc8439) construction can encrypt a practically unlimited number of messages, but individual messages cannot exceed 64*(2^32)-64 bytes (approximatively 256 GiB).

To encrypt a message, the sender provides a 32-byte symmetric key and a 12-byte nonce. The nonce is sent as part of the message, but the key is kept secret between the sender and recipient. The ChaCha20 stream cipher is used for encryption and decryption, and as part of the construction, a 16-byte authentication tag is generated using Poly1305, and is used to verify message integrity. An "additional authenticated data" field can also be provided, which is not encrypted, but it is included in the message authentication step. This field is often used to send metadata about the encrypted portion of the message. In all, the fields used and the names this document refers to them by are:

* `plaintext`: [Any length] The unencrypted message.
* `ciphertext`: [Same length as `plaintext`] The encrypted message.
* `aad`: [Any length] Additional Authenticated Data
* `key`: [32 bytes] The symmetric key.
* `nonce` [12 bytes] The nonce, which must not be repeated for the same key.
* `auth` [16 bytes] The authentication tag.

## CDDL for Secure Message

The following specification is written in [Concise Data Definition Language (CDDL)](https://tools.ietf.org/html/rfc8610).

When used embedded in another CBOR structure, this structure MUST be tagged `#6.48` (SEE WARNING ABOVE). When used as the top-level object of a UR, it MUST NOT be tagged.

The general format for a Secure Message is a CBOR array. The first element is always an integer that specifies the semantics of the remaining elements. Currently this specification only defines the semantics of the type integer `1` as being followed by fields that implement the IETF variant of the ChaCha20-Poly1305 construction.

```
crypto-msg = [ type, nonce, auth, aad, ciphertext ];

type: uint = 1
nonce: bytes .size 12
auth: bytes .size 16
aad: bytes
ciphertext: bytes
```

### Example/Test Vector

* Test Vector from [Section 2.8.2 of RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439#section-2.8.2):

plaintext: `4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e`

plaintext as UTF-8: `Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it.`

aad: `50515253c0c1c2c3c4c5c6c7`

key: `808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f`

nonce: `070000004041424344454647`

ciphertext: `d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116`

* In the CBOR diagnostic notation, with `#6.48` tag:

```
48( # crypto-msg
  [
    1, # type
    h'070000004041424344454647', # nonce
    h'1AE10B594F09E26A7E902ECBD0600691', # auth
    h'50515253C0C1C2C3C4C5C6C7', # aad
    h'D31A8D34648E60DB7B86AFBC53EF7EC2A4ADED51
      296E08FEA9E2B5A736EE62D63DBEA45E8CA96712
      82FAFB69DA92728B1A71DE0A9E060B2905D6A5B6
      7ECD3B3692DDBD7F2D778B8C9803AEE328091B58
      FAB324E4FAD675945585808B4831D7BC3FF4DEF0
      8E4B7A9DE576D26586CEC64B6116' # ciphertext
  ]
)
```

* Encoded as binary using [CBOR Playground](https://cbor.me):

```
D8 30                                   # tag(48) crypto-msg
   85                                   # array(5)
      01                                # unsigned(1) type: ietf-chacha-poly
      4C                                # bytes(12) nonce
         070000004041424344454647
      50                                # bytes(16) auth
         1AE10B594F09E26A7E902ECBD0600691
      4C                                # bytes(12) aad
         50515253C0C1C2C3C4C5C6C7
      58 72                             # bytes(114) ciphertext
         D31A8D34648E60DB7B86AFBC53EF7EC2A4ADED51
         296E08FEA9E2B5A736EE62D63DBEA45E8CA96712
         82FAFB69DA92728B1A71DE0A9E060B2905D6A5B6
         7ECD3B3692DDBD7F2D778B8C9803AEE328091B58
         FAB324E4FAD675945585808B4831D7BC3FF4DEF0
         8E4B7A9DE576D26586CEC64B6116
```

* As a hex string:

```
d83085014c070000004041424344454647501ae10b594f09e26a7e902ecbd06006914c50515253c0c1c2c3c4c5c6c75872d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116
```

* The structure above, as a UR:

NOTE: URs do not use CBOR tags for the top-level object. The type of the object is provided by the type field of the UR schema, in this case `crypto-msg`:

```
ur:crypto-msg/lpadgsataeaeaefzfpfwfxfyfefgflgdcyvybdhkgwasvoimkbmhdmsbtihnammegsgdgygmgurtsesasrssskswsthdjptecylgeeiemnhnuykglnperfguwskbsaoxpmwegydtjtayzeptvoreosenwyidtbfsrnoxhylkptiobglfzszointnmojplucyjsuebknnambddtahtbonrpkbsnfrenmoutrylbdpktlulkmkaxplvldeascwhdzsqddkvezstbkpmwgolplalufdehtsrffhwkuewtmngrknntvwkotdihlntoswgrhscmpmdpasgm
```

### Security Considerations

The security considerations for this type are the same as that for the cryptographic construction defined in [RFC-8439](https://datatracker.ietf.org/doc/html/rfc8439).
