# Community Known Values

This directory manages community-submitted Known Value assignments. Known Values are 64-bit unsigned integers representing ontological concepts, with the community namespace starting at code point 100,000.

## How to Submit a Request

1. **Create a JSON file** in the `requests/` directory following the naming convention: `<submitter>_<description>.json`
2. **Choose your code points** — each entry must specify a `codepoint` value ≥ 100,000 that is not already assigned
3. **Submit a Pull Request** with your request file(s)

Your PR will be automatically validated. If validation passes and the PR is merged, the code points will be registered in the community registry.

## JSON Schema

Each request file must conform to this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["request", "entries"],
  "properties": {
    "request": {
      "type": "object",
      "required": ["submitter", "description", "contact"],
      "properties": {
        "submitter": {
          "type": "string",
          "description": "Name or organization of the submitter"
        },
        "description": {
          "type": "string",
          "description": "Brief description of the request purpose"
        },
        "contact": {
          "type": "string",
          "description": "Email or GitHub handle for contact"
        },
        "url": {
          "type": "string",
          "format": "uri",
          "description": "Optional URL to documentation or specification"
        }
      }
    },
    "entries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["codepoint", "canonical_name", "type", "description"],
        "properties": {
          "codepoint": {
            "type": "integer",
            "minimum": 100000,
            "description": "The requested code point (must be ≥ 100,000 and not already assigned)"
          },
          "canonical_name": {
            "type": "string",
            "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$",
            "description": "CamelCase or snake_case identifier"
          },
          "type": {
            "type": "string",
            "enum": ["class", "property", "datatype", "constant"],
            "description": "The semantic type of this concept"
          },
          "uri": {
            "type": "string",
            "format": "uri",
            "description": "Optional authoritative URI for this concept"
          },
          "description": {
            "type": "string",
            "minLength": 10,
            "description": "Human-readable description (minimum 10 characters)"
          }
        }
      }
    }
  }
}
```

## Example Request File

```json
{
  "request": {
    "submitter": "Example Organization",
    "description": "Custom credential types for our attestation framework",
    "contact": "@exampleorg",
    "url": "https://example.org/specs/credentials"
  },
  "entries": [
    {
      "codepoint": 100500,
      "canonical_name": "employmentCredential",
      "type": "class",
      "uri": "https://example.org/credentials#EmploymentCredential",
      "description": "A verifiable credential asserting current or past employment status"
    },
    {
      "codepoint": 100501,
      "canonical_name": "employerName",
      "type": "property",
      "description": "The name of the employer issuing an employment credential"
    }
  ]
}
```

See [requests/_example_template.json](requests/_example_template.json) for a complete template.

## Field Reference

### Request Section (required)

| Field         | Required | Description                              |
| ------------- | -------- | ---------------------------------------- |
| `submitter`   | Yes      | Your name or organization                |
| `description` | Yes      | Brief description of the request purpose |
| `contact`     | Yes      | GitHub handle or email for contact       |
| `url`         | No       | Link to documentation or specification   |

### Entry Fields

| Field            | Required | Description                                         |
| ---------------- | -------- | --------------------------------------------------- |
| `codepoint`      | Yes      | Integer ≥ 100,000 (must not be already assigned)    |
| `canonical_name` | Yes      | Identifier matching `^[a-zA-Z][a-zA-Z0-9_]*$`       |
| `type`           | Yes      | One of: `class`, `property`, `datatype`, `constant` |
| `description`    | Yes      | Human-readable description (minimum 10 characters)  |
| `uri`            | No       | Authoritative URI for this concept                  |

## Validation

Your PR will be automatically validated. The validation checks:

- JSON syntax
- Schema conformance
- Code point validity (≥ 100,000)
- Code point availability (not already assigned)
- Uniqueness (no duplicate names, URIs, or code points within request)

If validation fails, fix the errors indicated in the PR comment and push again.

## Code Point Ranges

Organizations are encouraged to claim a contiguous range for their concepts to avoid fragmentation. Check the [community registry](../known-value-assignments/markdown/100000_community_registry.md) to see which code points are already assigned.

## Additional Documentation

For the full technical specification including workflow architecture and validation rules, see [Spec.md](Spec.md).
