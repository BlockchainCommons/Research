# UR Type Definition for Bitcoin Output Descriptors (Version 1)

## BCR-2020-010

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: June 8, 2020<br/>
Revised: November 8, 2021

---

### DEPRECATED: Superseded by Version 3 Output Descriptors

This document has been superseded by [Bitcoin Output Descriptors (Version 3)](bcr-2023-010-output-descriptor.md).

The content below is now deprecated and of historical interest only, but may still be supported for backwards compatibility.

### Introduction

Output descriptors [OD-IN-CORE] [OSD], also called output script descriptors, are a way of specifying Bitcoin payment outputs that can range from a simple address to multisig and segwit using a simple domain-specific language. For more on the motivation for output descriptors, see [WHY-OD].

This document specifies a native CBOR encoding for output descriptors, as well as a Uniform Resource [UR] type `crypto-output` (CBOR tag #6.308) for transmitting such descriptors.

### CDDL

The following specification is written in Concise Data Definition Language [CDDL]. The semantics and allowable nesting syntax is as described in [OD-IN-CORE] except for the extension described below.

This specification introduces an extension to [OD-IN-CORE], adding a new descriptor function `cosigner(KEY)`, which can be accepted by the `sh` and `wsh` script functions defined in [OD-IN-CORE]. The `cosigner(KEY)` is not used to derive ScriptPubKeys directly, but is used as a placeholder to be used when transmitting a single public key representing an account to be used by a party in a multisig transaction. This document defines a corresponding CBOR tag #6.410 to be used when encoding the `cosigner(KEY)` function.

```
key_exp = #6.306(crypto-eckey) / #6.303(crypto-hdkey)

script_exp = (
  script-hash /               ; sh
  witness-script-hash /       ; wsh
  public-key /                ; pk
  public-key-hash /           ; pkh
  witness-public-key-hash /   ; wpkh
  combo /                     ; combo
  multisig /                  ; multi
  sorted-multisig /           ; sortedmulti
  address /                   ; addr
  raw-script /                ; raw
  taproot /                   ; tr
  cosigner                    ; cosigner
)

script-hash = #6.400(script_exp)
witness-script-hash = #6.401(script_exp)
public-key = #6.402(key_exp)
public-key-hash = #6.403(key_exp)
witness-public-key-hash = #6.404(key_exp)
combo = #6.405(key_exp)
multikey = {
	threshold: uint,
	keys: [1* key_exp]
}
multisig = #6.406(multikey)
sorted-multisig = #6.407(multikey)
address = #6.307(crypto-address)
raw-script = #6.408(script-bytes)
taproot = #6.409(script_exp)
cosigner = #6.410(key_exp)

threshold = 1
keys = 2

script-bytes = bytes
```

### Example/Test Vector 1

* Describes a P2PKH output with the specified public key.

```
pkh(02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5)
```

* In the CBOR diagnostic notation:

```
403( ; public-key-hash
	306( ; crypto-eckey
		{
			3: h'02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5' ; data
		}
	)
)
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 0193                                 # tag(403) public-key-hash
   D9 0132                              # tag(306) crypto-eckey
      A1                                # map(1)
         03                             # unsigned(3) data
         58 21                          # bytes(33)
            02C6047F9441ED7D6D3045406E95C07CD85C778E4B8CEF3CA7ABAC09B95C709EE5
```

* As a hex string:

```
d90193d90132a103582102c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
```

* As a UR:

```
ur:crypto-output/taadmutaadeyoyaxhdclaoswaalbmwfpwekijndyfefzjtmdrtketphhktmngrlkwsfnospypsasrhhhjonnvwtsqzwljy
```

### Example/Test Vector 2

* Describes a P2SH-P2WPKH output with the specified public key.

```
sh(wpkh(03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556))
```

* In the CBOR diagnostic notation:

```
400( ; script-hash
	404( ; witness-public-key-hash
		306( ; crypto-eckey
			{
				3: h'03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556' ; data
			}
		)
	)
)
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 0190                                 # tag(400) script-hash
   D9 0194                              # tag(404) witness-public-key-hash
      D9 0132                           # tag(306) crypto-eckey
         A1                             # map(1)
            03                          # unsigned(3) data
            58 21                       # bytes(33)
               03FFF97BD5755EEEA420453A14355235D382F6472F8568A18B2F057A1460297556
```

* As a hex string:

```
d90190d90194d90132a103582103fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556
```

* As a UR:

```
ur:crypto-output/taadmhtaadmwtaadeyoyaxhdclaxzmytkgtlkphywyoxcxfeftbbecgmectelfynfldllpisoyludlahknbbhndtkphfhlehmust
```

### Example/Test Vector 3

* Describes a P2SH 2-of-2 multisig output with keys in the specified order.

```
sh(multi(2,022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01,03acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe))
```

* In the CBOR diagnostic notation:

```
400( ; script-hash
	406({ ; multisig
		1: 2, ; threshold
		2: [ ; keys
			306( ; crypto-eckey
				{
					3: h'022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01' ; data
				}
			),
			306( ; crypto-eckey
				{
					3: h'03acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe' ; data
				}
			)
		]
	})
)
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 0190                                 # tag(400) script-hash
   D9 0196                              # tag(406) multisig
      A2                                # map(2) threshold
         01                             # unsigned(1)
         02                             # unsigned(2) keys
         02                             # unsigned(2)
         82                             # array(2)
            D9 0132                     # tag(306) crypto-eckey
               A1                       # map(1)
                  03                    # unsigned(3) data
                  58 21                 # bytes(33)
                     022F01E5E15CCA351DAFF3843FB70F3C2F0A1BDD05E5AF888A67784EF3E10A2A01
            D9 0132                     # tag(306) crypto-eckey
               A1                       # map(1)
                  03                    # unsigned(3) data
                  58 21                 # bytes(33)
                     03ACD484E2F0C7F65309AD178A9F559ABDE09796974C57E714C35F110DFC27CCBE
```

* As a hex string:

```
d90190d90196a201020282d90132a1035821022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01d90132a103582103acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe
```

* As a UR:

```
ur:crypto-output/taadmhtaadmtoeadaoaolftaadeyoyaxhdclaodladvwvyhhsgeccapewflrfhrlbsfndlbkcwutahvwpeloleioksglwfvybkdradtaadeyoyaxhdclaxpstylrvowtstynguaspmchlenegonyryvtmsmtmsgshgvdbbsrhebybtztdisfrnpfadremh
```

### Example/Test Vector 4

* Describes a set of P2PKH outputs derived from this key by `/1/*`, but additionally specifies that the specified xpub is a child of a master with fingerprint `d34db33f`, and derived using path `44'/0'/0'`.

```
pkh([d34db33f/44'/0'/0']xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL/1/*)
```

Key:

```
04 ; version 4
88b21e ; `xpub`
04 ; depth 4
78412e3a ; parent fingerprint
fffffffe ; child number
637807030d55d01f9a0cb3a7839515d796bd07706386a6eddf06cc29a65a0e29 ; chain code
02d2b36900396c9282fa14628566582f206a5dd0bcc8d5e892611806cafb0301f0 ; key data
7e652001 ; base58 checksum
```

* In the CBOR diagnostic notation:

```
403( ; public-key-hash
	303({ ; crypto-hdkey
		3: h'02d2b36900396c9282fa14628566582f206a5dd0bcc8d5e892611806cafb0301f0', ; key-data
		4: h'637807030d55d01f9a0cb3a7839515d796bd07706386a6eddf06cc29a65a0e29', ; chain-code
		6: 304({ ; origin: crypto-keypath
			1: [ ; components
				44, true, 0, true, 0, true ; 44'/0'/0'
			],
			2: 3545084735, ; source-fingerprint
			3: 4 ; depth
		}),
		7: 304({ ; children: crypto-keypath
			1: [ ; components
				1, false, [], false ; 1/*
			]
		}),
		8: 2017537594 ; parent-fingerprint
	})
)
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 0193                                 # tag(403) public-key-hash
   D9 012F                              # tag(303) crypto-hdkey
      A5                                # map(5)
         03                             # unsigned(3) key-data
         58 21                          # bytes(33)
            02D2B36900396C9282FA14628566582F206A5DD0BCC8D5E892611806CAFB0301F0
         04                             # unsigned(4) chain-code
         58 20                          # bytes(32)
            637807030D55D01F9A0CB3A7839515D796BD07706386A6EDDF06CC29A65A0E29
         06                             # unsigned(6) origin
         D9 0130                        # tag(304) crypto-keypath
            A3                          # map(3)
               01                       # unsigned(1) components
               86                       # array(6)
                  18 2C                 # unsigned(44) child-index
                  F5                    # primitive(21) is-hardened true
                  00                    # unsigned(0) child-index
                  F5                    # primitive(21) is-hardened true
                  00                    # unsigned(0) child-index
                  F5                    # primitive(21) is-hardened true
               02                       # unsigned(2) source-fingerprint
               1A D34DB33F              # unsigned(3545084735)
               03                       # unsigned(3) depth
               04                       # unsigned(4)
         07                             # unsigned(7) children
         D9 0130                        # tag(304) crypto-keypath
            A1                          # map(1)
               01                       # unsigned(1) components
               84                       # array(4)
                  01                    # unsigned(1) child-index
                  F4                    # primitive(20) is-hardened false
                  80                    # array(0) child-index-wildcard
                  F4                    # primitive(20) is-hardened false
         08                             # unsigned(8) parent-fingerprint
         1A 78412E3A                    # unsigned(2017537594)
```

* As a hex string:

```
D90193D9012FA503582102D2B36900396C9282FA14628566582F206A5DD0BCC8D5E892611806CAFB0301F0045820637807030D55D01F9A0CB3A7839515D796BD07706386A6EDDF06CC29A65A0E2906D90130A30186182CF500F500F5021AD34DB33F030407D90130A1018401F480F4081A78412E3A
```

* As a UR:

```
ur:crypto-output/taadmutaaddlonaxhdclaotdqdinaeesjzmolfzsbbidlpiyhddlcximhltirfsptlvsmohscsamsgzoaxadwtaahdcxiaksataxbtgotictnybnqdoslsmdbztsmtryatjoialnolweuramsfdtolhtbadtamtaaddyotadlncsdwykaeykaeykaocytegtqdfhaxaaattaaddyoyadlradwklawkaycyksfpdmftkiiozsfd
```

### Example/Test Vector 5

* Describes a set of 1-of-2 P2WSH multisig outputs where the first multisig key is the 1/0/`i` child of the first specified xpub and the second multisig key is the 0/0/`i` child of the second specified xpub, and `i` is any number in a configurable range.

```
wsh(multi(1,xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB/1/0/*,xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH/0/0/*))
```

key 1:

```
04 ; version 4
88b21e ; `xpub`
00 ; depth 0 == public key of a master key
00000000 ; parent fingerprint
00000000 ; child index
60499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd9689 ; chain code
03cbcaa9c98c877a26977d00825c956a238e8dddfbd322cce4f74b0b5bd6ace4a7 ; key data
e233a252 ; base58 checksum
```

key 2:

```
04 ; version 4
88b21e ; `xpub`
01 ; depth 1
bd16bee5 ; parent fingerprint
00000000 ; child index
f0909affaa7ee7abe5dd4e100598d4dc53cd709d5a5c2cac40e7412f232f7c9c ; chain code
02fc9e5af0ac8d9b3cecfe2a888e2117ba3d089d8585886c9c826b6b22a98d12ea ; key data
44183bfc ; base58 checksum
```

* In the CBOR diagnostic notation:

```
401( ; witness-script-hash
	406({ ; multisig
		1: 1, ; threshold
		2: [ ; keys
			303({ ; crypto-hdkey
				3: h'03cbcaa9c98c877a26977d00825c956a238e8dddfbd322cce4f74b0b5bd6ace4a7', ; key-data
				4: h'60499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd9689', ; chain-code
				6: 304({ ; origin: crypto-keypath
					1: [], ; components
					3: 0 ; depth
				}),
				7: 304({ ; children: crypto-keypath
					1: [ ; components
						1, false, 0, false, [], false ; 1/0/*
					]
				})
			}),
			303({ ; crypto-hdkey
				3: h'02fc9e5af0ac8d9b3cecfe2a888e2117ba3d089d8585886c9c826b6b22a98d12ea', ; key-data
				4: h'f0909affaa7ee7abe5dd4e100598d4dc53cd709d5a5c2cac40e7412f232f7c9c', ; chain-code
				6: 304({ ; origin: crypto-keypath
					1: [ ; components
						0, false
					],
					2: 3172384485 ; source-fingerprint
				}),
				7: 304({ ; children: crypto-keypath
					1: [ ; components
						0, false, 0, false, [], false ; 0/0/*
					]
				})
			})
		]
	})
)
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 0191                                 # tag(401) witness-script-hash
   D9 0196                              # tag(406) multisig
      A2                                # map(2)
         01                             # unsigned(1) threshold
         01                             # unsigned(1)
         02                             # unsigned(2) keys
         82                             # array(2)
            D9 012F                     # tag(303) crypto-hdkey
               A4                       # map(4)
                  03                    # unsigned(3) key-data
                  58 21                 # bytes(33)
                     03CBCAA9C98C877A26977D00825C956A238E8DDDFBD322CCE4F74B0B5BD6ACE4A7
                  04                    # unsigned(4) chain-code
                  58 20                 # bytes(32)
                     60499F801B896D83179A4374AEB7822AAEACEAA0DB1F85EE3E904C4DEFBD9689
                  06                    # unsigned(6) origin
                  D9 0130               # tag(304) crypto-keypath
                     A2                 # map(2)
                        01              # unsigned(1)
                        80              # array(0)
                        03              # unsigned(3) depth
                        00              # unsigned(0)
                  07                    # unsigned(7) children
                  D9 0130               # tag(304) crypto-keypath
                     A1                 # map(1)
                        01              # unsigned(1) components
                        86              # array(6)
                           01           # unsigned(1) child-index
                           F4           # primitive(20) is-hardened: false
                           00           # unsigned(0) child-index
                           F4           # primitive(20) is-hardened: false
                           80           # array(0) child-index-wildcard
                           F4           # primitive(20) is-hardened: false
            D9 012F                     # tag(303) crypto-hdkey
               A4                       # map(4)
                  03                    # unsigned(3) key-data
                  58 21                 # bytes(33)
                     02FC9E5AF0AC8D9B3CECFE2A888E2117BA3D089D8585886C9C826B6B22A98D12EA
                  04                    # unsigned(4) chain-code
                  58 20                 # bytes(32)
                     F0909AFFAA7EE7ABE5DD4E100598D4DC53CD709D5A5C2CAC40E7412F232F7C9C
                  06                    # unsigned(6) origin
                  D9 0130               # tag(304) crypto-keypath
                     A2                 # map(2)
                        01              # unsigned(1) components
                        82              # array(2)
                           00           # unsigned(0) child-index
                           F4           # primitive(20) is-hardened: false
                        02              # unsigned(2) source-fingerprint
                        1A BD16BEE5     # unsigned(3172384485)
                  07                    # unsigned(7) children
                  D9 0130               # tag(304) crypto-keypath
                     A1                 # map(1)
                        01              # unsigned(1) components
                        86              # array(6)
                           00           # unsigned(0) child-index
                           F4           # primitive(20) is-hardened: false
                           00           # unsigned(0) child-index
                           F4           # primitive(20) is-hardened: false
                           80           # array(0) child-index
                           F4           # primitive(20) is-hardened: false
```

* As a hex string:

```
d90191d90196a201010282d9012fa403582103cbcaa9c98c877a26977d00825c956a238e8dddfbd322cce4f74b0b5bd6ace4a704582060499f801b896d83179a4374aeb7822aaeaceaa0db1f85ee3e904c4defbd968906d90130a20180030007d90130a1018601f400f480f4d9012fa403582102fc9e5af0ac8d9b3cecfe2a888e2117ba3d089d8585886c9c826b6b22a98d12ea045820f0909affaa7ee7abe5dd4e100598d4dc53cd709d5a5c2cac40e7412f232f7c9c06d90130a2018200f4021abd16bee507d90130a1018600f400f480f4
```

* As a UR:

```
ur:crypto-output/taadmetaadmtoeadadaolftaaddloxaxhdclaxsbsgptsolkltkndsmskiaelfhhmdimcnmnlgutzotecpsfveylgrbdhptbpsveosaahdcxhnganelacwldjnlschnyfxjyplrllfdrplpswdnbuyctlpwyfmmhgsgtwsrymtldamtaaddyoeadlaaxaeattaaddyoyadlnadwkaewklawktaaddloxaxhdclaoztnnhtwtpslgndfnwpzedrlomnclchrdfsayntlplplojznslfjejecpptlgbgwdaahdcxwtmhnyzmpkkbvdpyvwutglbeahmktyuogusnjonththhdwpsfzvdfpdlcndlkensamtaaddyoeadlfaewkaocyrycmrnvwattaaddyoyadlnaewkaewklawktdbsfttn
```

### References

* [WHY-OD] [StackOverflow answer by Peter Wuille explaining motivation for Output Descriptors](https://bitcoin.stackexchange.com/questions/89261/why-does-importmulti-not-support-zpub-and-ypub/89281#89281)
* [OD-IN-Core] [GitHub: Support for Output Descriptors in Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md)
* [OSD] [Bitcoin Optech: Output Script Descriptors](https://bitcoinops.org/en/topics/output-script-descriptors/)
* [CDDL] [RFC8610: Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://tools.ietf.org/html/rfc8610)
* [UR] [Uniform Resources (UR)](bcr-0005-ur.md)
