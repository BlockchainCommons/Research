# CID: Common Identifier

## BCR-2022-002

**© 2022 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen, Shannon Applecline<br/>
Date: Aug 10, 2022

---

## Introduction

Information systems use many kinds of identifiers for many purposes. The main purpose of an identifier is to uniquely point to an object, or *referent*, within a given domain. An identifier that is *universally* unique can be associated to any object or concept in all of existence and be relied on to be unique because it contains sufficient entropy (randomness) to ensure that it will, for every conceivable practical purpose, *never* collide with another such identifier.

## Survey

Universally unique identifers have precedent in (for example) [UUIDs](https://en.wikipedia.org/wiki/Universally_unique_identifier), [URIs](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier), and cryptographic digests.

### UUIDs

UUIDs are 128 bits in length and come in several different versions. Each version specifies several bitfields and their semantics. Version 4 is specified to be random, but is still not completely random because it does not specify that cryptographically strong randoness is always be used, and it reserves a 7 bits to identify it *as* a version 4 UUID, leaving 121 bits of actual randomness.

### URIs

URIs are (more or less) human readable text, and the specification of URIs usually focuses on human understandable semantics and are frequently hierarchical, starting with the `scheme` field, which describes a namespace within which the remainder of the URI is considered to point to a referent.

### Digests

A cryptographic hash algorithm such as SHA256 or BLAKE3 maps a block of data of arbitrary size to a fixed-length "digest." This digest reveals nothing about the source image by itself, but can only be computed by applying the same algorithm to the same image. A digest can thereby be considered a "pointer" to a particular binary referent.

## Introducing the CID

We propose herein a standard for a cryptographically strong, univerally unique identifier known as a Common Identifier, or CID.

The goals for this form of identifier are:

* Non-correlatability
* Neutral semantics
* Open generation
* Minimum strength
* Cryptographic suitability

## Non-Correlatability

To be a CID, the sequence of bits that comprise it MUST NOT be correlatable with its referent, nor any other CID. Therefore, it cannot be a hash or digest of another object.

The sequence of bits in a CID MUST be statistically indistinguishable from pure entropy. Therefore one method of generating a CID is to use a cryptographically strong random number generator.

However, the source of entropy for a CID does not itself have to actually be random; it simply has to be indistinguishable from randomness without additional hidden information. One example would be when a sequence of CIDs are generated from a ratcheting key generation algorithm. Knowing the current state of the ratchet and correct CID would give one the ability to ratchet the key to the next state and generate the next CID in the sequence. A third-party observer would be unable to correlate the next CID with the previous CID without access to the secret ratchet state.

## Neutral Semantics

Existing identifers frequently contain inherent type information (UUID version 4 identifies itself as such) and frequently specify the type of referent (URIs specify the `scheme` and often specify a referent type (such as `.jpg` in their path.)

CIDs (as such) contain no type information. Statistically, they are uniformly random sequences of bits. If you merely encoded a CID as a sequence of binary or hexadecimal digits, it would appear to be a randon sequence.

Type information can be added at higher levels. When encoded as [CBOR](https://cbor.io/), a CID is tagged with #6.58. Tagged this way, the receiver of a CID can still only determine that it *is* a CID, and nothing about the type or nature of its referent.

In particular, this construct provides no information about the lifetime of the referent. The referent could exist persistently for all time, such as in a blockchain, or it could exist for milliseconds, as in a distributed function call.

This construct also provides no information as to the source of its bit sequence. Since the sequence is statistically random, it could have been generated by a cryptographic random number generator or a sequence of ratcheting keys, and either case would be indistinguishable to a third-party observer.

Higher level semantics are provided by how a CID is further tagged, or by how it is positioned in a larger structure, or both. For instance, a distributed function call could have a header that includes the construct `request(CID(XXX))` where `request` is a CBOR tag indicating that the remainder of the structure specifies which function to call and with what parameters, and `CID` specifies its tagged contents as conforming to the other requirements of this document. Positional information would include, for example the position of the CID within a header, or which field a CID populates, such as `person: CID(XXX)`. In this example, being the value of the `person` field is sufficient to use the CID as a "person identifier" *unless* there is more than one distinct kind of "person", in which case another tag would be needed to disambiguate this.

### Open Generation

As mentioned above, *any* method of generating a CID is allowed as long as it fulfills the other requirements of this document, chiefly 1) statistically random bits, and 2) universal uniqueness.

### Minimum Strength

CIDs must be a minimum of 256 bits (32 bytes) in length. At this time, there is no perceived need for CIDs to be longer, and thus conformant processes that receive CIDs MAY reject CIDs that are longer or shorter than 256 bits, while processes that generate CIDs SHOULD only generate CIDs that are exactly 256 bits in length.

### Cryptographic suitability

The foregoing notwithstanding, CIDs MAY be used as inputs to cryptographic constructs such as a ratcheting key algorithms, or used as additional entropy for random number generators, or salt for hashing algorithms, as long as the output of such algorithms is necessarily related to the CID's referent.

For example in the distributed call scenario, a caller might transmit a structure including `request(CID(A))`, where A is a CID generated from an iteration of a ratcheting key algorithm. The receiver compares `A` to its own internal state, rejecting the call if it does not match, and advancing the state of its rachet if it does. The receiver computes the result of the call and returns a structure including `response(CID(B))`, where B is generated from the new state of the ratchet. The caller receives the response and uses the algorithm to correlate `B` in the response to its call `A`, and if further exchanges are needed, uses the ratchet to produce the next expected transaction ID, `C`. Third parties viewing the exchange cannot correlate `A`, `B`, or `C`, and in particular, they cannot correlate a specific response to its call.

## Not to be Confused With

CIDs MUST NOT be confused with any other sort of identifier or sequence of random or apparently random numbers.

* CIDs MUST NOT be cast to or from other identifier types such as UUIDs, nor should they be considered isomorphic to any other type.
* CIDs MUST NOT be cast from digests (hashes) or similar structures.
* CIDs are not [nonces](https://en.wikipedia.org/wiki/Cryptographic_nonce). Unlike nonces, CIDs always have a referent. CIDs MUST NOT be used as nonces, and MUST NOT be created by casting from a nonce used anywhere else.
* CIDs are not keys and MUST NOT be used as keys.
* CIDs are not cryptographic seeds. They are generally not considered secret, and MUST NOT be used as secret key material from which keys or other secret constructs are derived.