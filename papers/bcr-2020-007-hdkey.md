# UR Type Definition for Hierarchical Deterministic (HD) Keys

## BCR-2020-007

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: May 25, 2020<br/>
Revised: November 25, 2023

---

### Introduction

Hierarchical Deterministic Keys (HDKeys) [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) allow an entire tree of keys to be derived from a single master key, which was originally derived from random entropy: a seed. Former specifications [BCR-2020-005](bcr-2020-005-ur.md) [BCR-2020-006](bcr-2020-006-urtypes.md) defined UR types such as `seed` for encoding and transmitting such seeds. This specification defines a UR type `hdkey` (CBOR tag #6.40303) for encoding and transmitting HDKeys; either a master key or a derived key.

This specification also defines and incorporates a separate type `keypath` (CBOR tag #6.40304) that specifies a key derivation path.

This specification also defines and incorporates a separate type `coininfo` (CBOR tag #6.40305) that specifes cryptocurrency information.

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type      | CBOR Tag |
| :----------- | :------- |
| ur:hdkey     | #6.40303 |
| ur:keypath   | #6.40304 |
| ur:coin-info | #6.40305 |

These tags have been registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

**Note:** This specification describes version 2 `hdkey` (#6.40303), which differs from version 1 `crypto-hdkey` (#6.303) only in the UR types and CBOR tags it uses. Version 1 `crypto-hdkey` is deprecated, but may still be supported for backwards compatibility.

### HDKeys

HDKeys encoded according to [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) are represented as a text string, e.g.:

```
xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8
```

[BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) specifies that this result is the serialization of these fields:

> 4 byte: version bytes (mainnet: 0x0488B21E public, 0x0488ADE4 private; testnet: 0x043587CF public, 0x04358394 private)<br/>
> 1 byte: depth: 0x00 for master nodes, 0x01 for level-1 derived keys, ....<br/>
> 4 bytes: the fingerprint of the parent's key (0x00000000 if master key)<br/>
> 4 bytes: child number. This is ser32(i) for i in xi = xpar/i, with xi the key being serialized. (0x00000000 if master key)<br/>
> 32 bytes: the chain code<br/>
> 33 bytes: the public key or private key data (serP(K) for public keys, 0x00 || ser256(k) for private keys)

This serialization is then [BASE58-CHECK](https://en.bitcoin.it/wiki/Base58Check_encoding) encoded, which adds four more bytes at the end as a checksum.

The specification herein can be used in such a way that it is isomorphic with the serialization specified by BIP32. It also includes options that may break isomorphism.

### CDDL for Key Path

The following specification is written in Concise Data Definition Language [CDDL](https://tools.ietf.org/html/rfc8610).

When used embedded in another CBOR structure, this structure should be tagged #6.40304.

```
; Metadata for the complete or partial derivation path of a key.
;
; `source-fingerprint`, if present, is the fingerprint of the
; ancestor key from which the associated key was derived.
;
; If `components` is empty, then `source-fingerprint` MUST be a fingerprint of
; a master key.
;
; `depth`, if present, represents the number of derivation steps in
; the path of the associated key, regardless of whether steps are present in the `components` element
; of this structure.

tagged-keypath = #6.40304(keypath)

keypath = {
    components: [path-component], ; If empty, source-fingerprint MUST be present
    ? source-fingerprint: uint32 .ne 0 ; fingerprint of ancestor key, or master key if components is empty
    ? depth: uint8 ; 0 if this is a public key derived directly from a master key
}

path-component = (
    child-index-component /     ; A single child, possibly hardened
    child-range-component /		; A specific range of children, all possibly hardened
    child-wildcard-component /  ; An inspecific range of children, all possibly hardened
    child-pair-component        ; Used in output descriptors,
                                ; see https://github.com/bitcoin/bitcoin/pull/22838
)

uint32 = uint .size 4
uint31 = uint32 .lt 0x80000000
child-index-component = (child-index, is-hardened)
child-range-component = ([child-index, child-index], is-hardened) ; [low, high] where low < high
child-wildcard-component = ([], is-hardened)
child-pair-component = [
    child-index-component,	; Child to use for external addresses, possibly hardened
    child-index-component	; Child to use for internal addresses, possibly hardened
]

child-index = uint31
is-hardened = bool

components = 1
source-fingerprint = 2
depth = 3
```

### CDDL for Coin Info

The following specification is written in Concise Data Definition Language [CDDL](https://tools.ietf.org/html/rfc8610).

When used embedded in another CBOR structure, this structure should be tagged #6.40305.

```
; Metadata for the type and use of a cryptocurrency

tagged-coininfo = #6.40305(coininfo)

coininfo = {
    ? type: uint31 .default cointype-btc, ; values from [SLIP44](https://github.com/satoshilabs/slips/blob/master/slip-0044.md) with high bit turned off
    ? network: int .default mainnet ; coin-specific identifier for testnet
}

type = 1
network = 2

cointype-btc = 0
cointype-eth = 0x3c

mainnet = 0;
testnet-btc = 1;

; from [ETH-TEST-NETWORKS]
testnet-eth-ropsten = 1;
testnet-eth-kovan = 2;
testnet-eth-rinkeby = 3;
testnet-eth-gorli = 4;
```

### CDDL for HDKey

The following specification is written in Concise Data Definition Language [CDDL](https://tools.ietf.org/html/rfc8610) and includes the `keypath` spec above.

```
tagged-hdkey = #6.40303(hdkey)

; An HD key is either a master key or a derived key.

hdkey = {
    master-key / derived-key
}

; A master key is always private, has no use or derivation information,
; and always includes a chain code.
master-key = (
    is-master: true,
    key-data: key-data-bytes,
    chain-code: chain-code-bytes
)

; A derived key may be private or public, has an optional chain code, and
; may carry additional metadata about its use and derivation.
; To maintain isomorphism with [BIP32] and allow keys to be derived from
; this key `chain-code`, `origin`, and `parent-fingerprint` must be present.
; If `origin` contains only a single derivation step and also contains `source-fingerprint`,
; then `parent-fingerprint` MUST be identical to `source-fingerprint` or may be omitted.
derived-key = (
    ? is-private: bool .default false,     ; true if key is private, false if public
    key-data: key-data-bytes,
    ? chain-code: chain-code-bytes         ; omit if no further keys may be derived from this key
    ? use-info: tagged-coininfo, ; How the key is to be used
    ? origin: tagged-keypath,    ; How the key was derived
    ? children: tagged-keypath,  ; What children should/can be derived from this
    ? parent-fingerprint: uint32 .ne 0,    ; The fingerprint of this key's direct ancestor, per [BIP32]
    ? name: text,                          ; A short name for this key.
    ? note: text                           ; An arbitrary amount of text describing the key.
)

; If the `use-info` field is omitted, defaults (mainnet BTC key) are assumed.
; If `cointype` and `origin` are both present, then per [BIP44], the second path
; component's `child-index` must match `cointype`.

; The `children` field may be used to specify what set of child keys should or can be derived from this key. This may include `child-index-range` or `child-index-wildcard` as its last component. Any components that specify hardened derivation will require the key be private.

is-master = 1
is-private = 2
key-data = 3
chain-code = 4
use-info = 5
origin = 6
children = 7
parent-fingerprint = 8
name = 9
note = 10

uint8 = uint .size 1
key-data-bytes = bytes .size 33
chain-code-bytes = bytes .size 32
```

Schematic for a master key:

```
{
    is-master: true,
    key-data: bytes,
    chain-code: bytes
}
```

Schematic for a derived public testnet Ethereum key that maintains isomorphism with [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) and [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki):

```
{
    key-data: bytes,
    chain-code: bytes,
    use-info: {
        type: cointype-eth,
        network: testnet-eth-ropsten
    },
    origin: {
        source-fingerprint: uint32,
        components: [child-index, is-hardened],
        depth: uint8
    },
    parent-fingerprint: uint32
}
```

Schematic for a derived private mainnet Bitcoin key that maintains isomorphism with [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) and [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki), and that includes the full derivation path of the key per [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki): `m / purpose' / coin_type' / account' / change / address_index`

```
{
    is-private: true,
    key-data: bytes,
    chain-code: bytes,
    origin: {
        source-fingerprint: uint32,
        components: [44, true, 0, true, account, true, change, false, address_index, false]
    },
    parent-fingerprint: uint32
}
```

Schematic for a derived public mainnet Bitcoin key that includes only the key, excludes derivation of child keys, and is NOT isomorphic with [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki).

```
{
    key-data: bytes
}
```

### Example/Test Vector 1

* Test Vector 1 from [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki), a master key:

```
xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
```

* Decoded from Base58 (82 bytes):

```
0488ade4000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d50800e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35e77e9d71
```

* Separated into fields specified in [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki):

```
04 ; version 4
88ade4 ; `xprv`
00 ; depth 0 == master key
00000000 ; parent fingerprint
00000000 ; child number
873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508 ; chain code
00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35 ; key data
e77e9d71 ; base58 checksum
```

* In the CBOR diagnostic notation:

```
{
    1: true, / is-master /
    3: h'00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35', / key-data /
    4: h'873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508' / chain-code /
}
```

* Encoded as binary using [CBOR-PLAYGROUND](http://cbor.me):

```
a3                                      # map(3)
   01                                   # unsigned(1) is-master
   f5                                   # primitive(21) true
   03                                   # unsigned(3) key-data
   58 21                                # bytes(33)
      00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35
   04                                   # unsigned(4) chain-code
   58 20                                # bytes(32)
      873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508
```

* As a hex string (74 bytes):

```
a301f503582100e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35045820873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508
```

* As a UR:

```
ur:hdkey/otadykaxhdclaevswfdmjpfswpwkahcywspsmndwmusoskprbbehetchsnpfcybbmwrhchspfxjeecaahdcxltfszmlyrtdlgmhfcnzcctvwcmkbpsftgonbgauefsehgrqzdmvodizmweemtlaybakiylat
```

* UR as QR Code:

![](bcr-2020-007/1.png)

### Example/Test Vector 2

* Test Vector 2, a bitcoin testnet public key with derivation path `m/44'/1'/1'/0/1`:

```
$ SEED=`seedtool --count 32`
$ echo $SEED
d7074d5bdc46af55655244dd5a9d554d7779442d6f4b5a95c257878020188a64

$ DERIVED_KEY=`bx hd-new $SEED \
  | bx hd-private --index 44 --hard \
  | bx hd-private --index 1 --hard \
  | bx hd-private --index 1 --hard \
  | bx hd-private --index 0 \
  | bx hd-private --index 1 \
  | bx hd-to-public -v 70617039`
$ echo $DERIVED_KEY
tpubDHW3GtnVrTatx38EcygoSf9UhUd9Dx1rht7FAL8unrMo8r2NWhJuYNqDFS7cZFVbDaxJkV94MLZAr86XFPsAPYcoHWJ7sWYsrmHDw5sKQ2K
```

* Decoded from Base58:

```
$ bx base58-decode $DERIVED_KEY
043587cf05e9181cf300000001ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6951d4478
```

* Separated into fields specified in [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki):

```
04 ; version 4
3587cf ; `tpub`
05 ; depth 5
e9181cf3 ; parent fingerprint
00000001 ; child number
ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85 ; chain code
026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6 ; key data
951d4478 ; base58 checksum
```

* In the CBOR diagnostic notation:

```
{
    3: h'026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6', / key-data /
    4: h'ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85', / chain-code /
    5: 40305({ / use-info /
        2: 1 / network: testnet-btc /
    }),
    6: 40304({ / origin /
        1: [44, true, 1, true, 1, true, 0, false, 1, false] / components `m/44'/1'/1'/0/1` /
    }),
    8: 3910671603 / parent-fingerprint /
}
```

* Encoded as binary using [CBOR-PLAYGROUND](http://cbor.me):

```
A5                                      # map(5)
   03                                   # unsigned(3) key-data
   58 21                                # bytes(33)
      026FE2355745BB2DB3630BBC80EF5D58951C963C841F54170BA6E5C12BE7FC12A6
   04                                   # unsigned(4) chain-code
   58 20                                # bytes(32)
      CED155C72456255881793514EDC5BD9447E7F74ABB88C6D6B6480FD016EE8C85
   05                                   # unsigned(5) use-info
   D9 9D71                              # tag(40305) coininfo
      A1                                # map(1)
         02                             # unsigned(2) network
         01                             # unsigned(1) testnet-btc
   06                                   # unsigned(6) origin
   D9 9D70                              # tag(40304) keypath
      A1                                # map(1)
         01                             # unsigned(1) components
         8A                             # array(10)
            18 2C                       # unsigned(44) child-index
            F5                          # primitive(21) is-hardened: true
            01                          # unsigned(1) child-index
            F5                          # primitive(21) is-hardened: true
            01                          # unsigned(1) child-index
            F5                          # primitive(21) is-hardened: true
            00                          # unsigned(0) child-index
            F4                          # primitive(20) is-hardened: false
            01                          # unsigned(1) child-index
            F4                          # primitive(20) is-hardened: false
   08                                   # unsigned(8) parent-fingerprint
   1A E9181CF3                          # unsigned(3910671603)
```

* As a hex string:

```
a5035821026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6045820ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c8505d99d71a1020106d99d70a1018a182cf501f501f500f401f4081ae9181cf3
```

* As a UR:

```
ur:hdkey/onaxhdclaojlvoechgferkdpqdiabdrflawshlhdmdcemtfnlrctghchbdolvwsednvdztbgolaahdcxtottgostdkhfdahdlykkecbbweskrymwflvdylgerkloswtbrpfdbsticmwylklpahtantjsoyaoadamtantjooyadlecsdwykadykadykaewkadwkaycywlcscewfjnkpvllt
```

* UR as QR Code:

```
echo 'ur:hdkey/onaxhdclaojlvoechgferkdpqdiabdrflawshlhdmdcemtfnlrctghchbdolvwsednvdztbgolaahdcxtottgostdkhfdahdlykkecbbweskrymwflvdylgerkloswtbrpfdbsticmwylklpahtantjsoyaoadamtantjooyadlecsdwykadykadykaewkadwkaycywlcscewfjnkpvllt' \
  | tr '[:lower:]' '[:upper:]' \
  | qrencode -o 2.png -l L
```

![](bcr-2020-007/2.png)

#### HDKey Digest Source Specification

When a unique identifier to a `hdkey` is needed, an extract of its fields, called the *digest source* is created and then used as input to the SHA-256 hashing algorithm. The resulting digest can be compared to digests produced the same way to determine whether a key has a particular identity. See [BCR-2021-002: Digests for Digital Objects](bcr-2021-002-digest.md) for more information.

The digest source of a `hdkey` has the following CBOR structure:

```
hdkey-digest-source = [
    hdkey.key-data-bytes, ; key data
    hdkey.chain-code-bytes / null, ; encode `null` if key has no chain code
    coininfo.type ; coin type
    coininfo.network ; network
]
```

Example digest source from Test Vector 2:

```
[
    h'026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6', ; key data
    h'ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85', ; chain code
    0, ; cointype-btc
    1  ; mainnet
]
```

The digest source as binary:

```
84                                      # array(4)
   58 21                                # bytes(33)
      026FE2355745BB2DB3630BBC80EF5D58951C963C841F54170BA6E5C12BE7FC12A6
   58 20                                # bytes(32)
      CED155C72456255881793514EDC5BD9447E7F74ABB88C6D6B6480FD016EE8C85
   00                                   # unsigned(0)
   01                                   # unsigned(1)
```

The digest source as a hex string:

```
845821026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a65820ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c850001
```

The actual digest is the SHA-256 of the digest source:

```
362af3038da7600ad1581c19161c8594aafafc24e5acf1aefc8f7a0bbe366df2
```

The digest is encoded as CBOR field (diagnostic notation) is tagged with #6.40600 per [BCR-2020-006](https://github.com/BlockchainCommons/Research/papers/bcr-2020-006-urtypes.md)#object-fingerprints

```
hdkey-fingerprint = 40600(h'362af3038da7600ad1581c19161c8594aafafc24e5acf1aefc8f7a0bbe366df2')
```
