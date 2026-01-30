#!/usr/bin/env python3
"""
Semantic Ontology Ingest & Known Value Assigner

This tool automates the ingestion of major Semantic Web ontologies, parses their
concept definitions, and deterministically assigns "Known Value" integers (64-bit
unsigned) to each concept. The output is a standardized JSON registry for each
ontology, mapping semantic concepts to efficient binary identifiers for use in
Blockchain Commons Gordian Envelopes.

Based on BCR-2023-002: Known Values specification.
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS, DC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Namespace definitions
SCHEMA = Namespace("https://schema.org/")

# Core Known Values that may have semantic equivalents in ontologies
CORE_KNOWN_VALUES = {
    1: ("isA", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
    2: ("id", "http://purl.org/dc/terms/identifier"),
}


class ProcessingStrategy(Enum):
    """Processing strategies for different ontology formats."""
    STANDARD_RDF = "StandardRDF"
    SCHEMA_ORG_LD = "SchemaOrgLD"
    CONTEXT_MAP = "ContextMap"


class DataFormat(Enum):
    """Supported data formats for ontology retrieval."""
    RDF_XML = "application/rdf+xml"
    JSON_LD = "application/ld+json"
    TURTLE = "text/turtle"


@dataclass
class OntologyConfig:
    """Configuration for a single ontology to process."""
    name: str
    source_url: str
    start_code_point: int
    data_format: DataFormat
    strategy: ProcessingStrategy
    # Local bundled file path (fallback if URL fails)
    bundled_file: Optional[str] = None
    # Optional URI prefix filter - only include URIs starting with this
    uri_filter: Optional[str] = None


@dataclass
class Concept:
    """Represents an extracted ontological concept."""
    uri: str
    label: str
    description: str
    concept_type: str  # "Class", "Property", or "Datatype"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "uri": self.uri,
            "label": self.label,
            "description": self.description,
            "type": self.concept_type,
        }


@dataclass
class KnownValueEntry:
    """A Known Value registry entry."""
    codepoint: int
    name: str
    type: str
    uri: str
    description: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "codepoint": self.codepoint,
            "name": self.name,
            "type": self.type,
            "uri": self.uri,
            "description": self.description,
        }


# Ontology configurations as per spec
ONTOLOGY_CONFIGS = [
    OntologyConfig(
        name="rdf",
        source_url="http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        start_code_point=2000,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="rdfs",
        source_url="http://www.w3.org/2000/01/rdf-schema#",
        start_code_point=2050,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="owl2",
        source_url="http://www.w3.org/2002/07/owl#",
        start_code_point=2100,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="dce",
        source_url="http://purl.org/dc/elements/1.1/",
        start_code_point=2200,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="dct",
        source_url="http://purl.org/dc/terms/",
        start_code_point=2300,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="foaf",
        source_url="http://xmlns.com/foaf/0.1/",
        start_code_point=2500,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
        bundled_file="bundled/foaf.rdf",
        uri_filter="http://xmlns.com/foaf/",
    ),
    OntologyConfig(
        name="skos",
        source_url="http://www.w3.org/2004/02/skos/core#",
        start_code_point=2700,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="solid",
        source_url="http://www.w3.org/ns/solid/terms#",
        start_code_point=2800,
        data_format=DataFormat.RDF_XML,
        strategy=ProcessingStrategy.STANDARD_RDF,
    ),
    OntologyConfig(
        name="schema",
        source_url="https://schema.org/version/latest/schemaorg-current-https.jsonld",
        start_code_point=10000,
        data_format=DataFormat.JSON_LD,
        strategy=ProcessingStrategy.SCHEMA_ORG_LD,
        uri_filter="https://schema.org/",
    ),
    OntologyConfig(
        name="gs1",
        source_url="https://raw.githubusercontent.com/gs1/WebVoc/master/v1.16/gs1Voc.ttl",
        start_code_point=3000,
        data_format=DataFormat.TURTLE,
        strategy=ProcessingStrategy.STANDARD_RDF,
        uri_filter="https://ref.gs1.org/voc/",
    ),
    OntologyConfig(
        name="vc",
        source_url="https://www.w3.org/ns/credentials/v2",
        start_code_point=2900,
        data_format=DataFormat.JSON_LD,
        strategy=ProcessingStrategy.CONTEXT_MAP,
    ),
]


def get_ontology_by_id(cli_id: str) -> Optional[OntologyConfig]:
    """Find an ontology configuration by its name."""
    cli_id_lower = cli_id.lower()
    for config in ONTOLOGY_CONFIGS:
        if cli_id_lower == config.name.lower():
            return config
    return None


def list_ontologies() -> None:
    """Print available ontologies and their identifiers."""
    print("\nAvailable Ontologies:")
    print("-" * 40)
    print(f"{'Name':<15} {'Start Code'}")
    print("-" * 40)
    for config in ONTOLOGY_CONFIGS:
        print(f"{config.name:<15} {config.start_code_point}")
    print("-" * 40)


class OntologyFetcher:
    """Handles HTTP retrieval and caching of ontology files."""

    def __init__(self, cache_dir: Path, use_cache: bool = True, script_dir: Optional[Path] = None):
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        self.script_dir = script_dir or Path(__file__).parent
        if use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_filename(self, url: str, ontology_name: str) -> Path:
        """Generate a cache filename from URL and ontology name."""
        # Use hash of URL to handle special characters
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        if "json" in url.lower():
            extension = ".jsonld"
        elif url.lower().endswith(".ttl"):
            extension = ".ttl"
        else:
            extension = ".rdf"
        return self.cache_dir / f"{ontology_name}_{url_hash}{extension}"

    def fetch(self, url: str, data_format: DataFormat, ontology_name: str,
              bundled_file: Optional[str] = None) -> str:
        """Fetch ontology content from URL, cache, or bundled file."""
        cache_file = self._get_cache_filename(url, ontology_name)

        # Check cache first
        if self.use_cache and cache_file.exists():
            logger.info(f"Using cached content for {ontology_name} from {cache_file}")
            return cache_file.read_text(encoding="utf-8")

        # Try to fetch from network
        logger.info(f"Fetching {ontology_name} from {url}")
        headers = {
            "Accept": data_format.value,
            "User-Agent": "KnownValueAssigner/1.0 (Blockchain Commons)"
        }

        try:
            response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
            response.raise_for_status()
            content = response.text

            # Cache the response
            if self.use_cache:
                cache_file.write_text(content, encoding="utf-8")
                logger.info(f"Cached content to {cache_file}")

            return content

        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {e}")

            # Try bundled file as fallback
            if bundled_file:
                bundled_path = self.script_dir / bundled_file
                if bundled_path.exists():
                    logger.info(f"Using bundled file: {bundled_path}")
                    content = bundled_path.read_text(encoding="utf-8")
                    # Cache the bundled content for future use
                    if self.use_cache:
                        cache_file.write_text(content, encoding="utf-8")
                    return content
                else:
                    logger.warning(f"Bundled file not found: {bundled_path}")

            raise


class StandardRDFParser:
    """Parser for standard RDF/XML ontologies (RDF, RDFS, OWL, FOAF, SKOS, DC)."""

    # Types we're interested in extracting
    CONCEPT_TYPES = {
        RDFS.Class: "Class",
        OWL.Class: "Class",
        RDF.Property: "Property",
        RDFS.Datatype: "Datatype",
        OWL.ObjectProperty: "Property",
        OWL.DatatypeProperty: "Property",
        OWL.AnnotationProperty: "Property",
    }

    def __init__(self, fetcher: OntologyFetcher):
        self.fetcher = fetcher

    def parse(self, config: OntologyConfig) -> list[Concept]:
        """Parse an ontology and extract concepts."""
        graph = Graph()

        # Fetch and parse main URL
        content = self.fetcher.fetch(
            config.source_url,
            config.data_format,
            config.name,
            bundled_file=config.bundled_file
        )
        try:
            graph.parse(data=content, format="xml")
        except Exception as e:
            logger.warning(f"Failed to parse {config.source_url} as XML, trying auto-detection: {e}")
            graph.parse(data=content)

        # Extract concepts
        concepts = []
        seen_uris = set()

        for rdf_type, concept_type in self.CONCEPT_TYPES.items():
            for subject in graph.subjects(RDF.type, rdf_type):
                if not isinstance(subject, URIRef):
                    continue

                uri = str(subject)

                # Apply URI filter if specified in config
                if config.uri_filter and not uri.startswith(config.uri_filter):
                    continue

                if uri in seen_uris:
                    continue
                seen_uris.add(uri)

                label = self._get_label(graph, subject)
                description = self._get_description(graph, subject)

                concepts.append(Concept(
                    uri=uri,
                    label=label,
                    description=description,
                    concept_type=concept_type,
                ))

        logger.info(f"Extracted {len(concepts)} concepts from {config.name}")
        return concepts

    def _get_label(self, graph: Graph, subject: URIRef) -> str:
        """Extract the best label for a concept."""
        # Try rdfs:label first, preferring English
        for label in graph.objects(subject, RDFS.label):
            if isinstance(label, Literal):
                if label.language == "en" or label.language is None:
                    return str(label)

        # Try skos:prefLabel
        for label in graph.objects(subject, SKOS.prefLabel):
            if isinstance(label, Literal):
                if label.language == "en" or label.language is None:
                    return str(label)

        # Fall back to any label
        for label in graph.objects(subject, RDFS.label):
            return str(label)

        # Extract local name from URI
        return self._extract_local_name(str(subject))

    def _get_description(self, graph: Graph, subject: URIRef) -> str:
        """Extract the best description for a concept."""
        # Try rdfs:comment
        for desc in graph.objects(subject, RDFS.comment):
            if isinstance(desc, Literal):
                if desc.language == "en" or desc.language is None:
                    return str(desc)

        # Try dcterms:description
        for desc in graph.objects(subject, DCTERMS.description):
            if isinstance(desc, Literal):
                return str(desc)

        # Try skos:definition
        for desc in graph.objects(subject, SKOS.definition):
            if isinstance(desc, Literal):
                if desc.language == "en" or desc.language is None:
                    return str(desc)

        # Fall back to any comment
        for desc in graph.objects(subject, RDFS.comment):
            return str(desc)

        return ""

    def _extract_local_name(self, uri: str) -> str:
        """Extract the local name from a URI."""
        if "#" in uri:
            return uri.split("#")[-1]
        return uri.rstrip("/").split("/")[-1]


class SchemaOrgParser:
    """Parser for Schema.org JSON-LD ontology."""

    def __init__(self, fetcher: OntologyFetcher):
        self.fetcher = fetcher

    def parse(self, config: OntologyConfig) -> list[Concept]:
        """Parse Schema.org JSON-LD and extract concepts."""
        content = self.fetcher.fetch(
            config.source_url,
            config.data_format,
            config.name
        )

        # Parse JSON-LD into rdflib Graph
        graph = Graph()
        try:
            graph.parse(data=content, format="json-ld")
        except Exception as e:
            logger.error(f"Failed to parse Schema.org JSON-LD: {e}")
            raise

        concepts = []
        seen_uris = set()

        # Schema.org uses rdfs:Class and rdf:Property
        for rdf_type, concept_type in [
            (RDFS.Class, "Class"),
            (RDF.Property, "Property"),
        ]:
            for subject in graph.subjects(RDF.type, rdf_type):
                if not isinstance(subject, URIRef):
                    continue

                uri = str(subject)

                # Apply URI filter if specified in config
                if config.uri_filter and not uri.startswith(config.uri_filter):
                    continue

                if uri in seen_uris:
                    continue
                seen_uris.add(uri)

                label = self._get_label(graph, subject, uri)
                description = self._get_description(graph, subject)

                concepts.append(Concept(
                    uri=uri,
                    label=label,
                    description=description,
                    concept_type=concept_type,
                ))

        logger.info(f"Extracted {len(concepts)} concepts from {config.name}")
        return concepts

    def _get_label(self, graph: Graph, subject: URIRef, uri: str) -> str:
        """Extract label from Schema.org concept."""
        for label in graph.objects(subject, RDFS.label):
            return str(label)

        # Extract from URI
        return self._extract_local_name(uri)

    def _get_description(self, graph: Graph, subject: URIRef) -> str:
        """Extract description from Schema.org concept."""
        for desc in graph.objects(subject, RDFS.comment):
            return str(desc)
        return ""

    def _extract_local_name(self, uri: str) -> str:
        """Extract the local name from a URI."""
        return uri.rstrip("/").split("/")[-1]


class ContextMapParser:
    """Parser for JSON-LD Context files (W3C VC)."""

    def __init__(self, fetcher: OntologyFetcher):
        self.fetcher = fetcher

    def parse(self, config: OntologyConfig) -> list[Concept]:
        """Parse a JSON-LD context file and extract concepts."""
        content = self.fetcher.fetch(
            config.source_url,
            config.data_format,
            config.name
        )

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON context: {e}")
            raise

        concepts = []
        context = data.get("@context", data)

        # Handle nested context (array or dict)
        if isinstance(context, list):
            # Merge all context objects
            merged = {}
            for item in context:
                if isinstance(item, dict):
                    merged.update(item)
            context = merged

        if not isinstance(context, dict):
            logger.warning(f"Unexpected context type: {type(context)}")
            return concepts

        for key, value in context.items():
            # Skip system keys
            if key.startswith("@"):
                continue

            # Resolve the full IRI
            uri = self._resolve_uri(key, value, context)
            if not uri:
                continue

            # Determine type based on value structure
            concept_type = "Property"  # Default for VC contexts
            if isinstance(value, dict):
                if value.get("@type") == "@id":
                    concept_type = "Property"
                elif "@container" in value:
                    concept_type = "Property"

            # Generate label from key (CamelCase split)
            label = self._camel_case_to_words(key)
            description = f"Defined in {config.name}"

            concepts.append(Concept(
                uri=uri,
                label=label,
                description=description,
                concept_type=concept_type,
            ))

        logger.info(f"Extracted {len(concepts)} concepts from {config.name}")
        return concepts

    def _resolve_uri(self, key: str, value, context: dict) -> Optional[str]:
        """Resolve a context key to its full IRI."""
        if isinstance(value, str):
            # Simple string mapping
            if value.startswith("http://") or value.startswith("https://"):
                return value
            # Check for prefix:local format
            if ":" in value and not value.startswith("@"):
                prefix, local = value.split(":", 1)
                if prefix in context:
                    base = context[prefix]
                    if isinstance(base, str):
                        return base + local
            return None

        elif isinstance(value, dict):
            # Object with @id
            id_value = value.get("@id")
            if id_value:
                return self._resolve_uri(key, id_value, context)
            # If no @id, try to construct from vocab
            vocab = context.get("@vocab")
            if vocab:
                return vocab + key

        return None

    def _camel_case_to_words(self, name: str) -> str:
        """Convert CamelCase to space-separated words."""
        # Insert space before uppercase letters
        result = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        return result


class KnownValueAssigner:
    """Main class for assigning Known Values to ontological concepts."""

    def __init__(self, output_dir: Path, cache_dir: Path, use_cache: bool = True, verbose: bool = False):
        self.output_dir = output_dir
        self.fetcher = OntologyFetcher(cache_dir, use_cache)
        self.verbose = verbose

        # Initialize parsers
        self.standard_parser = StandardRDFParser(self.fetcher)
        self.schema_parser = SchemaOrgParser(self.fetcher)
        self.context_parser = ContextMapParser(self.fetcher)

        # Load Blockchain Commons core registry for URI -> codepoint mapping
        self.bc_uri_to_codepoint: dict[str, int] = {}
        self._load_blockchain_commons_registry()

    def _load_blockchain_commons_registry(self) -> None:
        """Load the Blockchain Commons registry to get pre-assigned codepoints and names."""
        bc_registry_path = self.output_dir / "json" / "0_blockchain_commons_registry.json"
        if not bc_registry_path.exists():
            logger.warning(f"Blockchain Commons registry not found at {bc_registry_path}")
            return

        try:
            with open(bc_registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)

            for entry in registry.get("entries", []):
                uri = entry.get("uri", "")
                codepoint = entry.get("codepoint")
                name = entry.get("name", "")
                if uri and codepoint is not None:
                    self.bc_uri_to_codepoint[uri] = (codepoint, name)

            logger.info(f"Loaded {len(self.bc_uri_to_codepoint)} URI mappings from Blockchain Commons registry")
        except Exception as e:
            logger.error(f"Failed to load Blockchain Commons registry: {e}")

    def process_ontology(self, config: OntologyConfig) -> Optional[list[KnownValueEntry]]:
        """Process a single ontology and return its Known Value entries."""
        logger.info(f"Processing ontology: {config.name}")

        try:
            # Parse based on strategy
            if config.strategy == ProcessingStrategy.STANDARD_RDF:
                concepts = self.standard_parser.parse(config)
            elif config.strategy == ProcessingStrategy.SCHEMA_ORG_LD:
                concepts = self.schema_parser.parse(config)
            elif config.strategy == ProcessingStrategy.CONTEXT_MAP:
                concepts = self.context_parser.parse(config)
            else:
                logger.error(f"Unknown strategy: {config.strategy}")
                return None

            if not concepts:
                logger.warning(f"No concepts extracted from {config.name}")
                return []

            # Deterministic assignment
            entries = self._assign_known_values(concepts, config)

            # Check for semantic collisions with core values
            self._check_collisions(entries)

            return entries

        except Exception as e:
            logger.error(f"Failed to process {config.name}: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return None

    def _assign_known_values(self, concepts: list[Concept], config: OntologyConfig) -> list[KnownValueEntry]:
        """Deterministically assign Known Values to concepts."""
        # Sort alphabetically by URI for deterministic assignment
        sorted_concepts = sorted(concepts, key=lambda c: c.uri)

        entries = []
        current_codepoint = config.start_code_point

        for concept in sorted_concepts:
            # Check if this URI already has a codepoint in Blockchain Commons registry
            if concept.uri in self.bc_uri_to_codepoint:
                bc_codepoint, bc_name = self.bc_uri_to_codepoint[concept.uri]
                logger.info(f"Using Blockchain Commons codepoint {bc_codepoint} ({bc_name}) for {concept.uri}")
                entry = KnownValueEntry(
                    codepoint=bc_codepoint,
                    name=bc_name,
                    type=concept.concept_type.lower(),
                    uri=concept.uri,
                    description=concept.description if concept.description else "",
                )
            else:
                # Extract local name from label or URI, then prepend ontology name as prefix
                local_name = self._to_local_name(concept.label, concept.uri)
                name = f"{config.name}:{local_name}"
                # Assign from ontology's range
                entry = KnownValueEntry(
                    codepoint=current_codepoint,
                    name=name,
                    type=concept.concept_type.lower(),
                    uri=concept.uri,
                    description=concept.description if concept.description else "",
                )
                current_codepoint += 1

            entries.append(entry)

        # Check for duplicate canonical names
        self._check_duplicate_names(entries, config)

        return entries

    def _check_duplicate_names(self, entries: list[KnownValueEntry], config: OntologyConfig) -> None:
        """Check for duplicate canonical names within an ontology.

        Raises ValueError if duplicates are found, as this indicates a logic error
        where two different URIs map to the same canonical name.
        """
        name_to_uris = {}
        for entry in entries:
            if entry.name not in name_to_uris:
                name_to_uris[entry.name] = []
            name_to_uris[entry.name].append(entry.uri)

        duplicates = {name: uris for name, uris in name_to_uris.items() if len(uris) > 1}

        if duplicates:
            error_msg = f"Duplicate canonical names found in {config.name} ontology:\n"
            for name, uris in duplicates.items():
                error_msg += f"  {name}:\n"
                for uri in uris:
                    error_msg += f"    - {uri}\n"
            logger.error(error_msg)
            raise ValueError(f"Found {len(duplicates)} duplicate canonical name(s) in {config.name} ontology")

    def _to_local_name(self, label: str, uri: str) -> str:
        """Convert URI to canonical name format.

        Prefers URI fragment over label for more concise, idiomatic names.
        Falls back to label processing only if URI has no usable fragment.
        """
        # Extract from URI first (preferred)
        if "#" in uri:
            fragment = uri.split("#")[-1]
            if fragment:  # Check it's not empty
                return fragment

        # Try path-based URI
        path_part = uri.rstrip("/").split("/")[-1]
        if path_part and path_part not in ["", uri]:
            return path_part

        # Fall back to label processing only if URI extraction failed
        if label and label != "[No Label]":
            # Clean up the label
            name = label.strip()
            # Remove any non-alphanumeric chars except spaces
            name = re.sub(r'[^\w\s]', '', name)
            # Convert to camelCase if it has spaces
            if ' ' in name:
                parts = name.split()
                name = parts[0].lower() + ''.join(p.capitalize() for p in parts[1:])
            return name

        # Ultimate fallback
        return "unknown"

    def _check_collisions(self, entries: list[KnownValueEntry]) -> None:
        """Check for semantic collisions with core Known Values."""
        for entry in entries:
            # Check for rdf:type equivalent
            if entry.uri.endswith("#type") or entry.uri.endswith("/type"):
                logger.warning(
                    f"Semantically equivalent to Core 'isA' (1): "
                    f"{entry.name} ({entry.codepoint}) -> {entry.uri}"
                )

            # Check for identifier equivalent
            if entry.uri.endswith("#identifier") or entry.uri.endswith("/identifier"):
                logger.warning(
                    f"Semantically equivalent to Core 'id' (2): "
                    f"{entry.name} ({entry.codepoint}) -> {entry.uri}"
                )

    def write_registry(self, config: OntologyConfig, entries: list[KnownValueEntry]) -> tuple[Path | None, Path | None]:
        """Write the registry to JSON and Markdown files."""
        # Create output subdirectories
        json_dir = self.output_dir / "json"
        markdown_dir = self.output_dir / "markdown"
        json_dir.mkdir(parents=True, exist_ok=True)
        markdown_dir.mkdir(parents=True, exist_ok=True)

        base_name = f"{config.start_code_point}_{config.name}_registry"
        json_file = json_dir / f"{base_name}.json"
        markdown_file = markdown_dir / f"{base_name}.md"

        # Protect manually-created 0_* files from being overwritten
        if base_name.startswith("0_"):
            logger.warning(f"Skipping protected file: {base_name} (0_* files are manually maintained)")
            return None, None

        registry = {
            "ontology": {
                "name": config.name,
                "source_url": config.source_url,
                "start_code_point": config.start_code_point,
                "processing_strategy": config.strategy.value,
            },
            "generated": {
                "tool": "KnownValueAssigner",
                "version": "1.0.0",
            },
            "entries": [entry.to_dict() for entry in entries],
            "statistics": {
                "total_entries": len(entries),
                "code_point_range": {
                    "start": config.start_code_point,
                    "end": config.start_code_point + len(entries) - 1 if entries else config.start_code_point,
                },
            },
        }

        # Write JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        logger.info(f"Wrote JSON registry to {json_file}")

        # Write Markdown
        self._write_markdown_registry(markdown_file, config, entries, registry)
        logger.info(f"Wrote Markdown registry to {markdown_file}")

        return json_file, markdown_file

    def _write_markdown_registry(self, filepath: Path, config: OntologyConfig,
                                  entries: list[KnownValueEntry], registry: dict) -> None:
        """Write the registry as a Markdown table."""
        lines = [
            f"# {config.name} Known Values Registry",
            "",
            "## Ontology Information",
            "",
            f"| Property | Value |",
            f"|----------|-------|",
            f"| **Name** | {config.name} |",
            f"| **Source URL** | {config.source_url} |",
            f"| **Start Code Point** | {config.start_code_point} |",
            f"| **Processing Strategy** | {config.strategy.value} |",
            "",
            "## Statistics",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| **Total Entries** | {registry['statistics']['total_entries']} |",
            f"| **Code Point Range** | {registry['statistics']['code_point_range']['start']} - {registry['statistics']['code_point_range']['end']} |",
            "",
            "## Entries",
            "",
            "| Codepoint | Name | Type | URI | Description |",
            "|-----------|------|------|-----|-------------|",
        ]

        for entry in entries:
            # Escape pipe characters in URIs and descriptions
            uri = entry.uri.replace("|", "\\|")
            name = entry.name.replace("|", "\\|")
            desc = entry.description.replace("|", "\\|").replace("\n", " ") if entry.description else ""
            lines.append(f"| {entry.codepoint} | `{name}` | {entry.type} | {uri} | {desc} |")

        lines.append("")  # Final newline

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Semantic Ontology Ingest & Known Value Assigner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         Process all ontologies
  %(prog)s -o schema               Process only Schema.org
  %(prog)s -o rdf -o owl           Process RDF/RDFS and OWL
  %(prog)s --list                  List available ontologies
  %(prog)s -o foaf -v -d ./output  Process FOAF with verbose output
        """
    )

    parser.add_argument(
        "-o", "--ontology",
        action="append",
        dest="ontologies",
        metavar="NAME",
        help="Process only the specified ontology. Can be specified multiple times."
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available ontology names and exit."
    )

    parser.add_argument(
        "-d", "--output-dir",
        type=Path,
        default=Path("../known-value-assignments"),
        help="Directory for output files. Defaults to ../known-value-assignments"
    )

    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("./cache"),
        help="Directory for cached ontology files. Defaults to ./cache"
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching; always fetch from network."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging output."
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Handle --list
    if args.list:
        list_ontologies()
        return 0

    # Determine which ontologies to process
    if args.ontologies:
        configs_to_process = []
        for ont_id in args.ontologies:
            config = get_ontology_by_id(ont_id)
            if config:
                if config not in configs_to_process:
                    configs_to_process.append(config)
            else:
                logger.error(f"Unknown ontology identifier: {ont_id}")
                logger.info("Use --list to see available ontologies.")
                return 1
    else:
        configs_to_process = ONTOLOGY_CONFIGS

    # Initialize assigner
    assigner = KnownValueAssigner(
        output_dir=args.output_dir,
        cache_dir=args.cache_dir,
        use_cache=not args.no_cache,
        verbose=args.verbose,
    )

    # Process each ontology
    success_count = 0
    failure_count = 0

    for config in configs_to_process:
        entries = assigner.process_ontology(config)
        if entries is not None:
            assigner.write_registry(config, entries)
            success_count += 1
        else:
            failure_count += 1

    # Summary
    logger.info(f"Processing complete: {success_count} succeeded, {failure_count} failed")

    return 0 if failure_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
