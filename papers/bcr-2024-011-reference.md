# Digital Object References

## BCR-2024-011

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 22, 2024

### Introduction

Many objects have some form of globally unique identifier that takes the form of a 32-byte (256 bit) value. Sometimes it is desirable to refer to an object by such an identifier.

Any globally unique object or identifier can be converted to a 32-byte identifier by, for example, taking its SHA-256 digest. This can work with 16-byte (128 bit) UUIDs, or tagged CBOR serializations of globally unique objects like public keys.

This document introduces a new CBOR tag, `#6.40025`, for representing globally unique references, simply called `Reference` herein. `Reference`s are used to indicate a globally unique object (the "referent").

For each type for which a `Reference` can be provied, the the object type documentation must publish a way to generate a globally unique identifier for it.

### Example: XIDs

A [XID](bcr-2024-010-xid.md) is a 32-byte identifier created by hashing the tagged CBOR encoding of a `SigningPublicKey`. The CBOR representation of a BIP-340 Schnorr `SigningPublicKey` in CBOR diagnostic notation would be:

```
40022(
    h'e8251dc3a17e0f2c07865ed191139ecbcddcbdd070ec1ff65df5148c7ef4005a'
)
```

Serialized to hex:

```
d9 9c56                                 # tag(40022) signing-public-key
    5820                                # bytes(32)
        e8251dc3a17e0f2c07865ed191139ecbcddcbdd070ec1ff65df5148c7ef4005a

=>

d99c565820e8251dc3a17e0f2c07865ed191139ecbcddcbdd070ec1ff65df5148c7ef4005a
```

Taking the SHA-256 hash this encoding gives a globally unique identifier for this `PublicSigningKey`:

```
d40e0602674df1b732f5e025d04c45f2e74ed1652c5ae1740f6a5502dbbdcd47
```

When wrapped in the CBOR tag for XIDs, `#6.40024`, this becomes a `XID`:

```
40024(
    h'd40e0602674df1b732f5e025d04c45f2e74ed1652c5ae1740f6a5502dbbdcd47'
)
```

This XID can in turn be the subject of a Gordian Envelope that contains much more information: the XID document. XID documents can be quite long and may be retrieved using the XID itself as a key.

In the case of XIDs, the hashed CBOR encoding of a specific `PublicSigningKey` (the "inception key") is used as the `Reference` for the `XID` object, so this would be wrapped in the `Reference` tag:

```
40025(
    h'd40e0602674df1b732f5e025d04c45f2e74ed1652c5ae1740f6a5502dbbdcd47'
)
```

Note that references do not include the type of object they refer to: they are used in contexts where the reference can be resolved to the full object, which could be done locally within a document, or globally by looking up the reference in a registry or index.

## User-Facing Description

The first four bytes of a `Reference`'s data are in most cases sufficiently unique for humans to identify the object referred to. For an object of a known type, like a XID, this can be displayed as a human-readable prefix:

```
XID(d40e0602)
```

while a `Reference` to that same XID would be displayed as:

```
Reference(d40e0602)
```

These four bytes can also be translated to [ByteWords](bcr-2020-012-bytewords.md) or [Bytemojis](bcr-2024-008-bytemoji.md) for a more human-friendly representation:

```
Reference(d40e0602)
TINY BETA ATOM ALSO
🧦 🤨 😎 😆
```

Similarly, if the display form of a `PublicKeys` is:

```
PublicKeys(c9ede672)
```

then a `Reference` to that `PublicKeys` would be:

```
Reference(c9ede672)
```

This correspondence between the identifier of object instances and references to them is machine-comparable (all 32 bytes are compared), and their shortened forms can be useful for end-user identification, debugging, and other contexts where human-readable identifiers are desired.

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type      | CBOR Tag |
| :----------- | :------- |
| ur:reference | #6.40025 |

## IANA Considerations

This document requests the assignment of a new CBOR tag for References: #6.40025.
