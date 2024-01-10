# dCBOR: A Deterministic CBOR Application Profile

## BCR-2024-002

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: January 9, 2024

---

This document is a pointer to the [dCBOR IETF Internet Draft](https://datatracker.ietf.org/doc/draft-mcnally-deterministic-cbor/).

As this specification now has several implementations by third parties and has been extensively discussed in the IETF CBOR working group, we now consider it to be on track to becoming a standard.

## Abstract

The purpose of determinism is to ensure that semantically equivalent data items are encoded into identical byte streams. CBOR (RFC 8949) defines "Deterministically Encoded CBOR" in its Section 4.2, but leaves some important choices up to the application developer. The CBOR Common Deterministic Encoding (CDE) Internet Draft builds on this by specifying a baseline for application profiles that wish to implement deterministic encoding with CBOR. The present document provides an application profile "dCBOR" that can be used to help achieve interoperable deterministic encoding based on CDE for a variety of applications wishing an even narrower and clearly defined set of choices.
