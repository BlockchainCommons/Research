# Uniform Resources (UR)

Encoding Structured Binary Data for Transport in URIs and QR Codes

## BCR-0005

**© 2020 Blockchain Commons**

Author: Wolf McNally<br/>
Date: May 4, 2020

---

### Introduction

In order to increase security, developers of hardware cryptocurrency wallets deliberately elide wireless networking capability from their devices. Nonetheless, such devices must send and receive data through some channel to function, and the quantity of data can easily exceed human patience for manual transcription. Many device makers have settled on QR codes [QRCode] as a way of optically sending data from their device displays to network-connected devices. Unconnected devices that include a camera can also read QR codes. Exclusively using QR codes for the transmission of data has the advantages of transparency and the reduction of the attack surface.

While QR codes have built-in error correction and several different encoding modes optimized for different forms of data, they do not impose an internal structure on the data they convey. They do however limit the maximum amount of data that can be conveyed in a single QR code. Ultimately this limitation is due to the inherent limitations of optical readers to resolve a captured image. The largest QR code ("version 40") consists of 177x177 "modules" (pixels). Version 40 QR codes, using the binary encoding mode and the lowest level of error correction have a capacity of 2,953 bytes [QRCodeCapacity]. This maximum capacity on QR codes becomes an issue when one wishes to convey data payloads longer than the maximum supported by the standard. In addition, since the assumed use case of QR codes is usually to convey human-readable text (the canonical example being a URL) the native binary encoding mode of QR codes is not consistently supported by readers [QRBinaryProblems].

QR Codes support an "alphanumeric" mode optimized for efficiently conveying a subset of ASCII consisting of 45 characters:

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:
```

This character set is optimized for industrial applications, not general text (e.g., lower case letters are not included) or even URL encoding (symbols used in URIs such as `?`, `=`, and `#` are not included). It is also impossible to convey binary data encoded as Base64 or Base64URL [RFC4648] using this character set as these formats require the use of both upper case and lower case letters [URIBinary].

Developers of cryptocurrency wallets currently all have their own bespoke ways of breaking a binary message into several parts suitable for display as a series of QR codes, and reassembling them on the destination device. This lack of standardization is one of several problems hampering interoperability between such devices.

### The Uniform Resource (UR) Encoding

This document proposes a method of encoding binary data of arbitrary content and length so that it is suitable for transport in either URIs *or* QR codes with little or no reformatting necessary.

The name of the URI scheme for this encoding is "UR" and is intended to be analogous to existing names such as "URL" ("Uniform Resource Locator"), "URI" ("Uniform Resource Identifier") and URN ("Uniform Resource Name"). As this encoding method is intended for self-contained resources themselves, we have chosen "UR" ("Uniform Resource").

This proposed method has the following goals:

* Transport binary data of arbitrary content and length using a sequence of one or more URIs or QR codes.
* Remain agnostic about whether QR codes are displayed together or time-sequenced (animated).
* Avoid the use of QR code binary mode to support transparency and wide compatibility with QR code reader libraries.
* Use the alphanumeric QR code mode for efficiency.
* Be case agnostic, allowing use of all upper case letters (for QR code transport) or all lower case letters (canonical for display and URIs.)
* Include sequencing information so the receiver can be certain of arrival and order of all parts.
* Include a cryptographic digest of the entire message in each part to tie them together, uniquely identify the whole message, and ensure the exact transmitted message has been reconstructed.
* Each single part should also be a valid URI and not require escaping (e.g. percent-encoding) of any of its characters.
* Combining a set of parts, which are separate URIs themselves, should involve simple textual manipulation, mostly concatenation, and should again result in a well-formed URI.
* Support the addition of structure in the binary data. Initially specify how binary data representing undifferentiated byte strings should be encoded.

### BC32

The method of encoding binary data as printable characters specified in this proposal is [BC32]. BC32 is a modification of [Bech32] that drops the prologue containing the "human readable part" and `1` numeral divider.

#### BC32 Example

The following UTF8 string:

```
Hello, world
```

Has the following bytes as payload:

```
48656c6c6f2c20776f726c64
```

Which encoded as BC32 is:

```
fpjkcmr09ss8wmmjd3jq6ax7w9
====================------
payload             checksum

```

**✳️ Note:** *The accompanying Wolfram Language (Mathematica) notebook includes a reference implementation of BC32.*

### CBOR

At the binary level, the goal of adding structure is accomplished by standardizing on the Concise Binary Object Representation [CBOR]. All payloads encoded according to this specification MUST be well-formed CBOR.

By specifying a standard for binary structure, users of this format can begin to standardize structures that go beyond undifferentiated byte strings. CBOR has many desirable traits, including being self-describing, fast to encode and decode, and having minimal implementation complexity. Encoding binary strings as CBOR according to this specification adds a single byte of overhead for payloads of 23 or fewer bytes, two bytes for payloads up to 255 bytes, and three bytes for payloads up to 65535 bytes, and lays the groundwork for encoding more complex structures in the future.

This specification does not require that a complete CBOR codec be used by implementors. It only specifies that a minimal canonical representation for encoding byte strings be used:

* If the encoded byte string has 23 or fewer bytes, it is preceded by the single byte (`0x40` + length).
* If the encoded byte string has 24..255 bytes, it is preceded by (`0x58`, length) where *length* is the length of the following byte string.
* If the encoded byte string has 256..65535 bytes, it is preceded by (`0x59`, h, l) where *h*, *l* is the big-endian two byte length of the following byte string.
* If the encoded byte string has 65536..2^32-1 bytes, it is preceded by (`0x60`, b1, b2, b3, b4) where *b(n)* is the big-endian four byte length of the following byte string.

Writers of this format MUST use the shortest encoding given the length of the payload. CBOR also supports an 8-byte length encoding for payloads longer than 2^32-1 bytes, and also encoding of "indefinite length" byte strings, but implementors of this specification MAY refuse to decode them. Implementors of this specification MAY also reject any other CBOR constructs.

**✳️ Note:** *The accompanying Wolfram Language (Mathematica) notebook includes a reference implementation of the minimal canonical codec for CBOR under this specification. It is not a complete CBOR implementation; only what is necessary to support this specification.*

#### CBOR Examples

A 16-byte cryptographic seed:

```
c3fb80bf2c80732f369225e20f7c7aed
```

The seed encoded as CBOR. It includes a one-byte header, 0x50, which is 0x40 + the length of 0x10 (16).

```
50c3fb80bf2c80732f369225e20f7c7aed
--================================
header
  payload
```

A 32-byte cryptographic seed:

```
ab1b5980595a6e13112c5739283ff5286379e0beac4f3427352a254c40a39ff
```

The seed encoded as CBOR. It includes a two-byte header, (0x58, 0x20), which is 0x58 to identify a single-byte length, and 0x20, which is the length of the string (32).

```
58203ab1b5980595a6e13112c5739283ff5286379e0beac4f3427352a254c40a39ff
----================================================================
header
    payload
```

### Types

Each UR encoded object includes a `type` component as the first path component after the `UR` scheme. Types may consist only of characters from the English letters (ignoring case) and Arabic numerals.

The only type this document specifies is `bytes` which represents an undifferentiated string of bytes of any length. It is intended that future specifications will register and document other types that will specify other forms of structured content intended to address various problem domains.

### Procedure for UR encoding

**✳️ Note:** *In this document, "part" refers to a well-formed URI as specified herein, while "fragment" refers to the subsequence of BC32-encoded characters contained in each part.*

Given `payload` is an array of bytes.

#### 1. Encode payload as CBOR

```
cborPayload = CBOREncodeBytes[payload];
```

#### 2. Encode the CBOR-encoded payload as BC32

```
bc32Payload = BC32Encode[cborPayload];
```

#### 3. Compute the SHA256 digest of the CBOR-encoded payload

```
digest = SHA256Hash[cborPayload];
```

#### 4. Encode the digest as BC32

```
bc32Digest = BC32Encode[digest];
```

#### 5. Partition the encoded payload into a sequence of fragments

The number of characters in each fragment is `maximumFragmentCharacters` and depends on the desired density of the resultant QR Codes. There is no requirement that all the fragments be of equal size. In the simplest partitioning scheme, the last fragment may be shorter than the others. 1000 characters per fragment is suggested based on experimentation with smaller display sizes.

```
maximumFragmentCharacters = 1000;
fragments = StringPartition[bc32Payload, UpTo[maximumFragmentCharacters]];
```

#### 6. Prepend each fragment with a header that includes scheme, type, sequencing, digest, and the fragment.

The URI scheme `ur` is separated from the rest by a colon. Forward slashes are used to delimit the `type`, optional `sequencing`, optional `digest`, and the payload `fragment` using the following syntax:

```
ur:type[/sequencing][/digest]/fragment
```

* If a complete resource is contained in a single fragment, then `sequencing` MAY be omitted.
* If a complete resource is contained in a single fragment and `sequencing` is present, it MUST be `1of1`.
* If `sequencing` is present, then `digest` MUST also be present.
* If `sequencing` is omitted, then `digest` MAY also be omitted.
* If `digest` is present, it MUST match the SHA256 hash of the decoded CBOR payload.

```
parts = AddHeadersToFragments[fragments, type, bc32Digest];
```

#### 7. Generate the QR Codes from the fragments

This step includes transforming the parts to upper case to take advantage of the QR Code alphanumeric encoding mode.

```
qrCodes = MakeQRCodes[parts];
```
 ---
 
### Example of UR encoding

**✳️ Note:** *The accompanying Wolfram Language (Mathematica) notebook includes a reference implementation of the methods needed to duplicate the example below.*

* Generate a random payload of 800 bytes.

```
:= payload = RandomInteger[255, 800] // ByteArray;
:= payload // ToHex // Short
590320daeabff1aa00f3b02bd84dbcf75ddaf124d0c6aabf4217c...6b8120d4eafdfc0da4e6c6522b6469b8eb3e359aea5c65c0f0905
```

* Encode payload as CBOR

```
:= cborPayload = CBOREncodeBytes[payload];
:= cborPayload // ToHex // Short
590320aa85acda37099768f5033130904fadcbeb9cf250585ee11...3ded28edce0b122b0e03f507f8fb158cb2a9c16e4820b2c0e9a83
```

* Encode CBOR payload as BC32

```
:= bc32Payload = BC32Encode[cborPayload];
:= bc32Payload // Short
typjp2594ndrwzvhdr6sxvfsjp86mjltnne9qkz7uydn9unk0a4d5...9sp9faa55wmnstzg4suql4qlu0k9vvk25uzmjgyzevp6dgx40kpkd
```

* Compute the SHA256 digest of the CBOR-encoded payload

```
:= digest = SHA256Hash[cborPayload];
:= digest // ToHex
94d9d7cbb398c9b4d83cf7ca2784bf69220243c0bb7a0b1725a66da391d181a3
```

* Encode digest as BC32

```
:= bc32Digest = BC32Encode[digest];
:= bc32Digest
jnva0jannrymfkpu7l9z0p9ldy3qys7qhdaqk9e95ek68yw3sx3s2akpkn
```

* Partition the BC32-encoded payload into a sequence of fragments

```
:= maximumFragmentCharacters = 200;
:= fragments = StringPartition[bc32Payload, UpTo[maximumFragmentCharacters]];
:= First[fragments]
typjp2594ndrwzvhdr6sxvfsjp86mjltnne9qkz7uydn9unk0a4d5kcvhawefx9yuvuax5t7av5u2rcx5ggpycq0vrtvvxlw38g96vz8538z25d66ugwkkeu7qspx2sk6l54atwk9tzg5ntndhekuxjemd5uw62gas3xen58phnyq5wwf4ce99q8sqn8nu4yle70542a
```

* Prepend each fragment with a header that includes scheme, type, sequencing, and digest

```
:= parts = AddHeadersToFragments[fragments, "bytes", bc32Digest];
:= First[parts]
ur:bytes/1of7/jnva0jannrymfkpu7l9z0p9ldy3qys7qhdaqk9e95ek68yw3sx3s2akpkn/typjp2594ndrwzvhdr6sxvfsjp86mjltnne9qkz7uydn9unk0a4d5kcvhawefx9yuvuax5t7av5u2rcx5ggpycq0vrtvvxlw38g96vz8538z25d66ugwkkeu7qspx2sk6l54atwk9tzg5ntndhekuxjemd5uw62gas3xen58phnyq5wwf4ce99q8sqn8nu4yle70542a
```

* Generate the QR Codes from the fragments

```
:= qrCodes = MakeQRCodes[parts];
DisplayQRCodes[qrCodes]
```

![](bcr-0005/1.png)

---

Example decoding of the first QR code above:

```
:= BarcodeRecognize[First[qrCodes]]
UR:BYTES/1OF7/JNVA0JANNRYMFKPU7L9Z0P9LDY3QYS7QHDAQK9E95EK68YW3SX3S2AKPKN/TYPJP2594NDRWZVHDR6SXVFSJP86MJLTNNE9QKZ7UYDN9UNK0A4D5KCVHAWEFX9YUVUAX5T7AV5U2RCX5GGPYCQ0VRTVVXLW38G96VZ8538Z25D66UGWKKEU7QSPX2SK6L54ATWK9TZG5NTNDHEKUXJEMD5UW62GAS3XEN58PHNYQ5WWF4CE99Q8SQN8NU4YLE70542A
```

### Combining Fragments

Each individual UR part is a well-formed URI. UR parts can be combined into a single part that is also a well-formed URI by concatenating in-order the fragments of every part and preserving the overall syntactical structure:

```
ur:type[/1of1][/digest]/concatenated-fragments
```

### References

* [QRCode] [Wikipedia: QR Code](https://en.wikipedia.org/wiki/QR_code)
* [QRCodeCapacity] [QRCode.com: Information Capacity and Versions of the QR Code](https://www.qrcode.com/en/about/version.html)
* [QRBinaryProblems] [StackOverflow: Storing binary data in QR codes](https://stackoverflow.com/questions/37996101/storing-binary-data-in-qr-codes)
* [RFC4648] [The Base16, Base32, and Base64 Data Encodings](https://tools.ietf.org/html/rfc4648)
* [BC32] [Blockchain Commons: The BC32 Data Encoding Format](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-0004-bc32.md)
* [Bech32] [BIP-173: Base32 address format for native v0-16 witness outputs](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki)
* [URIBinary] [Blockchain Commons: Encoding Binary Compatibly with URI Reserved Characters](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-0003-uri-binary-compatibility.md)
* [CBOR] [Concise Binary Object Representation (CBOR)](https://tools.ietf.org/html/rfc7049)
* [RFC3986] [Uniform Resource Identifier (URI): Generic Syntax](https://tools.ietf.org/html/rfc3986)
* [QRCodeAlphaNum] [QR Codes, Table of Alphanumeric Values](https://www.thonky.com/qr-code-tutorial/alphanumeric-table)
* [BinaryToText] [Encoding Standards for Binary-to-text Encoding](https://en.wikipedia.org/wiki/Binary-to-text_encoding#Encoding_standards)
