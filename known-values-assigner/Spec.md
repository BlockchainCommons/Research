# Technical Specification: Semantic Ontology Ingest & Known Value Assigner

## 1. Overview

This tool is a Python-based utility designed to automate the ingestion of major Semantic Web ontologies, parse their concept definitions, and deterministically assign "Known Value" integers (64-bit unsigned) to each concept. The output is a standardized JSON registry for each ontology, mapping semantic concepts to efficient binary identifiers for use in Blockchain Commons Gordian Envelopes.

## 2. Dependencies & Environment

* **Runtime:** Python 3.9+
* **Core Libraries:**
* `rdflib` (for parsing RDF/XML, Turtle, and JSON-LD graphs)
* `rdflib-jsonld` (extension for JSON-LD support)
* `requests` (for HTTP retrieval)
* `json` (native JSON handling)


* **Constraints:** Network access required for fetching authoritative definitions.

## 3. Command-Line Interface

The script shall provide a command-line interface using Python's `argparse` module.

### 3.1 Usage

```
python known_value_assigner.py [OPTIONS]
```

### 3.2 Options

| Option | Short | Description |
| --- | --- | --- |
| `--ontology <name>` | `-o` | Process only the specified ontology. Can be specified multiple times to select a subset. If omitted, all ontologies are processed. |
| `--list` | `-l` | List all available ontology names and exit. |
| `--output-dir <path>` | `-d` | Directory for output files. Defaults to current directory. |
| `--no-cache` | | Disable caching; always fetch from network. |
| `--verbose` | `-v` | Enable verbose logging output. |
| `--help` | `-h` | Display help message and exit. |

### 3.3 Ontology Name Identifiers

The following case-insensitive identifiers are valid for the `--ontology` option:

| Identifier | Ontology |
| --- | --- |
| `rdf` or `rdfs` | RDF & RDFS |
| `owl` | OWL 2 |
| `dc-elements` | Dublin Core (Elements) |
| `dc-terms` | Dublin Core (Terms) |
| `foaf` | FOAF |
| `skos` | SKOS |
| `schema` or `schema.org` | Schema.org |
| `vc` or `w3c-vc` | W3C VC |

### 3.4 Examples

```bash
# Process all ontologies (default behavior)
python known_value_assigner.py

# Process only Schema.org
python known_value_assigner.py --ontology schema

# Process RDF/RDFS and OWL
python known_value_assigner.py -o rdf -o owl

# List available ontologies
python known_value_assigner.py --list

# Process FOAF with verbose output to a specific directory
python known_value_assigner.py -o foaf -v -d ./output/
```

## 4. Configuration & Inputs

The script shall operate on a pre-defined list of **Input Tuples**. Each tuple defines the scope of a specific ontology to process.

### 4.1 Input Tuple Structure

`(Ontology Name, Source URL, Start Code Point, Data Format, Processing Strategy)`

### 4.2 Defined Inputs

| Ontology | Source URL | Start Code Point | Format | Strategy |
| --- | --- | --- | --- | --- |
| **RDF & RDFS** | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` (Merge with RDFS) | **1000** | RDF/XML | `StandardRDF` |
| **OWL 2** | `http://www.w3.org/2002/07/owl#` | **2000** | RDF/XML | `StandardRDF` |
| **Dublin Core (Elements)** | `http://purl.org/dc/elements/1.1/` | **3000** | RDF/XML | `StandardRDF` |
| **Dublin Core (Terms)** | `http://purl.org/dc/terms/` | **3500** | RDF/XML | `StandardRDF` |
| **FOAF** | `http://xmlns.com/foaf/0.1/` | **4000** | RDF/XML | `StandardRDF` |
| **SKOS** | `http://www.w3.org/2004/02/skos/core#` | **5000** | RDF/XML | `StandardRDF` |
| **Schema.org** | `https://schema.org/version/latest/schemaorg-current-https.jsonld` | **10000** | JSON-LD | `SchemaOrgLD` |
| **W3C VC** | `https://www.w3.org/ns/credentials/v2` | **20000** | JSON-LD Context | `ContextMap` |

---

## 5. Execution Flow

### Phase 1: Retrieval

For each Input Tuple:

1. Perform an HTTP GET request to the `Source URL`.
2. Ensure correct `Accept` headers are sent based on the `Format`:
* RDF/XML: `application/rdf+xml`
* JSON-LD: `application/ld+json`
* Turtle: `text/turtle`


3. Handle HTTP 3xx redirects automatically.
4. Cache the raw response locally (e.g., in a `./cache/` directory) using a filename derived from the Ontology Name to prevent redundant network calls during development.

### Phase 2: Parsing & Extraction

The script must implement specific **Processing Strategies** to normalize the diverse ontology formats into a single internal representation.

#### Strategy A: `StandardRDF` (for RDF, RDFS, OWL, FOAF, SKOS, DC)

1. Initialize an `rdflib.Graph`.
2. Parse the retrieved content.
3. Execute a SPARQL query against the graph to select all subjects that are defined as:
* `rdf:type` equal to `rdfs:Class`, `owl:Class`, `rdf:Property`, `owl:ObjectProperty`, `owl:DatatypeProperty`, `owl:AnnotationProperty`.


4. **Normalization Rules:**
* **Label:** query `rdfs:label` or `skos:prefLabel`. If multiple exist (multilingual), prefer English (`@en`). If no label exists, extract the local name from the URI.
* **Description:** query `rdfs:comment`, `dcterms:description`, or `skos:definition`.
* **Type:** Simplify the RDF type to a generic string: "Class", "Property", or "Datatype".



#### Strategy B: `SchemaOrgLD` (for Schema.org)

1. Load the JSON-LD content into an `rdflib.Graph`.
2. Schema.org definitions often use `schema:domainIncludes` instead of `rdfs:domain`. The parser must be resilient to "loose" definitions.
3. **Extraction:** Identify all subjects where `rdf:type` is `rdfs:Class` or `rdf:Property`.


#### Strategy C: `ContextMap` (for W3C VC)

1. Load the content as a raw JSON object (do not use `rdflib` parsing initially, as Context files define mappings, not always the ontology graph itself).
2. Iterate through the `@context` dictionary keys.
3. **Filter:** Ignore system keys starting with `@` (e.g., `@version`, `@protected`).
4. **Resolution:**
* For each key (e.g., `issuer`), resolve its value to the full IRI (e.g., `https://www.w3.org/2018/credentials#issuer`).
* If the value is an object (scoped context), extract the `@id`.


5. **Metadata Fetching (Optional):** Since the Context file lacks labels/comments, the script should attempt to dereference the resolved IRI to fetch `rdfs:comment` if possible. If not, default the Label to the key name (CamelCase split) and Description to "Defined in [Ontology Name]".

### Phase 3: Deterministic Assignment

To ensure the "Known Values" remain stable across different runs of the script:

1. **Sorting:** Collect all extracted concepts for the current ontology into a list.
2. **Primary Key:** Sort the list **alphabetically by their authoritative URI** (Subject IRI).
3. **Assignment Loop:**
* Initialize `current_code_point` = `Start Code Point`.
* Iterate through the sorted list.
* Assign `current_code_point` to the concept.
* Increment `current_code_point`.



### Phase 4: Output Generation

For each ontology, write a JSON file named `{ontology_name}_registry.json`.

**JSON Output Schema:**

```json


```

## 6. Detailed Logic Requirements

### 6.1 Handling "isA" and "id" collisions

The script must check if a term's label or URI conceptually matches the core Blockchain Commons values (Code point 1 `isA`, Code point 2 `id`).

* **Logic:** If `uri` ends in `#type` (RDF) or `/type` (DC), log a warning "Semantically equivalent to Core 'isA' (1)".
* **Action:** Still assign the new ontology-specific code point (e.g., 1020 for `rdf:type`) to preserve namespace sovereignty, as per the research report.

### 6.2 Error Handling

* **Parsing Failures:** If a URL fails to parse (e.g., malformed XML), the script must log an error to `stderr` and skip that ontology, rather than crashing.
* **Missing Metadata:** If `label` or `description` is missing, the script must generate a placeholder "[No Label]" or "" to ensure the JSON schema remains valid.

## 7. Deliverable Artifacts

The script will generate the following files:

1. `rdf_rdfs_registry.json`
2. `owl2_registry.json`
3. `dc_elements_registry.json`
4. `dc_terms_registry.json`
5. `foaf_registry.json`
6. `skos_registry.json`
7. `schema_org_registry.json`
8. `w3c_vc_registry.json`
