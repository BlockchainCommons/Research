# Fair Witness Predicates

## BCR-2026-010

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for Fair Witness attestations in Gordian Envelopes. These predicates support human observation and attestation, where a neutral third party observes and attests to facts without advocacy or interpretation.

Fair Witness predicates are distinct from Anchor predicates (BCR-2026-004): anchors provide **cryptographic attestation** to event logs, while Fair Witness predicates support **human observation attestation** with disclosures about independence and perspective.

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
- Whether these predicates fill genuine gaps in the Known Value registry
- Whether the 1000-1999 range is appropriate for this vocabulary
- Any conflicts or overlaps with existing ontologies
- Suggested refinements to predicate definitions

Please submit feedback via:
- [Gordian Developer Community Discussions](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions)
- Pull requests to this specification

## Introduction

### The Fair Witness Concept

The Fair Witness approach derives from Robert A. Heinlein's *Stranger in a Strange Land* (1961), where Fair Witnesses were professionals trained to observe events with perfect objectivity and recall. Rather than making assumptions, they reported only direct observations with acknowledged limitations.

A Fair Witness distinguishes between what was directly observed versus interpretation. When viewing a distant house, a Fair Witness might say: "It appears to be painted white on this side" — never making unqualified claims about what they haven't observed.

This approach rests on three foundational pillars:

1. **Core Observation** — Prioritize specificity about what was directly witnessed
2. **Context & Methodology** — Supply relevant background, explain how observations occurred, reference supporting evidence
3. **Limitations & Transparency** — Acknowledge what remained unobserved, separate facts from interpretations, disclose potential biases

### Problem Statement

Many assertions benefit from third-party attestation by someone who observed the facts being claimed. This is distinct from:

- **Signing** — which implies authorship or consent
- **Endorsing** — which implies approval or recommendation
- **Anchoring** — which provides cryptographic proof of existence in a log

A Fair Witness provides **neutral observation attestation** — "I observed X" — without implying approval, recommendation, or participation. This methodology enables trust-building by emphasizing *verifiability over authority* and *context over claims*.

### Temporal and Additive Nature

Fair Witness attestations are inherently **temporal and additive**:

- The same witness may observe the same subject multiple times
- Each observation is timestamped independently
- Observations are **never revoked** — newer observations supplement rather than replace older ones
- Trust builds through accumulated observations over time

This differs from credentials (which may be revoked) or endorsements (which may be withdrawn). A Fair Witness attestation from 2024 remains valid as "what the witness observed in 2024" even after new observations in 2026.

### Use Cases

The Fair Witness pattern is valuable for:

- Contract signing ceremonies
- Physical asset verification
- Event attestation and audit trails
- Progressive trust building in pseudonymous environments
- Legal depositions in digital form

### Terminology Distinction

The term "witness" is overloaded in technical contexts:

| Term | Domain | Meaning |
|------|--------|---------|
| **Fair Witness** | Human attestation | Neutral party observing and attesting to facts |
| **Cryptographic witness** | Event logs | Entity anchoring assertions to a log |
| **Witness** (legal) | Courts | Person giving testimony |
| **Witness** (cryptography) | Zero-knowledge proofs | Proof component |

This BCR uses the **`observer*`** prefix to avoid ambiguity with cryptographic witnesses (which use `anchor*` in BCR-2026-004).

### Solution

This specification defines five predicates for Fair Witness attestation, mapping to the three pillars:

| Predicate | Pillar | Purpose |
|-----------|--------|---------|
| `observerWitness` | Core | Who observed and attests |
| `observationTimestamp` | Core | When the observation occurred |
| `observerStatement` | Core | What was directly observed |
| `observerPhysicalPresence` | Context | Whether observer was physically present |
| `observerIndependence` | Transparency | Declaration of neutrality |

For transparency disclosure (biases and limitations), Fair Witness attestations use the general predicates from BCR-2026-005:

| Predicate | Codepoint | Purpose |
|-----------|-----------|---------|
| `disclosedBias` | 1003 | Potential biases affecting the observation |
| `disclosedLimitations` | 1004 | Limitations on the observer's knowledge or perspective |
| `assertionLimitations` | 1005 | Scope or constraints of the observation itself |

## Terminology

**Fair Witness**: A neutral third party who observes and attests to facts without advocacy or interpretation.

**Observation**: Direct perception of facts by the witness.

**Independence**: The absence of relationships that would bias the witness's attestation.

**Known Value**: A registered predicate identifier in the Gordian Envelope system. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Predicates from BCR-2026-005

This BCR uses transparency predicates from [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md) for disclosure:

| Codepoint | Predicate | Usage in Fair Witness Context |
|-----------|-----------|-------------------------------|
| 1003 | `disclosedBias` | Potential biases affecting the observer's perspective or relationship to the subject |
| 1004 | `disclosedLimitations` | Limitations on the observer's knowledge, visibility, or ability to verify |
| 1005 | `assertionLimitations` | Scope or constraints of the observation itself |

These general predicates provide consistency across all assertion types (endorsements, reviews, observations) while allowing Fair Witness attestations to express transparency about bias and limitations.

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### Fair Witness Predicates (1120-1124)

---

#### 1120: `observerWitness`

**Type**: property
**Definition**: The entity who observed and attests to facts.
**Domain**: Observation or attestation
**Range**: XID, DID, or identifier of the observer
**Usage**: Identifies who is providing the observation attestation.

```
    Digest(contract-signing-observation) [
        'observerWitness': XID(notary)
        'observationTimestamp': 2026-02-02T14:30:00Z
        'observerIndependence': "No relationship with either party"
    ]
```

**Notes**:
- The observer attests to what they directly perceived
- Multiple observers may attest to the same facts (separate assertions)
- Observer identity should be verifiable

---

#### 1121: `observationTimestamp`

**Type**: property
**Definition**: When the observation occurred.
**Domain**: Observation
**Range**: xsd:dateTime (ISO 8601)
**Usage**: Records when the witness made the observation.

**Notes**:
- This is when the observation happened, not when the attestation was created
- For attestation creation time, use `date` (16) or `validFrom` (21)
- **Essential for the additive pattern**: Multiple observations by the same witness are distinguished by timestamp
- Observations are never revoked — the timestamp preserves each observation's validity for its moment in time

---

#### 1122: `observerPhysicalPresence`

**Type**: property
**Definition**: Whether the observer was physically present during the observation.
**Domain**: Observation
**Range**: Boolean, or text description of presence type
**Usage**: Distinguishes direct physical observation from remote or indirect observation.

```
    Digest(asset-verification) [
        'observerWitness': XID(inspector)
        'observerPhysicalPresence': true
        'observationTimestamp': 2026-02-02T10:00:00Z
    ]
```

**Notes**:
- Physical presence often carries more weight in legal contexts
- For remote observations, describe the observation method
- Values: `true` (in-person), `false` (remote), or descriptive text

---

#### 1123: `observerIndependence`

**Type**: property
**Definition**: Declaration of the observer's independence from parties involved.
**Domain**: Observation
**Range**: Text or structured independence claim
**Usage**: Establishes that the observer has no stake in the outcome.

```
    Digest(dispute-observation) [
        'observerWitness': XID(mediator)
        'observerIndependence': "Court-appointed mediator with no prior relationship to either party"
    ]
```

**Notes**:
- Should disclose any relationships that might affect neutrality
- Absence of this predicate does not imply lack of independence
- For professional witnesses, may reference credentials or appointment

---

#### 1124: `observerStatement`

**Type**: property
**Definition**: A statement of what the observer directly perceived.
**Domain**: Observation
**Range**: Text
**Usage**: The core observation content — what the witness actually observed.

```
    Digest(site-inspection) [
        'observerWitness': XID(inspector)
        'observationTimestamp': 2026-02-02T10:00:00Z
        'observerStatement': "Building foundation complete; concrete cured; no visible cracks or defects on south and east faces"
    ]
```

**Notes**:
- Should describe only what was directly observed, not interpretations or conclusions
- Follows the Fair Witness principle: "It appears white on this side" rather than "It is white"
- May reference specific evidence or measurements
- Corresponds to the "Core Observation" pillar

---

## Usage Patterns

### Contract Signing Ceremony

A Fair Witness attesting to a contract signing:

```
    Digest(contract-signature-attestation) [
        'attestsTo': Digest(signed-contract)
        'observerWitness': XID(licensed-notary)
        'observationTimestamp': 2026-02-02T15:00:00Z
        'observerPhysicalPresence': true
        'observerIndependence': "Neutral third party; no business relationship with signers"
    ]
```

### Remote Attestation

Observation via video call:

```
    Digest(remote-verification) [
        'observerWitness': XID(remote-inspector)
        'observationTimestamp': 2026-02-02T11:00:00Z
        'observerPhysicalPresence': "Remote via video call; visual and audio confirmation"
        'disclosedBias': "Engaged by requesting party; payment contingent on completion, not outcome"
    ]
```

### Multiple Witnesses

Multiple independent observers for high-stakes attestation:

```
// Witness 1
    Digest(observation-1) [
        'attestsTo': Digest(event)
        'observerWitness': XID(witness-a)
        'observerIndependence': "Independent party"
    ]

// Witness 2
    Digest(observation-2) [
        'attestsTo': Digest(event)
        'observerWitness': XID(witness-b)
        'observerIndependence': "Independent party"
    ]
```

### Additive Observations Over Time

The same witness observing the same subject at different times — building progressive trust:

```
// Initial observation (2024)
    Digest(observation-2024) [
        'attestsTo': Digest(project-status)
        'observerWitness': XID(auditor)
        'observationTimestamp': 2024-06-15T10:00:00Z
        'observerPhysicalPresence': true
        'observerStatement': "Project infrastructure operational; 3 of 5 milestones complete"
    ]

// Follow-up observation (2025)
    Digest(observation-2025) [
        'attestsTo': Digest(project-status)
        'observerWitness': XID(auditor)
        'observationTimestamp': 2025-01-20T14:00:00Z
        'observerPhysicalPresence': true
        'observerStatement': "All 5 milestones complete; system in production use"
    ]

// Later observation (2026)
    Digest(observation-2026) [
        'attestsTo': Digest(project-status)
        'observerWitness': XID(auditor)
        'observationTimestamp': 2026-02-02T09:00:00Z
        'observerPhysicalPresence': "Remote via monitoring dashboard"
        'observerStatement': "System stable; 99.9% uptime over past 12 months"
    ]
```

All three observations remain valid — they represent what the witness observed at each point in time. Trust accumulates through the series.

### Fair Witness with Principal Authority

Combining observation with delegation context:

```
    Digest(witnessed-delegation) [
        'principalAuthority': XID(company-ceo)
        'assertsDelegationFrom': XID(company-ceo)
        'delegationScope': "Authority to sign vendor contracts"
    ]

    Digest(delegation-witness) [
        'attestsTo': Digest(witnessed-delegation)
        'observerWitness': XID(corporate-secretary)
        'observationTimestamp': 2026-02-02T09:00:00Z
        'observerPhysicalPresence': true
        'observerIndependence': "Corporate officer; role requires neutrality in delegation matters"
    ]
```

## Timestamp Considerations

### Observation Timestamps Are Self-Reported

The `observationTimestamp` predicate records when the observer claims the observation occurred. This is **self-reported**, not cryptographically proven. Relying parties should consider:

- The observer's credibility and independence
- Whether the timestamp is plausible given other evidence
- The gap between observation time and attestation creation

### Provenance Marks for Ordering

Observers may use [Provenance Marks (BCR-2025-001)](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2025-001-provenance-mark.md) to establish **ordering** of their observations. Provenance Marks provide:

- Self-sovereign, permissionless ordering proofs
- Forward-commit chains linking observations in sequence
- Evidence that observation B came after observation A

However, Provenance Marks establish **relative ordering**, not **absolute timestamps**. They prove "this came after that" but not "this happened at exactly 2:30 PM."

### Future Work: Provable Timestamps

For scenarios requiring cryptographically provable timestamps, future work may integrate:

- **OpenTimestamps** — Bitcoin-anchored timestamp proofs
- **Trusted timestamping services** — RFC 3161 Time-Stamp Protocol
- **Other distributed timestamp systems**

Such integration would allow observations to carry proof of when they were created, not just claims. This is particularly valuable for:

- Legal proceedings requiring tamper-evident timestamps
- Audit trails with regulatory timestamp requirements
- High-stakes attestations where timing disputes may arise

This BCR does not define predicates for provable timestamps. That work is deferred to a future specification.

## Distinction from Anchor Predicates

BCR-2026-004 defines anchor predicates for cryptographic event log attestation. The distinction:

| Aspect | Fair Witness (this BCR) | Anchor (BCR-2026-004) |
|--------|-------------------------|----------------------|
| **Nature** | Human observation | Cryptographic proof |
| **What it proves** | "I observed this" | "This exists in the log" |
| **Trust basis** | Observer's credibility | Log's integrity |
| **Independence** | Declared via `observerIndependence` | Structural (independent log operator) |
| **Bias disclosure** | Via `disclosedBias` (BCR-2026-005) | Not applicable |
| **Physical presence** | Often relevant | Not applicable |

**When to use which:**

- **Anchor predicates**: When you need cryptographic proof of existence and ordering
- **Fair Witness predicates**: When human observation and attestation are valuable (legal, ceremonial, verification)
- **Both**: When you want both human attestation AND cryptographic proof

## Security Considerations

### Observer Identity Verification

Relying parties should verify:
- The observer's identity (XID validation)
- Relevant credentials (notary license, professional certification)
- Independence claims (no undisclosed conflicts)

### Observation vs. Interpretation

Fair Witnesses attest to **what they observed**, not conclusions. Relying parties should:
- Distinguish factual observations from inferences
- Seek multiple witnesses for critical attestations
- Consider observation conditions (presence, timing, method)

### Disclosed Bias Interpretation

The `disclosedBias` predicate (BCR-2026-005) is voluntary self-disclosure. Absence of disclosure:
- Does not prove absence of bias
- Should not be interpreted as stronger than disclosed observations
- May warrant additional verification for high-stakes decisions

### Temporal Considerations

The `observationTimestamp` records when observation occurred. Consider:
- Time between observation and attestation creation
- Whether conditions could have changed
- Jurisdiction-specific requirements for timeliness

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2026-004: Anchor Predicates](bcr-2026-004-anchor-predicates.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [BCR-2026-007: Principal Authority Predicates](bcr-2026-007-principal-authority.md)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)
- [XID-Quickstart: Fair Witness Concept](https://github.com/BlockchainCommons/XID-Quickstart/blob/main/concepts/fair-witness.md) — Fair Witness pattern in Gordian context
- Heinlein, Robert A. *Stranger in a Strange Land* (1961) — Origin of Fair Witness concept

## Distinction from Peer Endorsements

BCR-2026-011 defines peer endorsement predicates. Fair Witness and Peer Endorsement serve different trust-building purposes:

| Aspect | Fair Witness (this BCR) | Peer Endorsement (BCR-2026-011) |
|--------|-------------------------|--------------------------------|
| **Purpose** | Neutral observation of facts | Personal vouching for another |
| **Relationship** | Independence required | Relationship expected |
| **Statement type** | "I observed X happened" | "I endorse X's skills/character" |
| **Lifecycle** | Temporal/additive (never revoked) | Can be withdrawn or updated |
| **Trust model** | Observer credibility | Endorser reputation stake |
| **Acceptance model** | Not applicable | Subject accepts/rejects endorsement |

**When to use which:**

- **Fair Witness**: When you need neutral attestation of facts without advocacy
- **Peer Endorsement**: When someone vouches for another person's skills, character, or work
- **Both**: A Fair Witness could observe a peer endorsement ceremony, attesting to the signing without endorsing the subject

## Related BCRs

- **BCR-2026-004: Anchor Predicates** — Cryptographic log attestation (complementary)
- **BCR-2026-005: General Assertion Predicates** — Transparency predicates (`disclosedBias`, `disclosedLimitations`, `assertionLimitations`) used by this BCR
- **BCR-2026-007: Principal Authority Predicates** — Authority relationships
- **BCR-2026-011: Peer Endorsement Predicates** — Personal endorsements (distinct from neutral observation)

---

*BCR-2026-010: Fair Witness Predicates*
*Draft - February 2, 2026*
