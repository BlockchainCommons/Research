# Community Known Values Request Directory

This directory contains request files for community-assigned Known Values.

## How to Submit a Request

1. **Create a JSON file** following the naming convention: `<submitter>_<description>.json`
2. **Follow the schema** defined in [../Spec.md](../Spec.md)
3. **Choose your code points** - each entry must specify a `codepoint` value ≥ 100,000
4. **Submit a Pull Request** with your request file(s)

## Request File Format

```json
{
  "request": {
    "submitter": "Your Name or Organization",
    "description": "Brief description of these Known Values",
    "contact": "@your-github-handle or email",
    "url": "https://optional-link-to-your-spec.org"
  },
  "entries": [
    {
      "codepoint": 100500,
      "canonical_name": "yourConceptName",
      "type": "class",
      "uri": "https://your-domain.org/ontology#YourConcept",
      "description": "Description of this concept (minimum 10 characters)"
    }
  ]
}
```

## Required Fields

### Request Section
- `submitter` - Your name or organization
- `description` - Brief description of the request purpose
- `contact` - GitHub handle or email for contact

### Entry Fields
- `codepoint` - Integer ≥ 100,000 (must not be already assigned)
- `canonical_name` - Identifier matching `^[a-zA-Z][a-zA-Z0-9_]*$`
- `type` - One of: `class`, `property`, `datatype`, `constant`
- `description` - Human-readable description (minimum 10 characters)

### Optional Fields
- `url` (in request) - Link to documentation or specification
- `uri` (in entry) - Authoritative URI for this concept

## Validation

Your PR will be automatically validated. The validation checks:

- JSON syntax
- Schema conformance
- Code point availability (≥ 100,000 and not already assigned)
- Uniqueness (no duplicate names, URIs, or code points)

If validation fails, fix the errors and push again.

## Example

See [_example_template.json](./_example_template.json) for a complete example.

## Code Point Ranges

Organizations are encouraged to claim a range for their concepts. For example:
- 100,000 - 100,999: Reserved for examples
- 101,000 - 101,999: Organization A
- 102,000 - 102,999: Organization B

Coordinate with the community to avoid conflicts when choosing your range.
