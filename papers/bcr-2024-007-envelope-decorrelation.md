# Decorrelation in Gordian Envelope

Discusses the concept of decorrelation and the extension of Gordian Envelope for implementing decorrelation.

## BCR-2024-007

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen, Shannon Appelcline<br/>
Date: August 4, 2024

## Overview

This document discusses decorrelation of Gordian Envelopes. It introduces terminology, then introduces opt-in decorrelation capabilities as an extension of Gordian Envelope.

## Definitions

### Image and Projection

This document uses the term *image* to mean the input to an algorithm $f$ and *projection* to mean the result of $f(\text{image})$:

$projection = f(image)$

### Correlatability, Noncorrelatability

Bit sequences are said to be *correlatable* if by examining them there is a way to determine whether they are projections of the same image. If there is no practical way to learn whether a set of sequences are projections of a common image, they are said to be *noncorrelatable*.

### Quasicorrelatability

Between projections that are definitely correlatable and definitely noncorrelatable, there are projections that may leak a little information about their image, specifically: it's size.

If multiple projections of the same image produce entirely noncorrelatable bit sequences, but the size of the projections are dependent on the size of the image, then the sequences are said to be *quasicorrelatable*. For example, if a function $f$ always produces a projection that is the same number of bits as the image, or some fixed number of bits greater than the image, then the images are quasicorrelatable.

### Decorrelation

*Decorrelation* is a correction for quasicorrelation through obfuscating the size of the image. By adding a pad of random bits to an image before projecting it, projections may be produced that may be of uniform size, or of sufficiently varying size. Either way the intent is that the size of a projection tells an observer nothing useful about the image, except that its size must be less than or equal to its projection.

## Signatures are Noncorrelatable

In [Gordian Envelope public key encryption](bcr-2023-013-envelope-crypto.md), a `Signature` is produced using:

* the Schnorr signature algorithm
* the original message (“image”)
* a private key, and
* entropy

Because of the use of entropy, two such `Signature`s produced from a single image will contain entirely different bit sequences, and yet both will still validate against the image. Furthermore, all signatures are the same size regardless of the size of the image: 64 bytes, so the size of the signature provides no clue as to the contents of the image. Therefore there is no way, without the image and the public key corresponding to the private key used to produce it, for a third-party to determine that the two signatures were derived from that image, or even that they were derived from the same image. Therefore, `Signature`s are noncorrelatable.

## Digests are Correlatable

Like `Signature`, producing a `Digest` in Gordian Envelopes (for example in the ELIDED cae) is a *lossy* operation (SHA-256): there is no way that the image or any information about the image can be recovered from the projection. However, unlike `Signature`,  `Digest` *is* correlatable by design: two `Digests` produced from the same image are always equal, and a specific `Digest` could *only* have been produced from a specific image. Therefore if one can determine the image used to produce one of the `Digest`s, then one knows that the same image must have produced the other.

## Encrypted Messages are Quasicorrelatable

In Gordian Envelope, an `ENCRYPTED` case (based on `EncryptedMessage`) is produced by a lossless operation that also uses entropy (IETF-ChaCha20-Poly1305). Because of the use of entropy, the bits of the ciphertext are noncorrelatable. But because the size of the ciphertext is always identical to the size of the plaintext, an `EncryptedMessage` is quasicorrelatable. This extends to constructs such as `SealedMessage` that incorporate `EncryptedMessage`.

Decorrelation of an `EncryptedMessage` could be accomplished by adding some number of bits to the plaintext before encryption. However the problem arises as to how to distinguish bits of the original plaintext from bits of the pad, which are to be thrown away upon decryption. Gordian Envelope offers an elegant solution to this problem, described below.

## SSKRShares are Correlatable

[SSKR](bcr-2023-013-envelope-crypto.md) breaks (*shards*) a fixed-length (32 byte) secret into a number of *shares*, a threshold of which can be used to recover the secret. Because the secret is always of a fixed, predermined length, the shares produced by SSKR are, by themselves, noncorrelatable. However, each SSKR share contains metadata that can be used for correlation, and in particular, a 16-bit session ID that identifies each share as having been produced by the same sharding operation.

This correlatability is inherited by the set of envelopes produced by the envelope sharding function, as each envelope carries an assertion with an `SSKRShare` produced by sharding an ephemeral symmertric content key.

Furthermore, the payload itself is encrypted into an `EncryptedMessage` using this content key, and because the `EncryptedMessage` is the same in every envelope, every one of these envelopes is correlatable by both its SSKR share and its identical `EncryptedMessage`.

To mitigate this:

* The SSKR algorithm would have to be enhanced to make its shares non-correlatable. Removing the session ID is the obvious first step, but doing this has downsides. The session ID is a check on foreign shares being introduced into the recovery process, and removing the session ID would make it impossible for an SSKR decoder to reject a share interactively: only upon receiving a quorum of shares and performing the secret recovery could the secret be checked for validity, for example by attempting to use the possibly-recovered secret as a key for decoding the payload. Even if the session ID were removed, an SSKR share contains other metadata such as the share index, member threshold, group index, group count, and group threshold that could still be used to (more weakly) correlate a set of shares.
* Rather than including the identical `EncryptedMessage` in every `Envelope`, they would each contain a unique `EncryptedMessage`, produced by the same key, but from a plaintext that has undergone decorrelation.

Combining a noncorrelatable SSKR share with a decorrelated encrypted payload would maximize noncorrelation for sharded payloads of arbitrary size.

## Decorrelation in Gordian Envelope

An envelope is a Merkle-like tree, where every node is associated with a characteristic digest:

* The envelope as a whole,
* The subject of the envelope,
* Each assertion on the subject,
* Each predicate of each assertion,
* Each object of each assertion,

Each of these element digests are used to form the image of the higher digests in the tree:

* each predicate digest and object digest are used to form the assertion digest,
* The subject digest and all the assertion digests (in sorted order) are used to form the envelope digest.

Therefore, a change to any element of an envelope propagates upwards and impacts every digest up that branch of the tree.

The tree itself inherits the correlatability of its elememts. So an envelope just containing a simple plaintext string will have the same envelope digest, and hence the same identity, as another envelope containing just that same simple plaintext string.

On the other hand, envelopes containing only elements that are noncorrelatable, or quasicorrelatable, inherit those attributes. For example, consider a message that has been signed then encrypted:

```
ENCRYPTED [
    'signed': Signature
]
```

In the above:

* the `EncryptedMessage` subject is quasicorrelatable, because it was constructed with entropy, but the ciphertext is the same length as the plaintext,
* the `signed` known value predicate is correlatable, because it is a well-known value, and
* the `Signature` is noncorrelatable, because it is fixed size and constructed with entropy.

If the assertion is elided, we get:

```
ENCRYPTED [
    ELIDED
]
```

When elided, an element is replaced with its digest, preserving the digest tree. Digests by themselves are noncorrelatable, but an attacker could infer certain things from the structure and positioning of the elements:

* the elided assertion's digest is noncorrelatable because it includes a `Signature`, which was generated using entropy and so the digest inherits its noncorrelatability.
* As described above, the `EncryptedMessage` is quasicorrelatable.

In general, a completely elided assertion (`ELIDED`) inherits the maximum noncorralatability of either its predicate or object. If only the predicate is elided (`ELIDED: object`) or only the object is elided (`predicate: ELIDED`), or both are individually elided but not the assertion as a whole (`ELIDED: ELIDED`), and noncorrelatability is desired, then each element must be analyzed separately.

## Opt-In Decorrelation in Gordian Envelope

The envelope API provides methods to add a `'salt': Salt` assertion.

- The known value `'salt'` is defined in [BCR-2023-002](bcr-2023-002-known-value.md).
- The `Salt` is object is number of random bytes as defined in [BCR-2023-017](bcr-2023-017-salt.md).

The number of bytes of salt to add may be chosen, but by default the Envelope API will choose a random size for the `Salt` object. The range of sizes for the `Salt` is chosen to minimize both correlation and quasicorrelation:

* For small objects, the number of bytes added will generally be from 8...16.
* For larger objects the number of bytes added will generally be from 5%...25% of the size of the object.

Adding salt to an element changes the digest of the element and all elements up to the root of the digest tree. Therefore, when decorrelation is to be enabled, salts should be added to the construction of the envelope before other constructs like signatures that depend on the stability of the digest tree.

## Choosing What to Decorrelate

A simple example in Envelope notation:

```
"Alpha" [
    'note': "Beta"
]
```

How we salt this envelope depends on which fields we wish to decorrelate. If we with to decorrelate the subject only, we cannot simply add a salt assertion:

```
"Alpha" [
    'note': "Beta"
    'salt': Salt
]
```

This will only decorrelate the entire envelope if the whole thing is elided:

```
ELIDED
```

If we wish to decorrelate the subject only, making it possible elide it only with decorrelation, we must first wrap it:

```
{
    "Alpha"
} [
    'note': "Beta"
]
```

And then add salt to it:

```
{
    "Alpha" [
        'salt': Salt
    ]
} [
    'note': "Beta"
]
```

Now if we elide just the subject it will be decorrelated.

```
ELIDED [
    'note': "Beta"
]
```

If we just want to decorrelate the note, we can do so by adding salt to the note assertion object:

```
"Alpha" [
    'note': "Beta" [
        'salt': Salt
    ]
]
```

Now it will be decorrelated if elided:

```
"Alpha" [
    'note': ELIDED
]
```

If we want to make it possible to elide the entire assertion without even leaving its predicate, we can add the salt assertion to the entire assertion:

```
"Alpha" [
    {
        'note': "Beta"
    } [
        'salt': Salt
    ]
]
```

Now when the assertion is elided, it will be fully decorrelated:

```
"Alpha" [
    ELIDED
]
```

Note that it is possible for a holder to reveal the salted object, but not the salt itself, and still keep the digest tree stable:

```
"Alpha" [
    {
        'note': "Beta"
    } [
        ELIDED
    ]
]
```
