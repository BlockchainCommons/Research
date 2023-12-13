# UR Type Definition for Cryptographic Nonce

## BCR-2023-015

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 9, 2023<br/>
Revised: December 9, 2023

## Overview

A `Nonce` is a cryptographically strong random "number used once" and is frequently used in algorithms where a random value is needed that should never be reused. This document defines a fixed-length 12-byte nonces.

## CDDL

```
nonce = #6.40014(bytes .size 12)
```
