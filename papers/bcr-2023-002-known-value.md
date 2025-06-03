# Known Values: A Compact, Deterministic Representation for Ontological Concepts

## BCR-2023-002

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022<br/>
Revised: April 26, 2025

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

> **✅ NOTE:** The known value `0` (zero) is the "unit type", and is printed as `''` (empty string). See the note below for more details.

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

| Tag   | Data Item | Semantics   |
| ----- | --------- | ----------- |
| 40000 | uint      | Known Value |

## Implementations

The [known-values](https://github.com/BlockchainCommons/known-values-rust) library provides a Rust registry of Known Values, including the ability to encode and decode them in CBOR.

## Appendix A: Registry

When encoded as CBOR, the amount of storage required for integer values varies, so ideally more commonly used Known Values would be assigned codepoints requiring less storage.

| Range                            | Bytes   |
| -------------------------------- | ------- |
| 0..23                            | 1+0 = 1 |
| 24..255                          | 1+1 = 2 |
| 256..65535                       | 1+2 = 3 |
| 65536..4294967295                | 1+4 = 5 |
| 4294967296..18446744073709551615 | 1+8 = 9 |

This table documents the Known Value codepoints currently assigned, but is currently subject to change. It should probably be brought into line with one or more of the foundational ontology vocabularies such as RDF or OWL.


### General

| Codepoint | Canonical Name   | Type     | Description                                                                                      | URI                                                   |
| --------- | ---------------- | -------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 0         | `''` _empty_     | unit     | The Unit type, and its sole inhabitant `''`, which is a value conveying no information.          |
| 1         | `isA`            | property | The subject is an instance of the class identified by the object.                                | http://www.w3.org/1999/02/22-rdf-syntax-ns#type       |
| 2         | `id`             | property | The object is an unambiguous identifier of the subject within a given context.                   | http://purl.org/dc/terms/identifier                   |
| 3         | `signed`         | property | The object is a cryptographic signature of the subject.                                          |
| 4         | `note`           | property | The object is a human-readable note about the subject.                                           | http://www.w3.org/2000/01/rdf-schema#comment          |
| 5         | `hasRecipient`   | property | The subject can be decrypted using the private key that decrypts the content key in the object.  |
| 6         | `sskrShare`      | property | The subject can be decrypted by a quorum of SSKR shares including the one in the object.         |
| 7         | `controller`     | property | The object is the subject's controlling entity.                                                  | https://www.w3.org/ns/solid/terms#owner               |
| 8         | `key`            | property | The entity identified by the subject holds the private half of the public keys(s) in the object. |
| 9         | `dereferenceVia` | property | The content referenced by the subject can be dereferenced using the object.                      |
| 10        | `entity`         | property | The entity referenced by the subject is specified in the object.                                 |
| 11        | `name`           | property | The subject is known by the name in the object.                                                  | http://xmlns.com/foaf/spec/#term_name                 |
| 12        | `language`       | property | The subject is written in the language of the ISO language code object.                          | http://www.w3.org/1999/02/22-rdf-syntax-ns#langString |
| 13        | `issuer`         | property | The object is the subject's issuing entity.                                                      |
| 14        | `holder`         | property | The object identifies the entity to which the subject has been issued.                           |
| 15        | `salt`           | property | The object is random salt used to decorrelate the digest of the subject.                         |
| 16        | `date`           | property | The object is a primary datestamp of the subject.                                                | http://purl.org/dc/terms/date                         |
| 17        | `Unknown`        | value    | Placeholder for an unknown value.                                                                | https://en.wikipedia.org/wiki/Blank_node              |
| 18        | `version`        | property | The object is the version of the subject.                                                        | http://purl.org/dc/terms/hasVersion                   |
| 19        | `hasSecret`      | property | The subject can be decrypted using the secret that decrypts the content key in the object.       |
| 20        | `edits`          | property | The object is a set of edits used by the `Envelope.transform(edits:)` method.                    |
| 21        | `validFrom`      | property | The subject is valid from the date in the object.                                                | http://purl.org/dc/terms/valid                        |
| 22        | `validUntil`     | property | The subject is valid until the date in the object.                                               | http://purl.org/dc/terms/valid                        |
| 23        | `position`       | property | The position of an item in a series or sequence of items.                                        | https://schema.org/position                           |
| 24        | `nickname`       | property | The subject is a nickname for the object.                                                        | http://xmlns.com/foaf/spec/#term_nick                 |
| 25-49     | *unassigned*     |

> **✅ NOTE:** Code-point 0 denotes **Unit**—a special entry that is
> *simultaneously* a class **and** its single inhabitant `''`.
>
> *Semantics:* **Unit** *positively* asserts that “nothing is being conveyed.”
> It is **not** a stand-in for a missing, null, or still-to-be-determined value,
> nor a marker that something *ought* to or *might* be here later. By using
> **Unit** you are saying, *precisely*, that this position carries zero
> informational content.
>
> Contrast this with `'Unknown'` (codepoint 17), which indicates that *some*
> value exists but is not known, and with explicit null constructs (e.g.,
> JavaScript or CBOR `null`), which signify *absence* rather than *deliberate
> emptiness.*
>
> **Language parallels:**
> • Rust: both the type and the value are written `()`
> • C / C++: the *type* `void` plays the same role, but there is **no
>   inhabitant value** (functions simply return to the caller)
> • Java: the primitive return type `void`; boxed analogue `java.lang.Void` is a
>   reference type whose only legal value is `null`
> • Python: the singleton value `None`, whose type is `types.NoneType`

### Attachments

| Codepoint | Canonical Name | Type     | Description                                                              | URI                                                 |
| --------- | -------------- | -------- | ------------------------------------------------------------------------ | --------------------------------------------------- |
| 50        | `attachment`   | property | Declares that the object is a vendor-defined attachment to the envelope. | [BCR-2023-006](bcr-2023-006-envelope-attachment.md) |
| 51        | `vendor`       | property | Declares the vendor of the subject.                                      | [BCR-2023-006](bcr-2023-006-envelope-attachment.md) |
| 52        | `conformsTo`   | property | An established standard to which the subject conforms.                   | http://purl.org/dc/terms/conformsTo                 |
| 53-59     | *unassigned*   |

### XID Documents

| Codepoint | Canonical Name | Type     | Description                                                                                                   | URI |
| --------- | -------------- | -------- | ------------------------------------------------------------------------------------------------------------- | --- |
| 60        | `allow`        | property | The object is a set of permissions that allow the subject to perform the actions specified in the object.     |
| 61        | `deny`         | property | The object is a set of permissions that deny the subject from performing the actions specified in the object. |
| 62        | `endpoint`     | property |
| 63        | `delegate`     | property |
| 64        | `provenance`   | property |
| 65        | `privateKey`   | property |
| 66        | `service`      | property |
| 67        | `capability`   | property |
| 68-69     | *unassigned*   |

#### XID Privileges

| Codepoint | Canonical Name | Type  | Description                                                                                       | URI |
| --------- | -------------- | ----- | ------------------------------------------------------------------------------------------------- | --- |
| 70        | `All`          | value | The set of all allowed privileges.                                                                |
| 71        | `Authorize`    | value | Operational privilege: authorize actions on behalf of the subject.                                |
| 72        | `Sign`         | value | Operational privilege: sign documents on behalf of the subject.                                   |
| 73        | `Encrypt`      | value | Operational privilege: encrypt messages from the subject and decrypt messages to the subject.     |
| 74        | `Elide`        | value | Operational privilege: elide the subject's documents.                                             |
| 75        | `Issue`        | value | Operational privilege: issue documents on behalf of the subject.                                  |
| 76        | `Access`       | value | Operational privilege: access resources on behalf of the subject.                                 |
| 77-79     | *unassigned*   |
| 80        | `Delegate`     | value | Management privilege: delegate the privileges of the subject to another entity.                   |
| 81        | `Verify`       | value | Management privilege: update the subject's documents, including the ability to reduce privileges. |
| 82        | `Update`       | value | Management privilege: update the subject's service endpoints.                                     |
| 83        | `Transfer`     | value | Management privilege: remove the inception key from the XID document.                             |
| 84        | `Elect`        | value | Management privilege: add or remove other verifiers (rotate keys).                                |
| 85        | `Burn`         | value | Management privilege: transition to a new provenance mark chain.                                  |
| 86        | `Revoke`       | value | Management privilege: revoke the XID entirely.                                                    |
| 87-99     | *unassigned*   |

### Expression and Function Calls

| Codepoint | Canonical Name          | Type     | Description                                                                                             | URI |
| --------- | ----------------------- | -------- | ------------------------------------------------------------------------------------------------------- | --- |
| 101       | `result`                | property | The object is the success result of the request identified by the subject.                              |
| 102       | `error`                 | property | The object is the failure result of the request identified by the subject.                              |
| 103       | `OK`                    | value    | The success result of a request that has no other return value.                                         |
| 104       | `Processing`            | value    | The "in processing" result of a request.                                                                |
| 105       | `sender`                | property | The object identifies the sender, including a way to verify messages from the sender (e.g. public key). |
| 106       | `senderContinuation`    | property | The object is a continuation owned by the sender.                                                       |
| 107       | `recipientContinuation` | property | The object is a continuation owned by the recipient.                                                    |
| 108       | `content`               | property | The object is the content of the event.                                                                 |
| 109-199   | *unassigned*            |

### Cryptography

| Codepoint | Canonical Name | Type  | Description                  | URI |
| --------- | -------------- | ----- | ---------------------------- | --- |
| 200       | `Seed`         | class | A cryptographic seed.        |
| 201       | `PrivateKey`   | class | A cryptographic private key. |
| 202       | `PublicKey`    | class | A cryptographic public key.  |
| 203       | `MasterKey`    | class | A cryptographic master key.  |
| 204-259   | *unassigned*   |

### Cryptocurrency Assets

| Codepoint | Canonical Name | Type     | Description                                                           | URI |
| --------- | -------------- | -------- | --------------------------------------------------------------------- | --- |
| 300       | `asset`        | property | Declares a cryptocurrency asset specifier, e.g. "Bitcoin", "Ethereum" |
| 301       | `Bitcoin`      | value    | The Bitcoin cryptocurrency ("BTC")                                    |
| 302       | `Ethereum`     | value    | The Ethereum cryptocurrency ("ETH")                                   |
| 303       | `Tezos`        | value    | The Tezos cryptocurrency ("XTZ")                                      |
| 304-399   | *unassigned*   |


### Cryptocurrency Networks

| Codepoint | Canonical Name | Type     | Description                                                  | URI |
| --------- | -------------- | -------- | ------------------------------------------------------------ | --- |
| 400       | `network`      | property | Declares a cryptocurrency network, e.g. "MainNet", "TestNet" |
| 401       | `MainNet`      | value    | A cryptocurrency main network                                |
| 402       | `TestNet`      | value    | A cryptocurrency test network                                |
| 403-499   | *unassigned*   |


### Bitcoin

| Codepoint | Canonical Name      | Type     | Description                                                      | URI |
| --------- | ------------------- | -------- | ---------------------------------------------------------------- | --- |
| 500       | `BIP32Key`          | class    | A BIP-32 HD key                                                  |
| 501       | `chainCode`         | property | Declares the chain code of a BIP-32 HD key                       |
| 502       | `DerivationPath`    | class    | A BIP-32 derivation path                                         |
| 503       | `parentPath`        | property | Declares the derivation path for a BIP-32 key                    |
| 504       | `childrenPath`      | property | Declares the allowable derivation paths from a BIP-32 key        |
| 505       | `parentFingerprint` | property | Declares the parent fingerprint of a BIP-32 key                  |
| 506       | `PSBT`              | class    | A Partially-Signed Bitcoin Transaction (PSBT)                    |
| 507       | `OutputDescriptor`  | class    | A Bitcoin output descriptor                                      |
| 508       | `outputDescriptor`  | property | Declares a Bitcoin output descriptor associated with the subject |
| 509-599   | *unassigned*        |

### Graphs

| Codepoint | Canonical Name      | Type     | Description                                                                                                                                                                                                                                         | URI |
| --------- | ------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| 600       | `Graph`             | class    | A graph. All other assertions in the envelope must be either `node` or `edge`.                                                                                                                                                                      |
| 601       | `SourceTargetGraph` | class    | A graph with edges that have `source` and `target` assertions.                                                                                                                                                                                      |
| 602       | `ParentChildGraph`  | class    | A graph with edges that have `parent` and `child` assertions.                                                                                                                                                                                       |
| 603       | `Digraph`           | class    | A directed graph. Implies `SourceTargetGraph`. `source` and `target` are distinct. Without this type, edges are undirected (symmetric) and `source` and `target` are interchangeable.                                                               |
| 604       | `AcyclicGraph`      | class    | A graph that does not admit cycles. Implies `SourceTargetGraph`. If `Digraph`, does not admit directed cycles.                                                                                                                                      |
| 605       | `Multigraph`        | class    | A multigraph (admits parallel edges). Implies `SourceTargetGraph`. Without this type, edges may not be parallel (i.e., there is at most one edge between any pair of nodes, in a directed graph, connecting the same `source` and `target` nodes.)  |
| 606       | `Pseudograph`       | class    | A pseudograph (admits self-loops and parallel edges). Implies `Multigraph`. Without this type, edges may not be self-loops (i.e., `source` and `target` are the same).                                                                              |
| 607       | `GraphFragment`     | class    | A fragment of a graph. May have references to external nodes and edges that are not resolvable in the fragment. As such, validation of a `GraphFragment` may be weaker. Without this type, all nodes and edges must be resolvable within the graph. |
| 608       | `DAG`               | class    | A directed acyclic graph. Implies `Digraph` and `AcyclicGraph`.                                                                                                                                                                                     |
| 609       | `Tree`              | class    | A tree. Implies `ParentChildGraph`. Exactly one node must have no `parent`. All other nodes must have exactly one `parent`.                                                                                                                         |
| 610       | `Forest`            | class    | A forest (set of trees). Implies `ParentChildGraph`. Edges use `parent` and `child` to define tree relationships. All nodes must have either no `parent` or exactly one `parent`.                                                                   |
| 611       | `CompoundGraph`     | class    | A compound graph (a graph with subgraphs). Implies `Forest` and `SourceTargetGraph`. Uses `source` and `target` to define graph relationships, and `parent` and `child` to define tree relationships.                                               |
| 612       | `Hypergraph`        | class    | An undirected hypergraph (edges may connect more than two nodes). There may be multiple `source` and `target` assertions in a hyperedge. Source and Target sets must be disjoint. `source` and `target` are interchangeable.                        |
| 613       | `Dihypergraph`      | class    | A directed hypergraph (edges may connect more than two nodes and have a direction). There may be multiple `source` and `target` assertions in a hyperedge. Source and Target sets must be disjoint. Implies `Hypergraph` and `Digraph`.             |
| 614-699   | *unassigned*        |
| 700       | `node`              | property | A node in a graph.                                                                                                                                                                                                                                  |
| 701       | `edge`              | property | An edge in a graph. Defines the edge's endpoints using either (`source` and `target`) assertions for `SourceTargetGraph`s or (`parent` and `child`) assertions for `ParentChildGraph`s.                                                             |
| 702       | `source`            | property | Identifies the source node of the subject edge of a `SourceTargetGraph`. Required. May not be repeated, except in a hyperedge.                                                                                                                      |
| 703       | `target`            | property | Identifies the target node of the subject edge of a `SourceTargetGraph`. Required. May not be repeated, except in a hyperedge.                                                                                                                      |
| 704       | `parent`            | property | Identifies the parent node of the subject edge of a `ParentChildGraph`. Omitted only for a root node, required for all other nodes. May not be repeated.                                                                                            |
| 705       | `child`             | property | Identifies a child node of the subject edge of a `ParentChildGraph`. Required. May not be repeated.                                                                                                                                                 |
| 706-...   | *unassigned*        |
