# Bech32 Encoding for Cryptographic Seeds
## BCR-2020-002

**© 2020 Blockchain Commons**

Author: Wolf McNally<br/>
Date: April 22, 2020

### DEPRECATED

The content below is now deprecated and of historical interest only.

---

### Introduction

[BIP173] "Bech32" is a checksummed base32 format, and a standard for native segregated witness output addresses.

A scheme for using Bech32 encoding for generalized cryptographic seeds is proposed. [BIP173] defines not only the syntactical format, but also a segwit version byte that is unnecessary for encoding a simple string of pseudorandom data.

### Specification

For cryptographic seeds, the "human readable part" (HRP) of the Bech32 encoding shall be `seed`. This means that bech32-encoded cryptographic seeds will be recognizable by starting with the characters `seed1` (The HRP + the mandatory numeral `1` divider.)

The payload of the seed shall be a minimum of 1 byte and a maximum of 64 bytes.

The payload of the seed shall be encoded as per [BIP173], leaving out the segwit version byte.

The checksum of the seed shall be calculated as per [Bech32bis].

### Test Vectors

| Length | Hex/Bech32 |
|--------|------------|
| 1 | `ee`<br/>`seed1acu7gj09` |
| 16 | `012f984d5b30831d4a256cdbcc0d5029`<br/>`seed1qyhesn2mxzp36j39dnducr2s9y5fu50r` |
| 32 | `80c35bd93dbbf67cdc046cb6eb2fb8f0fefe4aaefd71b23fe9aa337a5b537e19`<br/>`seed1srp4hkfah0m8ehqydjmwktac7rl0uj4wl4cmy0lf4geh5k6n0cvsj4f3dy` |
| 64 | `a2e77b0f0147801c3cc34c6341716e4fed12005e664820bacf0f6b5eabb1fcfff5ca2bdd1a25dc4f7354df3a430a7bce2d8eb63ae69e7e90a8f689002cae156a`<br/>`seed15tnhkrcpg7qpc0xrf335zutwflk3yqz7veyzpwk0pa44a2a3lnlltj3tm5dzthz0wd2d7wjrpfauutvwkcawd8n7jz50dzgq9jhp26sxcqn82` |

### References

* [BIP173] Pieter Wuille et al, [Base32 address format for native v0-16 witness outputs
](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki)
* [Bech32bis] Pieter Wuille, [Analysis of insertion in Bech32 strings](https://gist.github.com/sipa/a9845b37c1b298a7301c33a04090b2eb)
