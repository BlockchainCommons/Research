# Registry of Uniform Resource (UR) Types

## BCR-2020-006

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: May 12, 2020<br/>
Revised: December 11, 2020

---

### Introduction

A limited, base-32 character set is required by Uniform Resources (UR) [BCR5] in order to be compatible with both URI syntax [RFC3986] and QR Code alphanumeric mode [QRCodeAlphaNum]. In addition, [BCR5] specifies:

> Each UR encoded object includes a `type` component as the first path component after the `UR` scheme. Types MUST consist only of characters from the English letters (ignoring case), Arabic numerals, and the hyphen `-`.

Because this namespace intersects with but does not enclose existing type namespace definitions such as [MIME] and because defined types like MIME do not uniformly specify CBOR encoding (required by [BCR5]) a new namespace is necessary to easily identify the type of data encoded in a UR.

This document is a registry of UR types and CBOR tags maintained by Blockchain Commons. Each entry in the registry records the type string, its associated CBOR tag, a brief description of the type, and either a link to the type defintion or a reference to the type definition within this document. Additional types may be added by contacting this document's maintainers.

Types specified within this document are specified in [CDDL], the Concise Data Definition Language used as a human-readable notation for CBOR structures.

### User-Defined Types `x-*`

All types with the prefix `x-` are reserved for user-defined UR types.

### CBOR-Wrapped Types `cbor-*`

All types with the prefix `cbor-` are reserved for existing non-CBOR media types wrapped in a CBOR byte string. The only types currently specified in this registry are `cbor-png` for [PNG] images and `cbor-svg` for [SVG] images.

### Tags for Embedding

Each UR type defines a CBOR encoding. When a UR type is suitable for embedding within another CBOR structure, it SHOULD be tagged with a CBOR tag defined for this purpose. This document also lists the tag, if any, defined for the particular CBOR strucure contained in the UR encoding. The tags listed here may or may not currently be listed in IANA's registry of CBOR tags [CBOR-TAGS] but the intent is that they will be registered as they come into us.

### Registry

| Type | Tag | Description | Definition |
|------|-----|-------------|------------|
| `bytes` | | Undifferentiated byte string | [[BCR5]](bcr-0005-ur.md) |
| `cbor-png` | | PNG image | [[PNG]](https://tools.ietf.org/html/rfc2083) |
| `cbor-svg` | | SVG image | [[SVG]](https://www.w3.org/TR/SVG11/) |
| `cose-sign` | 98 | COSE_Sign: Signed message (multiple recipients) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-sign1` | 18 | COSE_Sign1: Signed message (single recipient) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-encrypt` | 96 | COSE_Encrypt: Encrypted message (multiple recipients) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-encrypt0` | 16 | COSE_Encrypt0: Encrypted message (implied recipient) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-mac` | 97 | COSE_Mac: Authenticated message (multiple recipients) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-mac0` | 17 | COSE_Mac0: Authenticated message (implied recipient) | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-key` | | COSE_Key: An encryption key | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `cose-keyset` | | COSE_KeySet: A set of encryption keys | [[COSE]](https://tools.ietf.org/html/rfc8152) |
| `crypto-seed` | 300 | Cryptographic seed | This document |
| `crypto-bip39` | 301 | BIP-39 encoded seed | This document |
| `crypto-slip39` | 302 | One or more SLIP-39 shares | deprecated, removed |
| `crypto-hdkey` | 303 | Hierarchical Deterministic (HD) key | [[BCR-2020-007]](bcr-2020-007-hdkey.md) |
| `crypto-keypath` | 304 | Key Derivation Path | [[BCR-2020-007]](bcr-2020-007-hdkey.md) |
| `crypto-coin-info` | 305 | Cryptocurrency Coin Use | [[BCR-2020-007]](bcr-2020-007-hdkey.md) |
| `crypto-eckey` | 306 | Elliptic Curve (EC) key | [[BCR-2020-008]](bcr-2020-008-eckey.md) |
| `crypto-address` | 307 | Cryptocurrency Address | [[BCR-2020-009]](bcr-2020-009-address.md) |
| `crypto-output` | 308 | Bitcoin Output Descriptor | [[BCR-2020-010]](bcr-2020-010-output-desc.md) |
| `crypto-sskr` | 309 | SSKR (Sharded Secret Key Reconstruction) shard | [[BCR-2020-011]](bcr-2020-011-sskr.md) |
| `crypto-psbt` | 310 | Partially Signed Bitcoin Transaction (PSBT) | This document |
| `crypto-account` | 311 | BIP44 Account | [[BCR-2020-015]](bcr-2020-015-account.md) |
| `crypto-request` | 312 | Request to and Response from Airgapped Devices | [[BCR-2021-001]](bcr-2021-001-request.md) |
| `crypto-response` | 313 | Request to and Response from Airgapped Devices | [[BCR-2021-001]](bcr-2021-001-request.md) |
| | 400–405 | Used as descriptor types in [`crypto-output`](bcr-2020-010-output-desc.md). | |
| | 500–502 | Used as request types in [`crypto-request`](bcr-2021-001-request.md). | |
| | 600 | Object Fingerprint | This document and as defined in each type |

### Object Fingerprints

It is sometimes desirable that a CBOR-encoded object refer to another object by its unique SHA-256 hash ("fingerprint".) The method of deriving a fingerprint for a particular type is unique to that type and MAY be defined by that type. The source data for the SHA-256 hash MUST only include data that uniquely and permanently identifies the object, and MUST NOT include data that may change over time, such as object's name or other incidental metadata. This document defines the method for fingerprinting `crypto-seed` below. [[BCR-2020-007]](bcr-2020-007-hdkey.md) describes the method for fingerprinting a `crypto-hdkey`.

When UR types refer to other objects using a fingerprint, it MUST be tagged #6.600 and the byte string length MUST be exactly 32.

#### CDDL

```
fingerprint = #6.600(bytes .size 32)
```

### Byte String `bytes`

The type `bytes` contains a single, deterministic length byte string having a length from 1 to 2^32-1 bytes. This specification places no semantic interpretation on the contents of the string. Because of this, its usefulness is generally limited to development and testing purposes. Actual applications of Uniform Resources SHOULD use a more specific type.

#### CDDL

```
bytes
```

#### Example/Test Vector

* CBOR diagnostic notation:

```
h'00112233445566778899aabbccddeeff'
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
50                                  # bytes(16)
   00112233445566778899AABBCCDDEEFF
```

* As a hex string:

```
5000112233445566778899AABBCCDDEEFF
```

* As a UR:

```
ur:bytes/gdaebycpeofygoiyktlonlpkrksfutwyzmwmfyeozs
```

* UR as QR Code:

![](bcr-2020-006/2.png)

### Cryptographic Seed `crypto-seed`

The type `crypto-seed` contains a single, deterministic length byte string having a length from 1 to 64 bytes. Semantically, this byte string SHOULD be a random or pseudorandom sequence generated by a cryptographically-strong algorithm.

The type may also include a `creation-date` attribute which is the number of days since the Unix epoch upon which this seed was generated. This attribute is tagged with #6.1 in accordance with [CBOR-TAGS].

The type may also include `name`, which SHOULD be a short name for the seed, and `note`, which is an arbitrary amount of text describing the seed.

#### CDDL

```
seed = {
	payload: bytes,
	? creation-date: date,
	? name: text,
	? note: text
}
payload = 1
creation-date = 2
name = 3
note = 4
date = #6.1(int / float) ; epoch-based date/time
```

#### Example/Test Vector

* For a 16 byte (128-bit) seed generated on May 13, 2020, in the CBOR diagnostic notation:

```
{
  1: h'c7098580125e2ab0981253468b2dbc52',
  2: 100(18394)
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A2                                     # map(2)
   01                                  # unsigned(1) payload:
   50                                  # bytes(16)
      C7098580125E2AB0981253468B2DBC52 # payload
   02                                  # unsigned(2) creation-date:
   D8 64                               # tag(100)
      19 47DA                          # unsigned(18394)
```

* As a hex string:

```
A20150C7098580125E2AB0981253468B2DBC5202D8641947DA
```

* As a UR:

```
ur:crypto-seed/oeadgdstaslplabghydrpfmkbggufgludprfgmaotpiecffltnlpqdenos
```

* UR as QR Code:

![](bcr-2020-006/1.png)

#### Seed Fingerprint

The fingerprint of a `crypto-seed` is the SHA-256 hash of the `payload` byte string. For the example test vector above, the payload is:

```
c7098580125e2ab0981253468b2dbc52
```

So the fingerprint would be the SHA-256 hash of those bytes:

```
cc81869bcf9d7295098d03229f3e40fd1d2f42a7e6c4f6c4ec929fdf6eed2c6b
```

When encoded as CBOR (diagnostic notiation):

```
crypto-seed-fingerprint = 600(h'cc81869bcf9d7295098d03229f3e40fd1d2f42a7e6c4f6c4ec929fdf6eed2c6b')
```

Encoded as binary:

```
D9 0258                                 # tag(600)
   58 20                                # bytes(32)
      CC81869BCF9D7295098D03229F3E40FD1D2F42A7E6C4F6C4EC929FDF6EED2C6B
```

### BIP-39 Encoded Seed `crypto-bip39`

The type `crypto-bip39` contains an array of BIP39 words and an optional language specifier [LANG], which if omitted is taken to be `en`.

The authors also considered possibly encoding a BIP39 seed as an array of indexes into the BIP39 dictionary, but this would be redundant with simply sending the seed itself using the `crypto-seed` type above. The purpose of BIP39 is to create a mnemonic sequence, and simply encoding the sequence as a series of indexes adds no value over simply sending the seed itself.

#### CDDL

```
bip39 = {
	words: [+ bip39Word],
	? lang: text
}
words = 1
lang = 2
bip39Word = text
```

#### Example/Test Vector

* A 16 byte (128-bit) seed, encoded as BIP39:

```
shield group erode awake lock sausage cash glare wave crew flame glove
```

* In CBOR diagnostic notation:

```
{
  1: ["shield", "group", "erode", "awake", "lock", "sausage", "cash", "glare", "wave", "crew", "flame", "glove"],
  2: "en"
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A2                      # map(2)
   01                   # unsigned(1) words:
   8C                   # array(12)
      66                # text(6)
         736869656C64   # "shield"
      65                # text(5)
         67726F7570     # "group"
      65                # text(5)
         65726F6465     # "erode"
      65                # text(5)
         6177616B65     # "awake"
      64                # text(4)
         6C6F636B       # "lock"
      67                # text(7)
         73617573616765 # "sausage"
      64                # text(4)
         63617368       # "cash"
      65                # text(5)
         676C617265     # "glare"
      64                # text(4)
         77617665       # "wave"
      64                # text(4)
         63726577       # "crew"
      65                # text(5)
         666C616D65     # "flame"
      65                # text(5)
         676C6F7665     # "glove"
   02                   # unsigned(2) lang:
   62                   # text(2)
      656E              # "en"
```

* As a hex string:

```
A2018C66736869656C646567726F75706565726F6465656177616B65646C6F636B6773617573616765646361736865676C6172656477617665646372657765666C616D6565676C6F76650262656E
```

* As a UR:

```
ur:crypto-bip39/oeadlkiyjkisinihjzieihiojpjlkpjoihihjpjlieihihhskthsjeihiejzjliajeiojkhskpjkhsioihieiahsjkisihiojzhsjpihiekthskoihieiajpihktihiyjzhsjnihihiojzjlkoihaoidihjtrkkndede
```

* UR as QR Code:

![](bcr-2020-006/3.png)

### Partially Signed Bitcoin Transaction (PSBT) `crypto-psbt`

The type `crypto-psbt` contains a single, deterministic length byte string of variable length up to 2^32-1 bytes. Semantically, this byte string MUST be a valid Partially Signed Bitcoin Transaction encoded in the binary format specified by [BIP174].

#### CDDL

```
bytes
```

#### Example/Test Vector

* CBOR diagnostic notation:

```
h'70736274ff01009a020000000258e87a21b56daf0c23be8e7070456c336f7cbaa5c8757924f545887bb2abdd750000000000ffffffff838d0427d0ec650a68aa46bb0b098aea4422c071b2ca78352a077959d07cea1d0100000000ffffffff0270aaf00800000000160014d85c2b71d0060b09c9886aeb815e50991dda124d00e1f5050000000016001400aea9a2e5f0f876a588df5546e8742d1d87008f000000000000000000'
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
58 A7                                   # bytes(167)
70736274FF01009A020000000258E87A21B56DAF0C23BE8E7070456C336F7CBAA5C8757924F545887BB2ABDD750000000000FFFFFFFF838D0427D0EC650A68AA46BB0B098AEA4422C071B2CA78352A077959D07CEA1D0100000000FFFFFFFF0270AAF00800000000160014D85C2B71D0060B09C9886AEB815E50991DDA124D00E1F5050000000016001400AEA9A2E5F0F876A588DF5546E8742D1D87008F000000000000000000
```

* As a hex string:

```
58A770736274FF01009A020000000258E87A21B56DAF0C23BE8E7070456C336F7CBAA5C8757924F545887BB2ABDD750000000000FFFFFFFF838D0427D0EC650A68AA46BB0B098AEA4422C071B2CA78352A077959D07CEA1D0100000000FFFFFFFF0270AAF00800000000160014D85C2B71D0060B09C9886AEB815E50991DDA124D00E1F5050000000016001400AEA9A2E5F0F876A588DF5546E8742D1D87008F000000000000000000
```

* As a UR:

```
ur:crypto-psbt/hdosjojkidjyzmadaenyaoaeaeaeaohdvsknclrejnpebncnrnmnjojofejzeojlkerdonspkpkkdkykfelokgprpyutkpaeaeaeaeaezmzmzmzmlslgaaditiwpihbkispkfgrkbdaslewdfycprtjsprsgksecdratkkhktikewdcaadaeaeaeaezmzmzmzmaojopkwtayaeaeaeaecmaebbtphhdnjstiambdassoloimwmlyhygdnlcatnbggtaevyykahaeaeaeaecmaebbaeplptoevwwtyakoonlourgofgvsjydpcaltaemyaeaeaeaeaeaeaeaeaebkgdcarh
```

* UR as QR Code:

![](bcr-2020-006/6.png)

### COSE Structures `cose-*`

[COSE] specifies CBOR-encoded structures for transmitting signed and/or encrypted objects. This document specifies UR types starting with `cose-` for the various COSE messages in their untagged form.

### Normative References

* [RFC3986] [Uniform Resource Identifier (URI): Generic Syntax](https://tools.ietf.org/html/rfc3986)
* [QRCodeAlphaNum] [QR Codes, Table of Alphanumeric Values](https://www.thonky.com/qr-code-tutorial/alphanumeric-table)
* [BCR5] [BCR-0005: Uniform Resources (UR): Encoding Structured Binary Data for Transport in URIs and QR Codes](bcr-2020-005-ur.md)
* [CDDL] [RFC8610: Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://tools.ietf.org/html/rfc8610)
* [BIP39] [BIP-39: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
* [SLIP39] [SLIP-0039: Shamir's Secret-Sharing for Mnemonic Codes](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)
* [COSE] [RFC8152: CBOR Object Signing and Encryption (COSE)](https://tools.ietf.org/html/rfc8152)
* [CBOR-PLAYGROUND] [CBOR Playground](http://cbor.me)
* [LANG] [List of ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
* [PNG] [PNG (Portable Network Graphics) Specification](https://tools.ietf.org/html/rfc2083)
* [SVG] [Scalable Vector Graphics (SVG) 1.1 (Second Edition)](https://www.w3.org/TR/SVG11/)
* [CBOR-TAGS] [Concise Binary Object Representation (CBOR) Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml)
* [UR] [Uniform Resources (UR)](bcr-0005-ur.md)
* [BIP174] [BIP-174: Partially Signed Bitcoin Transaction Format](https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki)

### Informative References

* [MIME] [Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types](https://tools.ietf.org/html/rfc2046)
