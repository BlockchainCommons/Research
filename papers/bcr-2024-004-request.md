# Gordian Transport Protocol / Envelope Request & Response Implementation Guide 📖

Implementer's guide for the Gordian Transport Protocol, which uses Request & Response Expressions in Gordian Envelope.

## BCR-2024-004

**© 2024 Blockchain Commons**

Authors: Shannon Appelcline, Wolf McNally, Christopher Allen<br/>
Date: February 20, 2024
Revised: March 6, 2024

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Expressions](#2-expressions-the-foundation-of-request--response)
3. [Gordian Transport Protocol](#3-gordian-transport-protocol-wrapping-a-request)
4. [Putting It Together](#4-putting-it-together)
5. [Gordian Sealed Transport Protocol](#5-gordian-sealed-transport-protocol-the-next-step)

## 1. Introduction

[Gordian Envelope](https://developer.blockchaincommons.com/envelope/) includes Request and Response functionality: one device can issue an Envelope requesting certain information or certain actions and then another device can respond to that request with the data. Working together, Requests and Responses form the Gordian Transport Protocol (GTP).

The Gordian Transport Protocol is crucial for enabling interoperability and thus interactions between different members of a digital-asset ecosystem. The two largest use cases for GTP are currently: seed vaults talking to transaction coordinators (for example if Gordian Seed Tool wants to talk to Sparrow); and seed vaults talking to share servers (for example if Gordian Seed Tool wants to talk to Gordian Depo).

**Example Seed Vault (SV) ⇔ Network Coordinator (NC) Interactions**

* **NC Request:** Seed Digest
   * **SV Response:** Specific Seed
* **NC Request:** Key Identifier
   * **SV Reponse:** Specific Key
* **NC Request:** Key-Derivation Path
   * **SV Response:** Specific Key
* **NC Request:** Unsigned PSBT
   * **SV Response:** Signed PSBT

**Example Seed Vault (SV) ⇔ Share Server (SS) Interactions**

* **SV Request:** Share with Receipt
  * **SS Response:** Specific Share
* **SV Request:** Shares
  * **SS Response:** All Shares

A Request/Response system helps to reduce the complexity of these digital tasks. A user may not be able to find a specific seed or to generate a key along an appropriate derivation path without guidance. A Request/Response system provides that guidance to minimize errors and user frustration alike.

A Request/Response system becomes even more important as tasks are combined together for more complex projects. The [multisig self-sovereign scenario](https://github.com/BlockchainCommons/SmartCustody/blob/master/Docs/Scenario-Multisig.md) is one such example. It demonstrates how to safely secure digital assets using keys on two closely held devices. However, it is too complex for more users. A system built on Requests and Responses that told users what to do as part of an interactive process would be more likely to be successful, as is described in [Improving Multisigs with Request/Response](https://github.com/BlockchainCommons/SmartCustody/blob/master/Docs/Scenario-Multisig-RR.md).

## 2. Expressions: The Foundation of Request & Response

Requests and Responses are built atop an Envelope functionality called [Expressions](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-012-envelope-expression.md). Expressions are essentially functions. They take the following form within a Gordian Envelope:

```
«function» [
    ❰parameter❱: argument
    ❰parameter❱: argument
    ...
]
```
The function is the Envelope subject. Envelope assertions then each define a paired parameter and argument for that function.

A function to retrieve a seed looks as follows:
```
«100» [
        ❰200❱: Digest(ffa11a8b)
]
```

The numbers refer to specific functions and specific parameters. They are essentially "known values" for Envelope Expressions. These values are defined in [Format.swift](https://github.com/BlockchainCommons/BCSwiftEnvelope/blob/master/Sources/Envelope/Base/Format.swift) in the [Envelope base code](https://github.com/BlockchainCommons/BCSwiftEnvelope/tree/master/Sources/Envelope/Base).

The function call is tagged with CBOR tag #40006, which defines it as a `ur:function` and the parameter is defined with CBOR tag #40007, which defines it as a `ur:parameter`. This is represented in `envelope-cli` (and in the examples here) with "«»" for `ur:function` and "❰❱" for `ur:parameter`.

The `ur:function` values are as follows:

| # | Function | Expected Response |
|---|----------|-----------------|
| 100 | getSeed | isA: Seed (200) |
| 101 | getKey | isA: PrivateKey (201) AND/OR<br>isA: PublicKey (202) AND/OR<br>isA MasterKey (203) AND/OR<br>isA BIP32Key (500) |
| 102 | signPSBT | isA: PSBT (506) |
| 103 | getOutputDescriptor | isA: OutputDescriptor (507) |

The `ur:parameter` values are as follows:

| # | Parameter |
|----|----------|
| 200 | seedDigest |
| 201 | derivationPath |
| 202 | isPrivate |
| 203 | useInfo |
| 204 | isDerivable |
| 205 | psbt |
| 206 | name |
| 207 | challenge |

The above function to retrieve a seed thus parses as follows:
```
«getSeed» [
        ❰seedDigest❱: Digest(ffa11a8b)
]
```

In other words, that's a Request to send a seed that matches the digest `ffa11a8b...`

### Responding to Expressions

Though Requests contain functions (Expressions), Responses are just standard Envelopes. A response to an Expression MUST contain the requested object as the subject of an Envelope and that subject MUST contain at least one assertion of the form 'isA: [object type]'. It MAY contain other assertions.

Here's an example of a response to the `«getSeed»` Expression for `ffa11a8b`.

```
Bytes(16) [
        1: 200
        11: "Dark Purple Peck Vial"
        507: output-descriptor(Map)
]
```

The subject is the seed, while the three assertions describe the seed. The subjects of those assertions are all [known values](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md) (as is the object of the first assertion). They can be read as follows:

```
Bytes(16) [
        'isA': 'Seed'
        'name': "Dark Purple Peck Vial"
        'outputDescriptor': output-descriptor(Map)
]
```

The `isA` assertion is the required one. The others are optional.

The output descriptor contains a map structure as described in [BCR-2023-010](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-010-output-descriptor.md).

## 3. Gordian Transport Protocol: Wrapping a Request

To turn a inquiry for information into a Request requires wrapping the Expression with a `ur:request` subject.

Creating the subject for a Request requires the following steps:

1. Generate an ["Apparently Random Identifier"](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2022-002-arid.md).
2. Tag it as `ur:arid` (CBOR tag #40012).
3. Tag that as `request` (CBOR tag #40004).

`envelope-cli` will display a Request subject as follows:
```
request(ARID(7b33b86e))
```
The actual CBOR looks like this:
```
40004(40012(
     h'7b33b86e604e3cb5ef9d1675d59c70b6ea7d1f625d062e4d14c4310f2e616cd9'
))
```

Creating the object for a Request requires the following addition steps:

4. Create an assertion with a subject of `body` (known value #100).
5. Make your Expression the object of that assertion.
6. Optionally create a `note` (known value #4) about the Request as an additional assertion.
7. Optionally create other info as additional assertions.

Putting that all together, here's a complete `request` containing the `«getSeed»` function call shown above:

```
request(ARID(7b33b86e)) [
    100: «100» [
        ❰200❱: Digest(ffa11a8b)
    ]
    4: "Seed requested by GeneraWallet with note 'Joe wants a copy of the seed'."
]
```

Here it is with all the known values and function values filled in:

```
request(ARID(7b33b86e)) [
    'body': «getSeed» [
        ❰seedDigest❱: Digest(ffa11a8b)
    ]
    'note': "Seed requested by GeneraWallet with note 'Joe wants a copy of the seed'."
]
```

Digging down instead, here's what the lower-level CBOR of that Request looks like:
```
[

 24(40004(40012(
     h'7b33b86e604e3cb5ef9d1675d59c70b6ea7d1f625d062e4d14c4310f2e616cd9'
   ))),

 {4: 24("Seed requested by GeneraWallet with note 'Joe wants a copy of the seed'.")},

 {100: [
        24(40006(100)),
        {24(40007(200)): 24(40001(
          h'ffa11a8b90954fc89ae625779ca11b8f0227573a2f8b4ed85d96ddf901a72cea'
        ))}
       ]
     }

]
```
Here's a more detailed look at the CBOR for this `request`:
```
/* Array of 3 */

[

 /* #1: request(ARID(7b33b86e)) */

     /* CBOR tag #24 = byte string */
     /* CBOR tag #40004 = request */
     /* CBOR tag #40012 = ur:arid */

 24(40004(40012(
     h'7b33b86e604e3cb5ef9d1675d59c70b6ea7d1f625d062e4d14c4310f2e616cd9'
   ))),


  /* #2: note */

     /* map */
     /* Known Value #4 = note */
     /* CBOR tag #24 = byte string */

 {4: 24("Seed requested by GeneraWallet with note 'Joe wants a copy of the seed'.")},

 /* #3: 'body': «getSeed» */

     /* map */
     /* Known Value #100 = body */

     /* array of 2 */

       /* CBOR tag #24 = bytestring */
       /* CBOR tag #40006 = ur:function */
       /* Function #100 = getSeed */

       /* CBOR tag #24 = bytestring */
       /* CBOR tag #40007 = ur:parameter */
       /* Parameter #200 = seedDigest */

       /* CBOR tag #24 = bytestring */
       /* CBOR tag #40001 = ur:digest */

 {100: [
        24(40006(100)),
        {24(40007(200)): 24(40001(
          h'ffa11a8b90954fc89ae625779ca11b8f0227573a2f8b4ed85d96ddf901a72cea'
        ))}
       ]
     }

]
```
### Responses to GTP Requests

Combining a Request with a Response fully enables the Gordian Transport Protocol (GTP).

To respond to a GTP Request:

1. Create a subject with the _same_ ARID as the Request.
2. Tag it as `ur:arid` (CBOR tag #40012).
3. Tag that as `response` (CBOR tag #40005).
4. Create an object with a 'result' subject (known value #101).
5. Add an object to the 'result' subject containing the Requested data.
6. Create an assertion under the 'result' assertion that contains 'isA:' and the appropriate data type.
7. Add additional assertions with any other metadata desired.

The response to the above request thus look as follows:

```
response(ARID(7b33b86e)) [
    101: Bytes(16) [
        1: 200
        11: "Dark Purple Peck Vial"
        507: output-descriptor(Map)
    ]
]
```

Or:
```
response(ARID(7b33b86e)) [
    'result': Bytes(16) [
        'isA': 'Seed'
        'name': "Dark Purple Peck Vial"
        'outputDescriptor': output-descriptor(Map)
    ]
]
```

### 4. Putting It Together

Here's a full example of GTP using the `request` and `response` examples from above.

```
request(ARID(7b33b86e)) [
    'body': «getSeed» [
        ❰seedDigest❱: Digest(ffa11a8b)
    ]
    'note': "Alias quam ullam qui reprehenderit ad quibusdam in hic occaecati aut ut voluptas dicta eligendi nobis. Molestiae neque voluptatibus et dolor qui quas?"
]
```

```
response(ARID(7b33b86e)) [
    'result': Bytes(16) [
        'isA': 'Seed'
        'name': "Dark Purple Peck Vial"
        'outputDescriptor': output-descriptor(Map)
    ]
]
```

Complete test vectors can be found at [Envelope Request & Response Test Vectors](https://developer.blockchaincommons.com/envelope/request/vectors/).

## 5. Gordian Sealed Transport Protocol: The Next Step

GTP can be further expanded to support the Gordian Sealed Transport Protocol (GSTP), which is fully described in [BCR: 2023-014](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-014-gstp.md).

The larger GSTP protocol includes encryption & signature steps, which are certainly best practices for Requests and Responses, but not required for many GTP scenarios. They grow many important when more sensitive data is being transmitted, which might include seeds, keys, and some of the other data discussed herein. The GSTP was originally designed for use in [Gordian Depo](https://github.com/BlockchainCommons/bc-depo-rust).

The entire GSTP stack can be imagined as follows:

| Stack |
|-------|
| [Gordian Sealed Transport Protocol (GSTP)](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-014-gstp.md) |
| Gordian Transport Protocol |
| [Envelope Expressions](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-012-envelope-expression.md) |
| [Gordian Envelope](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-003-envelope.md) |
| [Uniform Resources (URs)](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md) |
| [Bytewords](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md) |
| [dCBOR](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-002-dcbor.md) |

Of course, as a developer you don't have to worry about much of that if you're using a high-level library such as an [Envelope library](https://developer.blockchaincommons.com/libraries/#envelope-libraries) or even just reading specific, expected values from a bytestream.

## History

**3/6/2024:** Introduced term "Gordian Transport Protocol" for Request/Response process. Differentiated it from "Gordian Sealed Transport Protocol" with new section 5. Added link to [Improving Multisigs with Request/Response](https://github.com/BlockchainCommons/SmartCustody/blob/master/Docs/Scenario-Multisig-RR.md). Otherwise clarified document with small edits.

**2/20/2024:** Initial document.
