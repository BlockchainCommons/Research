#!/usr/bin/env python3
"""
Unit tests for Known Value Assigner.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from known_value_assigner import (
    Concept,
    KnownValueEntry,
    OntologyConfig,
    DataFormat,
    ProcessingStrategy,
    OntologyFetcher,
    StandardRDFParser,
    SchemaOrgParser,
    ContextMapParser,
    KnownValueAssigner,
    get_ontology_by_id,
    ONTOLOGY_CONFIGS,
)


class TestConcept:
    """Tests for Concept dataclass."""

    def test_concept_creation(self):
        """Test basic concept creation."""
        concept = Concept(
            uri="http://example.org/Thing",
            label="Thing",
            description="A generic thing",
            concept_type="Class",
        )
        assert concept.uri == "http://example.org/Thing"
        assert concept.label == "Thing"
        assert concept.description == "A generic thing"
        assert concept.concept_type == "Class"

    def test_concept_to_dict(self):
        """Test concept serialization."""
        concept = Concept(
            uri="http://example.org/Thing",
            label="Thing",
            description="A thing",
            concept_type="Class",
        )
        d = concept.to_dict()
        assert d["uri"] == "http://example.org/Thing"
        assert d["label"] == "Thing"
        assert d["type"] == "Class"


class TestKnownValueEntry:
    """Tests for KnownValueEntry dataclass."""

    def test_entry_creation(self):
        """Test basic entry creation."""
        entry = KnownValueEntry(
            codepoint=1000,
            name="Thing",
            type="class",
            uri="http://example.org/Thing",
            description="A thing",
        )
        assert entry.codepoint == 1000
        assert entry.name == "Thing"
        assert entry.type == "class"

    def test_entry_to_dict(self):
        """Test entry serialization."""
        entry = KnownValueEntry(
            codepoint=1000,
            name="Thing",
            type="class",
            uri="http://example.org/Thing",
            description="A thing",
        )
        d = entry.to_dict()
        assert d["codepoint"] == 1000
        assert d["name"] == "Thing"
        assert d["type"] == "class"
        assert d["uri"] == "http://example.org/Thing"
        assert d["description"] == "A thing"


class TestOntologyConfig:
    """Tests for ontology configuration."""

    def test_get_ontology_by_id_valid(self):
        """Test finding ontology by valid identifier."""
        config = get_ontology_by_id("rdf")
        assert config is not None
        assert config.name == "rdf_rdfs"

        config = get_ontology_by_id("schema")
        assert config is not None
        assert config.name == "schema_org"

    def test_get_ontology_by_id_case_insensitive(self):
        """Test that lookup is case insensitive."""
        config1 = get_ontology_by_id("RDF")
        config2 = get_ontology_by_id("rdf")
        config3 = get_ontology_by_id("Rdf")
        assert config1 == config2 == config3

    def test_get_ontology_by_id_invalid(self):
        """Test finding ontology by invalid identifier."""
        config = get_ontology_by_id("nonexistent")
        assert config is None

    def test_configs_have_unique_start_points(self):
        """Test that all configs have unique start code points."""
        start_points = [c.start_code_point for c in ONTOLOGY_CONFIGS]
        assert len(start_points) == len(set(start_points)), "Duplicate start code points found"


class TestOntologyFetcher:
    """Tests for OntologyFetcher."""

    def test_cache_filename_generation(self):
        """Test cache filename is generated correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=True)
            filename = fetcher._get_cache_filename(
                "http://example.org/ontology.rdf",
                "test_ontology"
            )
            assert "test_ontology" in str(filename)
            assert filename.suffix == ".rdf"

    def test_cache_filename_jsonld(self):
        """Test cache filename for JSON-LD files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=True)
            filename = fetcher._get_cache_filename(
                "http://example.org/ontology.jsonld",
                "test_ontology"
            )
            assert filename.suffix == ".jsonld"

    def test_cache_directory_creation(self):
        """Test cache directory is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "nested" / "cache"
            fetcher = OntologyFetcher(cache_dir, use_cache=True)
            assert cache_dir.exists()

    @patch('requests.get')
    def test_fetch_with_caching(self, mock_get):
        """Test that content is cached after fetching."""
        mock_response = Mock()
        mock_response.text = "<rdf>test content</rdf>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=True)

            # First fetch should hit network
            content1 = fetcher.fetch(
                "http://example.org/test.rdf",
                DataFormat.RDF_XML,
                "test"
            )
            assert mock_get.call_count == 1
            assert content1 == "<rdf>test content</rdf>"

            # Second fetch should use cache
            content2 = fetcher.fetch(
                "http://example.org/test.rdf",
                DataFormat.RDF_XML,
                "test"
            )
            assert mock_get.call_count == 1  # No additional call
            assert content2 == content1

    @patch('requests.get')
    def test_fetch_no_cache(self, mock_get):
        """Test fetching without caching."""
        mock_response = Mock()
        mock_response.text = "<rdf>test content</rdf>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)

            fetcher.fetch("http://example.org/test.rdf", DataFormat.RDF_XML, "test")
            fetcher.fetch("http://example.org/test.rdf", DataFormat.RDF_XML, "test")

            assert mock_get.call_count == 2  # Both should hit network


class TestStandardRDFParser:
    """Tests for StandardRDFParser."""

    SAMPLE_RDF = """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
        <rdfs:Class rdf:about="http://example.org/Person">
            <rdfs:label>Person</rdfs:label>
            <rdfs:comment>A human being</rdfs:comment>
        </rdfs:Class>
        <rdf:Property rdf:about="http://example.org/name">
            <rdfs:label>name</rdfs:label>
            <rdfs:comment>The name of something</rdfs:comment>
        </rdf:Property>
    </rdf:RDF>
    """

    def test_extract_local_name_hash(self):
        """Test local name extraction from hash URI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = StandardRDFParser(fetcher)
            name = parser._extract_local_name("http://example.org/ns#Thing")
            assert name == "Thing"

    def test_extract_local_name_slash(self):
        """Test local name extraction from slash URI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = StandardRDFParser(fetcher)
            name = parser._extract_local_name("http://example.org/vocab/Thing")
            assert name == "Thing"

    @patch.object(OntologyFetcher, 'fetch')
    def test_parse_rdf_concepts(self, mock_fetch):
        """Test parsing RDF content extracts concepts."""
        mock_fetch.return_value = self.SAMPLE_RDF

        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = StandardRDFParser(fetcher)

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            concepts = parser.parse(config)

            # Should find both Person class and name property
            assert len(concepts) == 2
            uris = [c.uri for c in concepts]
            assert "http://example.org/Person" in uris
            assert "http://example.org/name" in uris

            # Check Person concept
            person = next(c for c in concepts if "Person" in c.uri)
            assert person.label == "Person"
            assert person.concept_type == "Class"
            assert "human" in person.description.lower()


class TestContextMapParser:
    """Tests for ContextMapParser."""

    SAMPLE_CONTEXT = json.dumps({
        "@context": {
            "@version": 1.1,
            "@vocab": "https://www.w3.org/2018/credentials#",
            "issuer": {"@id": "https://www.w3.org/2018/credentials#issuer", "@type": "@id"},
            "credentialSubject": {"@id": "https://www.w3.org/2018/credentials#credentialSubject"},
            "type": "@type",
        }
    })

    def test_camel_case_to_words(self):
        """Test CamelCase splitting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = ContextMapParser(fetcher)

            assert parser._camel_case_to_words("credentialSubject") == "credential Subject"
            assert parser._camel_case_to_words("SimpleWord") == "Simple Word"
            assert parser._camel_case_to_words("ABC") == "ABC"

    @patch.object(OntologyFetcher, 'fetch')
    def test_parse_context(self, mock_fetch):
        """Test parsing JSON-LD context."""
        mock_fetch.return_value = self.SAMPLE_CONTEXT

        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = ContextMapParser(fetcher)

            config = OntologyConfig(
                name="test_vc",
                source_url="http://example.org/context.jsonld",
                start_code_point=20000,
                data_format=DataFormat.JSON_LD,
                strategy=ProcessingStrategy.CONTEXT_MAP,
            )

            concepts = parser.parse(config)

            # Should find issuer and credentialSubject (type maps to @type which is filtered)
            uris = [c.uri for c in concepts]
            assert any("issuer" in u for u in uris)
            assert any("credentialSubject" in u for u in uris)


class TestKnownValueAssigner:
    """Tests for KnownValueAssigner."""

    def test_deterministic_assignment(self):
        """Test that assignment is deterministic (sorted by URI)."""
        concepts = [
            Concept("http://example.org/Zebra", "Zebra", "", "Class"),
            Concept("http://example.org/Apple", "Apple", "", "Class"),
            Concept("http://example.org/Mango", "Mango", "", "Class"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = assigner._assign_known_values(concepts, config)

            # Should be sorted alphabetically by URI
            assert entries[0].name == "Apple"
            assert entries[0].codepoint == 1000
            assert entries[1].name == "Mango"
            assert entries[1].codepoint == 1001
            assert entries[2].name == "Zebra"
            assert entries[2].codepoint == 1002

    def test_deterministic_assignment_consistent(self):
        """Test that multiple runs produce same results."""
        concepts = [
            Concept("http://example.org/Zebra", "Zebra", "", "Class"),
            Concept("http://example.org/Apple", "Apple", "", "Class"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            # Run twice
            entries1 = assigner._assign_known_values(concepts.copy(), config)
            entries2 = assigner._assign_known_values(concepts.copy(), config)

            # Results should be identical
            assert len(entries1) == len(entries2)
            for e1, e2 in zip(entries1, entries2):
                assert e1.codepoint == e2.codepoint
                assert e1.name == e2.name
                assert e1.uri == e2.uri

    def test_name_generation(self):
        """Test canonical name generation from various inputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            # From simple label
            assert assigner._to_local_name("Person", "http://ex.org/Person") == "Person"

            # From multi-word label
            assert assigner._to_local_name("Human Being", "http://ex.org/HumanBeing") == "humanBeing"

            # From URI (hash)
            assert assigner._to_local_name("", "http://ex.org/ns#Thing") == "Thing"

            # From URI (slash)
            assert assigner._to_local_name("", "http://ex.org/vocab/Thing") == "Thing"

    def test_write_registry(self):
        """Test registry JSON file generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test_ontology",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = [
                KnownValueEntry(1000, "Thing", "class", "http://ex.org/Thing", "A thing"),
                KnownValueEntry(1001, "name", "property", "http://ex.org/name", "A name"),
            ]

            json_file, markdown_file = assigner.write_registry(config, entries)

            assert json_file is not None
            assert json_file.exists()
            assert "1000_test_ontology_registry.json" in str(json_file)

            # Verify content
            with open(json_file) as f:
                data = json.load(f)

            assert data["ontology"]["name"] == "test_ontology"
            assert data["ontology"]["start_code_point"] == 1000
            assert len(data["entries"]) == 2
            assert data["statistics"]["total_entries"] == 2
            assert data["statistics"]["code_point_range"]["start"] == 1000
            assert data["statistics"]["code_point_range"]["end"] == 1001


class TestCollisionDetection:
    """Tests for semantic collision detection with core Known Values."""

    def test_collision_with_rdf_type(self, caplog):
        """Test that rdf:type collision is logged."""
        concepts = [
            Concept("http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "type", "", "Property"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = assigner._assign_known_values(concepts, config)
            assigner._check_collisions(entries)

            # Should log warning about isA collision
            assert any("isA" in record.message for record in caplog.records)

    def test_collision_with_identifier(self, caplog):
        """Test that identifier collision is logged."""
        concepts = [
            Concept("http://purl.org/dc/terms/identifier", "identifier", "", "Property"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = assigner._assign_known_values(concepts, config)
            assigner._check_collisions(entries)

            # Should log warning about id collision
            assert any("id" in record.message for record in caplog.records)


class TestSchemaOrgParser:
    """Tests for SchemaOrgParser."""

    SAMPLE_SCHEMA_ORG = json.dumps({
        "@context": {
            "schema": "https://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        },
        "@graph": [
            {
                "@id": "https://schema.org/Person",
                "@type": "rdfs:Class",
                "rdfs:label": "Person",
                "rdfs:comment": "A person"
            },
            {
                "@id": "https://schema.org/name",
                "@type": "rdf:Property",
                "rdfs:label": "name",
                "rdfs:comment": "The name of the item"
            },
            {
                "@id": "https://schema.org/OldThing",
                "@type": "rdfs:Class",
                "rdfs:label": "OldThing",
                "schema:supersededBy": {"@id": "https://schema.org/NewThing"}
            }
        ]
    })

    @patch.object(OntologyFetcher, 'fetch')
    def test_parse_schema_org(self, mock_fetch):
        """Test parsing Schema.org JSON-LD."""
        mock_fetch.return_value = self.SAMPLE_SCHEMA_ORG

        with tempfile.TemporaryDirectory() as tmpdir:
            fetcher = OntologyFetcher(Path(tmpdir), use_cache=False)
            parser = SchemaOrgParser(fetcher)

            config = OntologyConfig(
                name="schema_org",
                source_url="https://schema.org/test.jsonld",
                start_code_point=10000,
                data_format=DataFormat.JSON_LD,
                strategy=ProcessingStrategy.SCHEMA_ORG_LD,
            )

            concepts = parser.parse(config)

            # Should find Person, name, and OldThing
            assert len(concepts) >= 2


class TestJSONOutputSchema:
    """Tests to validate JSON output matches expected schema."""

    def test_output_schema_completeness(self):
        """Test that output JSON has all required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="test",
                source_url="http://example.org/test.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = [
                KnownValueEntry(1000, "Thing", "class", "http://ex.org/Thing", "Desc"),
            ]

            json_file, markdown_file = assigner.write_registry(config, entries)

            assert json_file is not None
            with open(json_file) as f:
                data = json.load(f)

            # Check top-level structure
            assert "ontology" in data
            assert "generated" in data
            assert "entries" in data
            assert "statistics" in data

            # Check ontology metadata
            assert "name" in data["ontology"]
            assert "source_url" in data["ontology"]
            assert "start_code_point" in data["ontology"]
            assert "processing_strategy" in data["ontology"]

            # Check entry structure
            entry = data["entries"][0]
            assert "codepoint" in entry
            assert "name" in entry
            assert "type" in entry
            assert "uri" in entry
            assert "description" in entry


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
