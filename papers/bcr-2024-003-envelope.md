# The Gordian Envelope Structured Data Format

## BCR-2024-003

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: January 9, 2024

---

This document is a pointer to the [Gordian Envelope IETF Internet Draft](https://datatracker.ietf.org/doc/draft-mcnally-envelope/).

## Abstract

Gordian Envelope specifies a structured format for hierarchical binary data focused on the ability to transmit it in a privacy-focused way, offering support for privacy as described in RFC 6973 and human rights as described in RFC 8280. Envelopes are designed to facilitate "smart documents" and have a number of unique features including: easy representation of a variety of semantic structures, a built-in Merkle-like digest tree, deterministic representation using CBOR, and the ability for the holder of a document to selectively elide specific parts of a document without invalidating the digest tree structure. This document specifies the base Envelope format, which is designed to be extensible.
