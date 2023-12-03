# UR Type Definition for Bitcoin Output Descriptors (Version 3)

## BCR-2023-010

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: November 25, 2023<br/>
Revised: November 25, 2023

---

### Introduction

Output descriptors [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md), [[OSD]](https://bitcoinops.org/en/topics/output-script-descriptors/), also called output script descriptors, are a way of specifying Bitcoin payment outputs that can range from a simple address to multisig and segwit using a simple domain-specific language. For more on the motivation for output descriptors, see [[WHY-OD]](https://bitcoin.stackexchange.com/questions/89261/why-does-importmulti-not-support-zpub-and-ypub/89281#89281).

This document specifies a native CBOR encoding for output descriptors, as well as a Uniform Resource [[UR]](bcr-2020-006-urtypes.md) type `output-descriptor` (CBOR tag #6.40308) for transmitting such descriptors.

### Previous Versions

Version 1: [[BCR-2020-010]](bcr-2020-010-output-desc.md) was our first attempt at defining a CBOR schema for output descriptors. It had the advantage of being "pure CBOR" in that it did not rely on the text format of output descriptors. However, as the text format evolved, it became clear that the CBOR schema would need to be updated to keep up, and that this ongoing synchronization effort would be a burden. Version 1 also relied on a number of CBOR tags in a low-numbered range that would be difficult to get assigned by IANA. [[BCR-2020-015]](bcr-2020-015-account.md) that describes BIP44 accounts was also designed to rely on Version 1 output descriptors, and so inherited these problems.

Version 2: [[BCR-2023-007]](bcr-2023-007-envelope-output-desc.md) was our second attempt at defining a CBOR schema for output descriptors. It relies on [[Gordian Envelope]](https://datatracker.ietf.org/doc/draft-mcnally-envelope/) to wrap the text format of output descriptors, and also allows for the inclusion of a name and note. This version did not require any special CBOR tags, and inherits all the advantages of the Envelope container type, but the text format of output descriptors was still required, which is not as compact as a pure CBOR format would be, particularly where Base-58 encoded BIP-32 HD keys was concerned. In addition, some developers expressed concern that the Envelope format was too complex for their needs. While this is debatable, it is true that the Envelope format is not as simple as a pure CBOR format would be.

### Requirements for This Version

After community discussion, we arrived at a set of requirements for this (hopefully final) version 3 of the output descriptor format:

- Pure CBOR, without requiring Gordian Envelope.
- Compact encoding of keys.
- Able to represent all output descriptors that can be represented in the text format.
- Able to adapt to future changes in the text format.
- Supports metadata such as name and note.

### Solutions for This Version

- Encoded using [[Gordian dCBOR]](https://datatracker.ietf.org/doc/draft-mcnally-deterministic-cbor/).
    - dCBOR is a deterministic subset of CBOR, and compatible with existing CBOR implementations.
    - This is also a requirement in our previous CBOR definition documents.
- Uses the text format of output descriptors, but replaces keys with indexed placeholders {`@0`, `@1`, `@2`...}. The CBOR-encoded keys are included in a separate array corresponding to the placeholder indexes.
    - Affords compactness while allowing the text format to evolve without requiring changes to the CBOR format.
    - Using the text format means that the clients of this format still need to be able to parse the text format, but third-party libraries are available for this purpose.
    - Encoding this format may be a bit more challenging because the text format will either need to be output with placeholders, or the keys will need to be extracted from the text format, either by textual manipulation or specialized walking of the AST.
    - The use of placeholders is optional, and indeed the ability to parse or understand the output descriptor textual format are not requirements for writing this format, because complete textual output descriptors can simply be wrapped without using placeholders.
    - However, to read this format the ability to parse placeholders and substitute the decoded keys for them is a requirement.
- Uses Version 2 definitions in `hdkey` [[BCR-2020-007]](bcr-2020-007-hdkey.md), `eckey` [[BCR-2020-008]](bcr-2020-008-eckey.md), and `address` [[BCR-2020-009]](bcr-2020-009-address.md).
    - These definitions replace the CBOR tags used in Version 1 with higher-numbered tags that IANA will assign to us.

### CDDL

The following specification is written in Concise Data Definition Language [[CDDL]](https://tools.ietf.org/html/rfc8610). The semantics and allowable nesting syntax is as described in [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md) except for the extension described below.

This specification introduces an extension to [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md), adding a new descriptor function `cosigner(KEY)`, which can be accepted by the `sh` and `wsh` script functions defined in [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md). The `cosigner(KEY)` is not used to derive ScriptPubKeys directly, but is used as a placeholder to be used when transmitting a single public key representing an account to be used by a party in a multisig transaction.

```
output-descriptor = #6.40308(
    {
        source: text,       ; text descriptor with keys replaced by placeholders
        ? keys: [+key], ; array of keys corresponding to placeholders, omitted if source is a complete text descriptor with no placeholders
        ? name: text,       ; optional user-assigned name
        ? note: text        ; optional user-assigned note
    }
)

source = 1
keys = 2
name = 3
note = 4

key = (
    hd-key /    ; BCR-2020-007
    ec-key /    ; BCR-2020-008
    address     ; BCR-2020-009
)
```

### Cosigner

Following [[BCR-2020-010]](./bcr-2020-010-output-desc.md), this specification extends [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md), adding a new descriptor function `cosigner(KEY)`, which can be accepted by the `sh` and `wsh` script functions defined in [[OD-IN-CORE]](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md). The `cosigner(KEY)` is not used to derive ScriptPubKeys directly, but is used as a placeholder to be used when transmitting a single public key representing an account to be used by a party in a multisig transaction.

### Example/Test Vector 1

The textual format for a P2PK script (70 bytes):

```
pk(03e220e776d811c44075a4a260734445c8967865f5357ba98ead3bc6a6552c36f2)
```

With placeholder replacement for the key:

```
pk(@0)
```

The encoded CBOR:

```
40308(   / output-descriptor /
   {
      1:
      "pk(@0)",
      2:
      [
         40306(   / eckey /
            {
               3:
               h'03e220e776d811c44075a4a260734445c8967865f5357ba98ead3bc6a6552c36f2'
            }
         )
      ]
   }
)
```

Hex-encoded CBOR (54 bytes):

```
d99d74a20166706b284030290281d99d72a103582103e220e776d811c44075a4a260734445c8967865f5357ba98ead3bc6a6552c36f2
```

### Example/Test Vector 2

The textual format for a P2WPKH (native segwit) address (48 bytes):

```
addr(tb1qfm7nmm28m9n7gy3fsfpze8vymds9qwtjwn4w7y)
```

The encoded CBOR:

```
40308(   / output-descriptor /
   {
      1:
      "addr(@0)",
      2:
      [
         40307(   / address /
            {
               1:
               40305(   / coin-info /
                  {2: 1}
               ),
               2:
               2,
               3:
               h'4efd3ded47d967e4122982422c9d84db60503972'
            }
         )
      ]
   }
)
```

Hex-encoded CBOR (51 bytes):

```
d99d74a2016861646472284030290281d99d73a301d99d71a10201020203544efd3ded47d967e4122982422c9d84db60503972
```

### Example/Test Vector 3

The textual format of a P2PKH with a private key in WIF format (57 bytes):

```
pkh(Kxyjdi2KhJMBtPBJia5bmhZFfdMi1YrVYcq41QbnGToa2JXokeAu)
```

The encoded CBOR:

```
40308(   / output-descriptor /
   {
      1:
      "pkh(@0)",
      2:
      [
         40306(   / eckey /
            {
               2:
               true,
               3:
               h'347c4acb73f7bf2268b958230e215986eda87a984959c4ddbd4d62c07de6310e'
            }
         )
      ]
   }
)
```

Hex-encoded CBOR (56 bytes):

```
d99d74a20167706b68284030290281d99d72a202f5035820347c4acb73f7bf2268b958230e215986eda87a984959c4ddbd4d62c07de6310e
```

### Example/Test Vector 4

A descriptor for a 2-of-3 multisig wallet, including the use the `name` field to give it the name "Satoshi's Stash" (448 bytes):

```
wsh(sortedmulti(2,[dc567276/48'/0'/0'/2']xpub6DiYrfRwNnjeX4vHsWMajJVFKrbEEnu8gAW9vDuQzgTWEsEHE16sGWeXXUV1LBWQE1yCTmeprSNcqZ3W74hqVdgDbtYHUv3eM4W2TEUhpan/<0;1>/*,[f245ae38/48'/0'/0'/2']xpub6DnT4E1fT8VxuAZW29avMjr5i99aYTHBp9d7fiLnpL5t4JEprQqPMbTw7k7rh5tZZ2F5g8PJpssqrZoebzBChaiJrmEvWwUTEMAbHsY39Ge/<0;1>/*,[c5d87297/48'/0'/0'/2']xpub6DjrnfAyuonMaboEb3ZQZzhQ2ZEgaKV2r64BFmqymZqJqviLTe1JzMr2X2RfQF892RH7MyYUbcy77R7pPu1P71xoj8cDUMNhAMGYzKR4noZ/<0;1>/*))
```

With placeholder replacements for the keys:

```
wsh(sortedmulti(2,@0,@1,@2))
```

The encoded CBOR with the `hdkey` diagnostic notation omitted for brevity:

```
40308(   / output-descriptor /
    {
        1:
        "wsh(sortedmulti(2,@0,@1,@2))",
        2:
        [
            40303( / hd-key omitted / ),
            40303( / hd-key omitted / ),
            40303( / hd-key omitted / )
        ],
        3:
        "Satoshi's Stash"
    }
)
```

<details><summary>Full diagnostic output:</summary>
<pre><code>40308(   / output-descriptor /
    {
        1:
        "wsh(sortedmulti(2,@0,@1,@2))",
        2:
        [
            40303(   / hdkey /
            {
                3:
                h'021c0b479ecf6e67713ddf0c43b634592f51c037b6f951fb1dc6361a98b1e5735e',
                4:
                h'6b3a4cfb6a45f6305efe6e0e976b5d26ba27f7c344d7fc7abef7be2d06d52dfd',
                6:
                40304(   / keypath /
                    {
                        1:
                        [
                        48,
                        true,
                        0,
                        true,
                        0,
                        true,
                        2,
                        true
                        ],
                        2:
                        3696652918
                    }
                ),
                7:
                40304(   / keypath /
                    {
                        1:
                        [
                        [0, false, 1, false],
                        [],
                        false
                        ]
                    }
                ),
                8:
                418956007
            }
            ),
            40303(   / hdkey /
            {
                3:
                h'0397fcf2274abd243d42d42d3c248608c6d1935efca46138afef43af08e9712896',
                4:
                h'c887c72d9d8ac29cddd5b2b060e8b0239039a149c784abe6079e24445db4aa8a',
                6:
                40304(   / keypath /
                    {
                        1:
                        [
                        48,
                        true,
                        0,
                        true,
                        0,
                        true,
                        2,
                        true
                        ],
                        2:
                        4064652856
                    }
                ),
                7:
                40304(   / keypath /
                    {
                        1:
                        [
                        [0, false, 1, false],
                        [],
                        false
                        ]
                    }
                ),
                8:
                572437920
            }
            ),
            40303(   / hdkey /
            {
                3:
                h'028342f5f7773f6fab374e1c2d3ccdba26bc0933fc4f63828b662b4357e4cc3791',
                4:
                h'5afed56d755c088320ec9bc6acd84d33737b580083759e0a0ff8f26e429e0b77',
                6:
                40304(   / keypath /
                    {
                        1:
                        [
                        48,
                        true,
                        0,
                        true,
                        0,
                        true,
                        2,
                        true
                        ],
                        2:
                        3319296663
                    }
                ),
                7:
                40304(   / keypath /
                    {
                        1:
                        [
                        [0, false, 1, false],
                        [],
                        false
                        ]
                    }
                ),
                8:
                470477062
            }
            )
        ],
        3:
        "Satoshi's Stash"
    }
)</code></pre></details><br/>

Hex-encoded CBOR (405 bytes):

```
d99d74a301781c77736828736f727465646d756c746928322c40302c40312c403229290283d99d6fa5035821021c0b479ecf6e67713ddf0c43b634592f51c037b6f951fb1dc6361a98b1e5735e0458206b3a4cfb6a45f6305efe6e0e976b5d26ba27f7c344d7fc7abef7be2d06d52dfd06d99d70a201881830f500f500f502f5021adc56727607d99d70a101838400f401f480f4081a18f8c2e7d99d6fa50358210397fcf2274abd243d42d42d3c248608c6d1935efca46138afef43af08e9712896045820c887c72d9d8ac29cddd5b2b060e8b0239039a149c784abe6079e24445db4aa8a06d99d70a201881830f500f500f502f5021af245ae3807d99d70a101838400f401f480f4081a221eb5a0d99d6fa5035821028342f5f7773f6fab374e1c2d3ccdba26bc0933fc4f63828b662b4357e4cc37910458205afed56d755c088320ec9bc6acd84d33737b580083759e0a0ff8f26e429e0b7706d99d70a201881830f500f500f502f5021ac5d8729707d99d70a101838400f401f480f4081a1c0ae906036f5361746f7368692773205374617368
```

Note that this encoding is 405 bytes, while the text format is 448 bytes, even without the user-assigned name. [Another proposed special-purpose non-CBOR encoding](https://github.com/BlockchainCommons/Research/issues/135#issuecomment-1789542345) comes in at 396 bytes for this example, so for this example the present CBOR-based encoding is only larger by 9 bytes.
