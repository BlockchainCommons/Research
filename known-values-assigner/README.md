# Known Value Assigner

A Python utility for ingesting major Semantic Web ontologies and deterministically assigning "Known Value" integers (64-bit unsigned) to each concept. The output is standardized JSON registries for use in Blockchain Commons Gordian Envelopes.

Based on [BCR-2023-002: Known Values](../papers/bcr-2023-002-known-value.md) specification.

## Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Process all ontologies
python known_value_assigner.py

# Process specific ontology
python known_value_assigner.py -o schema

# Process multiple ontologies
python known_value_assigner.py -o rdf -o owl

# List available ontologies
python known_value_assigner.py --list

# Custom output directory with verbose logging
python known_value_assigner.py -o foaf -v -d ./my_output/
```

### Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--ontology <name>` | `-o` | Process only the specified ontology (repeatable) |
| `--list` | `-l` | List all available ontology names and exit |
| `--output-dir <path>` | `-d` | Directory for output files (default: ../known-value-assignments) |
| `--cache-dir <path>` | | Directory for cached ontology files (default: ./cache) |
| `--no-cache` | | Disable caching; always fetch from network |
| `--verbose` | `-v` | Enable verbose logging output |
| `--help` | `-h` | Display help message |

### Available Ontologies

| Identifier | Ontology | Start Code Point |
|------------|----------|------------------|
| `rdf`, `rdfs` | RDF & RDFS | 1000 |
| `owl` | OWL 2 | 2000 |
| `dc-elements` | Dublin Core (Elements) | 3000 |
| `dc-terms` | Dublin Core (Terms) | 3500 |
| `foaf` | FOAF | 4000 |
| `skos` | SKOS | 5000 |
| `solid` | Solid Terms | 6000 |
| `schema`, `schema.org` | Schema.org | 10000 |
| `vc`, `w3c-vc` | W3C Verifiable Credentials | 20000 |

## Output Format

Each ontology generates a JSON registry file:

```json
{
  "ontology": {
    "name": "skos",
    "source_url": "http://www.w3.org/2004/02/skos/core#",
    "start_code_point": 5000,
    "processing_strategy": "StandardRDF"
  },
  "generated": {
    "tool": "KnownValueAssigner",
    "version": "1.0.0"
  },
  "entries": [
    {
      "codepoint": 5000,
      "canonical_name": "Collection",
      "type": "class",
      "uri": "http://www.w3.org/2004/02/skos/core#Collection",
      "description": "A meaningful collection of concepts."
    }
  ],
  "statistics": {
    "total_entries": 32,
    "code_point_range": {
      "start": 5000,
      "end": 5031
    }
  }
}
```

## Generated Registries

Output files are organized into `../known-value-assignments/json/` and `../known-value-assignments/markdown/` directories:

| File | Entries | Code Point Range |
|------|---------|------------------|
| `0_blockchain_commons_registry` | 88 | 0-705 |
| `1000_rdf_rdfs_registry` | 33 | 1000-1032 |
| `2000_owl2_registry` | 75 | 2000-2074 |
| `3000_dc_elements_registry` | 15 | 3000-3014 |
| `3500_dc_terms_registry` | 84 | 3500-3583 |
| `4000_foaf_registry` | 83 | 4000-4082 |
| `5000_skos_registry` | 32 | 5000-5031 |
| `6000_solid_registry` | 33 | 6000-6032 |
| `10000_schema_org_registry` | 2664 | 10000-12663 |
| `20000_w3c_vc_registry` | 28 | 20000-20027 |

> **Note:** The `0_blockchain_commons_registry` files are manually maintained and protected from being overwritten by the script.

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=known_value_assigner
```

## Processing Strategies

The tool implements three parsing strategies:

1. **StandardRDF** - For RDF/XML ontologies (RDF, RDFS, OWL, DC, FOAF, SKOS)
2. **SchemaOrgLD** - For Schema.org JSON-LD
3. **ContextMap** - For JSON-LD Context files (W3C VC)

## Deterministic Assignment

Known Values are assigned deterministically:
1. All concepts are sorted alphabetically by their authoritative URI
2. Code points are assigned sequentially from the start code point
3. Multiple runs produce identical results

## Semantic Collision Warnings

The tool warns when ontology terms semantically overlap with core Known Values:
- `rdf:type` → Core `isA` (1)
- `dcterms:identifier` → Core `id` (2)

These are still assigned ontology-specific code points to preserve namespace sovereignty.

## License

This project follows Blockchain Commons' open source guidelines.
