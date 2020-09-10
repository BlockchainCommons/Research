# UR Type Definition for Hierarchical Deterministic (HD) Keys

## BCR-2020-007

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: May 25, 2020<br/>
Revised: June 25, 2020

---

### Introduction

Hierarchical Deterministic Keys (HDKeys) [BIP32] allow an entire tree of keys to be derived from a single master key, which was originally derived from random entropy: a seed. Former specifications [BCR5] [BCR6] defined UR types such as `crypto-seed` for encoding and transmitting such seeds. This specification defines a UR type `crypto-hdkey` (CBOR tag #6.303) for encoding and transmitting HDKeys; either a master key or a derived key.

This specification also defines and incorporates a separate type `crypto-keypath` (CBOR tag #6.304) that specifies a key derivation path.

This specification also defines and incorporates a separate type `crypto-coininfo` (CBOR tag #6.305) that specifes cryptocurrency information.

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

### CDDL for Key Path

The following specification is written in Concise Data Definition Language [CDDL].

When used embedded in another CBOR structure, this structure should be tagged #6.304.

```
; Metadata for the complete or partial derivation path of a key.
;
; `parent-fingerprint`, if present, is the [BIP32] fingerprint
; of the parent key from which the associated key was derived.
;
; `depth`, if present, represents the number of derivation steps in
; the path of the associated key, even if not present in the `components` element
; of this structure.

crypto-keypath = {
	components: [1* path-component],
	? parent-fingerint: uint32 .ne 0 ; parent fingerprint per [BIP32]
	? depth: uint8 ; 0 if this is a public key derived directly from a master key
}

path-component = (
	child-index / child-index-range / child-index-wildcard-range,
	is-hardened
)

uint32 = uint .size 4
uint31 = uint32 .lt 0x80000000
child-index = uint31
child-index-range = [child-index, child-index] ; low, high
child-index-wildcard = []

is-hardened = bool

components = 1
parent-fingerprint = 2
depth = 3
```

### CDDL for Coin Info

The following specification is written in Concise Data Definition Language [CDDL].

When used embedded in another CBOR structure, this structure should be tagged #6.305.

```
; Metadata for the type and use of a cryptocurrency
crypto-coininfo = {
	? type: uint31 .default cointype-btc, ; values from [SLIP44] with high bit turned off
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

The following specification is written in Concise Data Definition Language [CDDL] and includes the `crypto-keypath` spec above.

```
; An hd-key is either a master key or a derived key.
hd-key = {
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
; this key, `chain-code` must be present.
derived-key = (
	? is-private: bool .default false,   ; true if key is private, false if public
	key-data: key-data-bytes,
	? chain-code: chain-code-bytes       ; omit if no further keys may be derived from this key
	? use-info: #6.305(crypto-coininfo), ; How the key is to be used
	? origin: #6.304(crypto-keypath),    ; How the key was derived
	? children: #6.304(crypto-keypath)   ; What children should/can be derived from this
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

Schematic for a derived public testnet Ethereum key that maintains isomorphism with [BIP32] and [BIP44]:

```
{
	key-data: bytes,
	chain-code: bytes,
	use-info: {
		type: cointype-eth,
		network: testnet-eth-ropsten
	},
	origin: {
		parent-fingerprint: uint32,
		components: [child-index, is-hardened],
		depth: uint8
	}
}
```

Schematic for a derived private mainnet Bitcoin key that maintains isomorphism with [BIP32] and [BIP44], and that includes the full derivation path of the key per [BIP44]: `m / purpose' / coin_type' / account' / change / address_index`

```
{
	is-private: true,
	key-data: bytes,
	chain-code: bytes,
	origin: {
		parent-fingerprint: uint32,
		components: [44, true, 0, true, account, true, change, false, address_index, false]
	}
}
```

Schematic for a derived public mainnet Bitcoin key that includes only the key, excludes derivation of child keys, and is NOT isomorphic with [BIP32].

```
{
	key-data: bytes
}
```

### Example/Test Vector 1

* Test Vector 1 from [BIP32], a master key:

```
xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
```

* Decoded from Base58 (82 bytes):

```
0488ade4000000000000000000873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d50800e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35e77e9d71
```

* Separated into fields specified in [BIP32]:

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
ur:crypto-hdkey/otadykaxhdclaevswfdmjpfswpwkahcywspsmndwmusoskprbbehetchsnpfcybbmwrhchspfxjeecaahdcxlnfszolyrtdlgmhfcnzectvwcmkbpsftgonbgauefsehgrqzdmvodizoweemtlaybakiylat
```

* UR as QR Code:

![](bcr-2020-007/1.png)

### Example/Test Vector 2

* Test Vector 2, a bitcoin testnet public key with derivation path `m/44'/1'/1'/0/1`:

```
$ SEED=`seedtool --count 32`
$ echo $SEED
d7074d5bdc46af55655244dd5a9d554d7779442d6f4b5a95c257878020188a64

$ DERIVED_KEY=`bx hd-new $SEED |\
  bx hd-private --index 44 --hard |\
  bx hd-private --index 1 --hard |\
  bx hd-private --index 1 --hard |\
  bx hd-private --index 0 |\
  bx hd-private --index 1 |\
  bx hd-to-public -v 70617039`
$ echo $DERIVED_KEY
tpubDHW3GtnVrTatx38EcygoSf9UhUd9Dx1rht7FAL8unrMo8r2NWhJuYNqDFS7cZFVbDaxJkV94MLZAr86XFPsAPYcoHWJ7sWYsrmHDw5sKQ2K
```

* Decoded from Base58:

```
$ bx base58-decode $DERIVED_KEY
043587cf05e9181cf300000001ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6951d4478
```

* Separated into fields specified in [BIP32]:

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
	3: h'026fe2355745bb2db3630bbc80ef5d58951c963c841f54170ba6e5c12be7fc12a6', ; key-data
	4: h'ced155c72456255881793514edc5bd9447e7f74abb88c6d6b6480fd016ee8c85', ; chain-code
	5: 305({ ; use-info
		2: 1 ; network: testnet-btc
	}),
	6: 304({ ; origin
		1: [44, true, 1, true, 1, true, 0, false, 1, false], ; components `m/44'/1'/1'/0/1`
		2: 3910671603 ; parent-fingerprint
	})
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A4                                      # map(5)
   03                                   # unsigned(3) key-data
   58 21                                # bytes(33)
      026FE2355745BB2DB3630BBC80EF5D58951C963C841F54170BA6E5C12BE7FC12A6
   04                                   # unsigned(4) chain-code
   58 20                                # bytes(32)
      CED155C72456255881793514EDC5BD9447E7F74ABB88C6D6B6480FD016EE8C85
   05                                   # unsigned(5) use-info
   D9 0131                              # tag(305) crypto-coininfo
      A1                                # map(1)
         02                             # unsigned(2) network
         01                             # unsigned(1) testnet-btc
   06                                   # unsigned(6) origin
   D9 0130                              # tag(304) crypto-keypath
      A2                                # map(2)
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
         02                             # unsigned(2) parent-fingerprint
         1A E9181CF3                    # unsigned(3910671603)
```

* As a hex string:

```
A4035821026FE2355745BB2DB3630BBC80EF5D58951C963C841F54170BA6E5C12BE7FC12A6045820CED155C72456255881793514EDC5BD9447E7F74ABB88C6D6B6480FD016EE8C8505D90131A1020106D90130A2018A182CF501F501F500F401F4021AE9181CF3
```

* As a UR:

```
ur:crypto-hdkey/oxaxhdclaojlvoechgferkdpqdiabdrflawshlhdmdcemtfnlrctghchbdolvwsednvdzcbgolaahdcxtottgostdkhfdahdlykkecbbweskrymwflvdylgerkloswtbrpfdbsticmwylkltahtaadehoyaoadamtaaddyoeadlecsdwykadykadykaewkadwkaocywlcscewfiavorkat
```

* UR as QR Code:

![](bcr-2020-007/2.png)

### Normative References

* [BIP32] [Hierarchical Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
* [BCR5] [Uniform Resources (UR): Encoding Structured Binary Data for Transport in URIs and QR Codes](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md)
* [BCR6] [Registry of Uniform Resource (UR) Types](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-006-urtypes.md)
* [CDDL] [RFC8610: Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://tools.ietf.org/html/rfc8610)
* [BIP44] [Multi-Account Hierarchy for Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
* [SLIP44] [Registered coin types for BIP-0044](https://github.com/satoshilabs/slips/blob/master/slip-0044.md)
* [CBOR-PLAYGROUND] [CBOR Playground](http://cbor.me)
* [BASE58-CHECK] [Base58Check encoding](https://en.bitcoin.it/wiki/Base58Check_encoding)
* [ETH-TESTNETS] [Ethereum Test Networks](https://docs.ethhub.io/using-ethereum/test-networks/)
