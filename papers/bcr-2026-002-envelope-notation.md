# Gordian Envelope Notation - Quick Reference

## BCR-2026-002

**© 2026 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: January 28, 2026

## Introduction

[Gordian Envelope](https://developer.blockchaincommons.com/envelope/) is a binary smart document format. *Envelope Notation* is a human-readable text format used for inspecting envelopes. Intended for diagnostics and documentation, it is designed to be easy to read, but is *not* a round-trip format.

Understanding Envelope Notation is critical to understanding the capabilities of Gordian Envelope.

In this document, symbols enclosed in angle brackets `<` and `>` denote placeholders for values. They are *not* part of the syntax.

This document is intended to be read by humans and AI agents. It is *not* a formal grammar specification and does *not* define a parseable grammar.

## Structure

An envelope is a *subject* with multiple *assertions*. Each assertion asserts a *fact* about the subject. Square brackets `[` and `]` denote the start and end of the assertions for a subject. There are no line terminators or commas between assertions.

```envelope
<subject> [
    <assertion>
    <assertion>
    <assertion>
    ...
]
```

Assertions are composed of a *predicate* and an *object*, separated by a colon `:`.

```envelope
<subject> [
    <predicate>: <object>
    <predicate>: <object>
    <predicate>: <object>
    ...
]
```

Therefore every envelope having at least one assertion is a nonempty set of semantic triples:

$$(subject, predicate, object) \in Envelope$$

A subject can have no assertions (a *bare subject*):

```envelope
<subject>
```

Brackets always contain one or more assertions. An envelope with no assertions *must* omit the brackets entirely.

An assertion can also stand alone (a *bare assertion*):

```envelope
<predicate>: <object>
```

An envelope can be *wrapped*. The wrapped subject *and* its assertions become the subject of the envelope. It is denoted by enclosing the entire subject and its assertions in curly braces `{` and `}`.

```envelope
{
    <subject> [
        <assertion>
        <assertion>
    ]
}
```

This allows assertions to be placed on the entire wrapped envelope. Below, `inner-assertion`s are assertions about the *subject* of the inner envelope, while `outer-assertion`s are assertions about the *entire inner envelope*. This pattern is commonly used when signing.

```envelope
{
    <subject> [
        <inner-assertion>
        <inner-assertion>
    ]
} [
    <outer-assertion>
    <outer-assertion>
]
```

Every *position* within an envelope is *also itself* an envelope. So every position is recursively defined as a subject with optional assertions. This allows assertions to be made about any position within the envelope, enabling patterns for rich metadata, signing, encryption, and more.

**Positions:**
- Subject
- Assertion
- Predicate
- Object
- Envelope (wrapped subject + assertions)

Subject with an assertion (most common):

```envelope
<subject> [
    <predicate>: <object>
]
```

Wrapped envelope with an assertion (common):

```envelope
{
    <subject> [
        <inner-assertion>
    ]
} [
    <outer-assertion>
]
```

Object with an assertion (common):

```envelope
<subject> [
    <predicate>: <object> [
        <object-assertion>
    ]
]
```

Predicate with an assertion (rare):

```envelope
<subject> [
    <predicate> [
        <predicate-assertion>
    ]
    : <object>
]
```

Assertion with an assertion (less common):

```envelope
<subject> [
    {
        <predicate>: <object>
    } [
        <assertion-assertion>
    ]
]
```

Note this is a separate use of curly braces from wrapping. Here curly braces denote an assertion about an assertion. See the section on [Overloaded Punctuation](#overloaded-punctuation) below.

## Leaves

*Leaves* are the terminal values in an envelope. They can be any [dCBOR](https://developer.blockchaincommons.com/dcbor/)-encodable value, including:

- Strings (UTF-8, must be in Unicode NFC)
- Numbers (decimal and floating-point)
- Byte strings
- Booleans
- Null
- Arrays
- Maps
- Tagged values

Because Envelope Notation is a human-readable format, the envelope formatter may transform or abbreviate certain leaf values:

- Strings (denoted with double quotes `"`) may be truncated with an ellipsis `...` if they are very long.
- Byte strings display as `Bytes(<length>)` indicating their length.
- Numbers display in decimal or floating-point notation as appropriate.
- Booleans display as `true` or `false`.
- Null displays as `null`.
- Arrays display in square brackets `[` and `]` with comma-separated values.
- Maps display in curly braces `{` and `}` with comma-separated key-value pairs.
- Tagged values display with their tag number followed by the tagged value, and may be replaced with the name of a data type, by convention written using `UpperCamelCase` if known, and possibly including an abbreviated or formatted representation in parentheses (e.g. `SomeStruct(...)`).

A bare subject that is a leaf displays just the leaf value. This is the notation for a simple but complete envelope:

```envelope
"Just a string"
```

Here `UUID` and `Date` are known tagged CBOR types, so they are displayed with their canonical names and formatted values:

```envelope
UUID(dd1aaad2-0ae6-4402-9806-f60ba7a51361) {
    'isA': "HeartRateMeasurement"
    'date': Date(2026-01-15T10:30:00Z)
    'value': 92
}
```

## Known Values

*Known values* are a 64-bit space of integers assigned to ontological concepts. Known values are registered globally. When displayed in Envelope Notation, they are always denoted by single quotes, and where known, replaced with their canonical name, by convention written using `lowerCamelCase`.

For example, the known value `1` has the canonical name `isA`, and is used as a predicate to assert the type of a subject. By noticing what kinds of quotes are used, the reader can immediately see that `'isA'` is a known value and `"SomeType"` is a string:

```envelope
<subject> [
    'isA': "SomeType"
]
```

If the envelope formatter encounters an *unknown* known value, it will display the known value's integer code point in single quotes:

```envelope
<subject> [
    '9999': "No idea what's being asserted here"
]
```

Known values are most commonly used as predicates, but may also appear as subjects or objects.

Known value code points have been assigned to many common concepts, as well as the concepts from a number of major ontologies, including RDF, OWL2, FOAF, Dublin Core, and Schema.org. The canonical names of these known values include a prefix denoting their ontology, e.g. `foaf:firstName` or `dce:creator`.

Known value `0` represents the [Unit](https://grokipedia.com/page/Unit_type), which is a type as well as its sole inhabitant. It is used to denote not merely the *absence* of a value (that is what `null` is for), but to hold a position where there *can* be no information conveyed and it would be *invalid* to do so. It is displayed as empty single quotes `''`. The most common use of Unit is as the subject of an envelope entirely defined by its assertions:

```envelope
'' [
    'isA': 'foaf:Person'
    'foaf:firstName': "Alice"
    'foaf:lastName': "Smith"
]
```

In the case where such a structure has a unique identifier for the referent, the subject may instead be a known value representing the unique identifier, e.g. a UUID, or XID:

```envelope
UUID(a25e5f24-33e2-41ba-b5c3-61c7d630620a) [
    'isA': 'foaf:Person'
    'foaf:firstName': "Carol"
    'foaf:lastName': "Johnson"
]
```

Where a unique identifier is not available, `null` may be used as the subject to indicate the envelope refers an unidentified entity where the identifier may or may not exist:

```envelope
null [
    'isA': 'foaf:Person'
    'foaf:firstName': "Bob"
    'foaf:lastName': "Jones"
]
```

The `'unknown'` known value is used to indicate that the identifier *must* exist, but is not known:

```envelope
'unknown' [
    'isA': 'foaf:Person'
    'foaf:firstName': "Eve"
    'foaf:lastName': "Unknown"
]
```

## Obscuring

Envelopes may be *obscured* in three different ways: *elision*, *encryption*, and *compression*. The critical property is that even though the content may be obscured, the Merkle-like digest tree of the envelope remains intact, allowing integrity verification and selective disclosure.

- `ELIDED`: The content is replaced with an elision marker containing the digest of the original content.
- `ENCRYPTED`: The content has been symmetrically encrypted using IETF-ChaCha20-Poly1305, with the digest of the original content included as associated authenticated data (AAD). The symmetric key is known as the *content key*.
- `COMPRESSED`: The content has been compressed using zlib DEFLATE compression and declares the digest of the original uncompressed content.

In the examples below `<OBSCURED>` can appear as `ELIDED`, `ENCRYPTED`, or `COMPRESSED`, depending on the type of obscuring used. In every case, the top-level digest of the envelope remains the same. Internally these notations represent three different types serialized as tagged CBOR: `Digest`, `EncryptedMessage`, and `Compressed`.

No positions obscured:

```envelope
"Alice" [
    'foaf:knows': "Bob"
]
```

Subject obscured:

```envelope
<OBSCURED> [
    'foaf:knows': "Bob"
]
```

Predicate obscured:

```envelope
"Alice" [
    <OBSCURED>: "Bob"
]
```

Object obscured:

```envelope
"Alice" [
    'foaf:knows': <OBSCURED>
]
```

Predicate and object obscured:

```envelope
"Alice" [
    <OBSCURED>: <OBSCURED>
]
```

Entire assertion obscured:

```envelope
"Alice" [
    <OBSCURED>
]
```

Entire envelope obscured:

```envelope
<OBSCURED>
```

When more than one assertion has been obscured in the same way, they are grouped together for brevity. Here five assertions have been elided, but their digests remain separately verifiable:

```envelope
"Alice" [
    ELIDED (5)
]
```

## Duplicate Assertions are Never Allowed

In a Gordian Envelope, each assertion must have a unique digest. In other words, no two assertions can be identical. Because Envelope Notation can abbreviate values for readability, it may appear that duplicate assertions exist when they do not. For example, here are two assertions that *look* identical, but actually *must* have different byte strings for the objects:

```envelope
<subject> [
    'key': Bytes(16)
    'key': Bytes(16)
]
```

The important thing to remember is that in a Gordian Envelope, assertions are *uniquely identified by their digests*, not how they appear in Envelope Notation.

## Common Patterns

### Signing

Signatures are assertions. But as assertions assert facts about their subjects, an envelope like this would not sign the whole envelope, but only the subject.

```envelope
<subject> [
    <inner-assertion>
    'signed': Signature
]
```

To sign the entire envelope, including its assertions, the common pattern is to *wrap* the envelope first, then place the signature assertion on the outer envelope:

```envelope
{
    <subject> [
        <inner-assertion>
    ]
} [
    'signed': Signature
]
```

### Public Key Encryption

The plaintext envelope is optionally signed, then symmetrically encrypted with the symmetric content key, and the content key is itself asymmetrically encrypted for using each recipient's public key. Each recipient gets a `hasRecipient` assertion containing a `SealedMessage` object with the encrypted content key and necessary parameters.

Plaintext signed then wrapped:

```envelope
{
    {
        <subject> [
            <inner-assertion>
        ]
    } [
        'signed': Signature
    ]
}
```

The subject (now the entire signed envelope) is then encrypted using the content key:

```envelope
ENCRYPTED
```

The encrypted envelope is then asserted for each recipient:

```envelope
ENCRYPTED [
    'hasRecipient': SealedMessage
    'hasRecipient': SealedMessage
]
```

### Encrypting to a password

A password may be used to symmetrically encrypt the content key. The `hasSecret` assertion contains an `EncryptedKey` object with the encrypted content key and necessary parameters.

```envelope
ENCRYPTED [
    'hasSecret': EncryptedKey(Argon2id)
]
```

### Decorrelation with Salt

Before elision the assertion object is decorated with a salt assertion to prevent identical objects from producing identical digests.

```envelope
<subject> [
    {
        <predicate>: <object>
    } [
        'salt': Salt
    ]
]
```

After elision the digest remains, but the salt prevents correlation.

```envelope
<subject> [
    ELIDED
]
```

### Attachments

*Attachments* are a supported way for envelopes to carry third-party data that can be preserved without being interpreted. Attachments contain a *payload* envelope that can be anything, carrying a `'vendor'` assertion to identify the source of the attachment (required), and optionally a `'conformsTo'` assertion to identify the format of the payload (recommended).

Example: a cryptographic seed envelope with two attachments, each conforming to a different version of a seed attachment format, along with a name and note assertions:

```envelope
Bytes(16) [
    'isA': 'Seed'
    'attachment': {
        "Attachment Data V1"
    } [
        'conformsTo': "https://example.com/seed-attachment/v1"
        'vendor': "com.example"
    ]
    'attachment': {
        "Attachment Data V2"
    } [
        'conformsTo': "https://example.com/seed-attachment/v2"
        'vendor': "com.example"
    ]
    'name': "Alice's Seed"
    'note': "This is the note."
]
```

### Overloaded Punctuation

Envelope notation uses some punctuation characters in ways that are overloaded but always distinguishable by context:

- Curly braces `{` and `}` denote:
  - A wrapped envelope when enclosing a subject and its assertions.
  - One or more assertions about an assertion.
  - A leaf map value when enclosing key-value pairs.
- Square brackets `[` and `]` denote:
  - The start and end of assertions for a subject.
  - A leaf array value when enclosing comma-separated values.
- Colons `:` denote:
  - The separator between predicate and object in an assertion.
  - The separator between key and value in a leaf map.
- Commas `,` denote:
  - Separators between values in a leaf array.
  - Separators between key-value pairs in a leaf map.

## Mock Example: Supply Chain Manifest

```envelope
{
    UUID(550e8400-e29b-41d4-a716-446655440000) [
        'isA': "ElectronicComponent"
        'schema:description': "QPU-9000 Quantum Core"
        'schema:manufacturer': "Hyperion Foundries"
        'schema:productionDate': Date(2026-01-15T08:30:00Z)

        // SENSITIVE DATA: The exact cost has been ELIDED (redacted)
        // for this viewer, but the hash is still present to verify integrity.
        // The object of the assertion may have been salted to prevent correlation.
        'schema:costPerUnit': ELIDED

        // RECURSIVE ASSERTION: The destination is visible, but salt
        // was added before hashing to prevent correlation attacks if this
        // assertion is elided for other viewers.
        {
            'schema:deliveryAddress': "Facility 42"
        } [
            'salt': Salt
        ]

        // ATTACHMENT: An embedded PDF specification
        'attachment': {
            Bytes(1048576) // 1MB PDF file
        } [
            'vendor': "com.hyperion"
            'conformsTo': "https://www.iana.org/assignments/media-types/application/pdf"
            "fileName": "qpu-9000-specs.pdf" // String used as predicate is valid
        ]
    ]
} [
    // EXTERNAL METADATA: Assertions on the envelope itself
    "manifestID": "MAN-2026-001"
    "status": "In Transit"

    // SIGNATURE: Signs everything inside the curly braces {}
    'signed': Signature
]
```
