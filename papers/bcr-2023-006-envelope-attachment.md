# Gordian Envelope: Attachments

## BCR-2023-006

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 23, 2022<br/>
Revised: Mar 6, 2024

## Abstract

This document defines a method for adding vendor-specific information ("attachments") to a Gordian Envelope.

## Introduction

This document defines a protocol for specifying vendor-specific additional data ("attachments") to a Gordian Envelope.

## Known Values

This document uses the following [Known Values](bcr-2023-002-known-value.md):

| Codepoint | Canonical Name | Type | Description | URI
|--|--|--|--|--|
| 50 | `attachment` | property | Declares that the object is a vendor-defined attachment to the envelope. | [BCR-2023-006](bcr-2023-006-envelope-attachment.md)
| 51 | `vendor`     | property | Declares the vendor of the subject. | [BCR-2023-006](bcr-2023-006-envelope-attachment.md)
| 52 | `conformsTo` | property | An established standard to which the subject conforms. | http://purl.org/dc/terms/conformsTo

## Format Specification

A Gordian Envelope is specified by the format of its subject and the assertions it MUST or MAY include. For security, Envelope definitions SHOULD reject as invalid any unexpected assertions that are not defined for the Envelope type.

As an example, an Envelope containing a cryptographic seed has a subject that is a byte string containing the seed. It MUST include an `'isA': Seed` assertion to declare its type. A Seed Envelope MAY also include an optional `'name'` assertion, an optional `'note'` assertion, and an optional `'date'` assertion:

```
Bytes(16) [
    'isA': Seed
    'name': "Dark Purple Aqua Love"
    'note': "This is the note."
]
```

If an Envelope specification allows attachments, they are added by using one or more `attachment` assertions. For example:

```
Bytes(16) [
    'isA': Seed
    'attachment': {
        "Attachment Data"
    } [
        'conformsTo': "https://example.com/seed-envelope-attachment/v1"
        'vendor': "com.example"
    ]
    'name': "Dark Purple Aqua Love"
    'note': "This is the note."
]
```

The object-subject of the `'attachment'` assertion is its "payload", which in the above example is the string `"Attachment Data"`. The payload may be an Envelope of arbitrary complexity. The contents of the payload are defined by the vendor.

The payload is wrapped, and to this wrapped envelope is added one REQUIRED assertion: `'vendor'`, and optionally one RECOMMENDED assertion: `'conformsTo'`. No other assertions are permitted.

* The `'vendor'` assertion is REQUIRED and MUST be a string that uniquely identifies the entity that added the attachment data. It is RECOMMENDED that it be a reverse domain name. It MAY NOT be an empty string. It MAY NOT be any other data type have additional assertions.
* The `'conformsTo'` assertion is RECOMMENDED and MUST be a string that identifies the format of the attachment data. It is RECOMMENDED that it be a URL that points to a document that defines the format of the attachment data including version number. It MAY NOT be any other data type or have additional assertions.
* The source of the `'conformsTo'` URI does not have to be from the same vendor as the `'vendor'` assertion. In other words, the `'conformsTo'` URI MAY be from a third party that defines a standard format for the attachment data.

Multiple attachments MAY be added to an Envelope that accepts them. For example:

```
Bytes(16) [
    'isA': Seed
    'attachment': {
        "Attachment Data Version 1"
    } [
        'conformsTo': "https://example.com/seed-envelope-attachment/v1"
        'vendor': "com.example"
    ]
    'attachment': {
        "Attachment Data Version 2"
    } [
        'conformsTo': "https://example.com/seed-envelope-attachment/v2"
        'vendor': "com.example"
    ]
    'name': "Dark Purple Aqua Love"
    'note': "This is the note."
]
```

Applications that process Envelopes in which attachments are supported:

* MAY implement support for attachments they understand.
* MAY reject Envelopes with attachments that they do not understand.
* May ignore Envelopes with attachments that they do not understand (but note that ignored attachments still contribute to the digest of the Envelope)
* MAY store the Envelope's attachments for later retrieval.
* MAY transfer an Envelope's attachments to another Envelope when it makes sense to do so, such as when a new Envelope is created as a variant of an existing Envelope.
* MAY notify the user that the Envelope contains attachments, or provide affordances for the user to view or edit the attachments.
