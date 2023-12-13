# Gordian Envelope Expressions

## BCR-2023-012

**© 2023 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 8, 2023<br/>
Revised: December 8, 2023

## Overview

Envelope Expressions are a method for encoding machine-evaluatable expressions using Gordian Envelope. Using expression, envelope provides a cryptographically strong foundation on which to build requests and responses for distributed function calls. The syntax for encoding expressions described in this document is the basis for the [Gordian Sealed Transaction Protocol (GSTP)](bcr-2023-014-gstp.md).

## Goals

Ideally a method of encoding expressions will have the following traits:

* Allow any mathematical or algorithmic expressions.
    * This would include, for example, the evaluation of spending conditions and smart contracts.
* Be easy for humans to read.
* Leverage the existing Envelope notation.
* Produce results that can be [substituted](https://en.wikipedia.org/wiki/Substitution_(logic)) in-place for the original unevaluated expression.
* Support easy [composition](https://en.wikipedia.org/wiki/Function_composition).
* Support scoped variable substitution.
* Support [higher-order functions](https://en.wikipedia.org/wiki/Higher-order_function).
* Be [homoiconic](https://en.wikipedia.org/wiki/Homoiconicity).

## UR Types and CBOR Tags

This document defines the following UR types along with their corresponding CBOR tags:

| UR type          | CBOR Tag   |
| :--------------- | :--------- |
| ur:function      | #6.40006   |
| ur:parameter     | #6.40007   |
| ur:placeholder   | #6.40008   |
| ur:replacement   | #6.40009   |

These tags have been registered in the [IANA Registry of CBOR Tags](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml).

## The General Form of Expressions

An expression can be as simple as a constant, like the value `2`, or as complex as a mathematical formula like `a^2 + b^2 = c^2`, or function call, like `verifySignature(key: pubkey, sig: signature, digest: sha256(message))`.

In general, an expression is a function identifier along with zero or more parameters, and the result of evaluating an expression is a value.

In an envelope the function identifier is the subject, and each parameter is an assertion with the predicate being the parameter identifier and the object being the argument.

```
«function» [
    ❰parameter❱: argument
    ❰parameter❱: argument
    ...
]
```

When printed in envelope notation, function identifiers are enclosed in double angle brackets (`U+00AB` and `U+00BB`), and parameter identifiers are enclosed in heavy single angle brackets (`U+2770` and `U+2771`). When encoded, these brackets represent the presence of specific CBOR tags, `#6.40006` for function identifiers and `#6.40007` for parameter identifiers. The tagged value itself can either be an unsigned integer (more compact encoding) or a string (more human-readable).

In [CDDL](https://tools.ietf.org/html/rfc8610):

```
function = #6.40006(uint / text)
parameter = #6.40007(uint / text)
```

The envelope expression syntax therefore uses a form of named parameters, although it is not limited to this paradigm. The purpose of tagging functions and parameters is to make them machine-distinguishable from other metadata. Assertions that are not tagged as parameters are ignored by the expression evaluator. Assertions that are tagged as parameters but are not expected by the function are an error. Functions may have parameters that are required or optional, and not supplying all required parameters is an error.

By convention `camelCase` is used when assigning string values to function and parameter identifiers.

When a function or parameter identifier is a string, it is printed in quotes:

```
«"myFunction"» [
    ❰"parameter1"❱: argument
    ❰"parameter2"❱: argument
    ...
]
```

When a function or parameter identifier is an integer, it is printed as an integer. However, in the case where the identifier's name is known when it is being output, it may be printed as an unquoted string:

```
«123» [
    ❰456❱: argument
    ❰789❱: argument
    ...
]
```

```
«myFunction» [
    ❰parameter1❱: argument
    ❰parameter2❱: argument
    ...
]
```

Therefore, the presence of quotes always indicates that the identifier is a string, and the absence of quotes always indicates that the identifier is an integer.

## Example Expressions

The examples in this section are intended to show the expressiveness of the envelope expression syntax. Not all of the forms shown here have been implemented, and this is still a work in progress.

### Constants

Constants like numbers, strings, and even compound data types like `EncryptedMessage` are the simplest form of expression, and are directly encodable as an Envelope whose subject is an instance of the constant's CBOR type. Constants evaluate to themselves.

```
2
```

```
"Hello"
```

```
ENCRYPTED
```

### Binary Operator

Binary operations like addition are functions with two operands, `lhs` and `rhs`. Some such expressions are *commutative* where the order does not matter, while others like subtraction are *non-commutative*. These binary parameters are so common that they are assigned numeric parameter identifiers:

```
blank = 1  ; blank
lhs = 2    ; left-hand side
rhs = 3    ; right-hand side
```

Several basic arithmetic operations and predicates have also been assigned numeric function identifiers:

```
add = 1  ; addition
sub = 2  ; subtraction
mul = 3  ; multiplication
div = 4  ; division
neg = 5  ; unary negation
lt = 6   ; less than
le = 7   ; less than or equal to
gt = 8   ; greater than
ge = 9   ; greater than or equal to
eq = 10  ; equal to
ne = 11  ; not equal to
and = 12 ; logical and
or = 13  ; logical or
xor = 14 ; logical exclusive or
not = 15 ; logical not
```

So the expression `2 + 3` would be represented as:

```
«add» [
    ❰lhs❱: 2
    ❰rhs❱: 3
    'note': "The result of adding two numbers."
]
```

Note the inclusion of the `note` assertion, which is not part of the expression but is metadata about the expression. This is an example of how envelope expressions can be used to encode metadata about the expression that is ignored by the expression evaluator.

When evaluated, the result is an Envelope that may be algebraically substituted for the original expression:

```
5
```

### Unary Operator

Unary operators are simply functions of arity one. Where an expression has a single parameter whose purpose is understood from context, the `blank` parameter identifier is used, denoted `❰_❱`. The unary negation operator is a simple example:

```
«negate» [
    ❰_❱: 10
]
```

```
-10
```

Another example where the `blank` parameter would be used is something analogous to the `this` or `self` reference in object-oriented languages.

### Logical Predicates

Operators that evaluate to boolean values are often known as "predicates". To avoid confusing them with the "predicate" role in the Envelope type and in the nomenclature of semantic triples, we refer to these operations as "logical predicates" and where further clarification is needed, the other type as "semantic predicates".

`5 > 2` may be encoded as:

```
«gt» [
    ❰lhs❱: 5
    ❰rhs❱: 10
]
```

```
false
```

### Function Call (N-ary Operator)

Function calls of any arity may be encoded. For example this hypothetical function signature in Swift:

```swift
func verifySignature(key: SigningPublicKey, sig: Signature, digest: Digest) -> Bool
```

Would be represented as:

```
«"verifySignature"» [
    ❰"key"❱: SigningPublicKey
    ❰"sig"❱: Signature
    ❰"digest"❱: Digest
]
```

The `verifySignature` function is a logical predicate. The result of this expression is a boolean value that would typically be used as an argument in a boolean expression.

Note also that the function identifier and all the parameter identifiers are shown in quotes, and are therefore all string-valued. This is the convention for function and parameter identifiers that are not well-known.

### Function Composition

[Function composition](https://en.wikipedia.org/wiki/Function_composition) is the process of applying one function to the result of another.

For example, the composition `f(g(x))` may be represented as:

```
«f» [
    ❰_❱: «g» [
        ❰_❱: $x
    ]
]
```

The result of evaluating `«g»` may be substituted for the argument to `«f»`, and the result of evaluating `«f»` may be substituted for the entire expression.

Using the `verifySignature` function from the previous example, the composition `verifySignature(key: pubkey, sig: signature, digest: sha256(message))` may be represented as:

```
«"verifySignature"» [
    ❰"key"❱: SigningPublicKey
    ❰"sig"❱: Signature
    ❰"digest"❱: «"sha256"» [
        ❰_❱: messageData
    ]
]
```

Once the result of the `«"sha256"»` function is substituted for the argument of the `❰"digest"❱` digest parameter of `«"verifySignature"»`, the expression has been algebraically reduced to the previous example.

### Structured Parameters

Functions may take parameters that are sequences encoded as CBOR arrays, or dictionaries encoded as CBOR maps. For example, a hypothetical function that concatenates a sequence of strings might be represented as:

```
«"concatenate"» [
    ❰_❱: ["Foo", "Bar", "Baz"]
]
```

And evaluate the above expression to:

```
"FooBarBaz"
```

### Variable Substitution and Partially-Applied Expressions

Envelope expressions support scoped variable substitution. There are two CBOR tags to represent placeholders and values to be substituted into them. Like function and parameter identifiers, these are represented by unsigned integers or strings, and when printed, the same convention of using quotes to indicate strings applies, with placeholders being prefixed with `$` and replacements being prefixed with `/`.

```
placeholder = #6.40008(uint / text)
replacement = #6.40009(uint / text)
```

So for the `verifySignature` example, we can produce a "template" expression that can be partially applied by substituting values for the placeholders:

```
{
    «"verifySignature"» [
        ❰"key"❱: $"key"
        ❰"sig"❱: $"sig"
        ❰"digest"❱: «"sha256"» [
            ❰_❱: $"message"
        ]
    ]
} [
    /"key": SigningPublicKey
    /"sig": Signature
    /"message": Digest
]
```

When this expression is evaluated, the result is a partially-applied expression that is the same as the first `verifySignature` example above.

#### Complete Replacement

In the following examples, we are using these integer assignments for placeholders and replacements:

```
a = 1
b = 2
c = 3
d = 4
e = 5
```

The scope of replacement is recursive, but stops at any separately enclosed envelopes.

In this example, there is only a top set of replacements, so all variables are substituted.

```
{
    «add» [
        ❰lhs❱: $a
        ❰rhs❱: «mul» [
            ❰lhs❱: $b
            ❰rhs❱: $c
        ]
    ]
} [
    /a: 10
    /b: 20
    /c: 30
]
```

The result of evaluating this expression is:

```
a + (b * c)
= 10 + (20 * 30)
= 70
```

#### Scoped Replacement

In this case, the `rhs` argument of the top-level function has been enclosed, so the enclosed substitutions are considered to be in a different scope:

```
{
    «add» [
        ❰lhs❱: $a
        ❰rhs❱: {
            «mul» [
                ❰lhs❱: $b
                ❰rhs❱: $c
            ]
        }
    ]
} [
    /a: 10
    /b: 20
    /c: 30
]
```

Because of this, when the above expression is evaluated only the `$a` substitution is made, and the expression result is only partially applied:

```
«add» [
    ❰lhs❱: 10
    ❰rhs❱: {
        «mul» [
            ❰lhs❱: $b
            ❰rhs❱: $c
        ]
    }
]
```

#### Replacement with Rescoping

In this version, the inner expression has its own `replacement` assertions that pass the outer replacements inward under different names. One of these replacements is itself an expression:

```
{
    «add» [
        ❰lhs❱: $a
        ❰rhs❱: {
            «mul» [
                ❰lhs❱: $d
                ❰rhs❱: $e
            ]
        } [
            /d: $c
            /e: «add» [
                ❰lhs❱: $b
                ❰rhs❱: 2
            ]
        ]
    ]
} [
    /a: 10
    /b: 20
    /c: 30
]
```

After the outer replacements are made, the still partially-applied result is:

```
«add» [
    ❰lhs❱: 10
    ❰rhs❱: {
        «mul» [
            ❰lhs❱: $d
            ❰rhs❱: $e
        ]
    } [
        /d: 30
        /e: «add» [
            ❰lhs❱: 20
            ❰rhs❱: 2
        ]
    ]
]
```

After the inner replacements are made, the fully-applied result is:

```
«add» [
    ❰lhs❱: 10
    ❰rhs❱: {
        «mul» [
            ❰lhs❱: 30
            ❰rhs❱: «add» [
                ❰lhs❱: 20
                ❰rhs❱: 2
            ]
        ]
    }
]
```

So now we can evaluate the inner expression:

```
«add» [
    ❰lhs❱: 10
    ❰rhs❱: {
        «mul» [
            ❰lhs❱: 30
            ❰rhs❱: 22
        ]
    }
]
```

Then:

```
«add» [
    ❰lhs❱: 10
    ❰rhs❱: 660
]
```

And finally get the result:

```
670
```

### Higher-Ordered Functions

Functions that take functions as parameters are known as [higher-order functions](https://en.wikipedia.org/wiki/Higher-order_function). For example, the `map` function takes a function and a sequence, and returns a sequence of the results of applying the function to each element of the sequence. In this example, this hypothetical `map` function applies a function that squares its argument to each element of the sequence `[3, 4, 5]`:

```
«"map"» [
    ❰_❱ : [3, 4, 5]
    ❰"transform"❱: «mul» [
        ❰lhs❱: $0
        ❰rhs❱: $0
    ]
]
```

This expression evaluates to:

```
[9, 16, 25]
```

Each application of the `❰transform❱` expression to an element of the `❰_❱` argument results in a replacement expression:

```
{
    «mul» [
        ❰lhs❱: $0
        ❰rhs❱: $0
    ]
} [
    /0: 4
]
```

By substitution:

```
«mul» [
    ❰lhs❱: 4
    ❰rhs❱: 4
]
```

And finally:

```
16
```

### Structured Programming

Functions may perform tests yielding different evaluation paths. For example a hypothetical conditional expression in C-like languages: `20 > 10 ? "Big" : "Small"` may be represented as:

```
«"if"» [
    ❰"test"❱: «gt» [
        ❰lhs❱: 20
        ❰rhs❱: 10
    ]
    ❰"true"❱: "Big"
    ❰"false"❱: "Small"
]
```

```
"Big"
```

## Well-Known Expressions

Since every Envelope has a unique digest, any Envelope expression can be replaced by its digest as long as the expression can be found that matches it. In some cases, certain expressions may be so common as to be designated "well known". In this case they can be represented by their digest alone or even a small tagged integer, trusting that the recipient of an Envelope can resolve the expression should they wish to evaluate it. Expressions that solve problems in specific domains and include placeholders for their arguments may be good candidates for this, one example being common cryptocurrency spending conditions.

Even for expressions that are not "well known," like any other `Envelope`, an expression could appear as a reference to a `Digest` with one or more `dereferenceVia` assertions that tell the evaluator how to retrieve the expression that belongs in that place.

### Advanced Example: Atomic Swap

**⚠️ NOTE:** This section is a work in progress, and the example may not correctly conform to the syntax described above.

In this example an [adaptor signature](https://bitcoinops.org/en/topics/adaptor-signatures/) is represented by the type `EncryptedSignature`, and a "hidden value" or "tweak" is represented by the type `DecryptionKey`.

Alice and Bob wish to execute an atomic coin swap.

First, Alice gives Bob an unsigned transaction that promises to pay him 1 BTC. The transaction includes a `signature` assertion that when evaluated correctly will yield a valid signature for Alice's transaction.

The `encryptedSignature` parameter of the `decryptSignature` function is already filled out by Alice with her `EncryptedSignature`. An `EncryptedSignature` by itself can’t be used as a BIP-340 signature, so Alice hasn’t paid Bob yet:

```
Transaction(Alice) [
    signature: «decryptSignature» [
        ❰encryptedSignature❱: EncryptedSignature(Alice)
        ❰decryptionKey❱: «recoverDecryptionKey» [
            ❰message❱: «digest» [
                ❰_❱: $transaction
            ]
            ❰encryptedSignature❱: $encryptedSignature
            ❰signature❱: $signature
        ]
    ]
]
```

What Alice's `EncryptedSignature` does provide Bob is a commitment to Alice’s `DecryptionKey`. This commitment includes a parameter Bob can use to create a second `EncryptedSignature` that commits to the same `DecryptionKey` as Alice’s `EncryptedSignature`. Bob can make that commitment even without knowing Alice’s `DecryptionKey` or his own signature for that commitment.

Bob gives Alice his unsigned transaction that promises to pay her 1 BTC, along with a `signature` assertion containing his `EncryptedSignature`. Unlike Alice's `signature` assertion, which requires Bob to know the signature for Alice's transaction (which she hasn't placed on the network yet), this expression requires Alice to know the `DecryptionKey`:

```
Transaction(Bob) [
    signature: «recoverSignature» [
        ❰message❱: «digest» [
            ❰_❱: $transaction
        ]
        ❰encryptedSignature❱: EncryptedSignature(Bob)
        ❰decryptionKey❱: $decryptionKey
    ]
]
```

Alice has always known the `DecryptionKey`, so she can use it to decrypt Bob’s `EncryptedSignature` to get his signature for the transaction that pays her:

```
{
    Transaction(Bob) [
        signature: «recoverSignature» [
            ❰message❱: «digest» [
                ❰_❱: $transaction
            ]
            ❰encryptedSignature❱: EncryptedSignature(Bob)
            ❰decryptionKey❱: $decryptionKey
        ]
    ]
} [
    /transaction: Transaction(Bob)
    /decryptionKey: DecryptionKey
]
```

After the replacements are performed:

```
Transaction(Bob) [
    signature: «recoverSignature» [
        ❰message❱: «digest» [
            ❰_❱: Transaction(Bob)
        ]
        ❰encryptedSignature❱: EncryptedSignature(Bob)
        ❰decryptionKey❱: DecryptionKey
    ]
]
```

After the expression is evaluated:

```
Transaction(Bob) [
    signature: Signature(Bob)
]
```

Alice broadcasts the transaction and receives Bob’s payment. When Bob sees that transaction onchain, he can combine its signature with the adaptor he gave Alice, allowing him to derive the hidden value. Then he can combine that hidden value with the adaptor Alice gave him earlier.

```
{
    Transaction(Alice) [
        signature: «decryptSignature» [
            ❰encryptedSignature❱: EncryptedSignature(Alice)
            ❰decryptionKey❱: «recoverDecryptionKey» [
                ❰message❱: «digest» [
                    ❰_❱: $transaction
                ]
                ❰encryptedSignature❱: $encryptedSignature
                ❰signature❱: $signature
            ]
        ]
    ]
} [
    /transaction: Transaction(Alice)
    /encryptedSignature: EncryptedSignature(Bob)
    /signature: Signature(Bob)
]
```

After the replacements:

```
Transaction(Alice) [
    signature: «decryptSignature» [
        ❰encryptedSignature❱: EncryptedSignature(Alice)
        ❰decryptionKey❱: «recoverDecryptionKey» [
            ❰message❱: «digest» [
                ❰_❱: Transaction(Alice)
            ]
            ❰encryptedSignature❱: EncryptedSignature(Bob)
            ❰signature❱: Signature(Bob)
        ]
    ]
]
```

After the expression is evaluated:

```
Transaction(Alice) [
    signature: Signature(Alice)
]
```

Bob broadcasts that transaction to receive Alice’s payment, completing the coinswap.
