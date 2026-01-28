# skos Known Values Registry

## Ontology Information

| Property | Value |
|----------|-------|
| **Name** | skos |
| **Source URL** | http://www.w3.org/2004/02/skos/core# |
| **Start Code Point** | 2700 |
| **Processing Strategy** | StandardRDF |

## Statistics

| Metric | Value |
|--------|-------|
| **Total Entries** | 32 |
| **Code Point Range** | 2700 - 2731 |

## Entries

| Codepoint | Name | Type | URI | Description |
|-----------|------|------|-----|-------------|
| 2700 | `skos:Collection` | class | http://www.w3.org/2004/02/skos/core#Collection | A meaningful collection of concepts. |
| 2701 | `skos:Concept` | class | http://www.w3.org/2004/02/skos/core#Concept | An idea or notion; a unit of thought. |
| 2702 | `skos:ConceptScheme` | class | http://www.w3.org/2004/02/skos/core#ConceptScheme | A set of concepts, optionally including statements about semantic relationships between those concepts. |
| 2703 | `skos:OrderedCollection` | class | http://www.w3.org/2004/02/skos/core#OrderedCollection | An ordered collection of concepts, where both the grouping and the ordering are meaningful. |
| 2704 | `skos:altLabel` | property | http://www.w3.org/2004/02/skos/core#altLabel | The range of skos:altLabel is the class of RDF plain literals. |
| 2705 | `skos:broadMatch` | property | http://www.w3.org/2004/02/skos/core#broadMatch | skos:broadMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes. |
| 2706 | `skos:broader` | property | http://www.w3.org/2004/02/skos/core#broader | Broader concepts are typically rendered as parents in a concept hierarchy (tree). |
| 2707 | `skos:broaderTransitive` | property | http://www.w3.org/2004/02/skos/core#broaderTransitive | skos:broaderTransitive is a transitive superproperty of skos:broader. |
| 2708 | `skos:changeNote` | property | http://www.w3.org/2004/02/skos/core#changeNote | A note about a modification to a concept. |
| 2709 | `skos:closeMatch` | property | http://www.w3.org/2004/02/skos/core#closeMatch | skos:closeMatch is used to link two concepts that are sufficiently similar that they can be used interchangeably in some information retrieval applications. In order to avoid the possibility of "compound errors" when combining mappings across more than two concept schemes, skos:closeMatch is not declared to be a transitive property. |
| 2710 | `skos:definition` | property | http://www.w3.org/2004/02/skos/core#definition | A statement or formal explanation of the meaning of a concept. |
| 2711 | `skos:editorialNote` | property | http://www.w3.org/2004/02/skos/core#editorialNote | A note for an editor, translator or maintainer of the vocabulary. |
| 2712 | `skos:exactMatch` | property | http://www.w3.org/2004/02/skos/core#exactMatch | skos:exactMatch is disjoint with each of the properties skos:broadMatch and skos:relatedMatch. |
| 2713 | `skos:example` | property | http://www.w3.org/2004/02/skos/core#example | An example of the use of a concept. |
| 2714 | `skos:hasTopConcept` | property | http://www.w3.org/2004/02/skos/core#hasTopConcept | Relates, by convention, a concept scheme to a concept which is topmost in the broader/narrower concept hierarchies for that scheme, providing an entry point to these hierarchies. |
| 2715 | `skos:hiddenLabel` | property | http://www.w3.org/2004/02/skos/core#hiddenLabel | The range of skos:hiddenLabel is the class of RDF plain literals. |
| 2716 | `skos:historyNote` | property | http://www.w3.org/2004/02/skos/core#historyNote | A note about the past state/use/meaning of a concept. |
| 2717 | `skos:inScheme` | property | http://www.w3.org/2004/02/skos/core#inScheme | Relates a resource (for example a concept) to a concept scheme in which it is included. |
| 2718 | `skos:mappingRelation` | property | http://www.w3.org/2004/02/skos/core#mappingRelation | These concept mapping relations mirror semantic relations, and the data model defined below is similar (with the exception of skos:exactMatch) to the data model defined for semantic relations. A distinct vocabulary is provided for concept mapping relations, to provide a convenient way to differentiate links within a concept scheme from links between concept schemes. However, this pattern of usage is not a formal requirement of the SKOS data model, and relies on informal definitions of best practice. |
| 2719 | `skos:member` | property | http://www.w3.org/2004/02/skos/core#member | Relates a collection to one of its members. |
| 2720 | `skos:memberList` | property | http://www.w3.org/2004/02/skos/core#memberList | For any resource, every item in the list given as the value of the       skos:memberList property is also a value of the skos:member property. |
| 2721 | `skos:narrowMatch` | property | http://www.w3.org/2004/02/skos/core#narrowMatch | skos:narrowMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes. |
| 2722 | `skos:narrower` | property | http://www.w3.org/2004/02/skos/core#narrower | Narrower concepts are typically rendered as children in a concept hierarchy (tree). |
| 2723 | `skos:narrowerTransitive` | property | http://www.w3.org/2004/02/skos/core#narrowerTransitive | skos:narrowerTransitive is a transitive superproperty of skos:narrower. |
| 2724 | `skos:notation` | property | http://www.w3.org/2004/02/skos/core#notation | A notation, also known as classification code, is a string of characters such as "T58.5" or "303.4833" used to uniquely identify a concept within the scope of a given concept scheme. |
| 2725 | `skos:note` | property | http://www.w3.org/2004/02/skos/core#note | A general note, for any purpose. |
| 2726 | `skos:prefLabel` | property | http://www.w3.org/2004/02/skos/core#prefLabel | A resource has no more than one value of skos:prefLabel per language tag, and no more than one value of skos:prefLabel without language tag. |
| 2727 | `skos:related` | property | http://www.w3.org/2004/02/skos/core#related | skos:related is disjoint with skos:broaderTransitive |
| 2728 | `skos:relatedMatch` | property | http://www.w3.org/2004/02/skos/core#relatedMatch | skos:relatedMatch is used to state an associative mapping link between two conceptual resources in different concept schemes. |
| 2729 | `skos:scopeNote` | property | http://www.w3.org/2004/02/skos/core#scopeNote | A note that helps to clarify the meaning and/or the use of a concept. |
| 2730 | `skos:semanticRelation` | property | http://www.w3.org/2004/02/skos/core#semanticRelation | Links a concept to a concept related by meaning. |
| 2731 | `skos:topConceptOf` | property | http://www.w3.org/2004/02/skos/core#topConceptOf | Relates a concept to the concept scheme that it is a top level concept of. |
