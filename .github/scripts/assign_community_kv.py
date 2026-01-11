#!/usr/bin/env python3
"""
Assign Community Known Values to the Registry

This script processes validated request files and adds entries to the community registry.
It assumes validation has already passed (code points are valid and available).

Usage:
    python assign_community_kv.py --registry <json_path> --markdown <md_path> --files <file1> [file2 ...] --pr <number>
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_registry(registry_path: Path) -> dict[str, Any]:
    """Load the community registry JSON file."""
    if not registry_path.exists():
        return {
            "ontology": {
                "name": "community_registry",
                "start_code_point": 100000,
                "processing_strategy": "Custom",
            },
            "generated": {
                "tool": "CommunityValueAssigner",
                "version": "1.0.0",
            },
            "entries": [],
        }
    with open(registry_path) as f:
        return json.load(f)


def load_request_file(file_path: Path) -> dict[str, Any] | None:
    """Load a request JSON file."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return None


def add_entries_to_registry(
    registry: dict[str, Any],
    request_data: dict[str, Any],
    pr_number: int | None,
) -> int:
    """Add entries from a request to the registry. Returns count of entries added."""
    request_info = request_data.get("request", {})
    entries = request_data.get("entries", [])
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    added = 0
    for entry in entries:
        registry_entry = {
            "codepoint": entry["codepoint"],
            "name": entry["name"],
            "type": entry["type"],
            "description": entry["description"],
            "source": {
                "submitter": request_info.get("submitter", "Unknown"),
                "assigned_date": today,
            },
        }

        # Add optional fields
        if entry.get("uri"):
            registry_entry["uri"] = entry["uri"]
        if pr_number:
            registry_entry["source"]["pr_number"] = pr_number
        if request_info.get("contact"):
            registry_entry["source"]["contact"] = request_info["contact"]
        if request_info.get("url"):
            registry_entry["source"]["url"] = request_info["url"]

        registry["entries"].append(registry_entry)
        added += 1

    return added


def sort_entries(registry: dict[str, Any]):
    """Sort registry entries by code point."""
    registry["entries"].sort(key=lambda e: e["codepoint"])


def update_metadata(registry: dict[str, Any]):
    """Update registry metadata (timestamp)."""
    registry["generated"]["last_updated"] = datetime.now(timezone.utc).isoformat()


def compute_statistics(registry: dict[str, Any]) -> dict[str, Any]:
    """Compute statistics for the registry."""
    entries = registry.get("entries", [])
    if not entries:
        return {
            "total_entries": 0,
            "code_point_range": {"start": 100000, "end": None},
        }

    codepoints = [e["codepoint"] for e in entries]
    return {
        "total_entries": len(entries),
        "code_point_range": {
            "start": min(codepoints),
            "end": max(codepoints),
        },
    }


def save_registry(registry: dict[str, Any], registry_path: Path):
    """Save the registry to JSON file."""
    # Add statistics
    registry["statistics"] = compute_statistics(registry)

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")


def generate_markdown(registry: dict[str, Any], markdown_path: Path):
    """Generate Markdown version of the registry."""
    lines = []

    # Header
    lines.append("# Community Known Values Registry\n")

    # Ontology Information
    ontology = registry.get("ontology", {})
    lines.append("## Ontology Information\n")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    lines.append(f"| **Name** | {ontology.get('name', 'community')} |")
    lines.append(f"| **Start Code Point** | {ontology.get('start_code_point', 100000)} |")
    lines.append(f"| **Processing Strategy** | {ontology.get('processing_strategy', 'Custom')} |")
    lines.append("")

    # Statistics
    stats = registry.get("statistics", compute_statistics(registry))
    generated = registry.get("generated", {})
    lines.append("## Statistics\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| **Total Entries** | {stats.get('total_entries', 0)} |")

    code_range = stats.get("code_point_range", {})
    range_start = code_range.get("start", 100000)
    range_end = code_range.get("end")
    range_str = f"{range_start} - {range_end}" if range_end else f"{range_start} - ..."
    lines.append(f"| **Code Point Range** | {range_str} |")

    last_updated = generated.get("last_updated", "")
    if last_updated:
        # Format as date only
        date_str = last_updated.split("T")[0] if "T" in last_updated else last_updated
        lines.append(f"| **Last Updated** | {date_str} |")
    lines.append("")

    # Entries
    lines.append("## Entries\n")
    entries = registry.get("entries", [])

    if entries:
        lines.append("| Codepoint | Canonical Name | Type | URI | Description | Submitter |")
        lines.append("|-----------|----------------|------|-----|-------------|-----------|")

        for entry in entries:
            codepoint = entry.get("codepoint", "")
            name = entry.get("name", "")
            entry_type = entry.get("type", "")
            uri = entry.get("uri", "")
            description = entry.get("description", "")
            source = entry.get("source", {})
            submitter = source.get("submitter", "")

            # Escape pipe characters in description
            description = description.replace("|", "\\|")

            lines.append(f"| {codepoint} | {name} | {entry_type} | {uri} | {description} | {submitter} |")
    else:
        lines.append("| Codepoint | Canonical Name | Type | URI | Description | Submitter |")
        lines.append("|-----------|----------------|------|-----|-------------|-----------|")
        lines.append("")
        lines.append("*No entries yet.*")

    lines.append("")

    with open(markdown_path, "w") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Assign Community Known Values to registry")
    parser.add_argument(
        "--registry",
        type=Path,
        required=True,
        help="Path to the community registry JSON file",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        required=True,
        help="Path to the community registry Markdown file",
    )
    parser.add_argument(
        "--files",
        type=str,
        required=True,
        help="Space-separated list of request files to process",
    )
    parser.add_argument(
        "--pr",
        type=int,
        default=None,
        help="PR number for provenance tracking",
    )

    args = parser.parse_args()

    # Parse file list
    files = [f.strip() for f in args.files.split() if f.strip()]
    if not files:
        print("No files to process.")
        sys.exit(0)

    # Load registry
    registry = load_registry(args.registry)

    # Process each request file
    total_added = 0
    for file_str in files:
        file_path = Path(file_str)
        if not file_path.exists():
            print(f"Warning: File does not exist: {file_str}", file=sys.stderr)
            continue

        request_data = load_request_file(file_path)
        if request_data is None:
            continue

        added = add_entries_to_registry(registry, request_data, args.pr)
        total_added += added
        print(f"Added {added} entries from {file_path}")

    if total_added == 0:
        print("No entries were added.")
        sys.exit(0)

    # Sort entries
    sort_entries(registry)

    # Update metadata
    update_metadata(registry)

    # Save registry
    save_registry(registry, args.registry)
    print(f"Saved registry to {args.registry}")

    # Generate Markdown
    generate_markdown(registry, args.markdown)
    print(f"Generated Markdown at {args.markdown}")

    print(f"Successfully added {total_added} entries to the community registry.")


if __name__ == "__main__":
    main()
