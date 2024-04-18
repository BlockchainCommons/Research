# Known Values: A Compact, Deterministic Representation for Ontological Concepts

## BCR-2023-002

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022<br/>
Revised: Aug 15, 2023

## Abstract

This document introduces a standardized namespace of 64-bit unsigned integers that represent ontological concepts, potentially across many vocabularies. This standardization aims to enable compact binary representation, interoperability across systems that exchange semantic information, and enhanced security by mitigating the risks associated with URI manipulation.

## Introduction

Ontological concepts are things like relationships between entities (`containedIn`, `spouseOf`), classes of entities (`human`, `book`), properties of entities (`alphaChannel`, `publicationYear`), or enumerated values of properties (`female`, `red`). These concepts are used to define the structure and semantics of a domain, describing the types of things that exist and the ways they relate to each other.

Ontological concepts like relationships, classes, and properties stand alone in that they are independent and self-contained entities within the ontology. This is in contrast to something like CBOR tags, which are used to label and interpret specific data values within a particular encoding. CBOR tags depend on the context of the data they are applied to and don't have independent meaning outside that context. Ontological concepts, on the other hand, represent general ideas and relationships that are not tied to specific data values or encodings, giving them a more standalone nature.

In the context of current ontological vocabularies like RDF and OWL the use of URIs to represent concepts, while flexible, introduces possibilities for manipulation and ambiguity in representation. URIs are also verbose and do not lend themselves well to long documents involving many concepts and processing in constrained environments.

The Known Value approach addresses this by associating a unique 64-bit integer with each ontological concept. These integers, referred to as Known Values, are associated with canonical names and synonymous URIs within a centralized registry, ensuring that specific semantics have exactly one valid binary representation.

This approach carries several benefits:

* **Simplification and Efficiency:** Converting ontological concepts into unique integers enables compact encoding in various documents, particularly binary formats like CBOR.
* **Enhanced Security:** Utilizing integers instead of URIs eliminates the surface for manipulation attacks and helps ensure deterministic encoding, as used in Gordian Envelope.

## Scope

The scope of this specification includes the definition of the Known Value namespace, the structure of the registry, the rules for assigning and managing Known Values.

Appendix A is a list of currently assigned Known Values.

## Terminology

* **Known Value:** A unique 64-bit unsigned integer assigned to an ontological concept.
* **Codepoint:** The specific integer representing a Known Value.
* **Canonical Name:** The unique name for the ontological concept.
* **Registry:** A centralized table or database containing the mapping between codepoints, canonical names, and synonymous URIs.

This document assumes familiarity with ontological systems, including RDF, RDFS, OWL, and related standards.

## Representation

A Known Value is an unsigned integer in the range 0..2<sup>64</sup> - 1. When the context is understood it may be encoded in any suitable format.

When a Known Value's name is printed in text, whether as a name or integer value it is surrounded by single quotes (`U+0027`). For example, the Known Value for `isA` is printed as either `'1'` or `'isA'`. Therefore the presence of single quotes always indicates a Known Value.

When serialized as a tagged CBOR structure it uses tag `#6.40000`. The formal language used is the Concise Data Definition Language (CDDL) [RFC8610].

```
known-value = uint

tagged-known-value = #6.40000(known-value)
```

So the `tagged-known-value` for `isA` in CBOR diagnostic notation would be:

```
40000(1)
```

Since CBOR encodes integers using variable length encoding, the actual bytes encoded would be:

```
d99c4001
```

## Registry Structure

The Known Value Registry is a centralized database designed to hold the mapping between the unique 64-bit integers (codepoints), canonical names, and synonymous URIs for ontological concepts. This section details the structure and key components of the registry.

### Data Structure

*Work in progress.*

The registry consists of rows, with each row containing the following fields:

* **Codepoint:** A unique 64-bit unsigned integer assigned to an ontological concept.
* **Canonical Name:** The standardized name for the ontological concept.
* **Type:** The type of ontological concept, e.g. class, property, relationship, etc. By convention, classes and enumerated values are `CapitalizedCamelCase`, while properties and relationships are `uncapitalizedCamelCase`.
* **Description:** A human-readable description of the concept.
* **URI:** A URI that defines the concept. This may be a URI for an existing ontology, or a URI that is specific to another specification.

### Access Controls

*Work in progress.*

The Known Value Registry shall be maintained with specific access controls to ensure integrity and reliability:

* **Read Access:** Publicly available for any system or user to query and utilize Known Values.
* **Write Access:** Restricted to authorized entities who can propose, modify, or delete entries. The process for becoming an authorized entity is described in section 2.

### Consistency and Validation

*Work in progress.*

The Known Value Registry must maintain consistency and prevent conflicts. Specific validation rules include:

* No duplicate codepoints.
* No duplicate canonical names.
* Validation of URIs to ensure they are valid and conform to the respective ontology standards.

### Versioning and History

*Work in progress.*

The registry should include versioning and maintain a history of changes to allow tracking of modifications, additions, and deletions. This enables traceability and can support rollback in case of erroneous changes.

## Assignment Process

*Work in progress.*

* Process for requesting, assigning, and managing Known Values.
* Guidelines for what constitutes a valid ontological concept for inclusion.
* Considerations regarding similar, duplicate, or conflicting entries.

## Interoperability with Existing Systems

*Work in progress.*

* Explanation of how Known Values can be integrated with existing ontological systems like RDF, RDFS, and OWL.
* Examples or use cases demonstrating integration with Gordian Envelope, dCBOR, etc.

## Security Considerations

*Work in progress.*

* Detailed discussion of the security enhancements achieved through Known Values, including examples.
* Any potential security risks or considerations that should be addressed.

## IANA Considerations

This document requests the assignment of CBOR tag #6.40000:

| Tag | Data Item | Semantics |
|:----|:-----|:-----|
| 40000 | uint | Known Value |

## Appendix A: Registry

When encoded as CBOR, the amount of storage required for integer values varies, so ideally more commonly used Known Values would be assigned codepoints requiring less storage.

| Range | Bytes
|--|--|
| 0..23 | 1+0 = 1
| 24..255 | 1+1 = 2
| 256..65535 | 1+2 = 3
| 65536..4294967295 | 1+4 = 5
| 4294967296..18446744073709551615| 1+8 = 9

This table documents the Known Value codepoints currently assigned, but is currently subject to change. It should probably be brought into line with one or more of the foundational ontology vocabularies such as RDF or OWL.

### General

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 1  | isA            | property | Declares that the subject is an instance of the class identified by the object. | http://www.w3.org/1999/02/22-rdf-syntax-ns#type
| 2  | id             | property | Declares an unambiguous reference to the subject within a given context. | http://purl.org/dc/terms/identifier
| 3  | verifiedBy     | property | Declares a cryptographic signature of the subject.
| 4  | note           | property | Declares a human-readable note about the subject. | http://www.w3.org/2000/01/rdf-schema#comment
| 5  | hasRecipient   | property | Declares the subject can be decrypted by the ephemeral key contained in the object.
| 6  | sskrShare      | property | Declares the subject can be decrypted by a quorum of SSKR shares including the one in the object.
| 7  | controller     | property | Declares the subject's controlling entity. | https://www.w3.org/ns/solid/terms#owner
| 8  | publicKeys     | property | Declares the entity identified by the subject holds the private keys in the object.
| 9  | dereferenceVia | property | Declares the content referenced by the subject can be dereferenced using the object.
| 10 | entity         | property | Declares the entity referenced by the subject is specified in the object.
| 11 | hasName        | property | Declares the the subject is known by the name in the object. | http://xmlns.com/foaf/0.1/name
| 12 | language       | property | Declares the subject is written in the language of the ISO language code object. | http://www.w3.org/1999/02/22-rdf-syntax-ns#langString
| 13 | issuer         | property | Declares the subject's issuing entity.
| 14 | holder         | property | Declares the entity to which the subject has been issued.
| 15 | salt           | property | Declares that the object is random salt used to decorrelate the digest of the subject.
| 16 | date           | property | Declares a primary datestamp of the subject. | http://purl.org/dc/terms/date
| 17 | Unknown        | value    | Placeholder for an unknown value. | https://en.wikipedia.org/wiki/Blank_node
| 20 | edits          | property | Declares that the object is a set of edits using by the `Envelope.transform(edits:)` method to transform a `source` envelope into a `target` envelope.

### Vendor Extensions

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 50 | attachment | property | Declares that the object is a vendor-defined attachment to the envelope. | [BCR-2023-006](bcr-2023-006-envelope-attachment.md)
| 51 | vendor     | property | Declares the vendor of the subject. | [BCR-2023-006](bcr-2023-006-envelope-attachment.md)
| 52 | conformsTo | property | An established standard to which the subject conforms. | http://purl.org/dc/terms/conformsTo

### Graphs

Codepoints 60-89 are reserved for graph types. See [BCR-2024-006](bcr-2024-006-envelope-graph.md) for specific assignments.

### Expressions and Function Calls

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 100 | body       | property | Property declaring that the object is the body (parameters of) a distributed request identified by the subject.
| 101 | result     | property | Property declaring that the object is the success result of the request identified by the subject.
| 102 | error      | property | Property declaring that the object is the failure result of the request identified by the subject.
| 103 | OK         | value    | Instance providing the success result of a request that has no other return value.
| 104 | Processing | value    | Instance providing the "in processing" result of a request.

### Cryptography

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 200 | Seed       | class | A cryptographic seed.
| 201 | PrivateKey | class | A cryptographic private key.
| 202 | PublicKey  | class | A cryptographic public key.
| 203 | MasterKey  | class | A cryptographic master key.

### Cryptocurrency Assets

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 300 | asset    | property | Declares a cryptocurrency asset specifier, e.g. "Bitcoin", "Ethereum"
| 301 | Bitcoin  | value | The Bitcoin cryptocurrency ("BTC")
| 302 | Ethereum | value | The Ethereum cryptocurrency ("ETH")
| 303 | Tezos    | value | The Tezos cryptocurrency ("XTZ")

### Cryptocurrency Networks

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 400 | network | property | Declares a cryptocurrency network, e.g. "MainNet", "TestNet"
| 401 | MainNet | value | A cryptocurrency main network
| 402 | TestNet | value | A cryptocurrency test network

### Bitcoin

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 500 | BIP32Key          | class    | A BIP-32 HD key
| 501 | chainCode         | property | Declares the chain code of a BIP-32 HD key
| 502 | DerivationPath    | class    |A BIP-32 derivation path
| 503 | parentPath        | property | Declares the derivation path for a BIP-32 key
| 504 | childrenPath      | property | Declares the allowable derivation paths from a BIP-32 key
| 505 | parentFingerprint | property | Declares the parent fingerprint of a BIP-32 key
| 506 | PSBT              | class    | A Partially-Signed Bitcoin Transaction (PSBT)
| 507 | OutputDescriptor  | class    | A Bitcoin output descriptor
| 508 | outputDescriptor  | property | Declares a Bitcoin output descriptor associated with the subject
