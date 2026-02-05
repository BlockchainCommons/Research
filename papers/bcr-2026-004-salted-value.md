# Envelope Salted Values

This document defines a standard **Salted Value** pattern for Gordian Envelope, enabling optional decorrelation of small or easily enumerable values that may be elided.

## BCR-2026-004

**© 2026 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: February 4, 2026

---

## Abstract

Gordian Envelope supports *holder-based elision*: selectively withholding parts of an envelope while preserving verification through the digest tree. However, elided elements are replaced by their digests, and **digests are correlatable**: repeated elisions of the same underlying value yield identical digests, enabling cross-presentation linkage and (for small value spaces) dictionary attacks.

[BCR-2024-007](bcr-2024-007-envelope-decorrelation.md) introduces opt-in decorrelation in Gordian Envelope using `'salt': Salt` assertions. This document defines a **Salted Value** pattern—an Envelope-native wrapper that standardizes how to salt “atomic” values (strings, small enums, etc.) while keeping them readable when disclosed.

A value MAY be represented directly (unsalted):

```envelope
"Indiana"
```

Or as a Salted Value using **Unit** as subject:

```envelope
'' [
    'salt': Salt(<random-data>)
    'value': "Indiana"
]
```

This document also explains how envelope schemas may define assertions as:

- optionally accepting Salted Values,
- requiring Salted Values, or
- forbidding Salted Values,

depending on privacy needs, future elision expectations, and determinism requirements.

---

## Status of This Document

📙 This document is research and a proposed specification. It defines a reusable pattern intended for broad application across Envelope schemas, but it does not yet have a reference implementation.

---

## Background

### Unit and record-like values

[BCR-2026-001](bcr-2026-001-unit.md) defines **Unit** (`''`, Known Value 0) as deliberate emptiness: a position that carries zero informational content and must not be replaced with any other value. In Gordian Envelope, Unit is used as the subject when an envelope’s meaning is conveyed entirely by its assertions, without implying a subject identity.

Salted Values are *record-like wrappers*: they exist to carry assertions (`'salt'` and `'value'`). They are not independently-identified entities. Therefore, Salted Values use **Unit** as their subject.

### Salt

[BCR-2023-017](bcr-2023-017-salt.md) defines `salt` as random bytes used as an additional input to one-way algorithms where similar inputs should not yield the same outputs (“decorrelation”). Salts are not usually secret.

In Envelope, salt is carried as a `Salt` object with CBOR tag `#6.40018(bytes)`.

### Decorrelation and elision

[BCR-2024-007](bcr-2024-007-envelope-decorrelation.md) explains correlatability in the context of Envelope’s Merkle-like digest tree:

- When an element is elided, it is replaced with its digest, preserving the digest tree.
- Digests are correlatable: identical hidden values produce identical digests.
- Envelope supports opt-in decorrelation by adding `'salt': Salt` assertions at the correct level (subject, object, or assertion) to ensure elided digests do not correlate.

This BCR defines a standard wrapper that makes it easy for schemas to say: “this value may be salted in a consistent way.”

---

## Motivation

Many real-world fields are drawn from **small or enumerable sets**, and are often **privacy-sensitive** when withheld:

- US state codes (`"ID"`, `"CA"`, ...)
- cities/towns (often enumerable within a jurisdiction)
- standardized roles (`"Release Manager"`, `"Witness"`)
- categorical labels used in workflows

If such values are elided without decorrelation, their digests can be:

1. **Linked** across different presentations (correlation), and/or
2. **Recovered** via dictionary attack if the value space is small.

The Salted Value pattern provides a simple, schema-friendly way to represent these values so that if the *entire value object* is elided, its resulting digest is decorrelated.

---

## The Salted Value Pattern

### Definitions

A **Salted Value** is an envelope with:

- subject: **Unit** (`''`)
- required assertions:
  - `'salt': Salt(...)`
  - `'value': <any value>`

A Salted Value is semantically equivalent (for interpretation) to its underlying `'value'`, except that it carries a salt that changes its digest for decorrelation purposes.

### Representation

#### Unsalted value

Any ordinary Envelope value:

```envelope
"Indiana"
```

#### Salted value

A Salted Value wrapper:

```envelope
'' [
    'salt': Salt(<random-data>)
    'value': "Indiana"
]
```

### Required predicates

| Code Point | Predicate | Description                                                                                                                          |
|:-----------|:----------|:-------------------------------------------------------------------------------------------------------------------------------------|
| 15         | `'salt'`  | Random salt for decorrelation (see [BCR-2024-007](bcr-2024-007-envelope-decorrelation.md) and [BCR-2023-017](bcr-2023-017-salt.md)). |
| 25         | `'value'` | The wrapped underlying value.                                                                                                        |

### Pattern Invariants

- The subject MUST be Unit (`''`) per [BCR-2026-001](bcr-2026-001-unit.md).
- There MUST be exactly one `'salt'` assertion, and its object must be a `Salt` of at least 8 bytes (see below for further guidance),
- There MUST be exactly one `'value'` assertion, and its object may be anything.
- There MUST NOT be any other assertions.

---

## How Salted Values Provide Decorrelation

A Salted Value is itself an envelope element. Because it contains a `'salt': Salt(...)` assertion, its digest is altered by random data. If the Salted Value is elided as an *object* in some larger envelope, the resulting digest is decorrelated.

Example (field value is salted):

```envelope
'region': '' [
    'salt': Salt(<random-data>)
    'value': "CA"
]
```

If the holder later elides the entire object:

```envelope
'region': ELIDED
```

…the digest standing in for the elided object is now a digest of the **salted wrapper**, not of `"CA"` directly. This prevents correlation and makes dictionary attacks impractical (absent disclosure of the wrapper).

### Important disclosure guidance

If concealment is the goal, presentations SHOULD elide the **entire Salted Value object**, not merely the `'value'` assertion inside it.

Revealing the wrapper while eliding only `'value'`:

```envelope
'' [
    'salt': Salt(<random-data>)
    'value': ELIDED
]
```

…can leak enough structure to enable brute-force recovery in small value spaces (because the elided leaf digest corresponds to the underlying value). For small enumerated fields, that defeats the purpose.

One *can* disclose the `'value`' without disclosing the `'salt'`, although this provides little additional security benefit:

```envelope
'' [
    'salt': ELIDED
    'value': "CA"
]
```

**Rule of thumb:**

- To *reveal* the value: disclose the wrapper (or disclose the unsalted value, if allowed).
- To *conceal* the value: elide the wrapper object entirely.

---

## Salt Selection Guidance

[BCR-2024-007](bcr-2024-007-envelope-decorrelation.md) recommends salt sizes chosen to minimize correlation and quasicorrelation:

- For small objects, salt is generally 8…16 bytes.
- For larger objects, salt is generally 5%…25% of object size.

For Salted Values (which are commonly used for small strings/enums), producers SHOULD use random salts in the **8…16 byte** range, and MAY choose a random length within that range to reduce size-based leakage.

Salts MUST be random (see [BCR-2023-017](bcr-2023-017-salt.md)).

Salts SHOULD be added during envelope construction *before* applying any signatures that depend on the digest tree (see [BCR-2024-007](bcr-2024-007-envelope-decorrelation.md)).

---

## Schema Integration

Salted Values are most useful when schemas explicitly support them, so that producers and verifiers share expectations.

A schema may treat a field as:

1. **Optionally salted** (accept either form)
2. **Required salted** (always use the Salted Value wrapper)
3. **Forbidden salted** (the default: only accept the direct/unsalted form)

### Optionally salted

A schema MAY define a field as accepting either:

- the direct value, or
- a Salted Value wrapping that value

Example schema intent:

- `region` may be `"CA"` or `''['salt':..., 'value':"CA"]`

This choice is appropriate when:

- the field is usually disclosed, but
- the field might later be selectively withheld, and
- producers want the option to pre-commit in a decorrelatable way.

**Reasonable use case:** a location object where region/locality are usually present, but may be withheld in some presentations for privacy.

### Required salted

A schema MAY require that a field always be represented as a Salted Value wrapper.

This choice is appropriate when:

- the value space is small and correlation/dictionary attacks are a concern, and
- withholding is expected or common, and
- determinism (same inputs → same digests) is not required for that field.

**Reasonable use case:** `locality`, `role`, or other fields that are frequently elided and have high correlation risk.

### Forbidden salted

A schema MAY forbid Salted Value wrappers for fields that must remain deterministic or directly comparable at the digest level.

This choice is appropriate when:

- the field participates in canonical identifiers, keys, indexes, or deterministic commitments, or
- correlation is desired (e.g., you want equal values to be obviously equal across envelopes), or
- the field is always public and never elided.

**Reasonable use case:** fields intended as stable identifiers, fixed policy URIs, or other values where non-determinism would be harmful.

Where a schema is silent on whether Salted Values are allowed, the default is to forbid them.

---

## Examples

### Example 1: Optional salted region

Unsalted:

```envelope
'region': "CA"
```

Salted:

```envelope
'region': '' [
    'salt': Salt(<random-data>)
    'value': "CA"
]
```

### Example 2: Required salted locality

Schema requires locality to be salted because it may be elided and is easily enumerable:

```envelope
'locality': '' [
    'salt': Salt(<random-data>)
    'value': "Sacramento"
]
```

Concealed presentation:

```envelope
'locality': ELIDED
```

### Example 3: Combining with higher-level structures

A place object that supports optional salted small fields:

```envelope
'' [
    'country': "US"
    'region': '' [
        'salt': Salt(<random-data>)
        'value': "CA"
    ]
    'locality': '' [
        'salt': Salt(<random-data>)
        'value': "Sacramento"
    ]
    'timeZone': "America/Los_Angeles"
]
```

---

## Security Considerations

1. **Salt is not secrecy.** Salt is not usually secret; its purpose is decorrelation of projections, not encryption (see [BCR-2023-017](bcr-2023-017-salt.md)).
2. **Elide at the right level.** To conceal a value while benefiting from decorrelation, elide the Salted Value object as a whole. Revealing the wrapper while eliding only `'value'` can enable dictionary attacks in small value spaces.
3. **Non-determinism is intentional.** Salted Values break deterministic equality-at-the-digest-level. Schemas should forbid Salted Values where determinism is required.
4. **Add salt before signing.** Because salts change the digest tree, they must be part of the envelope before signatures that commit to those digests (see [BCR-2024-007](bcr-2024-007-envelope-decorrelation.md)).
5. **Fresh salt per value.** Reusing the same salt (or copying an entire Salted Value wrapper) across contexts reintroduces correlatability. Salts should be freshly generated per wrapped value.
6. **Eliding a parent node inherits its child salts.** When a parent node with salted children is elided, the parent MAY be considered effectively salted as well, as the child salt(s) also serve to decorrelate the parent.

---

## Future Work

- Define schema notation patterns (human- and machine-readable) for expressing “optional salted” vs “required salted” field constraints.

---

## References

### Internal (BCR)

- [BCR-2026-001: Unit: The Known Value for Deliberate Emptiness](bcr-2026-001-unit.md)
- [BCR-2023-017: UR Type Definition for Random Salt](bcr-2023-017-salt.md)
- [BCR-2024-007: Decorrelation in Gordian Envelope](bcr-2024-007-envelope-decorrelation.md)
- [BCR-2023-002: Known Values](bcr-2023-002-known-value.md)
- [BCR-2024-009: Signatures with Metadata in Gordian Envelope](bcr-2024-009-signature-metadata.md)

### External

- https://en.wikipedia.org/wiki/Salt_(cryptography)  (background concept; Envelope use is defined by the BCRs above)
