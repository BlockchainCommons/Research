# skos Known Values Registry

## Ontology Information

| Property | Value |
|----------|-------|
| **Name** | skos |
| **Source URL** | http://www.w3.org/2004/02/skos/core# |
| **Start Code Point** | 5000 |
| **Processing Strategy** | StandardRDF |

## Statistics

| Metric | Value |
|--------|-------|
| **Total Entries** | 32 |
| **Code Point Range** | 5000 - 5031 |

## Entries

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 5000 | `Collection` | class | http://www.w3.org/2004/02/skos/core#Collection | A meaningful collection of concepts. |
| 5001 | `Concept` | class | http://www.w3.org/2004/02/skos/core#Concept | An idea or notion; a unit of thought. |
| 5002 | `conceptScheme` | class | http://www.w3.org/2004/02/skos/core#ConceptScheme | A set of concepts, optionally including statements about semantic relationships between those concepts. |
| 5003 | `orderedCollection` | class | http://www.w3.org/2004/02/skos/core#OrderedCollection | An ordered collection of concepts, where both the grouping and the ordering are meaningful. |
| 5004 | `alternativeLabel` | property | http://www.w3.org/2004/02/skos/core#altLabel | The range of skos:altLabel is the class of RDF plain literals. |
| 5005 | `hasBroaderMatch` | property | http://www.w3.org/2004/02/skos/core#broadMatch | skos:broadMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes. |
| 5006 | `hasBroader` | property | http://www.w3.org/2004/02/skos/core#broader | Broader concepts are typically rendered as parents in a concept hierarchy (tree). |
| 5007 | `hasBroaderTransitive` | property | http://www.w3.org/2004/02/skos/core#broaderTransitive | skos:broaderTransitive is a transitive superproperty of skos:broader. |
| 5008 | `changeNote` | property | http://www.w3.org/2004/02/skos/core#changeNote | A note about a modification to a concept. |
| 5009 | `hasCloseMatch` | property | http://www.w3.org/2004/02/skos/core#closeMatch | skos:closeMatch is used to link two concepts that are sufficiently similar that they can be used interchangeably in some information retrieval applications. In order to avoid the possibility of "compound errors" when combining mappings across more than two concept schemes, skos:closeMatch is not declared to be a transitive property. |
| 5010 | `definition` | property | http://www.w3.org/2004/02/skos/core#definition | A statement or formal explanation of the meaning of a concept. |
| 5011 | `editorialNote` | property | http://www.w3.org/2004/02/skos/core#editorialNote | A note for an editor, translator or maintainer of the vocabulary. |
| 5012 | `hasExactMatch` | property | http://www.w3.org/2004/02/skos/core#exactMatch | skos:exactMatch is disjoint with each of the properties skos:broadMatch and skos:relatedMatch. |
| 5013 | `example` | property | http://www.w3.org/2004/02/skos/core#example | An example of the use of a concept. |
| 5014 | `hasTopConcept` | property | http://www.w3.org/2004/02/skos/core#hasTopConcept | Relates, by convention, a concept scheme to a concept which is topmost in the broader/narrower concept hierarchies for that scheme, providing an entry point to these hierarchies. |
| 5015 | `hiddenLabel` | property | http://www.w3.org/2004/02/skos/core#hiddenLabel | The range of skos:hiddenLabel is the class of RDF plain literals. |
| 5016 | `historyNote` | property | http://www.w3.org/2004/02/skos/core#historyNote | A note about the past state/use/meaning of a concept. |
| 5017 | `isInScheme` | property | http://www.w3.org/2004/02/skos/core#inScheme | Relates a resource (for example a concept) to a concept scheme in which it is included. |
| 5018 | `isInMappingRelationWith` | property | http://www.w3.org/2004/02/skos/core#mappingRelation | These concept mapping relations mirror semantic relations, and the data model defined below is similar (with the exception of skos:exactMatch) to the data model defined for semantic relations. A distinct vocabulary is provided for concept mapping relations, to provide a convenient way to differentiate links within a concept scheme from links between concept schemes. However, this pattern of usage is not a formal requirement of the SKOS data model, and relies on informal definitions of best practice. |
| 5019 | `hasMember` | property | http://www.w3.org/2004/02/skos/core#member | Relates a collection to one of its members. |
| 5020 | `hasMemberList` | property | http://www.w3.org/2004/02/skos/core#memberList | For any resource, every item in the list given as the value of the       skos:memberList property is also a value of the skos:member property. |
| 5021 | `hasNarrowerMatch` | property | http://www.w3.org/2004/02/skos/core#narrowMatch | skos:narrowMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes. |
| 5022 | `hasNarrower` | property | http://www.w3.org/2004/02/skos/core#narrower | Narrower concepts are typically rendered as children in a concept hierarchy (tree). |
| 5023 | `hasNarrowerTransitive` | property | http://www.w3.org/2004/02/skos/core#narrowerTransitive | skos:narrowerTransitive is a transitive superproperty of skos:narrower. |
| 5024 | `notation` | property | http://www.w3.org/2004/02/skos/core#notation | A notation, also known as classification code, is a string of characters such as "T58.5" or "303.4833" used to uniquely identify a concept within the scope of a given concept scheme. |
| 5025 | `note` | property | http://www.w3.org/2004/02/skos/core#note | A general note, for any purpose. |
| 5026 | `preferredLabel` | property | http://www.w3.org/2004/02/skos/core#prefLabel | A resource has no more than one value of skos:prefLabel per language tag, and no more than one value of skos:prefLabel without language tag. |
| 5027 | `hasRelated` | property | http://www.w3.org/2004/02/skos/core#related | skos:related is disjoint with skos:broaderTransitive |
| 5028 | `hasRelatedMatch` | property | http://www.w3.org/2004/02/skos/core#relatedMatch | skos:relatedMatch is used to state an associative mapping link between two conceptual resources in different concept schemes. |
| 5029 | `scopeNote` | property | http://www.w3.org/2004/02/skos/core#scopeNote | A note that helps to clarify the meaning and/or the use of a concept. |
| 5030 | `isInSemanticRelationWith` | property | http://www.w3.org/2004/02/skos/core#semanticRelation | Links a concept to a concept related by meaning. |
| 5031 | `isTopConceptInScheme` | property | http://www.w3.org/2004/02/skos/core#topConceptOf | Relates a concept to the concept scheme that it is a top level concept of. |
