# CRC-32 Checksums in CBOR

## BCR-2020-013

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: July 3, 2020

### DEPRECATED

The content below is now deprecated and of historical interest only.

### Introduction

This document registers a tag for serializing CRC-32 checksums in Concise Binary Object Representation (CBOR).

```
Tag: 19
Data item: unsigned integer in [0...2^32)
Semantics: CRC-32 checksum in network byte order (big-endian)
Created: 2020-07-03
```

### Introduction

[CRC-32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check#CRC-32_algorithm) is a common method for checksumming a block of data for later error detection. A CRC-32 checksum is an integer in the range [0...2^32).

### Semantics

A CRC-32 checksum is represented in the machine as an unsigned 32-bit integer. Memory layout may be little-endian or big-endian depending on the processor, so the checksum must be translated to network byte order (big-endian) before being encoded as CBOR. In CBOR, a CRC-32 checksum has tag 19 and is encoded as an unsigned integer (major type 0).

### Example

The CRC-32 checksum for the UTF-8 string "Hello, world!" is 0xebe6c6e6 in network byte order.

The integer checksum is then stored with tag 19:

```
D3             # tag(19)
   1A EBE6C6E6 # unsigned(3957769958)
```
