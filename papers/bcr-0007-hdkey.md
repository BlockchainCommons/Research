# UR Type Definition for Hierarchical Deterministic (HD) Keys

## BCR-0007

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: May 25, 2020

---

### Introduction

Hierarchical Deterministic Keys (HDKeys) [BIP32] allow an entire tree of keys to be derived from a single master key, which was originally derived from random entropy: a seed. Former specifications [BCR5] [BCR6] defined UR types such as `crypto-seed` for encoding and transmitting such seeds. This specification defines a UR type `crypto-hdkey` for encoding and transmitting HDKeys; either a master key or a derived key.

### HDKeys

HDKeys encoded according to [BIP32] are represented as a text string, e.g.:

```
xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8
```

[BIP32] specifies that this result is the serialization of these fields:

> 4 byte: version bytes (mainnet: 0x0488B21E public, 0x0488ADE4 private; testnet: 0x043587CF public, 0x04358394 private)<br/>
> 1 byte: depth: 0x00 for master nodes, 0x01 for level-1 derived keys, ....<br/>
> 4 bytes: the fingerprint of the parent's key (0x00000000 if master key)<br/>
> 4 bytes: child number. This is ser32(i) for i in xi = xpar/i, with xi the key being serialized. (0x00000000 if master key)<br/>
> 32 bytes: the chain code<br/>
> 33 bytes: the public key or private key data (serP(K) for public keys, 0x00 || ser256(k) for private keys)

This serialization is then [BASE58-CHECK] encoded, which adds four more bytes at the end as a checksum.

The specification herein can be used in such a way that it is isomorphic with the serialization specified by BIP32. It also includes options that may break isomorphism.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL].

```
; An hd-key is either a master key or a derived key.
hd-key = {
	master-key / derived-key
}

; Decoders can always expect that the first field in an hd-key will
; be either `is-master` or `is-public`. The second field will
; always be `key-data`.

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
; this key, `chain-code` must be present.
derived-key = (
	is-public: bool,                  ; false if key is private, true if public
	key-data: key-data-bytes,
	? chain-code: chain-code-bytes    ; omit if no further keys may be derived from this key
	use-info,                         ; metadata on how the key is to be used
	derivation-info,                  ; metadata on how the key was derived
)

; Metadata on how the key is to be used.
; To maintain isomorphism with [BIP32], `is-testnet` must be present.
; To maintain isomorphism with [BIP44], both fields must be present.
use-info = (
	? coin-type: uint31 .default coin-type-btc, ; values from [SLIP44] with high bit turned off
	? is-testnet: bool .default false ; false if key is mainnet, true if testnet
)

; Metadata on how the key was derived.
; To maintain isomorphism with [BIP32], `parent-fingerprint` must be present and
; either `child-info` or `path-info` must be present.
derivation-info = (
	? parent-fingerprint: uint32 .ne 0,  ; parent fingerprint per [BIP32]
	? child-info / path-info             ; only one of `child-info` or `path-info` may be provided
)

; Metadata on the derivation that derived this key, per [BIP32].
child-info = (
	child-number: [1 path-component],    ; an array of exactly 2 elements (child-index, is-hardened)
	depth: uint8 .gt 0                   ; the number of derivations used to derive this key
)

; Metadata on the complete derivation path of this key.
; This is a superset of the information provided in `child-info`:
;   `child-number` is the `child-index` element of the last path component.
;   `depth` is the number of elements in the path divided by two (each path component takes 2 elements.)
path-info = (
	derivation-path: path
)

; If `coin-type` an `path` are both present, then per [BIP44], the second path
; component's `child-index` must match `coin-type`.

is-master = 1
is-public = 2
key-data = 3
chain-code = 4
coin-type = 5
is-testnet = 6
parent-fingerprint = 7
child-number = 8
depth = 9
derivation-path = 10

coin-type-btc = 0
coin-type-eth = 0x3c

uint8 = uint .size 1
uint32 = uint .size 4
uint31 = uint32 .lt 0x80000000
child-index = uint31
key-data-bytes = bytes .size 33
chain-code-bytes = bytes .size 32

path = [1* path-component]
is-hardened = bool

path-component = (
	child-index,
	is-hardened
)
```

Schematic for a master key:

```
{
	is-master: true,
	key-data: bytes,
	chain-code: bytes
}
```

Schematic for a derived public testnet Ethereum key that maintains isomorphism with [BIP32] and [BIP44]:

```
{
	is-public: true,
	key-data: bytes,
	chain-code: bytes,
	coin-type: coin-type-eth,
	is-testnet: true,
	parent-fingerprint: uint32,
	child-number: [child-index, is-hardened],
	depth: uint8
}
```

Schematic for a derived private mainnet Bitcoin key that maintains isomorphism with [BIP32] and [BIP44], and that includes the full derivation path of the key per [BIP44]: `m / purpose' / coin_type' / account' / change / address_index`

```
{
	is-public: false,
	key-data: bytes,
	chain-code: bytes,
	parent-fingerprint: uint32,
	derivation-path: [44, true, 0, true, account, true, change, false, address_index, false]
}
```

Schematic for a derived public mainnet Bitcoin key that includes only the key, excludes derivation of child keys, and is NOT isomorphic with [BIP32].

```
{
	is-public: true,
	key-data: bytes
}
```

### Example/Test Vector 1

Test Vector 1 from [BIP32], a master key:

```
xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
```

Decoded from Base58 (82 bytes):

```
0488ade4000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d50800e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35e77e9d71
```

Separated into fields specified in [BIP32]:

```
0488ade4 ; version `xprv`
00 ; depth 0 == master node
00000000 ; parent fingerprint
00000000 ; child number
873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508 ; chain code
00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35 ; key data
e77e9d71 ; base58 checksum
```

In the CBOR diagnostic notation:

```
{
	1: true, ; is-master
	3: h'00e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35', ; key-data
	4: h'873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508' ; chain-code
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A3                                      # map(3)
   01                                   # unsigned(1) is-master
   F5                                   # primitive(21) true
   03                                   # unsigned(3) key-data
   58 21                                # bytes(33) 
      00E8F32E723DECF4051AEFAC8E2C93C9C5B214313817CDB01A1494B917C8436B35
   04                                   # unsigned(4) chain-code
   58 20                                # bytes(32)
      873DFF81C02F525623FD1FE5167EAC3A55A049DE3D314BB42EE227FFED37D508
```

* As a hex string (74 bytes):

```
A301F503582100E8F32E723DECF4051AEFAC8E2C93C9C5B214313817CDB01A1494B917C8436B35045820873DFF81C02F525623FD1FE5167EAC3A55A049DE3D314BB42EE227FFED37D508
```

* As a UR:

```
ur:crypto-hdkey/5vql2q6cyyqw3uewwg77eaq9rth6er3vj0yutvs5xyup0ndsrg2ffwgheppkkdgytqsgw00ls8qz75jky073legk06kr54dqf80r6v2tkshwyflla5ma2zqwu4mr8
```

* UR as QR Code:

![](bcr-0007/1.png)

### Example/Test Vector 2

Test Vector 2 from [BIP32], a public key with derivation path `m/0/2147483647'/1/2147483646'/2`:

```
xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt
```

Decoded from Base58:

```
0488b21e0531a507b8000000029452b549be8cea3ecb7a84bec10dcfd94afe4d129ebfd3b3cb58eedf394ed271024d902e1a2fc7a8755ab5b694c575fce742c48d9ff192e63df5193e4c7afe1f9ca2198df7
```

Separated into fields specified in [BIP32]:

```
0488b21e ; version `xpub`
05 ; depth 5
31a507b8 ; parent fingerprint
00000002 ; child number
9452b549be8cea3ecb7a84bec10dcfd94afe4d129ebfd3b3cb58eedf394ed271 ; chain code
024d902e1a2fc7a8755ab5b694c575fce742c48d9ff192e63df5193e4c7afe1f9c ; key data
a2198df7 ; base58 checksum
```

In the CBOR diagnostic notation:

```
{
	2: true, ; is-public
	3: h'024d902e1a2fc7a8755ab5b694c575fce742c48d9ff192e63df5193e4c7afe1f9c', ; key-data
	4: h'9452b549be8cea3ecb7a84bec10dcfd94afe4d129ebfd3b3cb58eedf394ed271', ; chain-code
	7: 832899000, ; parent-fingerprint
	10: [0, false, 2147483647, true, 1, false, 2147483646, true, 2, false] ; derivation-path
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A5                                      # map(5)
   02                                   # unsigned(2) is-public
   F5                                   # primitive(21) true
   03                                   # unsigned(3) key-data
   58 21                                # bytes(33)
      024D902E1A2FC7A8755AB5B694C575FCE742C48D9FF192E63DF5193E4C7AFE1F9C
   04                                   # unsigned(4) chain-code
   58 20                                # bytes(32)
      9452B549BE8CEA3ECB7A84BEC10DCFD94AFE4D129EBFD3B3CB58EEDF394ED271
   07                                   # unsigned(7) parent-fingerprint
   1A 31A507B8                          # unsigned(832899000)
   0A                                   # unsigned(10) derivation-path
   8A                                   # array(10)
      00                                # unsigned(0) child-index
      F4                                # primitive(20) is-hardened
      1A 7FFFFFFF                       # unsigned(2147483647) child-index
      F5                                # primitive(21) is-hardened
      01                                # unsigned(1) child-index
      F4                                # primitive(20) is-hardened
      1A 7FFFFFFE                       # unsigned(2147483646) child-index
      F5                                # primitive(21) is-hardened
      02                                # unsigned(2) child-index
      F4                                # primitive(20) is-hardened
```

* As a hex string:

```
A502F5035821024D902E1A2FC7A8755AB5B694C575FCE742C48D9FF192E63DF5193E4C7AFE1F9C0458209452B549BE8CEA3ECB7A84BEC10DCFD94AFE4D129EBFD3B3CB58EEDF394ED271071A31A507B80A8A00F41A7FFFFFFFF501F41A7FFFFFFEF502F4
```

* As a UR:

```
ur:crypto-hdkey/55p02q6cyypymypwrghu02r4t26md9x9wh7wwsky3k0lryhx8h63j0jv0tlpl8qytqsfg544fxlge637edagf0kpph8ajjh7f5ffa07nk0943mkl898dyug8rgc62pacp29qpaq60llllll4q86p5llllll02qh59t9khw
```

* UR as QR Code:

![](bcr-0007/2.png)

### Normative References

* [BIP32] [Hierarchical Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
* [BCR5] [Uniform Resources (UR): Encoding Structured Binary Data for Transport in URIs and QR Codes](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-0005-ur.md)
* [BCR6] [Registry of Uniform Resource (UR) Types](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-0006-urtypes.md)
* [CDDL] [RFC8610: Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://tools.ietf.org/html/rfc8610)
* [BIP44] [Multi-Account Hierarchy for Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
* [SLIP44] [Registered coin types for BIP-0044](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)
* [CBOR-PLAYGROUND] [CBOR Playground](http://cbor.me)
* [BASE58-CHECK] [Base58Check encoding](https://en.bitcoin.it/wiki/Base58Check_encoding)