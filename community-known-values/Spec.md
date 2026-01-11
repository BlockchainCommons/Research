# Community Known Values Assigner Specification

## 1. Overview

This document specifies a GitHub Actions workflow that automates the validation, merging, and assignment of community-requested Known Values. Community members submit requests via pull requests containing JSON files in `community-known-values/requests/`. Upon successful validation and merge, the workflow assigns code points and updates the community registry files.

### 1.1 Background

Known Values are 64-bit unsigned integers that represent ontological concepts, as defined in [BCR-2023-002](../papers/bcr-2023-002-known-value.md). The namespace is partitioned as follows:

| Range         | Registry            | Description                             |
| ------------- | ------------------- | --------------------------------------- |
| 0 – 999       | Blockchain Commons  | Core reserved values (manually curated) |
| 1000 – 99,999 | Standard Ontologies | RDF, OWL, DC, FOAF, Schema.org, etc.    |
| **100,000+**  | **Community**       | User-submitted custom concepts          |

The `known-values-assigner` tool processes standard Semantic Web ontologies and assigns code points deterministically. This specification defines a separate, automated process for community submissions that:

1. Validates submitted JSON request files (including that each requested code point is ≥ 100,000 and not already assigned)
2. Rejects invalid requests with clear error messages
3. Merges valid PRs automatically
4. Registers the requested code points in the community registry
5. Updates the `100000_community_registry.json` and `100000_community_registry.md` files

**Note:** Unlike the standard ontology assigner, the community process does *not* assign code points automatically. Submitters must specify the exact code point for each entry. This allows organizations to manage their own sub-ranges within the community namespace.

---

## 2. Request Schema

### 2.1 File Location

Community requests must be submitted as JSON files in the [BlockchainCommons/Research](https://github.com/BlockchainCommons/Research) repository:

```
community-known-values/requests/
```

### 2.2 File Naming Convention

Request files must follow the pattern:

```
yyyymmdd_<short_description>.json
```

Where `yyyymmdd` is the submission date (e.g., `20260107` for January 7, 2026). This ensures request files are sorted chronologically.

Examples:
- `20260107_credential_types.json`
- `20260115_payment_terms.json`

**Note:** The date is validated with ±1 day tolerance to account for timezone differences.

### 2.3 JSON Schema

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
        "required": ["codepoint", "name", "type", "description"],
        "properties": {
          "codepoint": {
            "type": "integer",
            "minimum": 100000,
            "description": "The requested code point (must be ≥ 100,000 and not already assigned)"
          },
          "name": {
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

### 2.4 Example Request File

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
      "name": "employmentCredential",
      "type": "class",
      "uri": "https://example.org/credentials#EmploymentCredential",
      "description": "A verifiable credential asserting current or past employment status"
    },
    {
      "codepoint": 100501,
      "name": "employerName",
      "type": "property",
      "description": "The name of the employer issuing an employment credential"
    },
    {
      "codepoint": 100502,
      "name": "employmentStartDate",
      "type": "property",
      "uri": "https://example.org/credentials#employmentStartDate",
      "description": "The date on which employment began"
    }
  ]
}
```

---

## 3. Validation Rules

The workflow must validate each request against the following rules. A PR is rejected if any rule fails.

### 3.1 Schema Validation

| Rule ID | Description                                                        |
| ------- | ------------------------------------------------------------------ |
| V-001   | File must be valid JSON                                            |
| V-002   | JSON must conform to the schema in §2.3                            |
| V-003   | `name` must match `^[a-zA-Z][a-zA-Z0-9_:]*$`              |
| V-004   | `type` must be one of: `class`, `property`, `datatype`, `constant` |
| V-005   | `description` must be at least 10 characters                       |
| V-006   | Filename must start with date in `yyyymmdd_` format (±1 day)       |

### 3.2 Code Point Rules

| Rule ID | Description                                                             |
| ------- | ----------------------------------------------------------------------- |
| V-100   | Each entry must specify a `codepoint`                                   |
| V-101   | Each `codepoint` must be ≥ 100,000                                      |
| V-102   | Each `codepoint` must not already be assigned in the community registry |
| V-103   | Code points must not conflict with other entries in the same request    |

### 3.3 Uniqueness Rules

| Rule ID | Description                                                          |
| ------- | -------------------------------------------------------------------- |
| V-200   | `name` must not already exist in the community registry    |
| V-201   | `uri` (if provided) must not already exist in the community registry |
| V-202   | `name` values must be unique within the request file       |

### 3.4 Path Rules

| Rule ID | Description                                                         |
| ------- | ------------------------------------------------------------------- |
| V-300   | PR must only add/modify files in `community-known-values/requests/` |
| V-301   | PR must not delete or modify existing request files                 |
| V-302   | PR must not modify files outside the requests directory             |

---

## 4. GitHub Actions Workflow Architecture

### 4.1 Workflow Trigger Strategy

The workflow uses a two-phase approach for security and capability reasons:

**Phase 1: Validation (`pull_request` event)**
- Triggers on PR opened/synchronized targeting `main`/`master`
- Runs validation in the context of the PR
- Has read-only access (safe for forks)
- Reports validation results as PR checks

**Phase 2: Assignment (`pull_request_target` + `closed` with `merged == true`)**
- Triggers only when a PR is merged to the default branch
- Runs in the context of the base repository
- Has write access to commit registry updates
- Processes merged request files and updates the community registry

### 4.2 Workflow File Structure

Two workflow files are required:

```
.github/workflows/
├── community-kv-validate.yml    # Phase 1: Validation
└── community-kv-assign.yml      # Phase 2: Assignment after merge
```

### 4.3 Security Considerations

| Concern                             | Mitigation                                                                         |
| ----------------------------------- | ---------------------------------------------------------------------------------- |
| Fork PRs executing malicious code   | Validation uses `pull_request` (not `pull_request_target`) for untrusted code      |
| Unauthorized registry modifications | Assignment only runs on merged PRs with `pull_request_target`                      |
| Token permission scope              | Minimal permissions: `contents: write`, `pull-requests: read` only when needed     |
| Branch protection bypass            | Workflow commits to a temporary branch, then creates a follow-up PR or direct push |

---

## 5. Phase 1: Validation Workflow

### 5.1 Trigger Configuration

```yaml
name: Validate Community Known Values Request

on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - 'community-known-values/requests/**/*.json'

permissions:
  contents: read
  pull-requests: write
```

### 5.2 Validation Steps

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout PR head
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install jsonschema

      - name: Get changed files
        id: changed
        uses: tj-actions/changed-files@v44
        with:
          files: |
            community-known-values/requests/**/*.json

      - name: Validate request files
        id: validate
        run: |
          python .github/scripts/validate_community_kv.py \
            --registry known-value-assignments/json/100000_community_registry.json \
            --files "${{ steps.changed.outputs.all_changed_files }}"
        continue-on-error: true

      - name: Post validation results
        uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            const result = '${{ steps.validate.outcome }}';
            const output = fs.existsSync('validation_report.md')
              ? fs.readFileSync('validation_report.md', 'utf8')
              : 'Validation completed.';

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: result === 'success'
                ? `✅ **Validation Passed**\n\n${output}`
                : `❌ **Validation Failed**\n\n${output}`
            });

      - name: Fail if validation failed
        if: steps.validate.outcome == 'failure'
        run: exit 1
```

### 5.3 Validation Script (`validate_community_kv.py`)

The validation script must:

1. Load the JSON schema from embedded definition or external file
2. Load the current community registry for uniqueness checks
3. For each changed JSON file:
   - Parse and validate against schema
   - Check code point constraints
   - Check uniqueness constraints
   - Accumulate errors with file/line references
4. Generate a Markdown report (`validation_report.md`)
5. Exit with code 0 on success, 1 on failure

---

## 6. Phase 2: Assignment Workflow

### 6.1 Trigger Configuration

```yaml
name: Assign Community Known Values

on:
  pull_request_target:
    types: [closed]
    paths:
      - 'community-known-values/requests/**/*.json'

permissions:
  contents: write
  pull-requests: read
```

### 6.2 Assignment Preconditions

The workflow must verify:

```yaml
jobs:
  assign:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
```

### 6.3 Assignment Steps

```yaml
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.ref }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install jsonschema

      - name: Get merged request files
        id: merged
        run: |
          # Get list of JSON files added in the merged PR
          FILES=$(git diff --name-only --diff-filter=A \
            ${{ github.event.pull_request.base.sha }} \
            ${{ github.event.pull_request.merge_commit_sha }} \
            -- 'community-known-values/requests/*.json')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: Assign code points and update registry
        id: assign
        run: |
          python .github/scripts/assign_community_kv.py \
            --registry known-value-assignments/json/100000_community_registry.json \
            --markdown known-value-assignments/markdown/100000_community_registry.md \
            --files "${{ steps.merged.outputs.files }}"

      - name: Commit and push registry updates
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add known-value-assignments/
          git commit -m "Assign community Known Values from PR #${{ github.event.pull_request.number }}"
          git push
```

### 6.4 Assignment Script (`assign_community_kv.py`)

The assignment script must:

1. Load the current community registry
2. For each request file:
   - Parse entries (each entry already has its `codepoint` specified)
   - Add entries to registry with the specified code points
3. Sort entries by code point
4. Update statistics in the registry metadata
5. Write updated JSON registry
6. Regenerate Markdown registry from JSON

**Note:** Since validation already confirmed all code points are valid and available, the assignment script does not need to perform code point allocation—it simply records the pre-specified values.

---

## 7. Output File Formats

### 7.1 JSON Registry Update

The `100000_community_registry.json` must maintain this structure:

```json
{
  "ontology": {
    "name": "community_registry",
    "start_code_point": 100000,
    "processing_strategy": "Custom"
  },
  "generated": {
    "tool": "CommunityValueAssigner",
    "version": "1.0.0",
    "last_updated": "2025-01-07T12:00:00Z"
  },
  "entries": [
    {
      "codepoint": 100000,
      "name": "exampleConcept",
      "type": "class",
      "uri": "https://example.org/concepts#Example",
      "description": "An example community-assigned concept",
      "source": {
        "submitter": "Example Org",
        "pr_number": 123,
        "assigned_date": "2025-01-07"
      }
    }
  ],
  "statistics": {
    "total_entries": 1,
    "code_point_range": {
      "start": 100000,
      "end": 100000
    }
  }
}
```

### 7.2 Markdown Registry Update

The `100000_community_registry.md` must be regenerated with this format:

```markdown
# Community Known Values Registry

## Ontology Information

| Property                | Value     |
| ----------------------- | --------- |
| **Name**                | community |
| **Start Code Point**    | 100000    |
| **Processing Strategy** | Custom    |

## Statistics

| Metric               | Value           |
| -------------------- | --------------- |
| **Total Entries**    | N               |
| **Code Point Range** | 100000 - NNNNNN |
| **Last Updated**     | YYYY-MM-DD      |

## Entries

| Codepoint | Canonical Name | Type  | URI         | Description    | Submitter |
| --------- | -------------- | ----- | ----------- | -------------- | --------- |
| 100000    | exampleConcept | class | https://... | Description... | @user     |
```

---

## 8. Error Handling

### 8.1 Validation Error Messages

Errors must be reported with:
- Rule ID (e.g., V-101)
- File path
- Entry index or field name
- Human-readable explanation

Example:
```
❌ V-101: File `alice_concepts.json`, entry[2]:
   Requested codepoint 100005 is already assigned to `existingConcept`.
```

### 8.2 Assignment Failure Recovery

If assignment fails:
1. No partial commits should be made
2. An issue should be opened automatically (or PR comment added)
3. Manual intervention should be documented

### 8.3 Conflict Resolution

If a race condition causes code point conflicts:
1. The assignment script must re-read the registry before writing
2. Code points should be re-assigned if conflicts are detected
3. A warning should be logged

---

## 9. Branch Protection Requirements

For this workflow to function correctly, the repository must configure:

| Setting                           | Value              | Reason                         |
| --------------------------------- | ------------------ | ------------------------------ |
| Require status checks             | `validate` job     | Prevents merge of invalid PRs  |
| Require branches to be up to date | Yes                | Ensures latest registry state  |
| Allow auto-merge                  | Optional           | Enables maintainer convenience |
| Restrict who can push             | Maintainers + bots | Protects registry integrity    |

---

## 10. Alternative Approach: Maintainer-Triggered Merge

If automatic merging upon validation is not desired, an alternative approach uses a maintainer command:

### 10.1 Comment-Triggered Assignment

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  assign_on_command:
    if: |
      github.event.issue.pull_request &&
      contains(github.event.comment.body, '/assign-kv') &&
      github.event.comment.author_association == 'MEMBER'
    runs-on: ubuntu-latest
    steps:
      # ... validation and assignment steps
```

This allows maintainers to review and explicitly trigger assignment with `/assign-kv` comment.

---

## 11. Implementation Checklist

- [ ] Create `.github/scripts/validate_community_kv.py`
- [ ] Create `.github/scripts/assign_community_kv.py`
- [ ] Create `.github/workflows/community-kv-validate.yml`
- [ ] Create `.github/workflows/community-kv-assign.yml`
- [ ] Add JSON schema file (optional: can be embedded in validation script)
- [ ] Configure branch protection rules
- [ ] Add `CONTRIBUTING.md` section for community Known Value requests
- [ ] Test with sample request PR

---

## 12. Feasibility Assessment

### 12.1 GitHub Actions Capabilities

| Requirement                | GitHub Actions Support | Notes                                        |
| -------------------------- | ---------------------- | -------------------------------------------- |
| PR validation              | ✅ Full                 | `pull_request` event with status checks      |
| Auto-merge after checks    | ✅ Full                 | Built-in auto-merge or `gh pr merge`         |
| File modification on merge | ✅ Full                 | `pull_request_target` with write permissions |
| JSON validation            | ✅ Full                 | Python `jsonschema` or JS libraries          |
| Cross-file uniqueness      | ✅ Full                 | Script reads existing registry               |
| Atomic commits             | ✅ Full                 | Standard git operations                      |
| PR comments                | ✅ Full                 | `github-script` action                       |

### 12.2 Limitations and Mitigations

| Limitation                           | Mitigation                                                                         |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| `pull_request` has read-only token   | Use `pull_request_target` for write operations (post-merge only)                   |
| Race conditions on concurrent merges | Re-read registry before write; use file locking or sequential merge queue          |
| Fork PR security                     | Never checkout untrusted code in `pull_request_target`; validate in `pull_request` |

### 12.3 Conclusion

GitHub Actions **can fully support** this workflow. The two-phase approach (validation on `pull_request`, assignment on `pull_request_target` after merge) provides both security and the necessary write permissions.
