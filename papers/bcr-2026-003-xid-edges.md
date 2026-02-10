# Edges in XID Documents

## BCR-2026-003

**© 2026 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: January 29, 2026

---

## Introduction

A [XID document](bcr-2024-010-xid.md) identifies an entity — a person, organization, device, or abstract subject — and declares the keys, endpoints, and permissions needed to interact with it. But identification alone is not enough. Entities exist in webs of relationships: a person holds a degree, an employee works for a company, a device is certified by a manufacturer. These relationships are *claims* — statements one entity makes about another (or about itself).

This document defines *edges*, the mechanism by which XID documents represent verifiable claims. An edge is a signed [Gordian Envelope](bcr-2024-003-envelope.md) that connects a *source* (the claimant) to a *target* (the entity the claim is about), typed by an ontological concept that describes the nature of the claim. Edges are designed to be independently verifiable: each one carries its own signature and can be extracted from its containing XID document and forwarded to third parties without losing its integrity.

The design draws on the graph representation patterns described in [BCR-2024-006](bcr-2024-006-envelope-graph.md), adapting them for the specific needs of identity documents.

### Status

⭐️ This document is has a reference implementation in the `bc-envelope` crate and downstream tools like `bc-envelope-cli`. It is open for community feedback.

## Design Rationale

In a full entity-relationship model, not every claim is a simple binary relationship. A credential, for instance, is an entity in its own right: a university *confers* a credential, and that credential is *conferred upon* a student. Modeling this faithfully would require the credential to be a first-class node with its own incoming and outgoing edges.

Edges in XID documents deliberately flatten this into a single directed connection — source, target, and a type — for two reasons:

1. **Edges connect agents.** Both the source and target of an edge are XIDs backed by XID documents: entities with keys, permissions, and the ability to sign and verify. The edge subject (a credential number, a UUID) is just an identifier — it has no XID document, no keys, and no ability to participate as a source or target of further edges. Modeling it as a first-class graph node would add complexity without a corresponding agent to anchor it.

2. **`'isA'` is intentionally overloaded.** For a colleague relationship, `'isA': 'schema:colleague'` types the relationship itself. For a credential, `'isA': 'schema:EducationalOccupationalCredential'` types what is formally an intermediate entity. This overloading is a pragmatic trade-off: the three-assertion structure remains uniform and simple, at the cost of not distinguishing relationship-typed edges from entity-typed edges at the structural level.

If a future use case requires intermediate objects to be first-class participants — holding their own edges, being independently resolvable, carrying their own keys — that would be defined by an envelope schema for that object type, outside the scope of this specification.

## Edge Structure

An edge is a [Gordian Envelope](bcr-2024-003-envelope.md) whose subject is a locally unique identifier. The edge has exactly three assertions:

- `'isA'` — The type of claim, drawn from a [supported ontology](bcr-2023-002-known-value.md). This classifies the edge (e.g., `'foaf:Person'`, `'schema:colleague'`, `'schema:EducationalOccupationalCredential'`).
- `'source'` — The XID of the *claimant*: the entity making the claim and signing the edge.
- `'target'` — The XID of the entity the claim is *about*. This may be the same as the source (a self-asserted claim) or a different entity (a third-party claim).

No other assertions are permitted on the edge subject. The edge subject and its three assertions define *what kind of claim is being made, by whom, and about whom*. All additional detail — the substance of the claim — is carried as assertions on the *target* object.

This placement follows directly from a foundational principle of Gordian Envelope: assertions on a subject are always claims about the *referent* — the real-world thing — that the subject identifies. The edge subject (a UUID, credential number, or other identifier) refers to the *claim itself*; its three assertions correctly describe properties of the claim — its type, its claimant, and its subject entity. The target XID, by contrast, refers to the *real-world entity* the claim is about. Placing claim details like `'foaf:firstName': "Bob"` or `'schema:credentialCategory': "degree"` on the target object therefore asserts those facts about the entity, which is semantically correct. Placing them on the edge subject would assert that the *claim* has a first name or credential category — a category error. The three-assertion constraint enforces this boundary, keeping the edge's topology (type, source, target) cleanly separated from the claim's substance (which belongs to the target's referent).

In schematic form:

```envelope
<edge-identifier> [
    'isA': <claim-type>
    'source': <claimant-XID>
    'target': <subject-XID> [
        <claim-detail>
        <claim-detail>
        ...
    ]
]
```

The `target` object MAY carry any number of assertions describing the claim. These assertions use predicates from supported ontologies (FOAF, Schema.org, Dublin Core, etc.) to express the claim's content in a machine-readable way. The target object MAY also include a `'dereferenceVia'` assertion providing a resolution method for the target XID, enabling verifiers to look up the target entity's full XID document.

Similarly, the source XID MAY carry a `'dereferenceVia'` assertion providing a resolution method for the claimant's XID document and verifying the edge's signature.

## Edge Identifiers

Every edge's subject MUST be locally unique within a scope defined by the claimant; by default this scope is the XID document itself. Claims may be issued with a natural external identifier — such as a credential number, certificate ID, or serial number — that identifier is the edge subject. When no natural identifier exists, a UUID SHOULD be generated.

The *globally unique reference* for any edge is the tuple of the source XID and the edge subject:

$$(\text{source XID}, \text{edge subject})$$

For example:

- $(XID(\texttt{5b9a72e1}), \texttt{"ESU-2024-CS-MS-1047"})$ — a credential issued by a university
- $(XID(\texttt{988f199d}), UUID(\texttt{97184e91-...}))$ — a self-asserted personal description

This tuple enables precise cross-document citation. A revocation, for instance, can reference a specific edge by its globally unique identifier without ambiguity.

## Signing

Every edge MUST be wrapped and signed by the claimant (the entity identified by `'source'`). This is the standard Gordian Envelope signing pattern: the edge envelope is wrapped in curly braces and a `'signed'` assertion is placed on the outer envelope.

```envelope
{
    <edge-identifier> [
        'isA': <claim-type>
        'source': <claimant-XID>
        'target': <subject-XID> [
            <claim-detail>
        ]
    ]
} [
    'signed': Signature
]
```

Signing each edge individually — rather than relying solely on the outer XID document signature — makes edges *portable*. An edge extracted from a XID document remains independently verifiable because it carries its own proof of authenticity.

When metadata such as the date of signing needs to accompany the signature, the [signature metadata](bcr-2024-009-signature-metadata.md) pattern is used. Rather than adding a `'date'` assertion to the edge subject (which would violate the three-assertion constraint), the date is attached to the signature itself:

```envelope
{
    <edge-identifier> [
        'isA': <claim-type>
        'source': <claimant-XID>
        'target': <subject-XID> [
            <claim-detail>
        ]
    ]
} [
    'signed': {
        Signature [
            'date': Date(2024-05-15)
        ]
    } [
        'signed': Signature
    ]
]
```

In this pattern, both the inner `Signature` (which signs the edge payload) and the outer `Signature` (which signs the signature-plus-metadata envelope) are produced by the same key. Verifiers check both signatures to confirm the edge's authenticity and the integrity of its metadata. See [BCR-2024-009](bcr-2024-009-signature-metadata.md) for a detailed treatment of this pattern.

## Embedding Edges in XID Documents

Edges are embedded in a XID document using the `'edge'` predicate. A single XID document may contain any number of edges, from any combination of sources. Some edges may be self-asserted (signed by the document holder), while others may be third-party claims (signed by external entities and embedded by the document holder).

```envelope
XID(988f199d) [
    'edge': <signed-edge-1>
    'edge': <signed-edge-2>
    'edge': <signed-edge-3>
    ...
]
```

The containing XID document is itself typically wrapped and signed, providing document-level integrity. But the individual edge signatures are what provide claim-level verifiability.

## Examples

The following examples build a XID document for a fictional person, Bob Johnson, demonstrating three patterns: self-description, a relationship claim, and a third-party credential.

### Self-Description

Bob describes himself. Both the source and target are Bob's own XID. The target object carries FOAF properties with Bob's personal information:

```envelope
{
    UUID(97184e91-03d5-4127-ac57-aabfd77e790c) [
        'isA': 'foaf:Person'
        'source': XID(988f199d)
        'target': XID(988f199d) [
            'foaf:firstName': "Bob"
            'foaf:lastName': "Johnson"
            'foaf:mbox': URI("mailto:bob@example.com")
        ]
    ]
} [
    'signed': Signature
]
```

The edge subject is a UUID generated by Bob, locally unique within his XID document. The globally unique reference for this edge is $(XID(\texttt{988f199d}), UUID(\texttt{97184e91-...}))$.

Because this is a self-asserted edge, the signature is Bob's own. The claim is not independently verified — it simply records that Bob chose to make these assertions about himself.

### Relationship Claim

Bob asserts that Alice is a colleague. The source is Bob's XID and the target is Alice's XID. The target object carries assertions describing the relationship, including details of a past collaboration:

```envelope
{
    UUID(b4e1a8c0-65f2-4e9b-9d3a-7c8f2d1e6b5a) [
        'isA': 'schema:colleague'
        'source': XID(988f199d)
        'target': XID(1a2b3c4d) [
            'dereferenceVia': URI("https://example.com/people/alice/xid/")
            'foaf:firstName': "Alice"
            'foaf:lastName': "Smith"
            'foaf:mbox': URI("mailto:alice@example.com")
            'foaf:pastProject': URI("https://example.com/projects/project-x") [
                'schema:roleName': "Lead Developer"
                'schema:startDate': Date(2020-01-15)
                'schema:endDate': Date(2023-06-30)
                'schema:responsibilities': "Developed the core architecture and led the development team."
                'schema:review': "Outstanding performance and leadership skills demonstrated."
            ]
        ]
    ]
} [
    'signed': Signature
]
```

The target XID includes a `'dereferenceVia'` assertion, allowing a verifier to resolve Alice's XID document and confirm her identity. The `'foaf:pastProject'` assertion on the target carries its own nested assertions describing the collaboration.

This edge is signed by Bob. It represents Bob's claim about his relationship with Alice — Alice has not necessarily endorsed it. For a mutually endorsed relationship, Alice would embed a reciprocal edge in her own XID document.

### Third-Party Credential

Example State University grants Bob a Master of Science in Computer Science. The university creates and signs the edge; Bob embeds it in his XID document. The edge subject is the university's own credential identifier:

```envelope
{
    "ESU-2024-CS-MS-1047" [
        'isA': 'schema:EducationalOccupationalCredential'
        'source': XID(5b9a72e1) [
            'dereferenceVia': URI("https://examplestate.edu/xid/")
            'isA': 'schema:CollegeOrUniversity'
            'schema:name': "Example State University"
        ]
        'target': XID(988f199d) [
            'schema:name': "Master of Science in Computer Science"
            'schema:credentialCategory': "degree"
            'schema:educationalLevel': "Master's"
        ]
    ]
} [
    'signed': {
        Signature [
            'date': Date(2024-05-15)
        ]
    } [
        'signed': Signature
    ]
]
```

Several things distinguish this edge from the self-asserted examples:

- The **source** is the university's XID, not Bob's. The university is the claimant.
- The **edge subject** is a domain-specific credential identifier (`"ESU-2024-CS-MS-1047"`) rather than a UUID. Its globally unique reference is $(XID(\texttt{5b9a72e1}), \texttt{"ESU-2024-CS-MS-1047"})$.
- The **signature** is the university's, not Bob's. Bob embeds this signed edge in his own XID document, but he cannot forge or alter it without invalidating the university's signature.
- The **date** is carried as [signature metadata](bcr-2024-009-signature-metadata.md), not as an assertion on the edge subject. This records when the credential was signed while respecting the three-assertion constraint on the edge subject.
- The source XID carries `'dereferenceVia'` and additional assertions identifying the university, enabling verifiers to resolve the university's XID document and obtain the public key needed to verify the signature.

### Complete XID Document

With all three edges embedded, Bob's complete XID document looks like this:

```envelope
{
    XID(988f199d) [
        'dereferenceVia': URI("https://example.com/people/bob/xid/")
        'edge': {
            UUID(97184e91-03d5-4127-ac57-aabfd77e790c) [
                'isA': 'foaf:Person'
                'source': XID(988f199d)
                'target': XID(988f199d) [
                    'foaf:firstName': "Bob"
                    'foaf:lastName': "Johnson"
                    'foaf:mbox': URI("mailto:bob@example.com")
                ]
            ]
        } [
            'signed': Signature
        ]
        'edge': {
            UUID(b4e1a8c0-65f2-4e9b-9d3a-7c8f2d1e6b5a) [
                'isA': 'schema:colleague'
                'source': XID(988f199d)
                'target': XID(1a2b3c4d) [
                    'dereferenceVia': URI("https://example.com/people/alice/xid/")
                    'foaf:firstName': "Alice"
                    'foaf:lastName': "Smith"
                    'foaf:mbox': URI("mailto:alice@example.com")
                    'foaf:pastProject': URI("https://example.com/projects/project-x") [
                        'schema:roleName': "Lead Developer"
                        'schema:startDate': Date(2020-01-15)
                        'schema:endDate': Date(2023-06-30)
                        'schema:responsibilities': "Developed the core architecture and led the development team."
                        'schema:review': "Outstanding performance and leadership skills demonstrated."
                    ]
                ]
            ]
        } [
            'signed': Signature
        ]
        'edge': {
            "ESU-2024-CS-MS-1047" [
                'isA': 'schema:EducationalOccupationalCredential'
                'source': XID(5b9a72e1) [
                    'dereferenceVia': URI("https://examplestate.edu/xid/")
                    'isA': 'schema:CollegeOrUniversity'
                    'schema:name': "Example State University"
                ]
                'target': XID(988f199d) [
                    'schema:name': "Master of Science in Computer Science"
                    'schema:credentialCategory': "degree"
                    'schema:educationalLevel': "Master's"
                ]
            ]
        } [
            'signed': {
                Signature [
                    'date': Date(2024-05-15)
                ]
            } [
                'signed': Signature
            ]
        ]
        'key': ELIDED
        'provenance': ELIDED
    ]
} [
    'signed': ELIDED
]
```

The outer `'signed': ELIDED` is Bob's signature over the entire XID document envelope. The `'key'` and `'provenance'` assertions are elided for this view, as described in [BCR-2024-010](bcr-2024-010-xid.md).

## Selective Disclosure

Because Gordian Envelope preserves its Merkle-like digest tree even when parts are elided, Bob can selectively disclose edges without invalidating the document-level signature. For example, Bob might share his credential while eliding his personal details and colleague relationship:

```envelope
{
    XID(988f199d) [
        'dereferenceVia': URI("https://example.com/people/bob/xid/")
        ELIDED (2)
        'edge': {
            "ESU-2024-CS-MS-1047" [
                'isA': 'schema:EducationalOccupationalCredential'
                'source': XID(5b9a72e1) [
                    'dereferenceVia': URI("https://examplestate.edu/xid/")
                    'isA': 'schema:CollegeOrUniversity'
                    'schema:name': "Example State University"
                ]
                'target': XID(988f199d) [
                    'schema:name': "Master of Science in Computer Science"
                    'schema:credentialCategory': "degree"
                    'schema:educationalLevel': "Master's"
                ]
            ]
        } [
            'signed': {
                Signature [
                    'date': Date(2024-05-15)
                ]
            } [
                'signed': Signature
            ]
        ]
        'key': ELIDED
        'provenance': ELIDED
    ]
} [
    'signed': ELIDED
]
```

The two elided edges are replaced by their digests. A verifier who has seen the full document can confirm these digests match, but the elided content is not disclosed.

Elision can also operate *within* an edge. Bob might disclose that he has a colleague relationship without revealing the colleague's identity or the project details:

```envelope
{
    UUID(b4e1a8c0-65f2-4e9b-9d3a-7c8f2d1e6b5a) [
        'isA': 'schema:colleague'
        'source': XID(988f199d)
        'target': ELIDED
    ]
} [
    'signed': Signature
]
```

The edge structure remains intact — the three required assertions are visible — but the target object (and all its assertions about Alice) has been elided.

## Extracting Edges

An edge can be extracted from a XID document and forwarded as an independent document, and remains fully meaningful outside its original context.

For example, Bob could extract the university credential and send it to a prospective employer:

```envelope
{
    "ESU-2024-CS-MS-1047" [
        'isA': 'schema:EducationalOccupationalCredential'
        'source': XID(5b9a72e1) [
            'dereferenceVia': URI("https://examplestate.edu/xid/")
            'isA': 'schema:CollegeOrUniversity'
            'schema:name': "Example State University"
        ]
        'target': XID(988f199d) [
            'schema:name': "Master of Science in Computer Science"
            'schema:credentialCategory': "degree"
            'schema:educationalLevel': "Master's"
        ]
    ]
} [
    'signed': {
        Signature [
            'date': Date(2024-05-15)
        ]
    } [
        'signed': Signature
    ]
]
```

This is a complete, self-contained document. The employer can verify it without needing Bob's XID document at all.

## Verifying Third-Party Edges

To verify a third-party edge such as the credential above, a verifier follows these steps:

1. **Identify the claimant.** The `'source'` assertion gives the claimant's XID: `XID(5b9a72e1)`.

2. **Resolve the claimant's XID document.** The `'dereferenceVia'` assertion on the source provides a resolution URL: `https://examplestate.edu/xid/`. The verifier fetches the university's full XID document from this URL.

3. **Obtain the claimant's public key.** The resolved XID document contains `'key'` assertions declaring the university's public keys and their permissions. The verifier selects a key with the appropriate permission (e.g., `'Sign'` or `'All'`).

4. **Verify the signature.** Using the university's public key, the verifier checks the signature on the edge envelope. If the signature metadata pattern is used, both the inner signature (over the edge payload) and the outer signature (over the signature-plus-metadata) must be valid.

5. **Evaluate trust.** Cryptographic verification confirms the edge was signed by a key controlled by `XID(5b9a72e1)`. Whether to *trust* that XID as a legitimate university is a separate question, answered by the verifier's own trust framework — web of trust, certificate authority, out-of-band verification, or other means.

## Known Value Assignments

The following [known values](bcr-2023-002-known-value.md) are used in edges:

| Code Point | Name             | Role in Edges                                       |
|------------|------------------|-----------------------------------------------------|
| 1          | `isA`            | Required. Types the edge.                           |
| 3          | `signed`         | Required. Carries the claimant's signature.         |
| 9          | `dereferenceVia` | Optional. Resolution URL for source or target XID.  |
| 16         | `date`           | Optional. Date of signing, in signature metadata.   |
| 701        | `edge`           | Predicate for embedding an edge in a XID document.  |
| 702        | `source`         | Required. The claimant's XID.                       |
| 703        | `target`         | Required. The XID of the entity the claim is about. |

Edge type values (the object of `'isA'`) are drawn from the known value registries for supported ontologies. See [BCR-2023-002](bcr-2023-002-known-value.md) for the full list of assigned code points.

## Summary of Constraints

An edge in a XID document:

- MUST have a subject that is locally unique within the claimant's scope (a UUID, credential ID, or other identifier).
- MUST have exactly three assertions on its subject: `'isA'`, `'source'`, and `'target'`. No other assertions are permitted on the edge subject.
- MUST be wrapped and signed by the claimant identified in `'source'`.
- MAY carry arbitrary assertions on the target object, describing the substance of the claim.
- MAY carry a `'dereferenceVia'` assertion on the source XID to enable resolution of the claimant's XID document.
- MAY use [signature metadata](bcr-2024-009-signature-metadata.md) to attach a date or other metadata to the signature.
- Is globally referenceable by the tuple (source XID, edge subject).
