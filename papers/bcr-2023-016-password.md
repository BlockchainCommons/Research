# UR Type Definition for Scrypt-Hashed Password

## BCR-2023-016

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 9, 2023<br/>
Revised: December 9, 2023

## Overview

[Scrypt](https://datatracker.ietf.org/doc/html/rfc7914) is a password-based key derivation function that is designed to be computationally intensive and memory-hard. It is designed to make brute-force attacks difficult to perform. This document defines a UR type for storing a password that has been salted and hashed using scrypt.

`password` is a password that has been salted and hashed using Scrypt, and is therefore suitable for storage and use for authenticating users via password. To validate an entered password, the same hashing algorithm using the same parameters and salt must be performed again, and the hashes compared to determine validity. This way the authenticator never needs to store the password. The processor and memory intensive design of the scrypt algorithm makes such hashes resistant to brute-force attacks.

### CDDL

```
password = #6.40015([n, r, p, salt, hashed-password])

n = uint                 ; iterations
r = uint                 ; block size
p = uint                 ; parallelism factor
salt = bytes             ; random salt (16 bytes recommended)
hashed-password = bytes  ; 32 bytes recommended
```
