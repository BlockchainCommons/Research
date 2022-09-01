# FIRST DRAFT
[ToC]
# Understanding Schnorr Signatures

The Bitcoin system, or cryptocurrencies in general, revolve around the concept of digital signatures. The blockchain ledger encrypts the ownership of digital assets. Unlike  traditional notions of ownership, that are enforced by legal documents and physical signatures, the ownership of a digital currency is proven by means of digital signatures.
Varieties of Digital Signature algorithms exist  throughout, each with their own advantages and disadvantages. Since it's inception, Bitcoin has used the ECDSA scheme for the purpose of Digital Signature. 
Within the biggest proposed protocol update being discussed in the community -Taproot, is a new digital signature algorithm called Schnorr(invented by Claus-Peter Schnorr, a German mathematician and cryptographer, back in the 1980s).

> :book: ***What is a Schnorr signature Scheme?*** Similar to the ECDSA scheme used by Bitcoin, the Schnorr signature algorithm generates cryptographic signatures for a given message, but with several advantages.A proposed future extension, it gives a new method to generate signatures (R,s) on a hash h.

Known for its simplicity,efficiency and short signatures, Schnorr is among the first schemes whose security is based on the intractability of discrete logarithm problems.  

> ***History*** It was covered by U.S. Patent that expired in February 2008.The first talk of implementing Schnorr signature on Bitcoin protocol came up in the bitcoin-talk forum in 2014. Four years later Blockstream engineer Pieter Wuille made the first draft proposal for a Schnorr Signature Scheme in Bitcoin. In Jan 2020, it was numbered BIP340, that describes the full technical definition of Schnorr Signature in Bitcoin.

The specific version of the algorithm proposed in BIP340 is tailor-made for Bitcoin’s requirement. Reviews and changes are still in the making as the proposal thrives as a work in progress. Schnorr signature, along with Taproot and Tapscript, was proposed as a combined upgrade package for the SegWit Version 1 Bitcoin protocol.

## Understanding the Math of Schnorr
Like ECDSA, Schnorr also uses private-public key pairs. The only difference presents itself in the signing and verification algorithm, that happen to be a lot more simple than ECDSA.

### Signing
We start with a given,

>Private key :             x            (integer) , 
Group generator :         G ,
Public key :              P = xG      (curve point) ,
Message hash:             h            (integer)

We then,

>Generate a random number: k            (integer)
Calculate:                R = kG      (curve point)
Calculate: s = k + hash(r| |P| |h)x    (integer)

where: r = X-coordinate of curve point R and | |  denotes binary concatenation
Signature = (r, s)     (integer, integer)

r, being a public key, would require 33 bytes to represent (32 bytes + 1 bit indicating "even" vs "odd").

### Verification
to check the validity of a signature (r, s) against a public key P, we obtain 

>the signature: (r,s)
public key : P
message: h

We then calculate the random point R from r and verify: 
>sG = R + hash(r| |P| |h)P

For a valid signature,
>sG will be equal to R + hash(r| |P| |h)P. 

So we simply compare to check the signature.

## Supporting MuSig

By now we know that **in Elliptic Curve Digital Signature Algorithm, the signature is calculated as s = (h + rx)/k** and **in Schnorr, the same is  calculated as s = k + Hash(r| |P| |h)x**.
>Note that there is no division involved in the calculation in Schnorr. This seemingly trivial change makes Schnorr signatures linear in nature and of the generic algebraic form y = a + bx [Equation of a line]. 

This property of Schnorr allows us to add two Schnorr signature and produce another valid schnorr signature. So to say, we can create a single signature that validates two or more separate transactions when multiple keys are used to sign the same message with Schnorr. This can be used to significantly reduce the size of multisig payments and other multisig related transactions. 
>Now that we can do algebra with signatures ( which was not possible with ECDSA), we can potentially do a lot more cool cryptographic tricks too.

>This further enables signers in a multi-signature transaction to combine their public keys into an aggregated key that formally represents the entire group; a property we know as **key aggregation**.

Though the feature of key aggregation sounds trivial, it's benefits are vast. Since multisigs are not natively supported by ECDSA, they had to be implemented in Bitcoin via a standardized smart contract called Pay-to-ScriptHash (P2SH). This enables users to add spend conditions called **encumbrances** to specify how funds can be spent e.g. “only unlock balance if both A and B sign this message.”

Unlike traditional multi-signatures which are smart contract (P2SH), MuSigs(Multi-signatures with Schnorr) are indistinguishable from regular signatures and plain old pay to public key (P2PKH) transactions. The only thing that gets recorded onchain is a single public key and a single signature.All of this ultimately gives a huge  boost to privacy in Bitcoin.

> Taproot uses the linearity of Schnorr signatures to add Tapscripts into regular P2PKH transactions. So with Taproot, there will be no way to tell whether a transaction is simple P2PKH or Multisig or some other exotic smart contracts because they will all look the same.

>To sum up, this simple property of linearity,that enables us to add “stuff” into the signature is very powerful. Using this we can create Adapter Signatures, details of which we shall be reading further in the chapter.

**Benefits :** Less footprint on the blockchain, lower transaction costs, and improved bandwidth.

**Problems with P2SH :**
- P2SH requires knowledge of the public keys of all signers participating in the multisig, which is an inefficient system.
- P2SH offers very little privacy guarantees.  Blockchain observers can not only identify all P2SH transactions in the network but can also pin point the identities within the multisig.

**MUSIG WITH SCHNORR :**

If P = P1 + P2 is the addition of two public keys (remember curve points can be added together), k = k1 + k2 is the addition of two random numbers chosen by users(nonce), h is the message being signed, then s = s1 + s2 is a valid signature for aggregate pubic key P and the common message h.

### Signing
s1 = k1 +hash(r| |P| |h)(x1)
s2 = k2 +hash(r| |P| |h)(x2)
s = s1 + s2
 = (k1 + k2) + hash(r| |P| |h)(x1 + x2)
### Verification
sG = (k1 + k2)G + hash(r| |P| |h)(x1 + x2)G
   = kG + hash(r| |P| |m)(P1 + P2)   [as P1 = (x1)G, P2 = (x2)G]
   = kG + hash(r| |P| |h)P
   
This method can easily be **generalised for any number of transactions.**

Thus the sum of two individual signatures is also valid for the sum of the individual public keys. With this multiple parties can collaborate and add up their public keys to create a single aggregate key. Coins from this public key can then be spent by an aggregate signature.

## Understanding the Use of Adapter Signatures

Contracts in Bitcoin can sometimes require a locking mechanism to ensure the indivisblity of a given set of payments, i.e. either all the payments succeed or all of them fail.

As mentioned earlier, Schnorr's property of linearity allows us to add things into the signature. Using this we can create Adapter Signatures, which are a powerful tool for locking in bitcoin contracts and can be used in Cross-Chain Atomic Swaps, Lightning channel creation, scriptless scripts and many more.

Traditionally, this locking was done by having all payments in a particular set relate to a preimage with the same hash digest. When the party who knows the preimage reveals it onchain, everyone else learns it and subsequently unlocks their own payments and therefore the link  between the set of payments is revealed because they all use the same preimage and digest. 

On the other hand, signature adaptors don't have to be published onchain. To anyone without a corresponding adaptor, a signature created with an adaptor will look like any other digital signature.This gives adaptors significant efficiency and privacy advantages over hashlocks.

#### RELATIONSHIP TO MUSIG
Signature adaptors usually can’t secure a contract entirely by themselves. This is,thus, done by combining signature adaptors with multiparty signatures. 

Signature adaptors are combined with multiparty signature schemes, e.g. MuSig to enable the published signature to look like a single-party signature thus increasing privacy and coherence. In ECDSA, this is possible still, but with elaborate algorithms that may either be slower or need security assumptions. in lieu, asimpler and safer scheme for adaptor signatures exists for Bitcoin that uses 2-of-2 OP_CHECKSIG multisig; though this is less efficient and less private.

An Adaptor signature is an encrypted signature S' which can be proven to decrypt to a signature S over a message m. The encryption can be done either using a **secret key t**(“Private key tweaking”) or a **public key T**(“Public key tweaking”). In general, encryption using t is used if the party performing the encryption knows t, while encryption using T is chosen if they do not know t. 

Adaptor signatures can be used in a single signer context, or in a two parties context. 

Single signer schnorr Adaptor signature
In this, the party creating the signature wishes to provide another party a signature that can be decrypted only using a secret t. However, even without knowing t, they can verify that the decrypted signature will be valid for a given message m.

 What is tweaking ?
 To create the Adaptor Schnorr signature we introduce t or T in the signature calculation. The signature is completed by either adding or subtracting t from the Adaptor signature. Verification of the signature is possible without using private information like p, r, and t.

Two party Adaptor signatures
In this, users engage in a multi-signature protocol that enables one user to obtain another’s part of the signature, while guaranteeing the latter that upon the revealing of the multi-signature by the former  they will learn the secret t without anyone else knowing it too.

Both parties create a common R and P (using Mu-sig), and agree on a tweak point T(=tG).
The first party, say A creates an Adaptor Schnorr signature and passes it on to the second user, say B.
B verifies Adaptor Schnorr signature and adds his signature to Adaptor Schnorr signature and passes it to A.
A verifies the signature from B and decrypt Adaptor Schnorr signature using t.
##  Knowing the Advantages of Schnorr
### **Reduced Size.**
Schnorr signatures are a fixed 64 bytes instead of the longer ECDSA signature format that takes up around 70–72 bytes per transaction and therefore stand as an improvement against it.
11% smaller than ECDSA signatures, Schnorr signatures take up less room in a transaction on the blockchain that further implies smaller transaction sizes and lower fees. 

>In ECDSA, if a bitcoin transaction contains many inputs, each of them requires their own signature. This means that each signer must post their separate ECDSA signature to the transaction that are then verified individually. Also, a compact multi-signature with ECDSA is difficult to produce as they are encoded using Distinguished Encoding Rules.
### **Linear**
Linearity in Schnorr enables key aggregation i.e. multiple signers in a multi-sig transaction can collaborate to produce an aggregated key that is valid for the sum of their public keys and  represents the group. This paves way for various advanced applications that improve efficiency and privacy, such as multi-signatures,Scriptless Scripts and smart contracts.
  All inputs need a single signature with Schnorr. This gives rise to more capacity for other transactions on the block. Smaller transaction sizes for multi-sig transactions leads to lower fees. With key aggregation, we do not have to check each individual input, thus speeding up verification. Schnorr enables validation of upto a million-sig multisig in 2 minutes.
>Verification happens for a fraction of the speed of validating them individually in ECDSA, giving Schnorr a steep edge over it.

### **Better privacy [no difference between MuSig and sig, no detection of Lightning]**
Schnorr guarantees better privacy that the traditionally used ECDSA by making different multisig spending policies indistinguishable on chain.
Schnorr enables simpler higher-level protocols, such as atomic swaps that are indistinguishable from normal payments. These can be used to build more efficient payment channel constructions.


>ECDSA signatures are inherently malleable, i.e.  a third party without access to the private key can  alter an existing valid signature and double-spend funds. In contrast, Schnorr signatures are provably non-malleable.
### **Better security and non-malleable**
The security of Schnorr signatures is easily provable when a sufficiently random hash function is used with a sufficiently hard  ellipic curve discrete logarithm problem (ECDLP) in the signature.
Both the ECDSA and Schnorr digital signature schemes rely on the discrete logarithm problem. But Schnorr uses fewer assumptions and has a secure formal proof as compared to ECDSA thatlacks a formal security proof and relies on extra assumptions.

> This document needs further additions to it and command line implementations of Schnorr. 