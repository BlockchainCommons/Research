# Known Values: A Compact, Deterministic Representation for Ontological Concepts

## BCR-2023-002

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022
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

* **Known Value:** A unique 64-bit integer assigned to an ontological concept.
* **Codepoint:** The specific integer representing a Known Value.
* **Canonical Name:** The unique name for the ontological concept.
* **Registry:** A centralized table or database containing the mapping between codepoints, canonical names, and synonymous URIs.

This document assumes familiarity with ontological systems, including RDF, RDFS, OWL, and related standards.

## Representation

A Known Value is an unsigned integer in the range 0..2<sup>64</sup> - 1. When the context is understood it may be encoded in any suitable format.

When serialized as a tagged CBOR structure it uses tag `#6.40000`. The formal language used is the Concise Data Definition Language (CDDL) [RFC8610].

~~~
known-value = uint

tagged-known-value = #6.40000(known-value)
~~~

So the `tagged-known-value` for `isA` in CBOR diagnostic notation would be:

~~~
40000(1)
~~~

Since CBOR encodes integers using variable length encoding, the actual bytes encoded would be:

~~~
D99C4001
~~~

## Registry Structure

The Known Value Registry is a centralized database designed to hold the mapping between the unique 64-bit integers (codepoints), canonical names, and synonymous URIs for ontological concepts. This section details the structure and key components of the registry.

### Data Structure

*Work in progress.*

The registry consists of rows, with each row containing the following fields:

* **Codepoint:** A unique 64-bit unsigned integer assigned to an ontological concept.
* **Canonical Name:** The standardized name for the ontological concept.
* **Synonymous URIs:** One or more URIs that are synonymous with the concept. These URIs can be linked to various ontologies and standards.

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

### Appendix A: Registry

When encoded as CBOR, the amount of storage required for integer values varies, so ideally more commonly used Known Values would be assigned codepoints requiring less storage.

| Range | Bytes
|--|--|
| 0..23 | 1+0 = 1
| 24..255 | 1+1 = 2
| 256..65535 | 1+2 = 3
| 65536..4294967295 | 1+4 = 5
| 4294967296..18446744073709551615| 1+8 = 9

This table documents the Known Value codepoints currently assigned, but is currently subject to change. It should probably be brought into line with one or more of the foundational ontology vocabularies such as RDF or OWL.

| Codepoint | Canonical Name | Description/URI
|--|--|--|
| 1   | isA            | Predicate declaring the subject is of a type identified by the object.<br/>http://www.w3.org/1999/02/22-rdf-syntax-ns#type
| 2   | id             | Predicate declaring the subject is known by the identifier object.
| 3   | verifiedBy     | Predicate declaring the subject is signed by the `Signature` object.
| 4   | note           | Predicate declaring the subject is accompanied by a human-readable note object.<br/>http://www.w3.org/2000/01/rdf-schema#comment
| 5   | hasRecipient   | Predicate declaring the subject can be decrypted by the ephemeral key contained in the `SealedMessage` object.
| 6   | sskrShare      | Predicate declaring the subject can be decrypted by a quorum of `SSKRShare`s including the one in the object.
| 7   | controller     | Predicate declaring that the document is controlled by the party identified by the object.<br/>https://www.w3.org/ns/solid/terms#owner
| 8   | publicKeys     | Predicate declaring that the party identified by the subject holds the private keys to the `PublicKeyBase` object.
| 9   | dereferenceVia | Predicate declaring that the content referenced by the subject can be dereferenced using the information in the object.
| 10  | entity         | Predicate declaring that the entity referenced by the subject is specified in the object.
| 11  | hasName        | Predicate declaring that the entity referenced by the subject is known by the name in the object.<br/>http://xmlns.com/foaf/0.1/name
| 12  | language       | Predicate declaring the the subject `String` is written in the language of the ISO language code object.<br/>http://www.w3.org/1999/02/22-rdf-syntax-ns#langString
| 13  | issuer         | Predicate declaring that the issuer of the object referenced in the subject is the entity referenced in the object.
| 14  | holder         | Predicate declaring that the holder of the credential or certificate referenced in the subject is the entity referenced in the object.
| 15  | salt           | Predicate declaring that the object is random salt used to decorrelate the digest of the subject.
| 16  | date           | Predicate declaring a primary datestamp on the envelope.<br/>http://purl.org/dc/terms/date
| 17  | unknown        | Placeholder for an unknown value.
| 20  | edits          | Predicate declaring that the object is a set of edits using by the `Envelope.transform(edits:)` method to transform a `source` envelope into a `target` envelope.
