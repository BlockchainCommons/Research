# UR Type Definition for BIP44 Accounts

## BCR-2020-015

**© 2021 Blockchain Commons**

Author: Craig Raw and Wolf McNally<br/>
Date: October 22, 2020<br/>
Revised: December 6, 2021<br/>

---

### DEPRECATED

The content below is now deprecated but may still be supported for backwards compatibility. It has been superseded by [BCR-2023-019](bcr-2023-019-account-descriptor.md).

### Abstract

This BCR describes a data format that promotes standards-based sharing of [BIP44] account level xpubs and other information, allowing devices to join wallets with little to no user interaction required.

### Motivation

A number of script types for both single and multisig have emerged, each with its own well known derivation path.
Devices (especially hardware wallets) need to share the xpub at the correct derivation path for a particular script type in order to be successfully represented in most wallet software.

In the absence of a standard, the burden of selecting the script type on the device falls to the user, requiring technical knowledge and made more difficult by the often limited display and input capabilities.
For multisig wallets, this choice must be repeated correctly on each device.

More commonly, a proprietary data format is used which bundles the information for several script types into a set, allowing the choice to be made once through the wallet software.
The wallet software can then select the appropriate type from the set provided by the device.
This BCR seeks to establish a standard format for creating this set using output descriptors [OD-IN-CORE] to share BIP44 account level data at standard derivations.

### Introduction

[BIP44] "Multi-Account Hierarchy for Deterministic Wallets" is a widely used standard that defines a standardized hierarchy for deterministic wallets.
It specifies a convention for deriving sets of keys from a master key to allow different wallets to find transaction outputs created with a variety of standard script types.

The standard defines 5 levels in a [BIP32] defined derivation path (later expanded to 6 for some multisig script types)

```
m / purpose' / coin_type' / account' / change / address_index
```

The first two levels define the script type used and the coin/network.
The next level defines a zero-based index for the account.
The penultimate level is either zero or one (receive or change addresses respectively), while the final level is a zero-based index for the keys from which to derive the address.

When sharing details of different wallets (for example to display addresses or create PSBTs), it is usual to export the following details:
 - Script type
 - Fingerprint for the master public key (see [BIP32])
 - Derivation path from the master key to the account level
 - The xpub at that derivation

This information can be contained in an output descriptor [OD-IN-CORE], which is defined in CBOR with [BCR-2020-010] and represented in UR using the `ur:crypto-output` type.
Using this format, each output descriptor defines a single script type, derivation path and parent fingerprint (`crypto-keypath`) and deterministic key (`crypto-hdkey`).

There is a common need however to share information for multiple script types.
For example, a user may define the script type on wallet software for which the relevant xpub must be retrieved from a hardware wallet.
This suggests that a number of output descriptors for standardized script types could be packaged into a CBOR data format.
Doing so removes the need for the user to also correctly define the matching script type when exporting from the hardware wallet.
The user would only (optionally) need to specify the account number.
In addition, this would promote standardization in derivation paths between different wallets.

This document specifies a native CBOR encoding for a number of standardized script types along with their common derivations to the account level.
This encoding can be shared as a Uniform Resource [UR] type `crypto-account` (CBOR tag #6.311) for transmitting account level data.

In the encoding, each script type is represented in an output descriptor, `crypto-output`, which describes the script type and its associated public key information.

In the case of multisig script types, a partial output descriptor is used, which contains the public key information for a single cosigner. This is expressed as an extension to the output descriptor specification [OD-IN-CORE] by adding a new descriptor function `cosigner(KEY)`, which can be accepted by the `sh` and `wsh` script functions defined in [OD-IN-CORE]. The `cosigner(KEY)` is not used to derive ScriptPubKeys directly, but is used as a placeholder to be used when transmitting a single public key representing an account to be used by a party in a multisig transaction. Please see the [crypto-output](bcr-2020-010-output-desc.md#cddl) specification for more details.

The top level packaging of `crypto-account` is a map of the master fingerprint, and the array of output descriptors `crypto-output`.

Since each `crypto-hdkey` embedded within a `crypto-output` may or may not include the master fingerprint, `crypto-account` includes the master fingerprint at its top level. The following resolution rule applies: If the `crypto-hdkey` contains the master fingerprint, then that fingerprint is the source of truth for that key, but if it omits the master fingerprint, then the master fingerprint at the top level of the `crypto-account` structure is the source of truth.

The following standardized script types may be present in a `crypto-account` encoding, shown here with default derivations for Bitcoin mainnet and account #0:

| Script type | Default Derivation |
| ----------- | ---------- |
| P2PKH | `m/44'/0'/0'` |
| P2SH-P2WPKH | `m/49'/0'/0'` |
| P2WPKH | `m/84'/0'/0'` |
| Multisig cosigner P2SH | `m/45'` |
| Multisig cosigner P2SH-P2WSH | `m/48'/0'/0'/1'` |
| Multisig cosigner P2WSH | `m/48'/0'/0'/2'` |
| Single key P2TR | `m/86'/0'/0'` |

If the software creating the encoding does not support a particular script type it should be omitted.
Note that legacy multisig with P2SH does not support different networks or accounts - as per [BIP45] the hardened derivation path is only one level of `m/45'`.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL].

```
; Output descriptors here are restricted to HD keys at account level key derivations only (no 0/* or 1/* children crypto-keypaths)

output_exp = #6.308(crypto-output)

account = {
    master-fingerprint: uint32, ; Master fingerprint (fingerprint for the master public key as per BIP32)
    output-descriptors: [+ output-exp] ; Output descriptors for various script types for this account
}

master-fingerprint = 1
output-descriptors = 2
```

### Example/Test Vector

* Defines the #0 account for BTC mainnet for the following BIP39 seed:

```
shield group erode awake lock sausage cash glare wave crew flame glove
```

The `crypto-account` encodes the following output descriptors as `crypto-output`:

```
pkh([37b5eed4/44'/0'/0']xpub6CnQkivUEH9bSbWVWfDLCtigKKgnSWGaVSRyCbN2QNBJzuvHT1vUQpgSpY1NiVvoeNEuVwk748Cn9G3NtbQB1aGGsEL7aYEnjVWgjj9tefu)
sh(wpkh([37b5eed4/49'/0'/0']xpub6CtR1iF4dZPkEyXDwVf3HE74tSwXNMcHtBzX4gwz2UnPhJ54Jz5unHx2syYCCDkvVUmsmoYTmcaHXe1wJppvct4GMMaN5XAbRk7yGScRSte))
wpkh([37b5eed4/84'/0'/0']xpub6BkU445MSEBXbPjD3g2c2ch6mn8yy1SXXQUM7EwjgYiq6Wt1NDwDZ45npqWcV8uQC5oi2gHuVukoCoZZyT4HKq8EpotPMqGqxdZRuapCQ23)
sh(cosigner([37b5eed4/45']xpub68JFLJTH96GUqC6SoVw5c2qyLSt776PGu5xde8ddVACuPYyarvSL827TbZGavuNbKQ8DG3VP9fCXPhQRBgPrS4MPG3zaZgwAGuPHYvVuY9X))
sh(wsh(cosigner([37b5eed4/48'/0'/0'/1']xpub6EC9f7mLFJQoPaqDJ72Zbv67JWzmpXvCYQSecER9GzkYy5eWLsVLbHnxoAZ8NnnsrjhMLduJo9dG6fNQkmMFL3Qedj2kf5bEy5tptHPApNf)))
wsh(cosigner([37b5eed4/48'/0'/0'/2']xpub6EC9f7mLFJQoRQ6qiTvWQeeYsgtki6fBzSUgWgUtAujEMtAfJSAn3AVS4KrLHRV2hNX77YwNkg4azUzuSwhNGtcq4r2J8bLGMDkrQYHvoed))
tr([37b5eed4/86'/0'/0']xpub6DAvL2L5bgGSpDygSQUDpjwE47saoMk2rSRtYhN7Dma7HvnFLTXNrcSC1AmEN8G2SCD958bUwgc6Bew4sAFa2kqYynF8Rmu6P5jMt2FDPtm)
```

Note that the above output descriptors take 997 bytes to encode as text, while the encoded CBOR for the `crypto-account` that encodes them takes only 776 bytes-- an over 20% savings. Further gains are realized when using the UR format to transmit, including human-friendly text encoding as URIs, error detection, efficiency of QR code encoding, and the ability to break up messages too large to fit into a QR code into a sequence of QR codes using sophisticated "fountain codes."

* In CBOR diagnostic form:

(Note the `crypto-hdkey` `use-info` field is omitted here because it takes on the default value for `asset` and `network`, include for other networks.)

```
{
  1: 934670036, ; master key fingerprint
  2: [ ; array of output descriptors
    308( ; crypto-output
      403( ; public-key-hash
        303({ ; crypto-hdkey
          3: h'03EB3E2863911826374DE86C231A4B76F0B89DFA174AFB78D7F478199884D9DD32', ; key-data
          4: h'6456A5DF2DB0F6D9AF72B2A1AF4B25F45200ED6FCC29C3440B311D4796B70B5B', ; chain-code
          6: 304({ ; origin: crypto-keypath
            1: [44, true, 0, true, 0, true], ; components 44'/0'/0'
            2: 934670036 ; source-fingerprint (master key fingerprint)
          }),
          8: 2583285239 ; parent fingerprint
        })
      )
    ),
    308( ; crypto-output
      400( ; script-hash
        404( ; witness-public-key-hash
          303({ ; crypto-hdkey
            3: h'02C7E4823730F6EE2CF864E2C352060A88E60B51A84E89E4C8C75EC22590AD6B69', ; key-data
            4: h'9D2F86043276F9251A4A4F577166A5ABEB16B6EC61E226B5B8FA11038BFDA42D', ; chain-code
            6: 304({ ; origin: crypto-keypath
              1: [49, true, 0, true, 0, true], ; components 49'/0'/0'
              2: 934670036 ; source-fingerprint (master key fingerprint)
            }),
            8: 2819587291 ; parent fingerprint
          })
        )
      )
    ),
    308( ; crypto-output
      404( ; witness-public-key-hash
        303({ ; crypto-hdkey
          3: h'03FD433450B6924B4F7EFDD5D1ED017D364BE95AB2B592DC8BDDB3B00C1C24F63F', ; key-data
          4: h'72EDE7334D5ACF91C6FDA622C205199C595A31F9218ED30792D301D5EE9E3A88', ; chain-code
          6: 304({ ; origin: crypto-keypath
            1: [84, true, 0, true, 0, true], ; components 84'/0'/0'
            2: 934670036 ; source-fingerprint (master key fingerprint)
          }),
          8: 224256471
        })
      )
    ),
    308( ; crypto-output ; parent fingerprint
      400( ; script-hash
        410( ; cosigner
          303({ ; crypto-hdkey
            3: h'035CCD58B63A2CDC23D0812710603592E7457573211880CB59B1EF012E168E059A', ; key-data
            4: h'88D3299B448F87215D96B0C226235AFC027F9E7DC700284F3E912A34DAEB1A23', ; chain-code
            6: 304({ ; origin: crypto-keypath
              1: [45, true], ; components 45'/0'
              2: 934670036 ; source-fingerprint (master key fingerprint)
            }),
            8: 934670036
          })
        )
      )
    ),
    308( ; crypto-output
      400( ; script-hash
        401( ; witness-script-hash
          410( ; cosigner
            303({ ; crypto-hdkey
              3: h'032C78EBFCABDAC6D735A0820EF8732F2821B4FB84CD5D6B26526938F90C050711', ; key-data
              4: h'7953EFE16A73E5D3F9F2D4C6E49BD88E22093BBD85BE5A7E862A4B98A16E0AB6', ; chain-code
              6: 304({ ; origin: crypto-keypath
                1: [48, true, 0, true, 0, true, 1, true], ; components 48'/0'/0'/1'
                2: 934670036 ; source-fingerprint (master key fingerprint)
              }),
              8: 1505139498 ; parent fingerprint
            })
          )
        )
      )
    ),
    308( ; crypto-output
      401( ; witness-script-hash
        410( ; cosigner
          303({ ; crypto-hdkey
            3: h'0260563EE80C26844621B06B74070BAF0E23FB76CE439D0237E87502EBBD3CA346', ; key-data
            4: h'2FA0E41C9DC43DC4518659BFCEF935BA8101B57DBC0812805DD983BC1D34B813', ; chain-code
            6: 304({ ; origin: crypto-keypath
              1: [48, true, 0, true, 0, true, 2, true], ; components 48'/0'/0'/2'
              2: 934670036 ; source-fingerprint (master key fingerprint)
            }),
            8: 1505139498 ; parent fingerprint
          })
        )
      )
    ),
    308( ; crypto-output
      409( ; taproot
        303({ ; crypto-hdkey
          3: h'02BBB97CF9EFA176B738EFD6EE1D4D0FA391A973394FBC16E4C5E78E536CD14D2D', ; key-data
          4: h'4B4693E1F794206ED1355B838DA24949A92B63D02E58910BF3BD3D9C242281E6', ; chain-code
          6: 304({ ; origin: crypto-keypath
            1: [86, true, 0, true, 0, true], ; components 86'/0'/0'
            2: 934670036 ; source-fingerprint (master key fingerprint)
          }),
          8: 3469149964 ; parent fingerprint
        })
      )
    )
  ]
}
```

* Encoded as a binary using [CBOR-PLAYGROUND]:

```
A2                                      # map(2)
   01                                   # unsigned(1)
   1A 37B5EED4                          # unsigned(934670036)
   02                                   # unsigned(2)
   87                                   # array(7)
      D9 0134                           # tag(308)
         D9 0193                        # tag(403)
            D9 012F                     # tag(303)
               A4                       # map(4)
                  03                    # unsigned(3)
                  58 21                 # bytes(33)
                     03EB3E2863911826374DE86C231A4B76F0B89DFA174AFB78D7F478199884D9DD32
                  04                    # unsigned(4)
                  58 20                 # bytes(32)
                     6456A5DF2DB0F6D9AF72B2A1AF4B25F45200ED6FCC29C3440B311D4796B70B5B
                  06                    # unsigned(6)
                  D9 0130               # tag(304)
                     A2                 # map(2)
                        01              # unsigned(1)
                        86              # array(6)
                           18 2C        # unsigned(44)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                        02              # unsigned(2)
                        1A 37B5EED4     # unsigned(934670036)
                  08                    # unsigned(8)
                  1A 99F9CDF7           # unsigned(2583285239)
      D9 0134                           # tag(308)
         D9 0190                        # tag(400)
            D9 0194                     # tag(404)
               D9 012F                  # tag(303)
                  A4                    # map(4)
                     03                 # unsigned(3)
                     58 21              # bytes(33)
                        02C7E4823730F6EE2CF864E2C352060A88E60B51A84E89E4C8C75EC22590AD6B69
                     04                 # unsigned(4)
                     58 20              # bytes(32)
                        9D2F86043276F9251A4A4F577166A5ABEB16B6EC61E226B5B8FA11038BFDA42D
                     06                 # unsigned(6)
                     D9 0130            # tag(304)
                        A2              # map(2)
                           01           # unsigned(1)
                           86           # array(6)
                              18 31     # unsigned(49)
                              F5        # primitive(21)
                              00        # unsigned(0)
                              F5        # primitive(21)
                              00        # unsigned(0)
                              F5        # primitive(21)
                           02           # unsigned(2)
                           1A 37B5EED4  # unsigned(934670036)
                     08                 # unsigned(8)
                     1A A80F7CDB        # unsigned(2819587291)
      D9 0134                           # tag(308)
         D9 0194                        # tag(404)
            D9 012F                     # tag(303)
               A4                       # map(4)
                  03                    # unsigned(3)
                  58 21                 # bytes(33)
                     03FD433450B6924B4F7EFDD5D1ED017D364BE95AB2B592DC8BDDB3B00C1C24F63F
                  04                    # unsigned(4)
                  58 20                 # bytes(32)
                     72EDE7334D5ACF91C6FDA622C205199C595A31F9218ED30792D301D5EE9E3A88
                  06                    # unsigned(6)
                  D9 0130               # tag(304)
                     A2                 # map(2)
                        01              # unsigned(1)
                        86              # array(6)
                           18 54        # unsigned(84)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                        02              # unsigned(2)
                        1A 37B5EED4     # unsigned(934670036)
                  08                    # unsigned(8)
                  1A 0D5DE1D7           # unsigned(224256471)
      D9 0134                           # tag(308)
         D9 0190                        # tag(400)
            D9 019A                     # tag(410)
               D9 012F                  # tag(303)
                  A4                    # map(4)
                     03                 # unsigned(3)
                     58 21              # bytes(33)
                        035CCD58B63A2CDC23D0812710603592E7457573211880CB59B1EF012E168E059A
                     04                 # unsigned(4)
                     58 20              # bytes(32)
                        88D3299B448F87215D96B0C226235AFC027F9E7DC700284F3E912A34DAEB1A23
                     06                 # unsigned(6)
                     D9 0130            # tag(304)
                        A2              # map(2)
                           01           # unsigned(1)
                           82           # array(2)
                              18 2D     # unsigned(45)
                              F5        # primitive(21)
                           02           # unsigned(2)
                           1A 37B5EED4  # unsigned(934670036)
                     08                 # unsigned(8)
                     1A 37B5EED4        # unsigned(934670036)
      D9 0134                           # tag(308)
         D9 0190                        # tag(400)
            D9 0191                     # tag(401)
               D9 019A                  # tag(410)
                  D9 012F               # tag(303)
                     A4                 # map(4)
                        03              # unsigned(3)
                        58 21           # bytes(33)
                           032C78EBFCABDAC6D735A0820EF8732F2821B4FB84CD5D6B26526938F90C050711
                        04              # unsigned(4)
                        58 20           # bytes(32)
                           7953EFE16A73E5D3F9F2D4C6E49BD88E22093BBD85BE5A7E862A4B98A16E0AB6
                        06              # unsigned(6)
                        D9 0130         # tag(304)
                           A2           # map(2)
                              01        # unsigned(1)
                              88        # array(8)
                                 18 30  # unsigned(48)
                                 F5     # primitive(21)
                                 00     # unsigned(0)
                                 F5     # primitive(21)
                                 00     # unsigned(0)
                                 F5     # primitive(21)
                                 01     # unsigned(1)
                                 F5     # primitive(21)
                              02        # unsigned(2)
                              1A 37B5EED4 # unsigned(934670036)
                        08              # unsigned(8)
                        1A 59B69B2A     # unsigned(1505139498)
      D9 0134                           # tag(308)
         D9 0191                        # tag(401)
            D9 019A                     # tag(410)
               D9 012F                  # tag(303)
                  A4                    # map(4)
                     03                 # unsigned(3)
                     58 21              # bytes(33)
                        0260563EE80C26844621B06B74070BAF0E23FB76CE439D0237E87502EBBD3CA346
                     04                 # unsigned(4)
                     58 20              # bytes(32)
                        2FA0E41C9DC43DC4518659BFCEF935BA8101B57DBC0812805DD983BC1D34B813
                     06                 # unsigned(6)
                     D9 0130            # tag(304)
                        A2              # map(2)
                           01           # unsigned(1)
                           88           # array(8)
                              18 30     # unsigned(48)
                              F5        # primitive(21)
                              00        # unsigned(0)
                              F5        # primitive(21)
                              00        # unsigned(0)
                              F5        # primitive(21)
                              02        # unsigned(2)
                              F5        # primitive(21)
                           02           # unsigned(2)
                           1A 37B5EED4  # unsigned(934670036)
                     08                 # unsigned(8)
                     1A 59B69B2A        # unsigned(1505139498)
      D9 0134                           # tag(308)
         D9 0199                        # tag(409)
            D9 012F                     # tag(303)
               A4                       # map(4)
                  03                    # unsigned(3)
                  58 21                 # bytes(33)
                     02BBB97CF9EFA176B738EFD6EE1D4D0FA391A973394FBC16E4C5E78E536CD14D2D
                  04                    # unsigned(4)
                  58 20                 # bytes(32)
                     4B4693E1F794206ED1355B838DA24949A92B63D02E58910BF3BD3D9C242281E6
                  06                    # unsigned(6)
                  D9 0130               # tag(304)
                     A2                 # map(2)
                        01              # unsigned(1)
                        86              # array(6)
                           18 56        # unsigned(86)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                        02              # unsigned(2)
                        1A 37B5EED4     # unsigned(934670036)
                  08                    # unsigned(8)
                  1A CEC7070C           # unsigned(3469149964)
```

* As a hex string:

```
a2011a37b5eed40287d90134d90193d9012fa403582103eb3e2863911826374de86c231a4b76f0b89dfa174afb78d7f478199884d9dd320458206456a5df2db0f6d9af72b2a1af4b25f45200ed6fcc29c3440b311d4796b70b5b06d90130a20186182cf500f500f5021a37b5eed4081a99f9cdf7d90134d90190d90194d9012fa403582102c7e4823730f6ee2cf864e2c352060a88e60b51a84e89e4c8c75ec22590ad6b690458209d2f86043276f9251a4a4f577166a5abeb16b6ec61e226b5b8fa11038bfda42d06d90130a201861831f500f500f5021a37b5eed4081aa80f7cdbd90134d90194d9012fa403582103fd433450b6924b4f7efdd5d1ed017d364be95ab2b592dc8bddb3b00c1c24f63f04582072ede7334d5acf91c6fda622c205199c595a31f9218ed30792d301d5ee9e3a8806d90130a201861854f500f500f5021a37b5eed4081a0d5de1d7d90134d90190d9019ad9012fa4035821035ccd58b63a2cdc23d0812710603592e7457573211880cb59b1ef012e168e059a04582088d3299b448f87215d96b0c226235afc027f9e7dc700284f3e912a34daeb1a2306d90130a20182182df5021a37b5eed4081a37b5eed4d90134d90190d90191d9019ad9012fa4035821032c78ebfcabdac6d735a0820ef8732f2821b4fb84cd5d6b26526938f90c0507110458207953efe16a73e5d3f9f2d4c6e49bd88e22093bbd85be5a7e862a4b98a16e0ab606d90130a201881830f500f500f501f5021a37b5eed4081a59b69b2ad90134d90191d9019ad9012fa40358210260563ee80c26844621b06b74070baf0e23fb76ce439d0237e87502ebbd3ca3460458202fa0e41c9dc43dc4518659bfcef935ba8101b57dbc0812805dd983bc1d34b81306d90130a201881830f500f500f502f5021a37b5eed4081a59b69b2ad90134d90199d9012fa403582102bbb97cf9efa176b738efd6ee1d4d0fa391a973394fbc16e4c5e78e536cd14d2d0458204b4693e1f794206ed1355b838da24949a92b63d02e58910bf3bd3d9c242281e606d90130a201861856f500f500f5021a37b5eed4081acec7070c
```

* As a UR:

```
ur:crypto-account/oeadcyemrewytyaolttaadeetaadmutaaddloxaxhdclaxwmfmdeiamecsdsemgtvsjzcncygrkowtrontzschgezokstswkkscfmklrtauteyaahdcxiehfonurdppfyntapejpproypegrdawkgmaewejlsfdtsrfybdehcaflmtrlbdhpamtaaddyoeadlncsdwykaeykaeykaocyemrewytyaycynlytsnyltaadeetaadmhtaadmwtaaddloxaxhdclaostvelfemdyynwydwyaievosrgmambklovabdgypdglldvespsthysadamhpmjeinaahdcxntdllnaaeykoytdacygegwhgjsiyonpywmcmrpwphsvodsrerozsbyaxluzcoxdpamtaaddyoeadlncsehykaeykaeykaocyemrewytyaycypdbskeuytaadeetaadmwtaaddloxaxhdclaxzcfxeegdrpmogrgwkbzctlttweadkiengrwlhtprremouoluutqdpfbncedkynfhaahdcxjpwevdeogthttkmeswzcolcpsaahcfnshkhtehytclmnteatmoteadtlwynnftloamtaaddyoeadlncsghykaeykaeykaocyemrewytyaycybthlvytstaadeetaadmhtaadnytaaddloxaxhdclaxhhsnhdrpftdwuocntilydibehnecmovdfekpjkclcslasbhkpawsaddmcmmnahnyaahdcxlotedtndfymyltclhlmtpfsadscnhtztaolbnnkistaedegwfmmedreetnwmcycnamtaaddyoeadlfcsdpykaocyemrewytyaycyemrewytytaadeetaadmhtaadmetaadnytaaddloxaxhdclaxdwkswmztpytnswtsecnblfbayajkdldeclqzzolrsnhljedsgminetytbnahatbyaahdcxkkguwsvyimjkvwteytwztyswvendtpmncpasfrrylprnhtkblndrgrmkoyjtbkrpamtaaddyoeadlocsdyykaeykaeykadykaocyemrewytyaycyhkrpnddrtaadeetaadmetaadnytaaddloxaxhdclaohnhffmvsbndslrfgclpfjejyatbdpebacnzokotofxntaoemvskpaowmryfnotfgaahdcxdlnbvecentssfsssgylnhkrstoytecrdlyadrekirfaybglahltalsrfcaeerobwamtaaddyoeadlocsdyykaeykaeykaoykaocyemrewytyaycyhkrpnddrtaadeetaadnltaaddloxaxhdclaorkrhkeytwsoykorletwstbwycagtbsotmeptjkesgwrfcmveskvdmngujzttgtdpaahdcxgrfgmuvyylmwcxjtttechplslgoegagaptdniatidmhdmebdwfryfsnsdkcplyvaamtaaddyoeadlncshfykaeykaeykaocyemrewytyaycytostatbngmdavolk
```

### References
* [BIP44] [Multi-Account Hierarchy for Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
* [BIP32] [Hierarchical Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
* [OD-IN-CORE] [GitHub: Support for Output Descriptors in Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md)
* [BCR-2020-010] [UR Type Definition for Bitcoin Output Descriptors](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-010-output-desc.md)
* [BIP45] [Structure for Deterministic P2SH Multisignature Wallets](https://github.com/bitcoin/bips/blob/master/bip-0045.mediawiki)
* [BIP48] [Multi-Script Hierarchy for Multi-Sig Wallets](https://github.com/bitcoin/bips/blob/master/bip-0048.mediawiki)
* [BIP86] [Key Derivation for Single Key P2TR Outputs](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki)
