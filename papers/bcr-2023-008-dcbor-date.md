# dCBOR: Preferred Encoding of Dates

## BCR-2023-008

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: Sep 2, 2022<br/>
Revised: Sep 4, 2023

## Abstract

This document defines a preferred format for dates in Gordian Deterministic CBOR (dCBOR).

## Format Specification

CBOR already has a well-defined date format using the tag #6.1 defined in [RFC 8949 §3.4.2 Epoch-Based Date Type](https://www.rfc-editor.org/rfc/rfc8949.html#section-3.4.2).

This document specifies this method, which MUST include its tag-based type declaration, as the preferred format to specify dates when using [Gordian dCBOR](https://datatracker.ietf.org/doc/draft-mcnally-deterministic-cbor/).

RFC 8949 says the tagged value may be either an integer or a float, but dCBOR's numeric reduction rules apply and MUST be used to determine the encoded numeric type.

## CDDL

```
tagged-date = #6.1(date)
date = int / float
```
