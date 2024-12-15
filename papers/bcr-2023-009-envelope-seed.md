# Gordian Envelope: Cryptographic Seeds

## BCR-2023-007

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Sep 4, 2022

## Abstract

This document defines a format for enclosing cryptographic seeds in Gordian Envelopes

## Introduction

Crypto seeds are large random numbers used to generate cryptographic keys.

## Known Values

The Known Values this protocol uses are defined in the [Known Values Registry](bcr-2023-002-known-value.md#appendix-a-registry):

* `Seed` (class)
* `isA` (property)
* `name` (property)
* `note` (property)
* `date` (property)
* `outputDescriptor` (property)
* `attachment` (property)

## Format Specification

An Envelope containing a cryptographic seed has a subject that is a byte string containing the seed.

* It MUST include an `isA: Seed` assertion to declare its type conforming to this document.
* It MAY include a single `name` assertion, where the object MUST be a non-empty string, which MAY have been elided.
* It MAY include a single `note` assertion, where the object MUST be a non-empty string, which MAY have been elided.
* It MAY include a single `date` assertion, where the object MUST be a date conforming to [BCR-2023-008](bcr-2023-008-dcbor-date.md).
* It MAY include a single `outputDescriptor` assertion, where the object MUST be a Bitcoin output descriptor conforming to [BCR-2023-007](bcr-2023-007-envelope-output-desc.md).
* It MAY include one or more `attachment` assertions conforming to [BCR-2023-006](bcr-2023-006-envelope-attachment.md).

**Example:**

```
Bytes(16) [
    'isA': Seed
    'attachment': {
        "Attachment Data"
    } [
        'conformsTo': "https://example.com/seed-envelope-attachment/v1"
        'vendor': "com.example"
    ]
    'date': 2021-02-24T09:19:01Z
    'name': "Dark Purple Aqua Love"
    'note': "This is the note."
    'outputDescriptor': "wpkh([37b5eed4/84'/0'/0']xpub6BkU445MSEBXbPjD3g2c2ch6mn8yy1SXXQUM7EwjgYiq6Wt1NDwDZ45npqWcV8uQC5oi2gHuVukoCoZZyT4HKq8EpotPMqGqxdZRuapCQ23/<0;1>/*)" [
        'isA': OutputDescriptor
        'name': "Example Descriptor"
        'note': "This is the descriptor's note."
    ]
]
```
