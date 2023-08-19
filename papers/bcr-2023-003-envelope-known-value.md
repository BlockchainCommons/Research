# Gordian Envelope Extension: Known Values

## BCR-2023-003

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Aug 15, 2022<br/>
Revised: Aug 15, 2023

## Abstract

Known Values are a namespace of unsigned integers used to represent stand-alone ontological concepts. This document extends the Gordian Envelope Base Specification to add the `known-value` case arm.

## Introduction

[BCR-2023-002](bcr-2023-002-known-value.md) defines Known Values as a uniform way to represent ontological concepts as unique 64-bit unsigned integers.

Within an Envelope, any Envelope may be used as a predicate in an assertion. Ontology vocabularies such as [OWL](https://www.w3.org/OWL/) and [RDF](https://www.w3.org/2001/sw/wiki/RDF) use URIs for this purpose, and Envelope support this. But URIs are verbose and subject to manipulation that may break determinism, an essential property of Gordian Envelopes.

In addition, many predicates are commonly used, e.g., `isA` for type declarations (analogous to the URI [http://www.w3.org/1999/02/22-rdf-syntax-ns#type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type)). It is desirable to keep common predicates both short and deterministically encoded. Known Values offer a solution to this problem within Gordian Envelope.

This document extends the [Gordian Envelope Base Specification](https://datatracker.ietf.org/doc/draft-mcnally-envelope/) to add the `known-value` case used to represent a Known Value.

## Format Specification

This section is normative, and specifies an additional case arm for the `envelope` type: `known-value`. The formal language used is the [Concise Data Definition Language (CDDL)](https://datatracker.ietf.org/doc/html/rfc8610). The top-level specification of Gordian Envelope with this extension added is:

```
envelope = #6.200(envelope-content)
envelope-content = (
    leaf / elided / node / assertion / wrapped /
    known-value
)
```

As defined in [BCR-2023-002](bcr-2023-002-known-value.md):

```
known-value = uint

tagged-known-value = #6.40000(known-value)
```

Within the context of an Envelope, `known-value` is represented as an untagged unsigned integer, and is distinguished from other case arms as the *only* one represented as such. So a Gordian Envelope containing only the Known Value for `isA` in CBOR diagnostic notation would be:

```
200(1)
```

## Computing the Digest

This section is normative.

The Envelope digest image of a Known Value is the CBOR serialization of its `tagged-known-value` representation. See the [Gordian Envelope Base Specification](https://datatracker.ietf.org/doc/draft-mcnally-envelope/) for the definition of the `digest` function.

```
digest(#6.40000(known-value))
```

**Example**

The `tagged-known-value` for `isA` in CBOR diagnostic notation is `40000(1)`, which in hex is `d99c4001`. The SHA-256 sum of this sequence is:

```bash
$ echo "d99c4001" | xxd -r -p | shasum --binary --algorithm 256 | \
    awk '{ print $1 }'
2be2d79b306a21ff8e3e6bd3d1c2c6c74ff4a693b1e7ba3a0f40cdfb9ea493f8
```

Using the [envelope command line tool](https://github.com/BlockchainCommons/envelope-cli-swift), we create an Envelope with this known value as the subject and display the Envelope's digest. The digest below matches the one above.

```bash
$ envelope subject --known isA | envelope digest --hex
2be2d79b306a21ff8e3e6bd3d1c2c6c74ff4a693b1e7ba3a0f40cdfb9ea493f8
```

## Reference Implementations

This section is informative.

Both the [Swift Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/BCSwiftEnvelope) and the [Rust Gordian Envelope Reference Implementation](https://github.com/BlockchainCommons/bc-envelope-rust) support this extension.

## Security Considerations

*Work in progress*

## IANA Considerations

This document makes no requests of IANA.
