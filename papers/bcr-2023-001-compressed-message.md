# UR Type Definition for Compressed Messages

## BCR-2023-001

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 13, 2022<br/>
Revised: Aug 13, 2023

---

## Introduction

This paper addresses the need for a way to compress messages using best practices and encode them using [CBOR](https://cbor.io/) and [URs](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md). It specifies a general "compressed message" structure and a specific encoding based on the DEFLATE algorithm as specified in [RFC 1951](https://datatracker.ietf.org/doc/html/rfc1951).

This specification defines a UR type `compressed` (CBOR tag `#6.40003`).

⚠️ WARNING: As of the date of this publication the tag `#6.40003` is unallocated in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml). Blockchain Commons is applying for this number to be assigned to the CBOR specification herein, but because it is in a range that is open to other applications, it may change. So for now, the `#6.40003` tag MUST be understood as provisional and subject to change by all implementors.

## The DEFLATE algorithm

The [DEFLATE algorithm](https://datatracker.ietf.org/doc/html/rfc1951) is a lossless compression algorithm that can compress a practically unlimited number of messages, but individual messages cannot exceed 2^32 bytes (approximately 4 GiB).

The following line of code using the ZLIB API obtains the recommended default configuration of the encoder:

```
deflateInit2(zstream,5,Z_DEFLATED,-15,8,Z_DEFAULT_STRATEGY)
```

The configuration of the encoder may be adjusted by the user, but the decoder MUST be able to decode any valid DEFLATE stream.

## CDDL for Compressed Message

The following specification is written in [Concise Data Definition Language (CDDL)](https://tools.ietf.org/html/rfc8610).

When used embedded in another CBOR structure, this structure MUST be tagged `#6.40003`. When used as the top-level object of a UR, it MUST NOT be tagged.

`tagged-digest` is defined in [BCR-2021-002](bcr-2021-002-digest.md).

```
tagged-compressed = #6.40003(compressed)

compressed = [
    checksum,           ; CRC-32 checksum of the uncompressed data
    uncompressed-size,
    compressed-data,
    ? tagged-digest    ; Optional user-defined SHA-256 digest
]

checksum = crc32
uncompressed-size = uint
compressed-data = bytes

crc32 = uint
```

The `checksum` field is a standard feature of most DEFLATE implementations, and MUST be validated by the decoder. The `digest` field is optional and is not validated by the decoder, but may be used by the application to validate the integrity of the uncompressed data in ways that are beyond the scope of this specification. It's format is as defined in "Digests for Digital Objects" [BCR-2021-002](bcr-2021-002-digest.md).

If the payload is too small to compress using DEFLATE, the uncompressed payload MUST be placed in the `compressedData` field and the length of that field MUST be the same as the `uncompressedSize` field.

Due to fixed overhead, the compressed form of very small messages may be somewhat larger than their uncompressed form.

## Future Proofing

The `#6.40003` tag is intended to be extensible to other compression constructs, if and when the need arises. The only requirement is that later constructs are distinguishable from the one defined herein, for example by inserting a distinguishing integer as the first element of the array.

## IANA Considerations

When a digest of another object is encoded as tagged CBOR, it is tagged #6.40001. This document requests registration of the following CBOR tag:

* Tag: 6.40003
* Data Item: array
* Semantics: Compressed Message
