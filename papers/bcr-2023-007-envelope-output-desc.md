# Gordian Envelope: Bitcoin Output Descriptors (Version 2)

## BCR-2023-007

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 30, 2022<br/>
Revised: Aug 30, 2023

### DEPRECATED: Superseded by Version 3 Output Descriptors

This document has been superseded by [Bitcoin Output Descriptors (Version 3)](bcr-2023-010-output-descriptor.md).

The content below is now deprecated and of historical interest only. It is not deployed anywhere of which we are aware.

## Abstract

This document defines a format for enclosing typed Bitcoin output descriptors in Gordian Envelopes.

## Introduction

The primary definition for Bitcoin output descriptors is text-based and defined in [BIP-174](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md).

This document defines a method for enclosing Bitcoin output descriptors in Gordian Envelopes, leveraging the existing text-based format and adding an assertion to declare the data type.

## Known Values

The two Known Values this protocol uses are defined in the [Known Values Registry](bcr-2023-002-known-value.md#appendix-a-registry):

* `OutputDescriptor` (class)
* `outputDescriptor` (property)
* `name` (property)
* `note` (property)

Note the difference in case of the two known values: `OutputDescriptor` is a type (class), and `outputDescriptor`, is a predicate (property).

## Format Specification

The subject of a Bitcoin Output Descriptor Envelope is a text string containing a Bitcoin output descriptor.

* It MUST include an `isA: OutputDescriptor` assertion to declare its type conforming to this document.
* It MAY include a `name` assertion, where the object MUST be a non-empty string.
* It MAY include a `note` assertion, where the object MUST be a non-empty string.

**Example:**

```
"wpkh([37b5eed4/84'/0'/0']xpub6BkU445MSEBXbPjD3g2c2ch6mn8yy1SXXQUM7EwjgYiq6Wt1NDwDZ45npqWcV8uQC5oi2gHuVukoCoZZyT4HKq8EpotPMqGqxdZRuapCQ23/<0;1>/*)" [
    'isA': OutputDescriptor
    'name': "Example"
    'note': "This is the note."
]
```

### In an Assertion

A Bitcoin Output Descriptor Envelope MAY be used as the object of an assertion with the `outputDescriptor` predicate.

**Example:**

```
"Example" [
    'outputDescriptor': "wpkh([37b5eed4/84'/0'/0']xpub6BkU445MSEBXbPjD3g2c2ch6mn8yy1SXXQUM7EwjgYiq6Wt1NDwDZ45npqWcV8uQC5oi2gHuVukoCoZZyT4HKq8EpotPMqGqxdZRuapCQ23/<0;1>/*)" [
        'isA': OutputDescriptor
        'name': "Example"
        'note': "This is the note."
    ]
]
```
