# UR Type Definition for Cryptocurrency Addresses

## BCR-0009

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: June 6, 2020<br/>

---

### Introduction

Bitcoin, Ethereum, and other cryptocurrencies use addresses as destinations for funds. Addresses are generated from public keys, which were in turn generated from private keys. Ultimately an address is just a string of bytes, but to facilitate recognition and handling by humans they are encoded as base58 (Bitcoin), bech32 (Bitcoin) or base16 (Ethereum). Encodings such as Bitcoin's include one or more tag characters at the front to help identify the string as an address, e.g., `1` for a Bitcoin P2PKH address or `m` for a Bitcoin testnet address, or `bc1` for a Bitcoin Bech32-encoded address.

This specification defines a UR type `crypto-address` (CBOR tag #6.307) for encoding and transmitting cryptocurrency addresses.

The `info` field of the CBOR type defined herein references the `crypto-coininfo` type defined in [BCR7]. This structure encodes both the type of coin and the network (main or test) the address is to be used with. If the optional `info` field is omitted, its defaults (mainnet Bitcoin address) are assumed.

The `data` field encodes the raw byte string comprising the address.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL].

When used embedded in another CBOR structure, this structure should be tagged #6.307.

```
crypto-address = {
	? info: #6.305(crypto-coininfo),
	? type: address-type,
	data: bytes
}

info = 1
type = 2
data = 3

address-type = p2pkh / p2sh / p2wpkh
p2pkh = 0
p2sh = 1
p2wpkh = 2

; The `type` field MAY be included for Bitcoin (and similar cryptocurrency) addresses, and MUST be ommitted for non-applicable types.

; `data` contains:
;   For addresses of type `p2pkh`, the hash160 of the public key (20 bytes).
;   For addresses of type `p2sh`, the hash160 of the script bytes (20 bytes).
;   For addresses of type `p2wphk`, the sha256 of the script bytes (32 bytes).
;   For ethereum addresses, the last 20 bytes of the keccak256 hash of the public key (20 bytes).
```

### Example/Test Vector 1

* A mainnet Bitcoin address.

```
1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
```

* Decoded

```
$ bx address-decode 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
wrapper
{
    checksum 1802900980
    payload 77bff20c60e522dfaa3350c39b030a5d004e839a
    version 0
}
```

* In the CBOR diagnostic notation:

```
{
	3: h'77bff20c60e522dfaa3350c39b030a5d004e839a' ; data
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A1                                      # map(1)
   03                                   # unsigned(3) ; data
   54                                   # bytes(20)
      77BFF20C60E522DFAA3350C39B030A5D004E839A
```

* As a hex string:

```
A1035477BFF20C60E522DFAA3350C39B030A5D004E839A
```

* As a UR:

```
ur:crypto-address/5yp4gaal7gxxpefzm74rx5xrnvps5hgqf6pe57dgdnk
```

* UR as QR Code:

![](bcr-0009/1.png)

### Example/Test Vector 2

* A testnet Ethereum address.

```
0x81b7E08F65Bdf5648606c89998A9CC8164397647
```

* In the CBOR diagnostic notation:

```
{
	1: 305({ ; info: crypto-coininfo [BCR7]
		1: 60, ; type: coin-type-eth (0x3c) [BCR7]
		2: 1 ; network: testnet-eth-ropsten [BCR7]
	}),
	3: h'81b7e08f65bdf5648606c89998a9cc8164397647' ; data
}
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
A2                                      # map(2)
   01                                   # unsigned(1) info
   D9 0131                              # tag(305) crypto-coininfo
      A2                                # map(2)
         01                             # unsigned(1) type
         18 3C                          # unsigned(60) coin-type-eth
         02                             # unsigned(2) network
         01                             # unsigned(1) testnet-eth-ropsten
   03                                   # unsigned(3) data
   54                                   # bytes(20)
      81B7E08F65BDF5648606C89998A9CC8164397647
```

* As a hex string:

```
A201D90131A201183C0201035481B7E08F65BDF5648606C89998A9CC8164397647
```

* As a UR:

```
ur:crypto-address/5gqajqf35gq3s0qzqyp4fqdhuz8kt004vjrqdjyenz5ueqty89mywpw6mtl
```

* UR as QR Code:

![](bcr-0009/2.png)

### References

* [BTC-ADDRESS] [Bitcoin Wiki: Address](https://en.bitcoin.it/wiki/Address)
* [BCR7] [UR Type Definition for Hierarchical Deterministic (HD) Keys](bcr-0007-hdkey.md)
* [CDDL] [RFC8610: Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://tools.ietf.org/html/rfc8610)
