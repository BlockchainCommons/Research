# Permits in Gordian Envelope

## BCR-2025-004

**© 2025 Blockchain Commons**

Authors: Wolf McNally\
Date: May 13, 2025

## Introduction

Gordian Envelope supports both symmetric and public key encryption. More generally, it bases its public key encryption system on its symmetric encryption system. This is quite a flexible architecture, because by encrypting a single symmetric key multiple ways, you can create envelopes that can be transmitted securely, then:

- Opened by multiple parties,
- Encrypted using strong passwords,
- "Sharded" into a number of pieces for social key recovery

In fact, you can use any of these "permits" in any combination on the same envelope. This document describes the permit system in detail.

## Walkthrough

This example shows how to create a Gordian Envelope, encrypt it, and then assign multiple permits to it.

### Composing the Payload Envelope

Alice composes a poem:

```rust
let poem_text = "At midnight, the clocks sang lullabies to the wandering teacups.";
```

She creates a new envelope and assigns the text as the envelope's subject. She also adds some metadata assertions to the envelope, including that the subject of the envelope is a poem, its title, the (pseudonymous) author, and the date.

```rust
use bc_envelope::prelude::*;

let original_envelope = Envelope::new(poem_text)
    .add_type("poem")
    .add_assertion("title", "A Song of Ice Cream")
    .add_assertion("author", "Plonkus the Iridescent")
    .add_assertion(known_values::DATE, Date::from_ymd(2025, 5, 15));
```

Right now, if `original_envelope` were printed using `format()`, it would look like this, with the subject being the poem text, and four assertions on it:

```
"At midnight, the clocks sang lullabies to the wandering teacups." [
    'isA': "poem"
    "author": "Plonkus the Iridescent"
    "title": "A Song of Ice Cream"
    'date': 2025-05-15
]
```

Alice signs the envelope with her private key by generating a keypair, and then using the `sign()` method with her private key. The `sign()` method wraps the envelope so the subject and all its assertions are signed, and adds a `'signed'` assertion to the wrapped envelope:

```rust
let (alice_private_keys, alice_public_keys) = keypair();
let signed_envelope = original_envelope.sign(&alice_private_keys);
```

The `format()` method will now show the wrapped and signed envelope:

```
{
    "At midnight, the clocks sang lullabies to the wandering teacups." [
        'isA': "poem"
        "author": "Plonkus the Iridescent"
        "title": "A Song of Ice Cream"
        'date': 2025-05-15
    ]
} [
    'signed': Signature
]
```

### Symmetric Encryption with a Content Key

Alice picks a random symmetric "content key" and uses it to encrypt the signed envelope. Even though the content key is not saved in the envelope in its unencrypted form, it is still considered a *permit* because it can be used to decrypt the envelope.

```rust
let content_key = SymmetricKey::new();
let encrypted_envelope = signed_envelope.encrypt(&content_key);
```

When printed, the encrypted envelope looks very... cryptic:

```
ENCRYPTED
```

Alice will provide several different methods ("permits") that can be used to unlock it. Each permit encrypts the same content key using a different method.

### Adding a Password Permit

First, Alice wants to be able to recover the envelope later using a password she can remember, so she adds the first permit to the envelope using the `add_secret()` method, providing a derivation method `Argon2id`, her password, and the content key. The `add_secret()` method encrypts the content key with a new key derived from her password, and adds it to the envelope as a `'hasSecret'` assertion:

```rust
let password = b"unicorns_dance_on_mars_while_eating_pizza";
let locked_envelope = encrypted_envelope.add_secret(
    KeyDerivationMethod::Argon2id,
    &password,
    &content_key
);
```

The encrypted envelope now has one permit:

```
ENCRYPTED [
    'hasSecret': EncryptedKey(Argon2id)
]
```

### Adding Public Key Recipient Permits

Next, Alice wants to be able to decrypt her envelope using her private key, and she also wants Bob to be able to decrypt it using his private key. To do this, she uses the `add_recipient()` with her own public key, and then Bob's public key. The `add_recipient()` method encrypts the content key with the recipient's public key, and adds it to the envelope as a `'hasRecipient'` assertion:

```rust
let (bob_private_keys, bob_public_keys) = keypair();

let locked_envelope = locked_envelope
    .add_recipient(&alice_public_keys, &content_key)
    .add_recipient(&bob_public_keys, &content_key);
```

The encrypted envelope now has three permits:

```
ENCRYPTED [
    'hasRecipient': SealedMessage
    'hasRecipient': SealedMessage
    'hasSecret': EncryptedKey(Argon2id)
]
```

### Adding Social Key Recovery Permits

An SSKR share is a kind of permit defined by the characteristic that one share by itself is not enough to decrypt the envelope: some *quorum* or *threshold* of shares is required.

Alice wants to back up her poem using a social recovery scheme, so even if she forgets her password and loses her private key, she can still recover the envelope by finding two of the three friends she entrusted with the shares.

Alice creates a 2-of-3 SSKR group and "shards" the envelope into three envelopes, each containing a unique SSKR share.

```rust
let sskr_group = SSKRGroupSpec::new(2, 3)?;
let spec = SSKRSpec::new(1, vec![sskr_group])?;
let sharded_envelopes = locked_envelope.sskr_split_flattened(&spec, &content_key)?;
```

Every envelope looks the same including the previous permits Alice added, but each one contains a different SSKR share, so we only show one of them here. There are now four permits, where each of the three envelopes has a different SSKR share:

```
ENCRYPTED [
    'hasRecipient': SealedMessage
    'hasRecipient': SealedMessage
    'hasSecret': EncryptedKey(Argon2id)
    'sskrShare': SSKRShare
]
```

Now there are three envelopes, each having four permits, and *five* different ways to recover the original envelope:

1. Using the original content key (could be stored in a safe place)
2. Using Alice's password
3. Using Alice's private key
4. Using Bob's private key
5. Using any two of the three SSKR shares

Alice will now:

- Keep one envelope for herself
- Give one envelope to Bob
- Give the three sharded envelopes to three other friends who don't know each other
- Use a password manager to store her password and private key
- Put the content key in a safe place (optional, not usually recommended as Alice's private key is sufficient)

### Decrypting the Envelope

Let's demonstrate using each of these permits to decrypt the envelope:

```rust
//
// Grab the first envelope from the SSKR shares.
//

let received_envelope = &sharded_envelopes[0];

//
// Decrypt using the content key.
//

let unlocked_envelope = received_envelope.decrypt(&content_key)?;
assert_eq!(unlocked_envelope, signed_envelope);

//
// Decrypt using the password.
//

let unlocked_envelope = received_envelope.unlock(&password)?;
assert_eq!(unlocked_envelope, signed_envelope);

//
// Decrypt using Alice's private key.
//

let unlocked_envelope = received_envelope.decrypt_to_recipient(&alice_private_keys)?;
assert_eq!(unlocked_envelope, signed_envelope);

//
// Decrypt using Bob's private key.
//

let unlocked_envelope = received_envelope.decrypt_to_recipient(&bob_private_keys)?;
assert_eq!(unlocked_envelope, signed_envelope);

//
// Decrypt using any two of the three SSKR shares.
//

let unlocked_envelope = Envelope::sskr_join(&[
    &sharded_envelopes[0],
    &sharded_envelopes[2]
])?.unwrap_envelope()?;
assert_eq!(unlocked_envelope, signed_envelope);

//
// And of course, Alice's signature still verifies.
//

unlocked_envelope.verify(&alice_public_keys)?;
```
