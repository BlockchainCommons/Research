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

> **✅ NOTE:** The known value `0` (zero) is the "unit type", and is printed as `''` (empty string). See [BCR-2026-001](bcr-2026-001-unit.md) for more information.

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

### Assigned Code Point Ranges

The following table summarizes the assigned Known Value code point ranges:

| Name                                                                                                             | Range       | Entries      | JSON                                                                       |
|------------------------------------------------------------------------------------------------------------------|-------------|--------------|----------------------------------------------------------------------------|
| [Blockchain Commons](../known-value-assignments/markdown/0_blockchain_commons_registry.md)                       | 0-999       | see registry | [JSON](../known-value-assignments/json/0_blockchain_commons_registry.json) |
| [Community Assigned](../known-value-assignments/markdown/1000_community_registry.md) (specification required)    | 1000-1999   | see registry | [JSON](../known-value-assignments/json/1000_community_registry.json)       |
| [RDF](../known-value-assignments/markdown/2000_rdf_registry.md)                                                  | 2000-2049   | 21           | [JSON](../known-value-assignments/json/2000_rdf_registry.json)             |
| [RDFS](../known-value-assignments/markdown/2050_rdfs_registry.md)                                                | 2050-2099   | 15           | [JSON](../known-value-assignments/json/2050_rdfs_registry.json)            |
| [OWL 2](../known-value-assignments/markdown/2100_owl2_registry.md)                                               | 2100-2199   | 75           | [JSON](../known-value-assignments/json/2100_owl2_registry.json)            |
| [Dublin Core Elements](../known-value-assignments/markdown/2200_dce_registry.md)                                 | 2200-2299   | 15           | [JSON](../known-value-assignments/json/2200_dce_registry.json)             |
| [Dublin Core Terms](../known-value-assignments/markdown/2300_dct_registry.md)                                    | 2300-2499   | 89           | [JSON](../known-value-assignments/json/2300_dct_registry.json)             |
| [FOAF](../known-value-assignments/markdown/2500_foaf_registry.md)                                                | 2500-2699   | 75           | [JSON](../known-value-assignments/json/2500_foaf_registry.json)            |
| [SKOS](../known-value-assignments/markdown/2700_skos_registry.md)                                                | 2700-2799   | 32           | [JSON](../known-value-assignments/json/2700_skos_registry.json)            |
| [Solid](../known-value-assignments/markdown/2800_solid_registry.md)                                              | 2800-2899   | 33           | [JSON](../known-value-assignments/json/2800_solid_registry.json)           |
| [W3C Verifiable Credentials](../known-value-assignments/markdown/2900_vc_registry.md)                            | 2900-2999   | 28           | [JSON](../known-value-assignments/json/2900_vc_registry.json)              |
| [Schema.org](../known-value-assignments/markdown/10000_schema_registry.md)                                       | 10000-19999 | 2450         | [JSON](../known-value-assignments/json/10000_schema_registry.json)         |
| [Community Assigned](../known-value-assignments/markdown/100000_community_registry.md) (first come-first served) | 100000-...  | see registry | [JSON](../known-value-assignments/json/100000_community_registry.json)     |

### Blockchain Commons Core Concepts

The Blockchain Commons range (0-999) contains core concepts specific to Gordian Envelope and related specifications. Where these concepts have equivalent URIs in other ontologies, the external ontology registries reference the Blockchain Commons code point rather than assigning a new one, ensuring 1:1 correspondence between code points and URIs.

- **Core envelope predicates** (0-49): Fundamental properties like `isA`, `id`, `signed`, `note`, `hasRecipient`, `salt`, `date`, `version`
- **Attachments** (50-59): Vendor-defined envelope extensions
- **XID Documents** (60-99): Extensible identifier documents for decentralized identity, including privileges like `allow`, `deny`, `delegate`, and operational/management capabilities
- **Expressions and Functions** (100-199): Request/response patterns including `result`, `error`, `sender`, and continuations
- **Cryptography** (200-299): Cryptographic primitives like `Seed`, `PrivateKey`, `PublicKey`, `MasterKey`
- **Cryptocurrency** (300-499): Asset types (`Bitcoin`, `Ethereum`, `Tezos`) and networks (`MainNet`, `TestNet`)
- **Bitcoin** (500-599): BIP-32 HD keys, derivation paths, PSBTs, and output descriptors
- **Graphs** (600-799): Graph structures including directed graphs, DAGs, trees, forests, hypergraphs, and related edge/node predicates

### Standard Supported Ontologies

This section describes the ontologies from which Known Values are assigned, organized from most fundamental to most specialized.

#### RDF (Resource Description Framework)

RDF is the foundational data model of the Semantic Web, providing a standard way to make statements about resources using subject-predicate-object triples. It defines core concepts like `rdf:type`, `rdf:Property`, `rdf:List`, and `rdf:Statement`. RDF is the most fundamental building block for any semantic system.

#### RDFS (RDF Schema)

RDFS extends RDF with basic schema vocabulary for defining classes and properties. It provides concepts like `rdfs:Class`, `rdfs:subClassOf`, `rdfs:domain`, `rdfs:range`, and `rdfs:comment`. Nearly all other semantic vocabularies are built upon RDF/RDFS primitives.

#### OWL 2 (Web Ontology Language)

OWL 2 extends RDF/RDFS with more expressive constructs for describing complex relationships and constraints. It provides vocabulary for cardinality restrictions, property characteristics (transitive, symmetric, functional), class expressions (unions, intersections, complements), and reasoning capabilities. OWL enables more sophisticated ontological modeling and automated inference.

#### Dublin Core (Elements and Terms)

Dublin Core is a widely-adopted metadata vocabulary originally developed for describing digital resources like documents, images, and web pages. The 15 core elements (title, creator, subject, description, publisher, date, etc.) provide a lingua franca for resource metadata. Dublin Core Terms extends this with additional properties and refined semantics. Many other vocabularies reference Dublin Core for basic metadata needs.

#### SKOS (Simple Knowledge Organization System)

SKOS provides vocabulary for representing knowledge organization systems such as thesauri, classification schemes, taxonomies, and folksonomies. It defines concepts like `Concept`, `ConceptScheme`, `broader`, `narrower`, `prefLabel`, and `altLabel`. SKOS is essential for organizing and relating concepts in controlled vocabularies.

#### FOAF (Friend of a Friend)

FOAF is a vocabulary for describing people, their activities, and their relationships to other people and objects. It defines classes like `Person`, `Organization`, and `Document`, along with properties like `name`, `knows`, `mbox`, and `homepage`. FOAF is widely used in social web applications and decentralized identity systems.

#### Solid

Solid (Social Linked Data) is a W3C project for decentralized data storage and identity. The Solid Terms vocabulary defines concepts for personal data pods, access control, type indexes, and WebID-based authentication. It includes properties like `owner`, `publicTypeIndex`, and `oidcIssuer` that are essential for Solid-based applications.

#### W3C Verifiable Credentials

The W3C Verifiable Credentials vocabulary provides terms for expressing credentials on the Web in a cryptographically secure, privacy-respecting, and machine-verifiable way. It defines concepts like `VerifiableCredential`, `VerifiablePresentation`, `credentialSubject`, `issuer`, and `proof`. This vocabulary is fundamental to decentralized identity and digital credential ecosystems.

#### Schema.org

Schema.org is a collaborative vocabulary created by major search engines (Google, Microsoft, Yahoo, Yandex) for structured data on web pages. It provides an extensive vocabulary of over 2,600 types and properties covering diverse domains: creative works, events, organizations, people, places, products, reviews, and more. While less formal than OWL ontologies, Schema.org is the most widely deployed structured data vocabulary on the Web.

## Community Known Values

The Known Value namespace reserves code points 100,000 and above for community-submitted registrations. This allows organizations and individuals to register their own ontological concepts while maintaining the centralized coordination benefits of the Known Value system.

The community registration process is automated through GitHub Actions workflows. Submitters create a JSON request file specifying their desired code points (≥ 100,000) and submit it via pull request. The system validates the request for schema conformance, code point availability, and uniqueness constraints. Upon successful validation and merge, the code points are automatically registered in the community registry.

For detailed information on submitting community Known Value requests, including the JSON schema, validation rules, and submission process, see [community-known-values/README.md](../community-known-values/README.md).
