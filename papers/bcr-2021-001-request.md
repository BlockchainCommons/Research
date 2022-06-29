# UR Type Definitions for Transactions Between Airgapped Devices

## BCR-2021-001

**© 2021 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Feb 16, 2021

---

### Introduction

Devices that are connected to the Internet can transact with devices having no network connection by using cameras and QR Codes, and the [Uniform Resource (UR) encoding](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md) is specifically designed to facilitate this. Typically an online device (hot wallet) requests data or a service from an offline device (cold wallet). This specification defines a UR type `crypto-request` (CBOR tag #6.312) for encoding such requests, and a corresponding type `crypto-response` (CBOR tag #6.313) for responding to such requests. These are intended to be extensible types, allowing (for example) a request that the offline device return a `crypto-seed` or `crypto-hdkey` matching a particular query, or that the offline device sign and return a PSBT `crypto-psbt`. The offline device responds by returning a `crypto-response` that wraps the requested data.

This specification is intended to be extensible, with existing request types adding new fields, and new request and response types being introduced in the future. Offline devices MUST reject request types they don't recognize, or requests including fields they don't recognize.

### Security Considerations

The user(s) overseeing the transaction SHOULD be given the opportunity to review and approve the request on the offline device before the response is returned to the online device. Therefore as a best practice the offline device SHOULD display the contents of the `crypto-request`, including any correlated data such as seed name, visual hashes, or transaction amounts needed for the user to validate the request, and receive user approval (possibly including authentication) before displaying the QR code containing the `crypto-response` UR.

`crypto-request` MAY include a `description` text field that the offline device SHOULD show the approving user along with data decoded from the request itself. Only the decoded request can be considered authoritative. Other than being displayed by the offline device, information in the `description` field MUST be ignored by the offline device and never used in the composition of the response.

Both `crypto-request` and `crypto-response` objects contain a `transaction-id` field containing a UUID that uniquely identifies the transaction. The online device MUST reject any offered `crypto-response` that does not contain the same `transaction-id` as the `crypto-request` contained.

**Currently Specified Requests:**

Though the `crypto-request` specification is extensible, the following request types are the ones defined in the current CDDL descriptions:

| Type | Tag | Description | Docs | Test Vectors |
| Seed | 500 | Request a seed from a digest | [Guide](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/ur-99-request-response.md#request--response-crypto-seed) | [Seed](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#sample-seed-yinmn-blue), [Digest](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#seed-digest-request-for-yinmn-blue), [Comments](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#seed-digest-request-for-yinmn-blue-with-comment) |
| HDKey | 501 | Request a key from a fingerprint and/or keypath | [Guide](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/ur-99-request-response.md#request--response-crypto-hdkey) | [Keypath](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#requests-for-key-derivations-from-any-seed), [Comments](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#requests-for-key-derivations-from-any-seed-with-comment) |
| PSBT | 502 | Request signature of a PSBT | | [Double Signing](https://github.com/BlockchainCommons/crypto-commons/blob/master/Docs/crypto-request-test-vectors.md#crypto-psbt-requests) |

The following data type specifications are written in Concise Data Definition Language [CDDL](https://tools.ietf.org/html/rfc8610).

### UUIDs

UUIDs in this specification notated `uuid` are CBOR binary strings tagged with #6.37, per the [IANA CBOR Tags Registry](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

```
uuid = #6.37(bstr)
```

### Seeds

Responses to requests for seeds use the `crypto-seed` type defined in [BCR-2020-006](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-006-urtypes.md)

### HDKeys

Requests for HDKeys use the `crypto-keypath` and `crypto-coininfo` types defined in [BCR-2020-007](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-007-hdkey.md). Responses for keys use the `crypto-hdkey` type from the same document.

### PSBTs

Requests for PSBTs use the `crypto-psbt` type defined in [BCR-2020-006](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-006-urtypes.md). Responses use the same type.

### CDDL for Request

When used embedded in another CBOR structure, this structure SHOULD be tagged #6.312.

```
crypto-request = {
	transaction-id: uuid,
	body: request-seed / request-hdkey-derivation / request-psbt-signature,
	? description: text        ; Text to be displayed to the approving user.
}

transaction-id = 1
body = 2
description = 3

;
; Returns the seed matching the requested fingerprint
;
request-seed = #6.500({
	seed-digest: crypto-seed-digest
})

crypto-seed-digest = #6.600(bytes .size 32); The SHA-256 of the seed.

seed-digest = 1

;
; Returns the HDKey matching the provided key path and use-info.
;
request-hdkey-derivation = #6.501({
    is-private: bool ; True if derived key is to be private, false if public
    keypath: crypto-keypath ; MUST include `source-fingerprint`
    ? use-info: crypto-coininfo ; If omitted defaults to `btc` and `mainnet`
    ? is-derivable: bool ; If true (default) derived key MUST contain a chain code
                         ; and can therefore be used to derive further keys.
                         ; If false derived key MAY contain no chain code.
                         ; The generator of the response must decide whether to
                         ; authorize a request for a key with a chain code.
})

is-private = 1
keypath = 2
use-info = 3
is-derivable = 4

;
; Returns the given PSBT with one or more outputs signed.
;
request-psbt-signature = #6.502({
	psbt: crypto-psbt
})

psbt = 1

```

### CDDL for Response

When used embedded in another CBOR structure, this structure SHOULD be tagged #6.313. The body of the response is the requested or transformed object.

```
crypto-response = {
	transaction-id: uuid,
	body: crypto-seed / crypto-hdkey / crypto-psbt ; the returned object MUST be tagged correctly according its type
}

transaction-id = 1
body = 2
```

### Example Request and Response

#### Request For a Seed

* In CBOR diagnostic notation:

```
{
	1: 37(h'3B5414375E3A450B8FE1251CBC2B3FB5') ; transaction-id: 3B541437-5E3A-450B-8FE1-251CBC2B3FB5
	2: 500({ ; body: request-seed
		1: 600(h'e824467caffeaf3bbc3e0ca095e660a9bad80ddb6a919433a37161908b9a3986') ; seed-digest
	}
}
```

* Encoded as binary using [CBOR Playground](http://cbor.me/):

```
A2                                      # map(2)
   01                                   # unsigned(1) transaction-id
   D8 25                                # tag(37) uuid
      50                                # bytes(16)
         3B5414375E3A450B8FE1251CBC2B3FB5
   02                                   # unsigned(2) body
   D9 01F4                              # tag(500) request-seed
      A1                                # map(1)
         01                             # unsigned(1) seed-digest
         D9 0258                        # tag(600) crypto-seed-digest
            58 20                       # bytes(32)
               E824467CAFFEAF3BBC3E0CA095E660A9BAD80DDB6A919433A37161908B9A3986
```

* As hex string:

```
A201D825503B5414375E3A450B8FE1251CBC2B3FB502D901F4A101D902585820E824467CAFFEAF3BBC3E0CA095E660A9BAD80DDB6A919433A37161908B9A3986
```

* As a UR:

```
ur:crypto-request/oeadtpdagdfrghbbemhyftfebdmyvydacerfdnfhreaotaadwkoyadtaaohdhdcxvsdkfgkepezepefrrffmbnnbmdvahnptrdtpbtuyimmemweootjshsmhlunyeslnkiledlmo
```

#### Response with Requested Seed

* In CBOR diagnostic notation:

```
{
	1: 37(h'3B5414375E3A450B8FE1251CBC2B3FB5'), ; transaction-id: 3B541437-5E3A-450B-8FE1-251CBC2B3FB5
	2: 300({ ; body: crypto-seed
		1: h'c7098580125e2ab0981253468b2dbc52', ; payload
		2: 100(18394) ; creation-date
	})
}
```

* Encoded as binary using [CBOR Playground](http://cbor.me/):

```
A2                                      # map(2)
   01                                   # unsigned(1) transaction-id
   D8 25                                # tag(37) uuid
      50                                # bytes(16)
         3B5414375E3A450B8FE1251CBC2B3FB5
   02                                   # unsigned(2) body
   D9 012C                              # tag(300) crypto-seed
      A2                                # map(2)
         01                             # unsigned(1) payload
         50                             # bytes(16)
            C7098580125E2AB0981253468B2DBC52
         02                             # unsigned(2) creation-date
         D8 64                          # tag(100) date
            19 47DA                     # unsigned(18394)
```

* As hex string:

```
A201D825503B5414375E3A450B8FE1251CBC2B3FB502D9012CA20150C7098580125E2AB0981253468B2DBC5202D8641947DA
```

* As a UR:

```
ur:crypto-response/oeadtpdagdfrghbbemhyftfebdmyvydacerfdnfhreaotaaddwoeadgdstaslplabghydrpfmkbggufgludprfgmaotpiecffltnvezsamyn
```
