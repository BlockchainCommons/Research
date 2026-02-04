# Peer Endorsement Predicates

## BCR-2026-011

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for peer endorsements in Gordian Envelopes — signed attestations from one party about another that build webs of trust. It also provides a patterns guide for leveraging existing schemas (Schema.org, Open Badges, Verifiable Credentials) before defining new predicates.

The goal is **minimal new predicates** combined with **maximum reuse** of established standards.

## Status: Pre-Registration Proposal

📙 **Research** — This BCR proposes new Known Values and is seeking community review.

### Registration Intent

We propose registering these predicates in the **Community Assigned (specification required)** range (1000-1999) as defined in [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

This range is currently unassigned. We are seeking **rough consensus** from the Gordian developer community before claiming these codepoints. If the community determines these predicates:
- Do not merit the 1000-1999 range, or
- Should use different codepoint assignments

We will register in the **Community Assigned (first come-first served)** range (100000+) instead.

### Request for Community Review

We invite feedback on:
- Whether these predicates fill genuine gaps not covered by existing standards
- Whether the 1000-1999 range is appropriate for this vocabulary
- Alignment with existing endorsement/attestation vocabularies
- Use cases that require additional predicates
- Domain-specific profiles for software development, scholarly work, etc.

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### Problem Statement

Peer endorsements are a cornerstone of web-of-trust systems. When Alice endorses Bob's skills, she stakes her reputation on him. This bilateral trust relationship requires structured vocabulary to express:

- **Who** endorses whom
- **What** was observed
- **Why** the endorsement is credible
- **How** the endorser knows the subject
- **Acceptance** — that the subject consents to include the endorsement

Existing standards address parts of this problem, but none provide a complete vocabulary for peer-to-peer endorsement with relationship transparency and acceptance modeling.

### Design Principle: Reuse First

Before defining new predicates, check if existing standards provide the semantics you need:

| Need | Check First | Then |
|------|-------------|------|
| General attestation structure | Verifiable Credentials, Open Badges | Only define unique predicates |
| Timestamps | Schema.org `dateCreated` | Core `validFrom` (21), `validUntil` (22) |
| Evidence URLs | VC `evidence`, Schema.org `url` | Custom only if unique semantics |
| Contributor roles | CRediT taxonomy, BCR-2026-008 | Custom only if gap exists |
| Transparency | BCR-2026-005 `disclosedBias`, `disclosedLimitations` | — |

This BCR defines **only** the predicates that cannot be adequately expressed with existing standards.

### Solution

This specification defines:

**Unique predicates for peer endorsement:**

| Codepoint | Predicate | Purpose |
|-----------|-----------|---------|
| 1150 | `endorsementTarget` | What/who is being endorsed |
| 1151 | `endorserStatement` | What the endorser observed |
| 1152 | `endorsementBasis` | Why this endorsement is credible |
| 1153 | `endorserRelationship` | Relationship transparency |
| 1154 | `acceptedEndorsement` | Container for accepted endorsement |
| 1155 | `endorsementContext` | Context/scope of the endorsement |

**Type markers for endorsement domains:**

| Codepoint | Type Marker | Domain |
|-----------|-------------|--------|
| 1170 | `PeerEndorsement` | General peer-to-peer endorsements |
| 1171 | `CodeReviewEndorsement` | Software development — code review |
| 1172 | `CollaborationEndorsement` | Project collaboration |
| 1173 | `SkillEndorsement` | Specific skill/competency endorsement |

## Patterns Guide: Using Existing Schemas

### Pattern 1: Verifiable Credentials for Formal Attestations

For formal credentials with institutional backing, use the W3C Verifiable Credentials Data Model:

```
    Digest(vc-endorsement) [
        '@context': ["https://www.w3.org/ns/credentials/v2"]
        'type': ["VerifiableCredential", "EndorsementCredential"]
        'issuer': XID(endorser)
        'credentialSubject': {
            'id': XID(subject)
            'achievement': "Security Code Review Competency"
        }
        'issuanceDate': 2026-02-02
        'evidence': {
            'type': "CodeReviewEvidence"
            'id': "https://github.com/org/repo/pull/123"
        }
    ]
```

**When to use VC pattern:**
- Organizational endorsements with formal credential semantics
- Credentials that need to interoperate with VC ecosystems
- Situations requiring revocation lists or status checks

### Pattern 2: Open Badges for Skill Recognition

For skill endorsements in educational or professional contexts, use Open Badges v3:

```
    Digest(badge-endorsement) [
        '@context': "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json"
        'type': ["VerifiableCredential", "OpenBadgeCredential"]
        'issuer': {
            'type': "Profile"
            'id': XID(endorser)
            'name': "Security Review Team"
        }
        'credentialSubject': {
            'type': "AchievementSubject"
            'achievement': {
                'type': "Achievement"
                'name': "Code Security Review"
                'criteria': {
                    'narrative': "Demonstrated secure coding practices in 5+ reviewed PRs"
                }
            }
        }
    ]
```

**When to use Open Badges pattern:**
- Skill recognition that benefits from badge ecosystem interoperability
- Achievements with defined criteria
- Educational or certification contexts

### Pattern 3: Schema.org for Web-Discoverable Endorsements

For endorsements that need web search discoverability:

```
    Digest(schema-endorsement) [
        '@context': "https://schema.org"
        '@type': "Recommendation"
        'author': {
            '@type': "Person"
            'identifier': XID(endorser)
        }
        'itemReviewed': {
            '@type': "Person"
            'identifier': XID(subject)
        }
        'reviewBody': "Excellent security architecture skills..."
        'dateCreated': "2026-02-02T00:00:00Z"
    ]
```

**When to use Schema.org pattern:**
- Public endorsements for web discoverability
- Integration with search engines and social platforms

### Pattern 4: BCR Predicates for Peer-to-Peer Trust

Use BCR predicates when you need:
- Relationship transparency (how endorser knows subject)
- Acceptance model (subject consents to endorsement)
- Fair witness methodology (direct observation + limitations)
- Web-of-trust contexts without institutional backing

```
{
    Digest(peer-endorsement) [
        'isA': 'PeerEndorsement'
        'endorsementTarget': XID(subject)
        'endorserStatement': "Reviewed 8 PRs over 6 months; consistently high-quality security-focused code"
        'endorserRelationship': "Project maintainer who merged their contributions"
        'endorsementBasis': "Direct observation of code quality and collaboration"
        'disclosedLimitations': "Only reviewed backend security; cannot speak to frontend skills"
        'validFrom': 2026-02-02
        'signed': Signature
    ]
}
```

## Referenced Predicates

### From BCR-2026-005 (General Assertions)

This BCR references transparency predicates from BCR-2026-005:

| Codepoint | Predicate | Usage in Endorsements |
|-----------|-----------|----------------------|
| 1003 | `disclosedBias` | Endorser's potential biases ("I'm a friend") |
| 1004 | `disclosedLimitations` | Limits of endorser's knowledge |
| 1005 | `assertionLimitations` | Scope of endorsement itself |

**Do not define endorsement-specific bias/limitations predicates.** Use the general predicates from BCR-2026-005.

### From Core Registry

| Codepoint | Predicate | Usage |
|-----------|-----------|-------|
| 21 | `validFrom` | When endorsement becomes effective |
| 22 | `validUntil` | When endorsement expires (if applicable) |

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### Peer Endorsement Predicates (1150-1155)

---

#### 1150: `endorsementTarget`

**Type**: property
**Definition**: The entity (person, work, skill) being endorsed.
**Domain**: Peer endorsement assertion
**Range**: XID, Digest, or URI identifying the endorsement target
**Usage**: Identifies what or who this endorsement is about.

```
    Digest(endorsement) [
        'endorsementTarget': XID(alice)
        'endorserStatement': "Demonstrated excellent security review skills"
    ]
```

**Notes**:
- Similar to VC `credentialSubject` but designed for peer-to-peer context
- Can reference a person (XID), a work (Digest), or an external resource (URI)

---

#### 1151: `endorserStatement`

**Type**: property
**Definition**: The endorser's specific statement about what they observed.
**Domain**: Peer endorsement assertion
**Range**: Text
**Usage**: Captures the endorser's direct observation using fair witness methodology.

```
    Digest(endorsement) [
        'endorserStatement': "I reviewed 8 of their PRs over 6 months. All were well-structured with comprehensive test coverage."
    ]
```

**Notes**:
- Should describe direct observation, not speculation or hearsay
- Specific statements are more valuable than vague praise
- "I reviewed their code" is stronger than "They seem competent"

---

#### 1152: `endorsementBasis`

**Type**: property
**Definition**: The basis on which the endorser makes this endorsement.
**Domain**: Peer endorsement assertion
**Range**: Text
**Usage**: Explains why the endorser is credible for this endorsement.

```
    Digest(endorsement) [
        'endorsementBasis': "12 years as security architect; reviewed similar systems at 3 organizations"
    ]
```

**Notes**:
- Establishes endorser's qualification to make this endorsement
- Combined with `disclosedLimitations` from BCR-2026-005, provides full context

---

#### 1153: `endorserRelationship`

**Type**: property
**Definition**: The relationship between endorser and endorsed party.
**Domain**: Peer endorsement assertion
**Range**: Text
**Usage**: Provides relationship transparency essential for trust calibration.

```
    Digest(endorsement) [
        'endorserRelationship': "Project maintainer who merged their contributions over 6 months"
    ]
```

**Notes**:
- Critical for trust evaluation — "friend for 10 years" vs "random stranger"
- Enables recipients to calibrate for potential bias
- Should be honest even when relationship implies bias

---

#### 1154: `acceptedEndorsement`

**Type**: property
**Definition**: Container for an endorsement that the subject has accepted.
**Domain**: XIDDoc or participation profile
**Range**: Signed endorsement envelope
**Usage**: Indicates the subject reviewed and accepted this endorsement.

```
{
    XID(alice) [
        'acceptedEndorsement': {
            Digest(endorsement-from-bob) [
                'endorsementTarget': XID(alice)
                'endorserStatement': "..."
                'signed': Signature(bob)
            ]
        }
        'signed': Signature(alice)
    ]
}
```

**Notes**:
- The acceptance model ensures subjects maintain control over their identity
- Subject's signature on the containing document implies acceptance
- Subjects may decline endorsements they find inaccurate or unwanted

---

#### 1155: `endorsementContext`

**Type**: property
**Definition**: The context or scope within which the endorsement applies.
**Domain**: Peer endorsement assertion
**Range**: Text
**Usage**: Bounds the endorsement to specific contexts or capabilities.

```
    Digest(endorsement) [
        'endorsementContext': "Security architecture and cryptographic implementation"
        'endorserStatement': "..."
    ]
```

**Notes**:
- Prevents over-generalization of endorsements
- "I endorse their security skills" is different from "I endorse everything about them"
- Works with `assertionLimitations` from BCR-2026-005 for complete scoping

---

### Type Markers (1170-1173)

---

#### 1170: `PeerEndorsement`

**Type**: class
**Definition**: A type marker indicating a peer-to-peer endorsement.
**Usage**: General endorsements between individuals without institutional backing.

```
    Digest(endorsement) [
        'isA': 'PeerEndorsement'
        'endorsementTarget': XID(subject)
    ]
```

---

#### 1171: `CodeReviewEndorsement`

**Type**: class
**Definition**: An endorsement based on code review in software development.
**Usage**: Software-specific endorsements where the endorser reviewed code.

```
    Digest(endorsement) [
        'isA': 'CodeReviewEndorsement'
        'endorserStatement': "Reviewed PRs #123, #145, #167 — all demonstrated solid security practices"
        'endorsementBasis': "As project maintainer, I merged these contributions"
    ]
```

---

#### 1172: `CollaborationEndorsement`

**Type**: class
**Definition**: An endorsement based on project collaboration.
**Usage**: Endorsements from people who worked on projects together.

```
    Digest(endorsement) [
        'isA': 'CollaborationEndorsement'
        'endorserStatement': "Collaborated on 3-month security audit; reliable, communicative, delivered on commitments"
        'endorserRelationship': "Project collaborator and co-author"
    ]
```

---

#### 1173: `SkillEndorsement`

**Type**: class
**Definition**: An endorsement of specific skills or competencies.
**Usage**: Focused skill endorsements, often used in participation profiles.

```
    Digest(endorsement) [
        'isA': 'SkillEndorsement'
        'endorsementTarget': XID(subject)
        'endorsementContext': "Rust memory safety patterns"
        'endorserStatement': "Demonstrated deep understanding in our systems programming collaboration"
    ]
```

---

## Usage Patterns

### Complete Peer Endorsement

A well-formed peer endorsement includes observation, relationship, basis, and transparency:

```
{
    Digest(complete-endorsement) [
        'isA': 'PeerEndorsement'
        'endorsementTarget': XID(alice)
        'endorserStatement': "I reviewed 8 of their security-focused PRs. All demonstrated understanding of constant-time operations, proper key handling, and defense in depth."
        'endorserRelationship': "Project maintainer for crypto library; merged their contributions over 6 months"
        'endorsementBasis': "15 years security engineering; maintain similar libraries at 2 other organizations"
        'endorsementContext': "Cryptographic implementation and secure coding practices"
        'disclosedLimitations': "Only reviewed their crypto code; cannot speak to UI/UX or project management skills"
        'disclosedBias': "We have become professional friends through this collaboration"
        'validFrom': 2026-02-02
        'signed': Signature(endorser)
    ]
}
```

### Acceptance Model

The subject accepts endorsements by including them in their signed XIDDoc:

```
{
    XID(alice) [
        'acceptedEndorsement': {
            Digest(endorsement-from-bob) [
                'isA': 'CodeReviewEndorsement'
                'endorsementTarget': XID(alice)
                'endorserStatement': "..."
                'signed': Signature(bob)
            ]
        }
        'acceptedEndorsement': {
            Digest(endorsement-from-carol) [
                'isA': 'CollaborationEndorsement'
                'endorsementTarget': XID(alice)
                'endorserStatement': "..."
                'signed': Signature(carol)
            ]
        }
        'signed': Signature(alice)
    ]
}
```

The subject's signature on the outer document implies acceptance of all included endorsements.

### Combined with Signature Context

For endorsements that involve delegation or institutional context, combine with BCR-2026-006:

```
{
    Digest(institutional-endorsement) [
        'isA': 'PeerEndorsement'
        'endorsementTarget': XID(subject)
        'signingAs': "Security Review Committee Chair"
        'onBehalfOf': XID(organization)
        'endorserStatement': "Committee approved contributor status"
        'signed': Signature
    ]
}
```

## Relationship to Other BCRs

### BCR-2026-005 (General Assertions)

Use transparency predicates from BCR-2026-005:
- `disclosedBias` (1003) — endorser's biases
- `disclosedLimitations` (1004) — endorser's knowledge limits
- `assertionLimitations` (1005) — endorsement scope limits

### BCR-2026-006 (Signature Context)

For endorsements involving institutional or delegated signing:
- `signingAs` (1020) — capacity in which endorser signs
- `onBehalfOf` (1021) — organization endorser represents

### BCR-2026-007 (Principal Authority)

For endorsements that imply authority relationships:
- `principalAuthority` (1040) — when endorsement implies direction authority
- `assertsDelegationFrom` (1041) — when endorser claims delegation

### BCR-2026-008 (CreativeWork Roles)

For endorsements about creative contributions, use role predicates from BCR-2026-008 alongside endorsement predicates.

### BCR-2026-010 (Fair Witness)

Fair Witness predicates (BCR-2026-010) and Peer Endorsement predicates serve different purposes:

| Fair Witness | Peer Endorsement |
|--------------|------------------|
| Neutral third-party observation | Personal vouching for another |
| "I observed X happened" | "I endorse X's skills/character" |
| Temporal/additive (never revoked) | Can be withdrawn or superseded |
| Independence required | Relationship expected |

Use Fair Witness for neutral attestation of facts; use Peer Endorsement for personal vouching.

## Security Considerations

### Endorsement Trust

An endorsement is only as trustworthy as:
- The endorser's reputation
- The specificity of the observation
- The transparency of the relationship
- The endorser's domain expertise

Vague endorsements ("X is great!") carry less weight than specific ones ("I reviewed X's code for 6 months").

### Acceptance Model Importance

The acceptance model protects against:
- Unwanted association with endorsers
- Inaccurate endorsements damaging reputation
- Endorsement spam or manipulation

Subjects should review endorsements before accepting them into their identity documents.

### Herd Privacy

When multiple pseudonymous identities have endorsements, individual identification becomes harder. This "herd privacy" is a feature, not a bug — it enables pseudonymous participation while building real trust through endorsements.

### Endorsement Lifecycle

Endorsements are point-in-time statements. They don't automatically update if:
- The subject's skills change
- The relationship changes
- The endorser's opinion changes

For changed circumstances, endorsers can create superseding endorsements using `supersedes` from BCR-2026-005.

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model-2.0/)
- [Open Badges Specification v3.0](https://www.imsglobal.org/spec/ob/v3p0/)
- [Schema.org Recommendation](https://schema.org/Recommendation)
- [XID-Quickstart: Attestation and Endorsement Model](https://github.com/BlockchainCommons/XID-Quickstart/blob/main/concepts/attestation-endorsement-model.md)

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Transparency predicates (`disclosedBias`, etc.)
- **BCR-2026-006: Signature Context Predicates** — Institutional/delegated signing
- **BCR-2026-007: Principal Authority Predicates** — Authority relationships
- **BCR-2026-010: Fair Witness Predicates** — Neutral observation (distinct from endorsement)

---

*BCR-2026-011: Peer Endorsement Predicates*
*Draft - February 2, 2026*
