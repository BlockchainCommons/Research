# UR Type Definition for BIP44 Accounts

## BCR-2020-015

**© 2020 Blockchain Commons**

Author: Craig Raw<br/>
Date: October 22, 2020<br/>

---

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

This information can be contained in an output descriptor [OD-IN-CORE], which is defined in CBOR with [BCR-2020-010] and represented in UR using the ``ur:crypto-output`` type. 
Using this format, each output descriptor defines a single script type, derivation path and parent fingerprint (``crypto-keypath``) and deterministic key (``crypto-hdkey``).

There is a common need however to share information for multiple script types. 
For example, a user may define the script type on wallet software for which the relevant xpub must be retrieved from a hardware wallet.
This suggests that a number of output descriptors for standardized script types could be packaged into a CBOR data format.
Doing so removes the need for the user to also correctly define the matching script type when exporting from the hardware wallet.
The user would only (optionally) need to specify the account number.
In addition, this would promote standardization in derivation paths between different wallets.

This document specifies a native CBOR encoding for a number of standardized script types along with their common derivations to the account level. 
This encoding can be shared as a Uniform Resource [UR] type `crypto-account` (CBOR tag #6.311) for transmitting account level data.

In the encoding, each script type is represented in an output descriptor. 
These output descriptors are then packaged into an array. 
Note that in order to include the parent fingerprint for each ``crypto-hdkey``, the master fingerprint (which is common to all accounts) is included separately.
The top level packaging is a map of the master fingerprint, and the array of output descriptors.

The following standardized script types may be present in a ``crypto-account`` encoding, shown here with default derivations for Bitcoin mainnet and account #0:

| Script type | Default Derivation |
| ----------- | ---------- |
| P2PKH | ``m/44'/0'/0'`` |
| P2SH-P2WPKH | ``m/49'/0'/0'`` |
| P2WPKH | ``m/84'/0'/0'`` |
| Multisig P2SH | ``m/45'/0'/0'`` |
| Multisig P2SH-P2WSH | ``m/48'/0'/0'/1'`` |
| Multisig P2WSH | ``m/48'/0'/0'/2'`` |

If the software creating the encoding does not support a particular script type it should be omitted.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL].

```
; Output descriptors here are restricted to HD keys at account level key derivations only (no 0/* or 1/* children crypto-keypaths)

output_exp = #6.308(crypto-output)

account = {
    1: uint32, ; Master fingerprint (fingerprint for the master public key as per BIP32)
    2: [+ output-exp] ; Output descriptors for various script types for this account
}
```

### Example/Test Vector

* Defines the #0 account for BTC mainnet for the following BIP39 seed:

```
shield group erode awake lock sausage cash glare wave crew flame glove
```

* In CBOR diagnostic form (note the `crypto-hdkey` `use-info` field is omitted here, include for other networks):

```
{
    1: 934670036, ; master fingerprint (for the master public key)
    2: [ ; array of output descriptors
            403( ; public-key-hash
                303({ ; crypto-hdkey
                    3: h'03eb3e2863911826374de86c231a4b76f0b89dfa174afb78d7f478199884d9dd32', ; key-data
                    4: h'6456a5df2db0f6d9af72b2a1af4b25f45200ed6fcc29c3440b311d4796b70b5b', ; chain-code
                    6: 304({ ; origin: crypto-keypath
                        1: [ ; components
                            44, true, 0, true, 0, true ; 44'/0'/0'
                        ],
                        2: 2583285239 ; parent fingerprint (for the immediate parent to this key in order to reconstruct the xpub)
                    })
                })
            ),
            400( ; script-hash
                404( ; witness-public-key-hash
                    303({ ; crypto-hdkey
                        3: h'02c7e4823730f6ee2cf864e2c352060a88e60b51a84e89e4c8c75ec22590ad6b69', ; key-data
                        4: h'9d2f86043276f9251a4a4f577166a5abeb16b6ec61e226b5b8fa11038bfda42d', ; chain-code
                        6: 304({ ; origin: crypto-keypath
                            1: [ ; components
                                49, true, 0, true, 0, true ; 49'/0'/0'
                            ],
                            2: 2819587291 ; parent fingerprint
                        })
                    })
                )
            ),
            404( ; witness-public-key-hash
                303({ ; crypto-hdkey
                    3: h'03fd433450b6924b4f7efdd5d1ed017d364be95ab2b592dc8bddb3b00c1c24f63f', ; key-data
                    4: h'72ede7334d5acf91c6fda622c205199c595a31f9218ed30792d301d5ee9e3a88', ; chain-code
                    6: 304({ ; origin: crypto-keypath
                        1: [ ; components
                            84, true, 0, true, 0, true ; 84'/0'/0'
                        ],
                        2: 224256471 ; parent fingerprint
                    })
                })
            ),
            400( ; script-hash
                303({ ; crypto-hdkey
                    3: h'03fd05e2404a079f5ba41baae32ce26a4dca86caeffaba40cc2c0d83cb754b5111', ; key-data
                    4: h'82a7aafb63f5206e87c794ecf5f50483e8f3fdecb33832acb85b43c2cbc93f4f', ; chain-code
                    6: 304({ ; origin: crypto-keypath
                        1: [ ; components
                            45, true, 0, true, 0, true ; 45'/0'/0'
                        ],
                        2: 1836147603 ; parent fingerprint
                    })
                })
            ),
            400( ; script-hash
                401( ; witness-script-hash
                    303({ ; crypto-hdkey
                        3: h'032c78ebfcabdac6d735a0820ef8732f2821b4fb84cd5d6b26526938f90c050711', ; key-data
                        4: h'7953efe16a73e5d3f9f2d4c6e49bd88e22093bbd85be5a7e862a4b98a16e0ab6', ; chain-code
                        6: 304({ ; origin: crypto-keypath
                            1: [ ; components
                                48, true, 0, true, 0, true, 1, true ; 48'/0'/0'/1'
                            ],
                            2: 1505139498 ; parent fingerprint
                        })
                    })
                )
            ),
            401( ; witness-script-hash
                303({ ; crypto-hdkey
                    3: h'0260563ee80c26844621b06b74070baf0e23fb76ce439d0237e87502ebbd3ca346', ; key-data
                    4: h'2fa0e41c9dc43dc4518659bfcef935ba8101b57dbc0812805dd983bc1d34b813', ; chain-code
                    6: 304({ ; origin: crypto-keypath
                        1: [ ; components
                            48, true, 0, true, 0, true, 2, true ; 48'/0'/0'/2'
                        ],
                        2: 1505139498 ; parent fingerprint
                    })
                })
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
   86                                   # array(6)
      D9 0193                           # tag(403)
         D9 012F                        # tag(303)
            A3                          # map(3)
               03                       # unsigned(3)
               58 21                    # bytes(33)
                  03EB3E2863911826374DE86C231A4B76F0B89DFA174AFB78D7F478199884D9DD32
               04                       # unsigned(4)
               58 20                    # bytes(32)
                  6456A5DF2DB0F6D9AF72B2A1AF4B25F45200ED6FCC29C3440B311D4796B70B5B
               06                       # unsigned(6)
               D9 0130                  # tag(304)
                  A2                    # map(2)
                     01                 # unsigned(1)
                     86                 # array(6)
                        18 2C           # unsigned(44)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                     02                 # unsigned(2)
                     1A 99F9CDF7        # unsigned(2583285239)
      D9 0190                           # tag(400)
         D9 0194                        # tag(404)
            D9 012F                     # tag(303)
               A3                       # map(3)
                  03                    # unsigned(3)
                  58 21                 # bytes(33)
                     02C7E4823730F6EE2CF864E2C352060A88E60B51A84E89E4C8C75EC22590AD6B69
                  04                    # unsigned(4)
                  58 20                 # bytes(32)
                     9D2F86043276F9251A4A4F577166A5ABEB16B6EC61E226B5B8FA11038BFDA42D
                  06                    # unsigned(6)
                  D9 0130               # tag(304)
                     A2                 # map(2)
                        01              # unsigned(1)
                        86              # array(6)
                           18 31        # unsigned(49)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                        02              # unsigned(2)
                        1A A80F7CDB     # unsigned(2819587291)
      D9 0194                           # tag(404)
         D9 012F                        # tag(303)
            A3                          # map(3)
               03                       # unsigned(3)
               58 21                    # bytes(33)
                  03FD433450B6924B4F7EFDD5D1ED017D364BE95AB2B592DC8BDDB3B00C1C24F63F
               04                       # unsigned(4)
               58 20                    # bytes(32)
                  72EDE7334D5ACF91C6FDA622C205199C595A31F9218ED30792D301D5EE9E3A88
               06                       # unsigned(6)
               D9 0130                  # tag(304)
                  A2                    # map(2)
                     01                 # unsigned(1)
                     86                 # array(6)
                        18 54           # unsigned(84)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                     02                 # unsigned(2)
                     1A 0D5DE1D7        # unsigned(224256471)
      D9 0190                           # tag(400)
         D9 012F                        # tag(303)
            A3                          # map(3)
               03                       # unsigned(3)
               58 21                    # bytes(33)
                  03FD05E2404A079F5BA41BAAE32CE26A4DCA86CAEFFABA40CC2C0D83CB754B5111
               04                       # unsigned(4)
               58 20                    # bytes(32)
                  82A7AAFB63F5206E87C794ECF5F50483E8F3FDECB33832ACB85B43C2CBC93F4F
               06                       # unsigned(6)
               D9 0130                  # tag(304)
                  A2                    # map(2)
                     01                 # unsigned(1)
                     86                 # array(6)
                        18 2D           # unsigned(45)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                     02                 # unsigned(2)
                     1A 6D716393        # unsigned(1836147603)
      D9 0190                           # tag(400)
         D9 0191                        # tag(401)
            D9 012F                     # tag(303)
               A3                       # map(3)
                  03                    # unsigned(3)
                  58 21                 # bytes(33)
                     032C78EBFCABDAC6D735A0820EF8732F2821B4FB84CD5D6B26526938F90C050711
                  04                    # unsigned(4)
                  58 20                 # bytes(32)
                     7953EFE16A73E5D3F9F2D4C6E49BD88E22093BBD85BE5A7E862A4B98A16E0AB6
                  06                    # unsigned(6)
                  D9 0130               # tag(304)
                     A2                 # map(2)
                        01              # unsigned(1)
                        88              # array(8)
                           18 30        # unsigned(48)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           00           # unsigned(0)
                           F5           # primitive(21)
                           01           # unsigned(1)
                           F5           # primitive(21)
                        02              # unsigned(2)
                        1A 59B69B2A     # unsigned(1505139498)
      D9 0191                           # tag(401)
         D9 012F                        # tag(303)
            A3                          # map(3)
               03                       # unsigned(3)
               58 21                    # bytes(33)
                  0260563EE80C26844621B06B74070BAF0E23FB76CE439D0237E87502EBBD3CA346
               04                       # unsigned(4)
               58 20                    # bytes(32)
                  2FA0E41C9DC43DC4518659BFCEF935BA8101B57DBC0812805DD983BC1D34B813
               06                       # unsigned(6)
               D9 0130                  # tag(304)
                  A2                    # map(2)
                     01                 # unsigned(1)
                     88                 # array(8)
                        18 30           # unsigned(48)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                        00              # unsigned(0)
                        F5              # primitive(21)
                        02              # unsigned(2)
                        F5              # primitive(21)
                     02                 # unsigned(2)
                     1A 59B69B2A        # unsigned(1505139498)
   
```

* As a hex string:

```
A2011A37B5EED40286D90193D9012FA303582103EB3E2863911826374DE86C231A4B76F0B89DFA174AFB78D7F478199884D9DD320458206456A5DF2DB0F6D9AF72B2A1AF4B25F45200ED6FCC29C3440B311D4796B70B5B06D90130A20186182CF500F500F5021A99F9CDF7D90190D90194D9012FA303582102C7E4823730F6EE2CF864E2C352060A88E60B51A84E89E4C8C75EC22590AD6B690458209D2F86043276F9251A4A4F577166A5ABEB16B6EC61E226B5B8FA11038BFDA42D06D90130A201861831F500F500F5021AA80F7CDBD90194D9012FA303582103FD433450B6924B4F7EFDD5D1ED017D364BE95AB2B592DC8BDDB3B00C1C24F63F04582072EDE7334D5ACF91C6FDA622C205199C595A31F9218ED30792D301D5EE9E3A8806D90130A201861854F500F500F5021A0D5DE1D7D90190D9012FA303582103FD05E2404A079F5BA41BAAE32CE26A4DCA86CAEFFABA40CC2C0D83CB754B511104582082A7AAFB63F5206E87C794ECF5F50483E8F3FDECB33832ACB85B43C2CBC93F4F06D90130A20186182DF500F500F5021A6D716393D90190D90191D9012FA3035821032C78EBFCABDAC6D735A0820EF8732F2821B4FB84CD5D6B26526938F90C0507110458207953EFE16A73E5D3F9F2D4C6E49BD88E22093BBD85BE5A7E862A4B98A16E0AB606D90130A201881830F500F500F501F5021A59B69B2AD90191D9012FA30358210260563EE80C26844621B06B74070BAF0E23FB76CE439D0237E87502EBBD3CA3460458202FA0E41C9DC43DC4518659BFCEF935BA8101B57DBC0812805DD983BC1D34B81306D90130A201881830F500F500F502F5021A59B69B2A
```

* As a UR:

```
ur:crypto-account/oeadcyemrewytyaolntaadmutaaddlotaxhdclaxwmfmdeiamecsdsemgtvsjzcncygrkowtrontzschgezokstswkkscfmklrtauteyaahdcxiehfonurdppfyntapejpproypegrdawkgmaewejlsfdtsrfybdehcaflmtrlbdhpamtaaddyoeadlncsdwykaeykaeykaocynlytsnyltaadmhtaadmwtaaddlotaxhdclaostvelfemdyynwydwyaievosrgmambklovabdgypdglldvespsthysadamhpmjeinaahdcxntdllnaaeykoytdacygegwhgjsiyonpywmcmrpwphsvodsrerozsbyaxluzcoxdpamtaaddyoeadlncsehykaeykaeykaocypdbskeuytaadmwtaaddlotaxhdclaxzcfxeegdrpmogrgwkbzctlttweadkiengrwlhtprremouoluutqdpfbncedkynfhaahdcxjpwevdeogthttkmeswzcolcpsaahcfnshkhtehytclmnteatmoteadtlwynnftloamtaaddyoeadlncsghykaeykaeykaocybthlvytstaadmhtaaddlotaxhdclaxzcahvofzgeatnehpoxcwpkvldwvoimgtsglnsgwszsrdfzsfdwbtlssbkpgrgybyaahdcxlfospkzoiaykcxjtltstmwwpykykaalsvswfzcwpqdeteypsrohpfxsasbsofhgwamtaaddyoeadlncsdpykaeykaeykaocyjnjsiamutaadmhtaadmetaaddlotaxhdclaxdwkswmztpytnswtsecnblfbayajkdldeclqzzolrsnhljedsgminetytbnahatbyaahdcxkkguwsvyimjkvwteytwztyswvendtpmncpasfrrylprnhtkblndrgrmkoyjtbkrpamtaaddyoeadlocsdyykaeykaeykadykaocyhkrpnddrtaadmetaaddlotaxhdclaohnhffmvsbndslrfgclpfjejyatbdpebacnzokotofxntaoemvskpaowmryfnotfgaahdcxdlnbvecentssfsssgylnhkrstoytecrdlyadrekirfaybglahltalsrfcaeerobwamtaaddyoeadlocsdyykaeykaeykaoykaocyhkrpnddrhngevsry
```

### References
* [BIP44] [Multi-Account Hierarchy for Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
* [BIP32] [Hierarchical Deterministic Wallets](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)
* [OD-IN-CORE] [GitHub: Support for Output Descriptors in Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md)
* [BCR-2020-010] [UR Type Definition for Bitcoin Output Descriptors](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-010-output-desc.md)