# Gordian Envelope Extension: Compression

## BCR-2023-005

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022<br/>
Revised: Aug 15, 2023

## Abstract

This document extends the Gordian Envelope Base Specification to add the `compressed` case arm, which supports the general purpose compression of any Envelope.

## Introduction

This document extends the [Gordian Envelope Base Specification](https://datatracker.ietf.org/doc/draft-mcnally-envelope/) to add the `compressed` case arm used to represent an Envelope that has been compressed. The scheme defined herein supports the [DEFLATE](https://datatracker.ietf.org/doc/html/rfc1951) algorithm.

Like elision, which is supported by the Envelope Base Specification, compression is a reversible transformation of an Envelope that does not alter its unique digest. And since Envelope is a recursively nested structure of Envelopes in a Merkle-like digest tree, any of these nested envelopes can be elided or compressed without disturbing the tree, hence preserving constructs like signatures.

## Format Specification

This section is normative, and specifies an additional case arm for the `envelope` type: `compressed`. It also specifies that assertions may be compressed by adding the `compressed-assertion` case to Envelope's `assertion-element` type.

The formal language used is the [Concise Data Definition Language (CDDL)](https://datatracker.ietf.org/doc/html/rfc8610). The top-level specification of Gordian Envelope with this extension added is:

```
envelope = #6.200(envelope-content)
envelope-content = (
    leaf / elided / node / assertion / wrapped /
    compressed
)

assertion-element = (
    assertion / elided-assertion /
    compressed-assertion
)

compressed-assertion = compressed     ; MUST represent an assertion
```

The format for `compressed` corresponds to `tagged-compressed` as defined in [UR Type Definition for Compressed Messages](bcr-2023-001-compressed-message.md), including the CBOR tag `#6.40003`. In this specification, the optional fourth array element `tagged-digest` (defined in [BCR-2021-002](bcr-2021-002-digest.md)) is REQUIRED, and MUST contain the CBOR-encoded tagged digest of the envelope:

```
compressed = #6.40003([checksum, uncompressed-size, compressed-data, tagged-digest])

checksum = crc32
crc32 = uint

uncompressed-size = uint
compressed-data = bytes
```

The `compressed` case can be discriminated from other Envelope case arms by the fact that it is the only one that is tagged using `#6.40003`.

## Declaring the Digest

This section is normative.

The `compressed` case directly declares the compressed envelope's digest as the fourth element of its array, `digest`. The `tagged-digest` encoded therein MUST match the actual digest of the Envelope that has been compressed. Decompressing an envelope MUST be validated by matching the uncompressed Envelope's actual computed digest to the one declared, and the decompression operation MUST reject the result if the digests do not match.

**Example**

In the following example, the test envelope is too small for effective compression by DEFLATE, so the uncompressed payload is used where the compressed payload would normally be. This is as is specified in [UR Type Definition for Compressed Messages](bcr-2023-001-compressed-message.md) and is only for example purposes.

```
$ ENVELOPE=`envelope subject "Hello"`

$ envelope format --diag $ENVELOPE

200(   / envelope /
   24("Hello")   / leaf /
)

$ envelope digest --hex $ENVELOPE

4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b

$ COMPRESSED_ENVELOPE=`envelope compress $ENVELOPE`
$ envelope format --diag $COMPRESSED_ENVELOPE

200(   / envelope /
   40003(   / compressed /
      [
         1146116589,
         10,
         h'd8c8d8186548656c6c6f',
         40001(   / digest /
            h'4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b'
         )
      ]
   )
)

$ envelope digest --hex $COMPRESSED_ENVELOPE

4d303dac9eed63573f6190e9c4191be619e03a7b3c21e9bb3d27ac1a55971e6b
```

Notice that the digest of the unencrypted and encrypted Envelopes both match. This is because the fourth array element of the encrypted Envelope declares the uncompressed envelope's digest.

## Reference Implementations

This section is informative.

Both the [Swift Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/BCSwiftEnvelope) and the [Rust Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/bc-envelope-rust) support this extension.

## Future Proofing

To support this extension, future extensions to the compressed message used herein and defined in [UR Type Definition for Compressed Messages](bcr-2023-001-compressed-message.md) may support other compression constructs. To work with this specification, they MUST support an equivalent of the `digest` field so that the digest of the encrypted Envelope can be declared.

## Security Considerations

In general, this specification inherits any security considerations of the DEFLATE algorithm.

## IANA Considerations

This document makes no requests of IANA.
