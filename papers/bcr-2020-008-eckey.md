# UR Type Definition for Elliptic Curve (EC) Keys

## BCR-2020-008

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: June 5, 2020<br/>
Revised: November 25, 2023

---

### Introduction

Elliptical Curve Keys (ECKeys) have numerous uses in cryptocurrencies and elsewhere [EC-Crypto](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography). Like other forms of public key cryptography, EC keys come in two flavors: private and public. Public EC keys come in two flavors, compressed and uncompressed, with compressed being preferred.

The only other variable that needs to be determined to create an EC key is the elliptic curve parameters, with the parameters known as "secp256k1" being the most popular and the ones that Bitcoin is based on.

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type      | CBOR Tag |
| :----------- | :------- |
| ur:eckey     | #6.40306 |

These tags have been registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

This specification defines a UR type `eckey` (CBOR tag #6.40306) for encoding and transmitting EC private and public keys.

**Note:** This specification describes version 2 `eckey` (#6.40306), which differs from version 1 `crypto-eckey` (#6.306) only in the UR type and CBOR tag it uses. Version 1 `crypto-eckey` is deprecated, but may still be supported for backwards compatibility.

### EC Curve Selector

[SEC2-ECPARMS](http://www.secg.org/sec2-v2.pdf) lists 20 sets of parameters for elliptic curve cryptography, and a current invocation of `openssl ecparam -list_curves | wc -l` shows that OpenSSL currently supports 87. The `curve` field below selects which curve is used by the represented key. However, the only value specified in the current version of this document is `0` which represents the curve `secp256k1`.

### Key Data

The required `data` field carries the key data. The length of this field will depend on the curve, whether it is a public or private key, and if it is a public key, whether or not it is represented in compressed format.

For the `secp256k1` curve, the `data` field MUST contain exactly 32 bytes for a private key, or 64 bytes for an uncompressed public key, or 33 bytes (including the 1-byte prefix) for a compressed public key.

The `curve` and `is-private` fields allow a decoder to determine the nature of the key and whether it is supported by the encoder, without having to parse the contents of the `data` field.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL](https://tools.ietf.org/html/rfc8610).

```
tagged-eckey = #6.40306(eckey)

eckey = {
  ? curve: uint .default 0,
  ? is-private: bool .default false,
  data: bytes
}

curve = 1
is-private = 2
data = 3
```

### Example/Test Vector 1

* An EC private key:

```
$ seedtool --count 32
8c05c4b4f3e88840a4f4b5f155cfd69473ea169f3d0431b7a6787a23777f08aa
```

* In the CBOR diagnostic notation:

```
{
	; `curve` is implied to be 0 (secp256k1)
	2: true, ; is-private
	3: h'8c05c4b4f3e88840a4f4b5f155cfd69473ea169f3d0431b7a6787a23777f08aa' ; data
}
```

* Encoded as binary using [CBOR-PLAYGROUND](http://cbor.me):

```
a2                                      # map(2)
   02                                   # unsigned(2) is-private
   f5                                   # primitive(21) true
   03                                   # unsigned(3) data
   58 20                                # bytes(32)
      8c05c4b4f3e88840a4f4b5f155cfd69473ea169f3d0431b7a6787a23777f08aa
```

* As a hex string:

```
a202f50358208c05c4b4f3e88840a4f4b5f155cfd69473ea169f3d0431b7a6787a23777f08aa
```

* As a UR:

```
ur:eckey/oeaoykaxhdcxlkahssqzwfvslofzoxwkrewngotktbmwjkwdcmnefsaaehrlolkskncnktlbaypkrphsmyid
```

* UR as QR Code:

![](bcr-2020-008/1.png)

### Example/Test Vector 2

* Convert the private key above into a public key:

```
$ bx ec-to-public
8c05c4b4f3e88840a4f4b5f155cfd69473ea169f3d0431b7a6787a23777f08aa
^D
03bec5163df25d8703150c3a1804eac7d615bb212b7cc9d7ff937aa8bd1c494b7f
```

* In the CBOR diagnostic notation:

```
{
	3: h'03bec5163df25d8703150c3a1804eac7d615bb212b7cc9d7ff937aa8bd1c494b7f' ; data
}
```

* Encoded as binary using [CBOR-PLAYGROUND](http://cbor.me):

```
a1                                      # map(1)
   03                                   # unsigned(3) data
   58 21                                # bytes(33)
      03bec5163df25d8703150c3a1804eac7d615bb212b7cc9d7ff937aa8bd1c494b7f
```

* As a hex string:

```
a103582103bec5163df25d8703150c3a1804eac7d615bb212b7cc9d7ff937aa8bd1c494b7f
```

* As a UR:

```
ur:eckey/oyaxhdclaxrnskcmfswzhlltaxbzbnftcsaawdsttbbzrkcldnkesotszmmuknpdrycegagrlbemdevtlp
```

* UR as QR Code:

![](bcr-2020-008/2.png)
