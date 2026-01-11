#!/usr/bin/env python3
"""
Integration tests for Known Value Assigner.

These tests validate the end-to-end processing pipeline using real (mocked) data.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from known_value_assigner import (
    KnownValueAssigner,
    OntologyConfig,
    DataFormat,
    ProcessingStrategy,
    ONTOLOGY_CONFIGS,
    main,
)


class TestIntegrationEndToEnd:
    """Integration tests for the complete processing pipeline."""

    # Sample RDF ontology content
    SAMPLE_ONTOLOGY = """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
             xmlns:owl="http://www.w3.org/2002/07/owl#">

        <owl:Ontology rdf:about="http://example.org/test#">
            <rdfs:label>Test Ontology</rdfs:label>
        </owl:Ontology>

        <rdfs:Class rdf:about="http://example.org/test#Animal">
            <rdfs:label>Animal</rdfs:label>
            <rdfs:comment>A living creature</rdfs:comment>
        </rdfs:Class>

        <rdfs:Class rdf:about="http://example.org/test#Person">
            <rdfs:label>Person</rdfs:label>
            <rdfs:comment>A human being</rdfs:comment>
        </rdfs:Class>

        <rdf:Property rdf:about="http://example.org/test#name">
            <rdfs:label>name</rdfs:label>
            <rdfs:comment>The name of something</rdfs:comment>
        </rdf:Property>

        <rdf:Property rdf:about="http://example.org/test#age">
            <rdfs:label>age</rdfs:label>
            <rdfs:comment>The age in years</rdfs:comment>
        </rdf:Property>
    </rdf:RDF>
    """

    @patch('requests.get')
    def test_full_pipeline_standard_rdf(self, mock_get):
        """Test complete pipeline for StandardRDF strategy."""
        mock_response = Mock()
        mock_response.text = self.SAMPLE_ONTOLOGY
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            cache_dir = Path(tmpdir) / "cache"

            assigner = KnownValueAssigner(
                output_dir=output_dir,
                cache_dir=cache_dir,
                use_cache=True,
            )

            config = OntologyConfig(
                name="test_ontology",
                source_url="http://example.org/test.rdf",
                start_code_point=9000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = assigner.process_ontology(config)
            assert entries is not None
            assert len(entries) == 4  # 2 classes + 2 properties

            # Verify deterministic ordering (sorted by URI)
            uris = [e.uri for e in entries]
            assert uris == sorted(uris)

            # Verify code point assignment
            assert entries[0].codepoint == 9000
            assert entries[1].codepoint == 9001
            assert entries[2].codepoint == 9002
            assert entries[3].codepoint == 9003

            # Write registry and verify output
            json_file, markdown_file = assigner.write_registry(config, entries)
            assert json_file is not None
            assert json_file.exists()

            with open(json_file) as f:
                registry = json.load(f)

            assert registry["ontology"]["name"] == "test_ontology"
            assert registry["statistics"]["total_entries"] == 4
            assert registry["statistics"]["code_point_range"]["start"] == 9000
            assert registry["statistics"]["code_point_range"]["end"] == 9003


class TestDeterministicAssignment:
    """Tests verifying deterministic and stable assignment across runs."""

    SAMPLE_ONTOLOGY = """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
        <rdfs:Class rdf:about="http://example.org/Zebra">
            <rdfs:label>Zebra</rdfs:label>
        </rdfs:Class>
        <rdfs:Class rdf:about="http://example.org/Apple">
            <rdfs:label>Apple</rdfs:label>
        </rdfs:Class>
        <rdfs:Class rdf:about="http://example.org/Mango">
            <rdfs:label>Mango</rdfs:label>
        </rdfs:Class>
    </rdf:RDF>
    """

    @patch('requests.get')
    def test_multiple_runs_produce_same_results(self, mock_get):
        """Verify that multiple runs produce identical assignments."""
        mock_response = Mock()
        mock_response.text = self.SAMPLE_ONTOLOGY
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        results = []

        for _ in range(3):  # Run 3 times
            with tempfile.TemporaryDirectory() as tmpdir:
                assigner = KnownValueAssigner(
                    output_dir=Path(tmpdir),
                    cache_dir=Path(tmpdir) / "cache",
                    use_cache=False,  # Don't cache to test fresh parsing
                )

                config = OntologyConfig(
                    name="test",
                    source_url="http://example.org/test.rdf",
                    start_code_point=1000,
                    data_format=DataFormat.RDF_XML,
                    strategy=ProcessingStrategy.STANDARD_RDF,
                )

                entries = assigner.process_ontology(config)
                assert entries is not None
                results.append([(e.codepoint, e.name, e.uri) for e in entries])

        # All runs should produce identical results
        assert results[0] == results[1] == results[2]

        # Should be sorted by URI (Apple < Mango < Zebra)
        assert results[0][0][1] == "Apple"
        assert results[0][1][1] == "Mango"
        assert results[0][2][1] == "Zebra"


class TestOutputValidation:
    """Tests validating the JSON output format."""

    @patch('requests.get')
    def test_json_schema_compliance(self, mock_get):
        """Verify JSON output matches expected schema."""
        mock_response = Mock()
        mock_response.text = """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
            <rdfs:Class rdf:about="http://example.org/Thing">
                <rdfs:label>Thing</rdfs:label>
                <rdfs:comment>A generic thing</rdfs:comment>
            </rdfs:Class>
        </rdf:RDF>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

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

            entries = assigner.process_ontology(config)
            assert entries is not None
            json_file, markdown_file = assigner.write_registry(config, entries)
            assert json_file is not None

            with open(json_file) as f:
                registry = json.load(f)

            # Validate top-level structure
            assert "ontology" in registry
            assert "generated" in registry
            assert "entries" in registry
            assert "statistics" in registry

            # Validate ontology section
            ont = registry["ontology"]
            assert ont["name"] == "test"
            assert ont["source_url"] == "http://example.org/test.rdf"
            assert ont["start_code_point"] == 1000
            assert ont["processing_strategy"] == "StandardRDF"

            # Validate generated section
            gen = registry["generated"]
            assert gen["tool"] == "KnownValueAssigner"
            assert "version" in gen

            # Validate entries
            assert len(registry["entries"]) == 1
            entry = registry["entries"][0]
            assert entry["codepoint"] == 1000
            assert entry["name"] == "Thing"
            assert entry["type"] == "class"
            assert entry["uri"] == "http://example.org/Thing"
            assert entry["description"] == "A generic thing"

            # Validate statistics
            stats = registry["statistics"]
            assert stats["total_entries"] == 1
            assert stats["code_point_range"]["start"] == 1000
            assert stats["code_point_range"]["end"] == 1000


class TestCLIInterface:
    """Tests for command-line interface."""

    def test_list_option(self, capsys):
        """Test --list option prints available ontologies."""
        from known_value_assigner import list_ontologies
        list_ontologies()
        captured = capsys.readouterr()

        assert "Available Ontologies" in captured.out
        assert "rdf" in captured.out.lower()
        assert "owl" in captured.out.lower()
        assert "schema" in captured.out.lower()

    def test_invalid_ontology_id(self):
        """Test that invalid ontology ID is handled."""
        from known_value_assigner import get_ontology_by_id
        result = get_ontology_by_id("nonexistent_ontology")
        assert result is None

    def test_all_configs_processable(self):
        """Verify all configured ontologies have valid configurations."""
        for config in ONTOLOGY_CONFIGS:
            # Each config should have required fields
            assert config.name, f"Config missing name"
            assert config.source_url, f"{config.name} missing source_url"
            assert config.start_code_point > 0, f"{config.name} has invalid start_code_point"
            assert config.data_format is not None, f"{config.name} missing data_format"
            assert config.strategy is not None, f"{config.name} missing strategy"


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    @patch('requests.get')
    def test_malformed_rdf_graceful_failure(self, mock_get):
        """Test that malformed RDF is handled gracefully."""
        mock_response = Mock()
        mock_response.text = "This is not valid RDF/XML content"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="broken",
                source_url="http://example.org/broken.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            # Should return None (failure) rather than crashing
            entries = assigner.process_ontology(config)
            assert entries is None

    @patch('requests.get')
    def test_empty_ontology(self, mock_get):
        """Test handling of empty ontology."""
        mock_response = Mock()
        mock_response.text = """<?xml version="1.0" encoding="utf-8"?>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        </rdf:RDF>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            assigner = KnownValueAssigner(
                output_dir=Path(tmpdir),
                cache_dir=Path(tmpdir) / "cache",
            )

            config = OntologyConfig(
                name="empty",
                source_url="http://example.org/empty.rdf",
                start_code_point=1000,
                data_format=DataFormat.RDF_XML,
                strategy=ProcessingStrategy.STANDARD_RDF,
            )

            entries = assigner.process_ontology(config)
            assert entries is not None
            assert len(entries) == 0  # Empty but valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
