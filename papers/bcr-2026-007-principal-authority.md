# Principal Authority Predicates

## BCR-2026-007

**© 2026 Blockchain Commons**

Authors: Christopher Allen<br/>
Date: February 2, 2026

---

## Abstract

This document specifies Known Value predicates for expressing principal-agent authority relationships in Gordian Envelopes. These predicates enable clear attribution when authorship and responsibility are distinct — such as AI-generated content under human direction, ghostwritten works, or any delegation of creative authority.

This BCR depends on [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md) for lifecycle management (`supersedes`, `revocationReason`, `processDisclosure`).

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

### Problem Statement

Existing metadata schemas (Schema.org, Dublin Core, FOAF) conflate two concepts that are increasingly distinct:

1. **Authorship** — who performed the act of creating (writing words, generating code, making artifacts)
2. **Responsibility** — who directed the creation, whose judgment shaped it, who stands behind it

This conflation was always imperfect — ghost writers, collaborators, and editors have existed for centuries — but it becomes untenable when AI agents perform authorship under human direction. Current predicates force a false choice: either the human claims authorship they didn't perform, or the AI is attributed authorship without having any authority over what was created.

### Why This Matters

The interest in terms like "principal" isn't just about credit or convenience — it's about preserving agency as AI tools become more capable.

When we delegate to AI agents, there's a subtle risk that our "augmented" selves stop being fully ours. Systems can erode autonomy not just through coercion, but through convenience, defaults, and invisible delegation. The agent rewrites your draft and it's better — but is it still you? The agent makes a thousand small decisions and ships the project — but whose judgment shaped it?

Without vocabulary to express these relationships, attribution becomes a polite fiction. With it, attribution becomes a meaningful statement about where agency actually lives.

### Solution

This specification defines four predicates for principal-agent authority relationships:

1. **`principalAuthority`** — Identifies who directs and takes responsibility
2. **`assertsConferralFrom`** — Agent asserts authority was conferred by a principal
3. **`conferralScope`** — What the conferral covers
4. **`conferralConstraints`** — What limits apply to the conferral
5. **`conferredBy`** — Who granted authority (single-hop)
6. **`conferralChain`** — Full chain of authority conferral (multi-hop)
7. **`confersTo`** — Principal declares conferral to an agent

These predicates draw on the legal concept of Principal Authority from the Laws of Agency, where a principal confers authority to an agent who acts on their behalf while owing duties back to the principal. The term "conferral" is used instead of "delegation" to avoid confusion with cryptographic delegation (XID `delegate` predicate).

### Scope Boundary

This BCR defines **authority relationship predicates**, not:
- Contribution roles (Author, Editor, etc.) — see [BCR-2026-008: CreativeWork Role Predicates](bcr-2026-008-creativework-roles.md)
- Signature context (`signingAs`, `onBehalfOf`) — see [BCR-2026-006: Signature Context Predicates](bcr-2026-006-signature-context.md)
- Assertion lifecycle (`supersedes`, `revocationReason`) — see [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)

## Terminology

**Principal**: An entity with ultimate authority over a work or action, who takes responsibility for it and to whom agents owe duties.

**Agent**: An entity that acts on behalf of a principal, within conferred authority boundaries.

**Conferral**: The grant of authority from principal to agent to act within specified scope and constraints. This term is used instead of "delegation" to distinguish from cryptographic delegation (XID `delegate` predicate) which grants cryptographic signing privileges.

**Authorship**: The act of creating content — writing, coding, generating.

**Responsibility**: The authority over and accountability for content — directing, reviewing, standing behind.

**Known Value**: A registered predicate identifier in the Gordian Envelope system, encoded as a numeric codepoint for efficient representation. See [BCR-2023-002](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md).

## Referenced Specifications

### BCR-2026-005: General Assertion Predicates

This BCR uses predicates from BCR-2026-005 for assertion lifecycle:

| Codepoint | Predicate | Usage in This Context |
|-----------|-----------|----------------------|
| 1000 | `supersedes` | Updating or replacing authority assertions |
| 1001 | `revocationReason` | Documenting why authority conferral was revoked |
| 1002 | `processDisclosure` | Describing how work was produced |

### Core Registry

| Codepoint | Predicate | Usage in This Context |
|-----------|-----------|----------------------|
| 21 | `validFrom` | When authority conferral becomes effective |
| 22 | `validUntil` | When authority conferral expires |

### Distinction from XID Predicates

The core registry includes predicates for cryptographic key operations:

| Codepoint | Predicate | Purpose |
|-----------|-----------|---------|
| 63 | `delegate` | Grants cryptographic signing privileges to another key |
| 86 | `Revoke` | Revokes cryptographic key permissions |

These XID predicates manage **cryptographic signing privileges** — who can sign on behalf of which keys. The predicates in this BCR manage **authority relationships** — who directed what work and under what terms.

The two concerns are orthogonal:
- A key may have `delegate` (63) privileges without any `assertsConferralFrom` authority
- An `assertsConferralFrom` assertion may exist without granting cryptographic `delegate` privileges
- Both may be used together when authority conferral includes signing rights

## Proposed Known Value Assignments

All proposed codepoints are in the **Community Assigned (specification required)** range (1000-1999).

### Principal Authority (1040-1046)

---

#### 1040: `principalAuthority`

**Type**: property
**Definition**: The entity who directed the work and takes responsibility for it.
**Domain**: Creative work, assertion, or action
**Range**: XID, DID, or identifier of the principal
**Usage**: Identifies who holds ultimate authority, regardless of who performed the work.

```
    Digest(ai-generated-document) [
        'principalAuthority': XID(alice)
        'processDisclosure': "Generated by Claude under Alice's direction and review."
    ]
```

**Notes**:
- The principal need not have performed any authorship
- Multiple principals are possible for collaborative direction (use multiple assertions or array)
- This predicate answers "whose work is this?" in terms of authority, not performance

---

#### 1041: `assertsConferralFrom`

**Type**: property
**Definition**: The agent asserts that it acts under authority conferred by the specified principal.
**Domain**: Agent declaration or work attribution
**Range**: XID, DID, or identifier of the conferring principal
**Usage**: Expresses the agent's claim of conferred authority.

```
    Digest(agent-work-claim) [
        'assertsConferralFrom': XID(alice)
        'conferralScope': "Draft technical documentation"
        'conferralConstraints': "Subject to human review before publication"
    ]
```

**Notes**:
- This is an **assertion by the agent**, not a statement of fact
- The principal may separately confirm or deny the conferral
- The assertion-first framing (`assertsConferralFrom` rather than `agentOf`) makes the claim nature explicit
- Relying parties must evaluate whether to trust the conferral claim
- "Conferral" is used instead of "delegation" to distinguish from cryptographic delegation (XID `delegate` predicate)

---

#### 1042: `conferralScope`

**Type**: property
**Definition**: The boundaries of what the authority conferral covers.
**Domain**: Conferral context
**Range**: Text description or structured scope definition
**Usage**: Documents what the agent is authorized to do.

```
    Digest(authority-conferral) [
        'assertsConferralFrom': XID(corporate-principal)
        'conferralScope': "Sign routine vendor contracts under $10,000"
    ]
```

**Notes**:
- Scope defines the positive space — what is included
- Use `conferralConstraints` for limitations and exclusions
- Scope can be narrow ("this specific document") or broad ("all technical writing")

---

#### 1043: `conferralConstraints`

**Type**: property
**Definition**: Limitations or conditions on the conferred authority.
**Domain**: Conferral context
**Range**: Text description or structured constraints
**Usage**: Documents what the agent is NOT authorized to do or conditions that apply.

```
    Digest(authority-conferral) [
        'assertsConferralFrom': XID(alice)
        'conferralScope': "Manage social media presence"
        'conferralConstraints': "No political statements. No financial commitments. Human approval required for crisis response."
    ]
```

**Notes**:
- Constraints define the negative space — what is excluded or conditional
- Constraints may include approval requirements, prohibited actions, or review processes
- The prefix `conferral-` provides symmetry with `conferralScope`

---

#### 1044: `conferredBy`

**Type**: property
**Definition**: The entity that granted the signer's or agent's authority.
**Domain**: Signature context or authority assertion
**Range**: XID, DID, or identifier of the conferring party
**Usage**: Documents the immediate source of authority.

```
{
    Digest(approval-document) [
        'signed': {
            XID(department-head) [
                'signingAs': "Authorized Approver"
                'conferredBy': XID(cfo)
            ]
        }
    ]
}
```

**Notes**:
- For single-hop authority conferral, `conferredBy` is sufficient
- For multi-hop conferral, use `conferralChain`
- The conferral may be standing (ongoing) or contextual (one-time)
- Works with both signature contexts and work authority assertions

---

#### 1045: `conferralChain`

**Type**: property
**Definition**: The full chain of authority conferral from original authority to current actor.
**Domain**: Signature context or authority assertion
**Range**: Ordered list of XIDs/DIDs representing the conferral path
**Usage**: Documents multi-hop authority conferral for complex authority structures.

```
{
    Digest(field-authorization) [
        'signed': {
            XID(field-manager) [
                'signingAs': "Emergency Coordinator"
                'onBehalfOf': XID(corporation)
                'conferralChain': [XID(board), XID(ceo), XID(coo), XID(regional-vp)]
            ]
        }
    ]
}
```

**Notes**:
- Chain is ordered from original authority to immediate conferrer
- The actor (signer or agent) is implicitly at the end of the chain
- Use for audit trails and authority verification
- Simpler cases can use `conferredBy` alone

---

#### 1046: `confersTo`

**Type**: property
**Definition**: The principal declares that authority is conferred to the specified agent.
**Domain**: Authority declaration by principal
**Range**: XID, DID, or identifier of the agent receiving authority
**Usage**: Principal signs a conferral TO an agent, establishing the authority relationship.

```
{
    Digest(authority-grant) [
        'confersTo': XID(agent-alice)
        'conferralScope': "Draft technical documentation"
        'conferralConstraints': "Subject to review before publication"
        'validFrom': 2026-02-01
        'signed': {
            XID(principal-bob) [
                'signingAs': "Project Lead"
            ]
        }
    ]
}
```

**Notes**:
- This is a **declaration by the principal**, signed by them
- Complements `assertsConferralFrom` which is the agent's claim
- Together they provide bidirectional verification:
  - Agent claims: `assertsConferralFrom`: XID(principal)
  - Principal confirms: `confersTo`: XID(agent)
- For standing conferrals, use `validFrom`/`validUntil` for time bounds
- The signed conferral can be referenced by the agent as proof of authority

---

## Usage Patterns

### Basic Principal-Agent Attribution

The simplest case: identifying who directed a work.

```
    Digest(blog-post) [
        'principalAuthority': XID(human-author)
        'processDisclosure': "Written with AI assistance for research and drafting."
    ]
```

### Agent Claiming Authority Conferral

An agent (human or AI) asserting its authority source.

```
    Digest(code-commit) [
        'assertsConferralFrom': XID(project-lead)
        'conferralScope': "Implement feature X per specification"
        'conferralConstraints': "No changes to public API without review"
    ]
```

### Authority Conferral with Lifecycle

Using BCR-2026-005 predicates for conferral management.

```
    Digest(conferral-v2) [
        'assertsConferralFrom': XID(alice)
        'conferralScope': "Extended to include customer communications"
        'supersedes': Digest(conferral-v1)
        'validFrom': 2026-03-01
    ]
```

### Revoked Authority Conferral

```
    Digest(revocation) [
        'supersedes': Digest(original-conferral)
        'revocationReason': "Project concluded"
    ]
```

## Design Notes

### Standing vs. Contextual Authority Conferral

This BCR does not distinguish between:
- **Standing conferral** — ongoing authority ("you may always sign contracts under $10K")
- **Contextual conferral** — task-specific authority ("draft this specific document")

Both use the same predicates. The distinction, when needed, is expressed through:
- `conferralScope` (narrow vs. broad)
- `validFrom`/`validUntil` (time-bounded vs. open-ended)
- Context of the work itself

This intentional collapse keeps the predicate set minimal. Domain profiles may add distinctions if needed.

### The `producedBy` Question

Earlier drafts considered a `producedBy` predicate to mark causal participation (who/what actually created the content). This BCR intentionally omits it because:

1. **Role predicates handle "who did what"** — BCR-2026-006 defines Author, Editor, etc.
2. **Process disclosure handles "how"** — `processDisclosure` captures production method
3. **Principal authority handles "whose"** — `principalAuthority` captures responsibility

A separate `producedBy` would duplicate these concerns. If a use case emerges that these three don't cover, it can be added in a future BCR.

### Domain Profiles

Domain-specific applications (legal, medical, financial) may define profiles that:
- **Constrain** which predicates are required or optional
- **Specialize** range values (e.g., specific role vocabularies)
- **Add** domain-specific predicates that reference these

Profiles should **not redefine** the core predicate semantics. A `principalAuthority` means the same thing in healthcare as in publishing — profiles add context, not new meanings.

### Meaningful Principal Authority

For `principalAuthority` to represent genuine direction rather than nominal attribution, three conditions should hold:

1. **Legibility** — The principal can see what the agent is doing and why. Black-box systems that can't explain their reasoning undermine this.

2. **Boundaries** — The agent operates within constraints the principal defined. Autonomous systems that decide their own scope undermine this.

3. **Override** — The principal can intervene, revoke, or redirect at any point. Systems that resist correction undermine this.

Without these conditions, "I directed this" becomes a polite fiction. With them, `principalAuthority` is a meaningful statement about where agency actually lives.

These conditions are guidance for system designers and relying parties, not predicates to be asserted. A `principalAuthority` claim does not prove these conditions hold — it asserts who bears responsibility regardless.

### Why "Conferral" Instead of "Delegation"

This BCR uses "conferral" terminology (`assertsConferralFrom`, `conferralScope`, `conferralConstraints`) rather than "delegation" to avoid collision with cryptographic delegation:

**Cryptographic delegation** (object capabilities):
- Core registry predicate `delegate` (63) grants signing privileges to another key
- This is a verifiable, enforceable capability transfer
- The delegation IS the grant — possession of the delegated key proves authority

**Authority conferral** (this BCR):
- Expresses claims about principal-agent relationships from agency law
- These are assertions about social/legal relationships, not cryptographic capabilities
- The conferral claim must be evaluated for trustworthiness, not just verified

The term "conferral" was chosen because:
1. It's the formal legal term for granting authority ("confer authority")
2. It has minimal collision with existing technical vocabulary (OAuth, access control, cryptographic delegation)
3. It clearly signals a social/legal relationship rather than a cryptographic operation

BCR-2026-006 (Signature Context) uses matching terminology (`conferredBy`, `conferralChain`) for consistency.

## Security Considerations

### Authority Conferral Claims Are Assertions

The `assertsConferralFrom` predicate expresses a **claim by the agent**. Relying parties must:
- Verify the agent's identity
- Evaluate whether to trust the conferral claim
- Optionally seek confirmation from the claimed principal

The predicate structure does not enforce or verify the conferral — it only expresses the claim.

### Authority vs. Key Privileges

Having `principalAuthority` over a work does not grant cryptographic signing privileges. Having cryptographic `delegate` (63) privileges does not grant authority. Systems must track both concerns when both apply.

### Scope and Constraint Interpretation

The `conferralScope` and `conferralConstraints` predicates contain human-readable text (or structured data). Automated systems should:
- Treat scope/constraints as advisory unless they can parse structured formats
- Default to restrictive interpretation when scope is ambiguous
- Require human review for high-stakes decisions

## Open Questions

### Responsibility vs. Authority

This BCR defines `principalAuthority` as the entity who "directs the work AND takes responsibility." Community discussion is invited on whether these should be separate concerns:

- **External accountability** (to society) — Who receives feedback, complaints, or legal action
- **Internal authority** (to team/agents) — Who directs the creative process

A publisher might be externally accountable for a work they didn't direct. A director might shape work without being the public face of responsibility. Should these be expressible separately, or does conflating them serve most use cases adequately?

### Oversight as Distinct from Authority

Is there a need for an `oversightAuthority` predicate — the entity responsible for ongoing monitoring/approval of the work or process?

Oversight suggests a monitoring relationship distinct from:
- **Direction** — deciding what to create
- **Execution** — doing the work
- **Review** — one-time quality check (already covered by `Reviewer` role in BCR-2026-008)

Examples where oversight and authority might be held by different parties:
- A board provides oversight of a CEO's work (CEO has authority, board monitors)
- An editor provides ongoing oversight of drafts (author has authority, editor monitors quality)
- A code reviewer must approve before merge (author has authority, reviewer gates release)

The "Meaningful Principal Authority" design note describes Legibility, Boundaries, and Override as conditions for genuine direction — but these are also aspects of oversight. Should oversight be expressible as a separate relationship when it's held by a different party than the principal?

## References

- [BCR-2023-002: Known Value Registry](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2023-002-known-value.md)
- [BCR-2026-005: General Assertion Predicates](bcr-2026-005-general-assertions.md)
- [BCR-2026-006: Signature Context Predicates](bcr-2026-006-signature-context.md)
- [Gordian Envelope Specification](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2024-001-envelope.md)

## Related BCRs

- **BCR-2026-005: General Assertion Predicates** — Lifecycle predicates used by this BCR
- **BCR-2026-006: Signature Context Predicates** — Signing capacity (`signingAs`, `onBehalfOf`); references this BCR for authority chains
- **BCR-2026-008: CreativeWork Role Predicates** — Contribution roles (Author, Editor, etc.)

---

*BCR-2026-007: Principal Authority Predicates*
*Draft - February 2, 2026*
