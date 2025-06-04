# Domain Separation in Derived Keys

## BCR-2025-005

**© 2025 Blockchain Commons**

Authors: Wolf McNally\
Date: June 3, 2025

## Introduction

_Domain separation_ is the practice of tagging cryptographic primitives (like hashes or derived keys) with unique, purpose-specific inputs, frequently called "salts" or "info" strings that ensure outputs for different uses don't overlap. This separation:

- Prevents keys or hashes created for one purpose from being misused for another,
- Blocks attacks that try to mix protocols,
- Maintains security guarantees, and
- Allows different systems to safely use the same algorithms without information leaking between them.

Many applications require private-public key pairs used for both signing and public key encryption. For some key types, these can be derived from the same source key material. While a single derived key pair could in theory be used for both signing and key agreement, this is a bad idea. In the Blockchain Commons stack, wherever both a "signing" key and an "agreement" key are needed, and where these can both be derived from the same key material, we use distinct salts to derive them.

This document shows where domain separation is applied in the Blockchain Commons software stack: particularly in the [`bc-components`](https://crates.io/crates/bc-components) ("Secure Components") Rust crate.

## `PrivateKeyBase`

The [`PrivateKeyBase`](https://github.com/BlockchainCommons/bc-components-rust/blob/master/src/private_key_base.rs) structure simply holds an array of bytes representing _not_ a private key, but the raw key material from which a private key can be derived:

```rust
pub struct PrivateKeyBase(Vec<u8>);
```

Just using the `new` method, you can create a new `PrivateKeyBase` using a cryptographically secure random number generator:

```rust
let private_key_base = PrivateKeyBase::new();
```

Or you can create a `PrivateKeyBase` from an existing byte array:

```rust
let private_key_base = PrivateKeyBase::from_data(&[0x01, 0x02, 0x03, 0x04]);
```

Using such a simple sequence of bytes should never be done in production code as it is a critical security risk. However it is useful for testing and debugging purposes, as the keys derived from it will be deterministic and predictable.

`PrivateKeyBase` also provides a number of convenience methods for deriving keys, such as `x25519_private_key()`. X25519 is used for key agreement, upon which Blockchain Commons builds its public key encryption structures.

If we drill down into its implementation, we eventually arrive at the `derive_agreement_private_key()` function in the `bc-crypto`, which is used to derive the X25519 private key from the key material using  HKDF (HMAC-based Key Derivation Function) with a specific salt for agreement keys:

```rust
impl PrivateKeyBase {
    pub fn x25519_private_key(&self) -> X25519PrivateKey {
        X25519PrivateKey::derive_from_key_material(&self.0)
    }
}

impl X25519PrivateKey {
    pub fn derive_from_key_material(key_material: impl AsRef<[u8]>) -> Self {
        Self::from_data(bc_crypto::derive_agreement_private_key(key_material))
    }
}

pub fn derive_agreement_private_key(
    key_material: impl AsRef<[u8]>
) -> [u8; GENERIC_PRIVATE_KEY_SIZE] {
    hkdf_hmac_sha256(key_material, "agreement".as_bytes(), GENERIC_PRIVATE_KEY_SIZE)
        .try_into()
        .unwrap()
}
```

The string `"agreement"` is the salt used for deriving agreement keys, ensuring that the derived key is distinct from any signing keys that might be derived from the same key material.

Next to the above function, we also have a `derive_signing_private_key()` primitive function that derives signing keys from the same key material, but with a different salt:

```rust
pub fn derive_signing_private_key(key_material: impl AsRef<[u8]>) -> [u8; GENERIC_PUBLIC_KEY_SIZE] {
    hkdf_hmac_sha256(key_material, "signing".as_bytes(), GENERIC_PUBLIC_KEY_SIZE)
        .try_into()
        .unwrap()
}
```

For all the key types that support deterministic key derivation, we ultimately uses these primitives to derive the keys, ensuring that agreement and signing keys are always derived into separate domains.

## `PrivateKeys`

Because many applications require both signing and agreement keys, `PrivateKeyBase` also provides ways to derive an agreement key and and a signing key in a single step. For example:

```rust
let private_keys: PrivateKeys = my_private_key_base.schnorr_private_keys();
```

The `schnorr_private_keys()` method derives a BIP-340 Schnorr private key for signing and a X25519 private key for agreement from the `PrivateKeyBase`. The keys are derived using distinct salts, and packaged in a single [`PrivateKeys`](https://github.com/BlockchainCommons/bc-components-rust/blob/master/src/private_keys.rs) structure for convenience:

```rust
pub struct PrivateKeys {
    signing_private_key: SigningPrivateKey,
    encapsulation_private_key: EncapsulationPrivateKey,
}
```

Because the `PrivateKeys` structure implements the `Signer` and `Decrypter` traits, it can be used directly for signing messages and decrypting messages, both of which require private keys. In each case the key derived from the `PrivateKeyBase` with the appropriate salt is used.

## Non-Deterministic Key Generation and Best Practices

The Blockchain Commons stack also supports key types where both keys are derived randomly and independently, such as the post-quantum algorithms like "ML-KEM" and "ML-DSA". In these cases, the production of these keys is never deterministic, so no domain separation is needed, and there is no separate step to derive the public keys. Instead, the `keypair()` or `keypair_opt()` methods can be used to generate all the keys at once. This is the recommended method for generating keys in production code, and works for all the signature and encapsulation schemes supported by the Blockchain Commons stack:

```rust
// Generates the keys using the default signature and encapsulation schemes.
let (private_keys: PrivateKeys, public_keys: PublicKeys) =
    keypair();

// Generates the keys using the specified signature and encapsulation schemes.
let (private_keys: PrivateKeys, public_keys: PublicKeys) =
    keypair_opt(SignatureScheme::MLDSA44, EncapsulationScheme::MLKEM512);
```
