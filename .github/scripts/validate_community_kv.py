#!/usr/bin/env python3
"""
Validate Community Known Values Request Files

This script validates JSON request files for community Known Value assignments.
It checks schema conformance, code point availability, and uniqueness constraints.

Usage:
    python validate_community_kv.py --registry <path> --files <file1> [file2 ...]
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# JSON Schema for request files (embedded)
REQUEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["request", "entries"],
    "properties": {
        "request": {
            "type": "object",
            "required": ["submitter", "description", "contact"],
            "properties": {
                "submitter": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 1},
                "contact": {"type": "string", "minLength": 1},
                "url": {"type": "string"},
            },
        },
        "entries": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["codepoint", "canonical_name", "type", "description"],
                "properties": {
                    "codepoint": {"type": "integer", "minimum": 100000},
                    "canonical_name": {"type": "string", "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$"},
                    "type": {"type": "string", "enum": ["class", "property", "datatype", "constant"]},
                    "uri": {"type": "string"},
                    "description": {"type": "string", "minLength": 10},
                },
            },
        },
    },
}

CANONICAL_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
VALID_TYPES = {"class", "property", "datatype", "constant"}
MIN_CODEPOINT = 100000


@dataclass
class ValidationError:
    """Represents a single validation error."""

    rule_id: str
    file_path: str
    message: str
    entry_index: int | None = None
    field: str | None = None


@dataclass
class ValidationResult:
    """Aggregates validation results."""

    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(
        self,
        rule_id: str,
        file_path: str,
        message: str,
        entry_index: int | None = None,
        field: str | None = None,
    ):
        self.errors.append(ValidationError(rule_id, file_path, message, entry_index, field))

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def load_registry(registry_path: Path) -> dict[str, Any]:
    """Load the community registry JSON file."""
    if not registry_path.exists():
        return {"entries": []}
    with open(registry_path) as f:
        return json.load(f)


def get_assigned_codepoints(registry: dict[str, Any]) -> set[int]:
    """Extract all assigned code points from the registry."""
    return {entry["codepoint"] for entry in registry.get("entries", [])}


def get_assigned_names(registry: dict[str, Any]) -> set[str]:
    """Extract all assigned canonical names from the registry."""
    return {entry["canonical_name"] for entry in registry.get("entries", [])}


def get_assigned_uris(registry: dict[str, Any]) -> set[str]:
    """Extract all assigned URIs from the registry."""
    return {entry["uri"] for entry in registry.get("entries", []) if entry.get("uri")}


def validate_json_syntax(file_path: Path, result: ValidationResult) -> dict[str, Any] | None:
    """V-001: Validate that the file contains valid JSON."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        result.add_error("V-001", str(file_path), f"Invalid JSON: {e}")
        return None
    except OSError as e:
        result.add_error("V-001", str(file_path), f"Cannot read file: {e}")
        return None


def validate_schema(data: dict[str, Any], file_path: str, result: ValidationResult) -> bool:
    """V-002: Validate JSON structure against schema."""
    # Check required top-level keys
    if "request" not in data:
        result.add_error("V-002", file_path, "Missing required field: 'request'")
        return False
    if "entries" not in data:
        result.add_error("V-002", file_path, "Missing required field: 'entries'")
        return False

    # Validate request section
    request = data.get("request", {})
    for required_field in ["submitter", "description", "contact"]:
        if required_field not in request:
            result.add_error(
                "V-002", file_path, f"Missing required field in 'request': '{required_field}'"
            )
            return False

    # Validate entries array
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        result.add_error("V-002", file_path, "'entries' must be an array")
        return False
    if len(entries) == 0:
        result.add_error("V-002", file_path, "'entries' must contain at least one entry")
        return False

    # Validate each entry has required fields
    valid = True
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            result.add_error("V-002", file_path, f"Entry {i} must be an object", entry_index=i)
            valid = False
            continue
        for required_field in ["codepoint", "canonical_name", "type", "description"]:
            if required_field not in entry:
                result.add_error(
                    "V-002",
                    file_path,
                    f"Missing required field: '{required_field}'",
                    entry_index=i,
                    field=required_field,
                )
                valid = False

    return valid


def validate_canonical_names(
    entries: list[dict[str, Any]], file_path: str, result: ValidationResult
):
    """V-003: Validate canonical_name format."""
    for i, entry in enumerate(entries):
        name = entry.get("canonical_name", "")
        if not CANONICAL_NAME_PATTERN.match(name):
            result.add_error(
                "V-003",
                file_path,
                f"Invalid canonical_name '{name}': must match ^[a-zA-Z][a-zA-Z0-9_]*$",
                entry_index=i,
                field="canonical_name",
            )


def validate_types(entries: list[dict[str, Any]], file_path: str, result: ValidationResult):
    """V-004: Validate type values."""
    for i, entry in enumerate(entries):
        entry_type = entry.get("type", "")
        if entry_type not in VALID_TYPES:
            result.add_error(
                "V-004",
                file_path,
                f"Invalid type '{entry_type}': must be one of {sorted(VALID_TYPES)}",
                entry_index=i,
                field="type",
            )


def validate_descriptions(entries: list[dict[str, Any]], file_path: str, result: ValidationResult):
    """V-005: Validate description length."""
    for i, entry in enumerate(entries):
        desc = entry.get("description", "")
        if len(desc) < 10:
            result.add_error(
                "V-005",
                file_path,
                f"Description too short ({len(desc)} chars): must be at least 10 characters",
                entry_index=i,
                field="description",
            )


def validate_codepoint_required(
    entries: list[dict[str, Any]], file_path: str, result: ValidationResult
):
    """V-100: Each entry must specify a codepoint."""
    for i, entry in enumerate(entries):
        if "codepoint" not in entry:
            result.add_error(
                "V-100",
                file_path,
                "Missing required field: 'codepoint'",
                entry_index=i,
                field="codepoint",
            )


def validate_codepoint_minimum(
    entries: list[dict[str, Any]], file_path: str, result: ValidationResult
):
    """V-101: Each codepoint must be >= 100,000."""
    for i, entry in enumerate(entries):
        codepoint = entry.get("codepoint")
        if codepoint is not None and codepoint < MIN_CODEPOINT:
            result.add_error(
                "V-101",
                file_path,
                f"Codepoint {codepoint} is less than minimum ({MIN_CODEPOINT})",
                entry_index=i,
                field="codepoint",
            )


def validate_codepoint_availability(
    entries: list[dict[str, Any]],
    file_path: str,
    assigned_codepoints: set[int],
    result: ValidationResult,
):
    """V-102: Each codepoint must not already be assigned."""
    for i, entry in enumerate(entries):
        codepoint = entry.get("codepoint")
        if codepoint is not None and codepoint in assigned_codepoints:
            result.add_error(
                "V-102",
                file_path,
                f"Codepoint {codepoint} is already assigned in the registry",
                entry_index=i,
                field="codepoint",
            )


def validate_codepoint_uniqueness_within_request(
    entries: list[dict[str, Any]], file_path: str, result: ValidationResult
):
    """V-103: Code points must not conflict within the same request."""
    seen_codepoints: dict[int, int] = {}
    for i, entry in enumerate(entries):
        codepoint = entry.get("codepoint")
        if codepoint is None:
            continue
        if codepoint in seen_codepoints:
            result.add_error(
                "V-103",
                file_path,
                f"Codepoint {codepoint} is duplicated (also in entry {seen_codepoints[codepoint]})",
                entry_index=i,
                field="codepoint",
            )
        else:
            seen_codepoints[codepoint] = i


def validate_name_availability(
    entries: list[dict[str, Any]],
    file_path: str,
    assigned_names: set[str],
    result: ValidationResult,
):
    """V-200: canonical_name must not already exist in the registry."""
    for i, entry in enumerate(entries):
        name = entry.get("canonical_name", "")
        if name in assigned_names:
            result.add_error(
                "V-200",
                file_path,
                f"Canonical name '{name}' is already assigned in the registry",
                entry_index=i,
                field="canonical_name",
            )


def validate_uri_availability(
    entries: list[dict[str, Any]],
    file_path: str,
    assigned_uris: set[str],
    result: ValidationResult,
):
    """V-201: uri (if provided) must not already exist in the registry."""
    for i, entry in enumerate(entries):
        uri = entry.get("uri")
        if uri and uri in assigned_uris:
            result.add_error(
                "V-201",
                file_path,
                f"URI '{uri}' is already assigned in the registry",
                entry_index=i,
                field="uri",
            )


def validate_name_uniqueness_within_request(
    entries: list[dict[str, Any]], file_path: str, result: ValidationResult
):
    """V-202: canonical_name values must be unique within the request."""
    seen_names: dict[str, int] = {}
    for i, entry in enumerate(entries):
        name = entry.get("canonical_name", "")
        if name in seen_names:
            result.add_error(
                "V-202",
                file_path,
                f"Canonical name '{name}' is duplicated (also in entry {seen_names[name]})",
                entry_index=i,
                field="canonical_name",
            )
        else:
            seen_names[name] = i


def validate_request_file(
    file_path: Path,
    assigned_codepoints: set[int],
    assigned_names: set[str],
    assigned_uris: set[str],
    result: ValidationResult,
):
    """Validate a single request file against all rules."""
    # V-001: Parse JSON
    data = validate_json_syntax(file_path, result)
    if data is None:
        return

    file_str = str(file_path)

    # V-002: Schema validation
    if not validate_schema(data, file_str, result):
        return

    entries = data.get("entries", [])

    # V-003: canonical_name format
    validate_canonical_names(entries, file_str, result)

    # V-004: type values
    validate_types(entries, file_str, result)

    # V-005: description length
    validate_descriptions(entries, file_str, result)

    # V-100: codepoint required
    validate_codepoint_required(entries, file_str, result)

    # V-101: codepoint minimum
    validate_codepoint_minimum(entries, file_str, result)

    # V-102: codepoint availability
    validate_codepoint_availability(entries, file_str, assigned_codepoints, result)

    # V-103: codepoint uniqueness within request
    validate_codepoint_uniqueness_within_request(entries, file_str, result)

    # V-200: name availability
    validate_name_availability(entries, file_str, assigned_names, result)

    # V-201: uri availability
    validate_uri_availability(entries, file_str, assigned_uris, result)

    # V-202: name uniqueness within request
    validate_name_uniqueness_within_request(entries, file_str, result)


def generate_report(result: ValidationResult, files: list[str]) -> str:
    """Generate a Markdown validation report."""
    lines = []

    if result.is_valid:
        lines.append("## Validation Results\n")
        lines.append(f"✅ **All {len(files)} file(s) passed validation.**\n")
        lines.append("\n### Files Validated\n")
        for f in files:
            lines.append(f"- `{f}`")
    else:
        lines.append("## Validation Results\n")
        lines.append(f"❌ **Validation failed with {len(result.errors)} error(s).**\n")
        lines.append("\n### Errors\n")
        for err in result.errors:
            entry_info = f", entry[{err.entry_index}]" if err.entry_index is not None else ""
            field_info = f", field `{err.field}`" if err.field else ""
            lines.append(f"- **{err.rule_id}**: `{err.file_path}`{entry_info}{field_info}")
            lines.append(f"  - {err.message}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate Community Known Values requests")
    parser.add_argument(
        "--registry",
        type=Path,
        required=True,
        help="Path to the community registry JSON file",
    )
    parser.add_argument(
        "--files",
        type=str,
        required=True,
        help="Space-separated list of request files to validate",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("validation_report.md"),
        help="Path to write the validation report",
    )

    args = parser.parse_args()

    # Parse file list
    files = [f.strip() for f in args.files.split() if f.strip()]
    if not files:
        print("No files to validate.")
        sys.exit(0)

    # Load registry
    registry = load_registry(args.registry)
    assigned_codepoints = get_assigned_codepoints(registry)
    assigned_names = get_assigned_names(registry)
    assigned_uris = get_assigned_uris(registry)

    # Validate each file
    result = ValidationResult()
    for file_str in files:
        file_path = Path(file_str)
        if not file_path.exists():
            result.add_error("V-001", file_str, f"File does not exist: {file_str}")
            continue
        validate_request_file(file_path, assigned_codepoints, assigned_names, assigned_uris, result)

    # Generate report
    report = generate_report(result, files)
    args.report.write_text(report)
    print(report)

    # Exit with appropriate code
    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
