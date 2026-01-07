# blockchain_commons Known Values Registry

## Ontology Information

| Property | Value |
|----------|-------|
| **Name** | blockchain_commons |
| **Source URL** | https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md |
| **Start Code Point** | 0 |
| **Processing Strategy** | Manual |

## Statistics

| Metric | Value |
|--------|-------|
| **Total Entries** | 88 |
| **Code Point Range** | 0 - 705 |

## Entries

### General (0-24)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 0 | `''` | unit |  | The Unit type, and its sole inhabitant '', which is a value conveying no information. |
| 1 | `isA` | property | http://www.w3.org/1999/02/22-rdf-syntax-ns#type | The subject is an instance of the class identified by the object. |
| 2 | `id` | property | http://purl.org/dc/terms/identifier | The object is an unambiguous identifier of the subject within a given context. |
| 3 | `signed` | property |  | The object is a cryptographic signature of the subject. |
| 4 | `note` | property | http://www.w3.org/2000/01/rdf-schema#comment | The object is a human-readable note about the subject. |
| 5 | `hasRecipient` | property |  | The subject can be decrypted using the private key that decrypts the content key in the object. |
| 6 | `sskrShare` | property |  | The subject can be decrypted by a quorum of SSKR shares including the one in the object. |
| 7 | `controller` | property | https://www.w3.org/ns/solid/terms#owner | The object is the subject's controlling entity. |
| 8 | `key` | property |  | The entity identified by the subject holds the private half of the public keys(s) in the object. |
| 9 | `dereferenceVia` | property |  | The content referenced by the subject can be dereferenced using the object. |
| 10 | `entity` | property |  | The entity referenced by the subject is specified in the object. |
| 11 | `name` | property | http://xmlns.com/foaf/spec/#term_name | The subject is known by the name in the object. |
| 12 | `language` | property | http://www.w3.org/1999/02/22-rdf-syntax-ns#langString | The subject is written in the language of the ISO language code object. |
| 13 | `issuer` | property |  | The object is the subject's issuing entity. |
| 14 | `holder` | property |  | The object identifies the entity to which the subject has been issued. |
| 15 | `salt` | property |  | The object is random salt used to decorrelate the digest of the subject. |
| 16 | `date` | property | http://purl.org/dc/terms/date | The object is a primary datestamp of the subject. |
| 17 | `Unknown` | value | https://en.wikipedia.org/wiki/Blank_node | Placeholder for an unknown value. |
| 18 | `version` | property | http://purl.org/dc/terms/hasVersion | The object is the version of the subject. |
| 19 | `hasSecret` | property |  | The subject can be decrypted using the secret that decrypts the content key in the object. |
| 20 | `edits` | property |  | The object is a set of edits used by the Envelope.transform(edits:) method. |
| 21 | `validFrom` | property | http://purl.org/dc/terms/valid | The subject is valid from the date in the object. |
| 22 | `validUntil` | property | https://schema.org/validUntil | The subject is valid until the date in the object. |
| 23 | `position` | property | https://schema.org/position | The position of an item in a series or sequence of items. |
| 24 | `nickname` | property | http://xmlns.com/foaf/spec/#term_nick | The subject is a nickname for the object. |

### Attachments (50-52)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 50 | `attachment` | property |  | Declares that the object is a vendor-defined attachment to the envelope. |
| 51 | `vendor` | property |  | Declares the vendor of the subject. |
| 52 | `conformsTo` | property | http://purl.org/dc/terms/conformsTo | An established standard to which the subject conforms. |

### XID Documents (60-68)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 60 | `allow` | property |  | The object is a set of permissions that allow the subject to perform the actions specified in the object. |
| 61 | `deny` | property |  | The object is a set of permissions that deny the subject from performing the actions specified in the object. |
| 62 | `endpoint` | property |  | The object is a service endpoint associated with the subject. |
| 63 | `delegate` | property |  | The object is a delegate authorized by the subject. |
| 64 | `provenance` | property |  | The object is a provenance mark associated with the subject. |
| 65 | `privateKey` | property |  | The object is a private key associated with the subject. |
| 66 | `service` | property |  | The object is a service associated with the subject. |
| 67 | `capability` | property |  | The object is a capability associated with the subject. |
| 68 | `provenanceGenerator` | property |  | The object is a provenance mark generator associated with the subject. |

### XID Privileges (70-86)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 70 | `All` | value |  | The set of all allowed privileges. |
| 71 | `Authorize` | value |  | Operational privilege: authorize actions on behalf of the subject. |
| 72 | `Sign` | value |  | Operational privilege: sign documents on behalf of the subject. |
| 73 | `Encrypt` | value |  | Operational privilege: encrypt messages from the subject and decrypt messages to the subject. |
| 74 | `Elide` | value |  | Operational privilege: elide the subject's documents. |
| 75 | `Issue` | value |  | Operational privilege: issue documents on behalf of the subject. |
| 76 | `Access` | value |  | Operational privilege: access resources on behalf of the subject. |
| 80 | `Delegate` | value |  | Management privilege: delegate the privileges of the subject to another entity. |
| 81 | `Verify` | value |  | Management privilege: update the subject's documents, including the ability to reduce privileges. |
| 82 | `Update` | value |  | Management privilege: update the subject's service endpoints. |
| 83 | `Transfer` | value |  | Management privilege: remove the inception key from the XID document. |
| 84 | `Elect` | value |  | Management privilege: add or remove other verifiers (rotate keys). |
| 85 | `Burn` | value |  | Management privilege: transition to a new provenance mark chain. |
| 86 | `Revoke` | value |  | Management privilege: revoke the XID entirely. |

### Expression and Function Calls (101-108)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 101 | `result` | property |  | The object is the success result of the request identified by the subject. |
| 102 | `error` | property |  | The object is the failure result of the request identified by the subject. |
| 103 | `OK` | value |  | The success result of a request that has no other return value. |
| 104 | `Processing` | value |  | The "in processing" result of a request. |
| 105 | `sender` | property |  | The object identifies the sender, including a way to verify messages from the sender (e.g. public key). |
| 106 | `senderContinuation` | property |  | The object is a continuation owned by the sender. |
| 107 | `recipientContinuation` | property |  | The object is a continuation owned by the recipient. |
| 108 | `content` | property |  | The object is the content of the event. |

### Cryptography (200-203)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 200 | `Seed` | class |  | A cryptographic seed. |
| 201 | `PrivateKey` | class |  | A cryptographic private key. |
| 202 | `PublicKey` | class |  | A cryptographic public key. |
| 203 | `MasterKey` | class |  | A cryptographic master key. |

### Cryptocurrency Assets (300-303)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 300 | `asset` | property |  | Declares a cryptocurrency asset specifier, e.g. "Bitcoin", "Ethereum" |
| 301 | `Bitcoin` | value |  | The Bitcoin cryptocurrency ("BTC") |
| 302 | `Ethereum` | value |  | The Ethereum cryptocurrency ("ETH") |
| 303 | `Tezos` | value |  | The Tezos cryptocurrency ("XTZ") |

### Cryptocurrency Networks (400-402)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 400 | `network` | property |  | Declares a cryptocurrency network, e.g. "MainNet", "TestNet" |
| 401 | `MainNet` | value |  | A cryptocurrency main network |
| 402 | `TestNet` | value |  | A cryptocurrency test network |

### Bitcoin (500-508)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 500 | `BIP32Key` | class |  | A BIP-32 HD key |
| 501 | `chainCode` | property |  | Declares the chain code of a BIP-32 HD key |
| 502 | `DerivationPath` | class |  | A BIP-32 derivation path |
| 503 | `parentPath` | property |  | Declares the derivation path for a BIP-32 key |
| 504 | `childrenPath` | property |  | Declares the allowable derivation paths from a BIP-32 key |
| 505 | `parentFingerprint` | property |  | Declares the parent fingerprint of a BIP-32 key |
| 506 | `PSBT` | class |  | A Partially-Signed Bitcoin Transaction (PSBT) |
| 507 | `OutputDescriptor` | class |  | A Bitcoin output descriptor |
| 508 | `outputDescriptor` | property |  | Declares a Bitcoin output descriptor associated with the subject |

### Graphs (600-705)

| Codepoint | Canonical Name | Type | URI | Description |
|-----------|----------------|------|-----|-------------|
| 600 | `Graph` | class |  | A graph. All other assertions in the envelope must be either node or edge. |
| 601 | `SourceTargetGraph` | class |  | A graph with edges that have source and target assertions. |
| 602 | `ParentChildGraph` | class |  | A graph with edges that have parent and child assertions. |
| 603 | `Digraph` | class |  | A directed graph. Implies SourceTargetGraph. source and target are distinct. |
| 604 | `AcyclicGraph` | class |  | A graph that does not admit cycles. Implies SourceTargetGraph. |
| 605 | `Multigraph` | class |  | A multigraph (admits parallel edges). Implies SourceTargetGraph. |
| 606 | `Pseudograph` | class |  | A pseudograph (admits self-loops and parallel edges). Implies Multigraph. |
| 607 | `GraphFragment` | class |  | A fragment of a graph. May have references to external nodes and edges that are not resolvable in the fragment. |
| 608 | `DAG` | class |  | A directed acyclic graph. Implies Digraph and AcyclicGraph. |
| 609 | `Tree` | class |  | A tree. Implies ParentChildGraph. Exactly one node must have no parent. All other nodes must have exactly one parent. |
| 610 | `Forest` | class |  | A forest (set of trees). Implies ParentChildGraph. |
| 611 | `CompoundGraph` | class |  | A compound graph (a graph with subgraphs). Implies Forest and SourceTargetGraph. |
| 612 | `Hypergraph` | class |  | An undirected hypergraph (edges may connect more than two nodes). |
| 613 | `Dihypergraph` | class |  | A directed hypergraph (edges may connect more than two nodes and have a direction). Implies Hypergraph and Digraph. |
| 700 | `node` | property |  | A node in a graph. |
| 701 | `edge` | property |  | An edge in a graph. |
| 702 | `source` | property |  | Identifies the source node of the subject edge of a SourceTargetGraph. |
| 703 | `target` | property |  | Identifies the target node of the subject edge of a SourceTargetGraph. |
| 704 | `parent` | property |  | Identifies the parent node of the subject edge of a ParentChildGraph. |
| 705 | `child` | property |  | Identifies a child node of the subject edge of a ParentChildGraph. |
