# Control Library Framework: Enterprise AI Agent Security

This document defines the v1 control library for the framework. It establishes scope, structure, the per-control template, the implementation domain taxonomy, and the relationship between controls and existing security standards. It is the foundational artifact for `data/controls.json` and feeds the controls section of the practitioner guide and the web tool's control browser.

## Purpose

To provide CISOs and security program leads with a small, scannable library of agent-specific security controls that:

| Goal | How the library achieves it |
|---|---|
| Maps cleanly to the threat model | Every control addresses one or more threats from the threat catalog |
| Maps cleanly to existing security programs | Each control references the closest equivalents in NIST SP 800-53, ISO 27001 Annex A, and BSI grundschutz |
| Stays small enough to read in one sitting | v1 targets 10 to 20 broad controls rather than a comprehensive checklist |
| Provides implementation guidance without prescribing products | Patterns and considerations are vendor-neutral; vendor-specific mappings are external contributions |

## Audience and Reading Mode

| Aspect | Choice |
|---|---|
| Primary audience | CISOs and security program leads |
| Secondary audience | Enterprise security architects, regulatory and compliance leads |
| Reading mode | Reference, accessed during program design or threat-driven control selection |
| Expected use | Look up which controls address a specific threat, or select controls during security program design |

## Scope and Granularity

This is v1 of the control library. It uses a deliberately coarse-grained approach: 10 to 20 broad controls covering the full threat catalog. v2 may subdivide controls into more specific entries as customer engagements surface where the broad controls are insufficient.

| Decision | Choice for v1 |
|---|---|
| Granularity | Coarse-grained (10 to 20 controls total) |
| Consolidation rule | Distinct implementation patterns that share the same goal are grouped under a single control |
| Subdivision rule (v2 only) | A broad control may be subdivided in v2 if customer engagements show its variants need separate guidance |
| Out of scope (v1) | Detailed implementation playbooks, vendor-specific patterns, deep operational runbooks |

The risk of going too broad is that controls become abstract platitudes ("apply least privilege") that don't help practitioners. The risk of going too narrow is that the library becomes a checklist nobody reads. v1 deliberately accepts the first risk in exchange for the second, and trusts the threat-control mapping to keep controls grounded in concrete attack patterns.

## Categorization: Implementation Domain Primary, Function Secondary

Controls are organized by **implementation domain**, the part of the security program that typically owns implementation. Each control also has a **function** attribute mapping to the classical preventive / detective / corrective / deterrent taxonomy.

### Implementation domains

| Domain | Description | Example controls |
|---|---|---|
| Identity | Authentication, authorization, identity propagation, delegation | User-context propagation, on-behalf-of authorization |
| Runtime | Agent execution environment, tool invocation, sandboxing, isolation | Tool-output provenance, sandboxed tool execution |
| Data | Information flow, data access, output filtering, data minimization | Authorization-aware output filtering |
| Governance | Policy, oversight, human-in-the-loop, configuration management | Action verification at high-impact boundaries |
| Audit and accountability | Logging, traceability, attribution, monitoring | End-to-end audit traceability |

### Functions

| Function | Description |
|---|---|
| Preventive | Stops the threat from occurring |
| Detective | Identifies that the threat is occurring or has occurred |
| Corrective | Reduces or contains harm after the threat has occurred |
| Deterrent | Discourages the threat by raising cost or visibility |

Most agent-specific controls are preventive. Detective controls are particularly valuable in this domain because traditional detection is poorly suited to agent threats. Corrective controls (rollback, isolation) are important for the residual risk that preventive controls cannot eliminate.

## Relationship to Existing Standards

Each control includes mappings to the closest equivalent in three reference frameworks:

| Framework | Why it matters |
|---|---|
| NIST SP 800-53 Rev. 5 | Most widely cited US federal control catalog; the basis for many enterprise programs and CMMC |
| ISO 27001 Annex A | International control standard; widely adopted in EU enterprises |
| BSI grundschutz | German federal IT security standard; directly relevant to DACH audience |

The framework's controls are **refinements or extensions** of existing principles applied to the agent context, not novel inventions. Where an agent-specific control has no clean equivalent in existing standards, this is noted explicitly and is itself a finding. Where an existing standard already addresses the agent-specific concern adequately, the framework defers to it rather than restating it.

This positioning protects the framework from the criticism that it reinvents existing security wheels. Every control is justified relative to the gap it fills.

## v1 Control Library: Consolidated List

The following is the v1 starting point. The list consolidates the 11 specific control IDs already referenced by AGT-001 and AGT-002 into broader controls, plus reserved IDs for the remaining 8 threats.

### Controls populated by AGT-001 and AGT-002 work

| ID | Title | Domain | Function | Consolidates from prior work |
|---|---|---|---|---|
| CTL-001 | Identity and authorization context propagation | Identity | Preventive | CTL-008, CTL-009, CTL-011, CTL-016, CTL-022 (the five user-context, on-behalf-of, tenant boundary, delegation context, and per-user scoping controls) |
| CTL-002 | Tool-output and context provenance | Runtime | Preventive, Detective | CTL-014, CTL-033 (tool-output isolation/tagging and provenance tracking) |
| CTL-003 | Action verification at high-impact boundaries | Governance | Preventive | CTL-021, CTL-027 (intent verification and out-of-band confirmation) |
| CTL-004 | Authorization-aware output filtering | Data | Preventive | CTL-031 |
| CTL-005 | End-to-end audit and accountability | Audit and accountability | Detective | CTL-029 |

These five controls cover the threats in AGT-001 and AGT-002 fully. AGT-001 and AGT-002 will be updated to reference these consolidated IDs.

### Reserved IDs for remaining threats

The following IDs are reserved for controls that will emerge from drafting AGT-003 through AGT-010. The list is approximate and subject to refinement; the v1 target is 10 to 15 total controls. Specific titles will be assigned when the relevant threats are populated.

| Reserved ID | Likely focus area | Likely domain |
|---|---|---|
| CTL-006 | Tool-chain authorization and composition limits | Runtime |
| CTL-007 | Output channel sanitization for downstream systems | Data |
| CTL-008 | Memory and persistence integrity | Runtime |
| CTL-009 | Goal and instruction integrity | Governance |
| CTL-010 | Inter-agent trust and delegation governance | Identity |
| CTL-011 | Resource and rate limits for agent loops | Runtime |
| CTL-012 to CTL-015 | Reserved for emergent controls during drafting | TBD |

The framework reserves the right to consolidate further or split as the remaining threats are drafted. The final v1 library will likely settle between 10 and 15 controls.

## Per-Control Template

Each control in `data/controls.json` and the controls section of the document follows this template:

| Field | Type | Description |
|---|---|---|
| `id` | string | Internal identifier, format `CTL-NNN` |
| `title` | string | Action-oriented control name |
| `domain` | enum | One of: identity, runtime, data, governance, audit_accountability |
| `function` | array of enums | One or more of: preventive, detective, corrective, deterrent |
| `description` | string | Plain-language explanation in 2 to 4 sentences |
| `implementation_pattern` | string | Concrete pattern for how the control is built; vendor-neutral; 1 to 2 paragraphs |
| `operational_considerations` | array of objects | For each: `consideration`, `description`; covers performance, complexity, integration, cost trade-offs |
| `common_failure_modes` | array of objects | For each: `failure_mode`, `description`; the ways this control breaks in practice |
| `threats_addressed` | array of strings | AGT-NNN IDs from the threat catalog |
| `regulatory_basis` | array of objects | For each: `regulation`, `article_or_section`, `relevance` |
| `existing_standard_mappings` | array of objects | For each: `standard` (NIST 800-53, ISO 27001, BSI), `control_id`, `relationship` (equivalent, refinement, extension, novel) |
| `maturity` | enum | One of: experimental, emerging, established, mature |
| `related_controls` | array of strings | Other CTL-NNN IDs that complement, depend on, or conflict with this control |
| `references` | array of objects | Citations: standards, papers, public guidance |
| `vendor_mappings` | not in this file | Vendor-specific implementations live in `data/vendor-mappings/` and reference this control by ID externally |

### Template field rules

| Rule | Reason |
|---|---|
| `description` must be readable by a non-technical CISO | Audience requirement |
| `implementation_pattern` must be vendor-neutral | Framework positioning; vendor specifics live in vendor-mappings |
| `common_failure_modes` is required and non-trivial | This is the differentiated insight of the framework |
| `existing_standard_mappings.relationship` must be one of four values | Forces clarity about whether this is novel or derivative |
| `vendor_mappings` is deliberately not part of this template | Vendor mappings are external contributions, not part of the controls library itself |
| Severity, priority, and cost scoring are deliberately omitted | Subjective; varies by context; encourages false precision |

## Worked Example

To make the template concrete, here is one fully populated control. This is the reference example for how every entry in `data/controls.json` should look.

---

### CTL-001: Identity and Authorization Context Propagation

**Domain**: Identity
**Function**: Preventive
**Maturity**: Emerging

**Description**: An AI agent's effective authorization for any action must be derived from both its own service authorization and the authorization of the user it is currently serving. The agent does not act with its full service-level privileges; it acts with the intersection of its privileges and the originating user's. Identity and authorization claims about the user are propagated through every downstream call the agent makes, and downstream systems verify against the user's identity rather than the agent's alone.

**Implementation pattern**: At the agent runtime layer, every user request is associated with an authorization context that includes the user's verified identity, applicable claims (roles, group memberships, tenant), and any constraints derived from the session (time-bound, scope-bound). When the agent invokes a tool or downstream service, the request includes this context as structured data, typically as an OAuth 2.0 Token Exchange (RFC 8693) on-behalf-of token, a SPIFFE workload identity bound to the user session, or a custom signed claims envelope.

Downstream services authorize the action against the user identity, not the agent identity, using their existing authorization infrastructure. The agent identity is used only for the agent-to-service authentication leg; the action authorization is a separate decision based on the propagated user context. Where a downstream service does not natively support user-context-aware authorization, the agent must restrict its actions on that service to the narrowest scope acceptable to all users it serves, or refuse to integrate with that service for sensitive operations.

For multi-tenant deployments, tenant identity is part of the propagated context and must be enforced at every layer. For multi-step delegation chains, the user context is forwarded explicitly at each step; the chain breaks if any step strips or replaces it.

**Operational considerations**:

| Consideration | Description |
|---|---|
| Latency | Token issuance and verification at each downstream call adds latency, typically 10 to 50 ms per hop; cumulative across delegation chains |
| Caching complexity | Per-user authorization scoping reduces the value of shared caches; caches must be partitioned by user, or invalidated on authorization changes |
| Legacy integration | Many enterprise systems do not support user-context-aware authorization; the agent must either widen its trust to those systems or exclude them from sensitive operations |
| Token lifetime tuning | Short-lived tokens improve security but increase issuance load; long-lived tokens reduce load but expand the window of compromise; typical compromise: minutes-scale lifetime with refresh |
| Audit volume | Per-user authorization decisions increase audit log volume substantially; storage and SIEM ingestion costs grow accordingly |

**Common failure modes**:

| Failure mode | Description |
|---|---|
| Service account fallback | Under integration pressure, the agent is configured to call a particular service with its own identity rather than the user's; the agent retains broad privileges and the user-context model is bypassed for that integration |
| Token scope drift | Initial deployment uses correctly scoped tokens; over time, scopes expand to accommodate new use cases without re-evaluating the original constraints |
| Caching across users | A naive cache of tool outputs is queried by all users; one user's authorized retrieval becomes accessible to other users via the cache |
| Delegation chain context loss | An agent invokes a sub-agent or external service that does not preserve the user context; the chain continues with the agent's identity rather than the user's |
| Static configuration vs dynamic context | The agent's authorization model is configured once at deployment; runtime changes to user permissions are not reflected in the agent's effective authorization |

**Threats addressed**: AGT-002 (primary), AGT-001 (secondary, by limiting blast radius), AGT-005 (secondary, by enabling cleaner attribution)

**Regulatory basis**:

| Regulation | Article or section | Relevance |
|---|---|---|
| EU AI Act | Art. 14 | Human oversight; authorization scoping is a structural prerequisite for meaningful oversight |
| EU AI Act | Art. 15 | Cybersecurity; resilience to unauthorized use requires user-context enforcement |
| NIS2 | Art. 21 | Access control policies; agents are critical assets requiring proportionate authorization controls |
| DORA | Art. 9 | Identity management; financial entities must maintain robust identity and access controls |
| GDPR | Art. 5(1)(f) | Integrity and confidentiality; user-context propagation prevents cross-user data exposure |
| GDPR | Art. 25 | Data protection by design; user-scoped authorization is a design-level control |
| GDPR | Art. 32 | Security of processing; technical measures including access control |

**Existing standard mappings**:

| Standard | Control ID | Relationship |
|---|---|---|
| NIST SP 800-53 Rev. 5 | AC-3 (Access Enforcement) | Refinement: AC-3 establishes the principle; CTL-001 extends to agent-mediated authorization specifically |
| NIST SP 800-53 Rev. 5 | AC-6 (Least Privilege) | Refinement: least privilege applied to the agent-user composition |
| NIST SP 800-53 Rev. 5 | IA-9 (Service Identification and Authentication) | Refinement: IA-9 covers service-to-service authentication; CTL-001 extends to user-context propagation through services |
| ISO 27001 Annex A | A.5.15 (Access control) | Refinement: extends to agent-mediated access |
| ISO 27001 Annex A | A.8.2 (Privileged access rights) | Refinement: privileged access scoping for agents |
| BSI grundschutz | ORP.4 (Identitäts- und Berechtigungsmanagement) | Refinement: identity and authorization management extended to agent context |

**Related controls**:

| Control | Relationship |
|---|---|
| CTL-003 (Action verification at high-impact boundaries) | Complementary: where CTL-001 cannot fully scope authorization, CTL-003 provides a fallback |
| CTL-004 (Authorization-aware output filtering) | Complementary: CTL-001 controls what data is retrieved; CTL-004 controls what is delivered to the user |
| CTL-005 (End-to-end audit and accountability) | Dependent: audit traceability requires the user-context propagation that CTL-001 provides |

**References**:

- NIST SP 800-53 Rev. 5, Access Control family (AC-3, AC-6, IA-9)
- NIST SP 800-207, Zero Trust Architecture
- IETF RFC 8693, OAuth 2.0 Token Exchange
- IETF RFC 9068, JSON Web Token Profile for OAuth 2.0 Access Tokens
- BSI IT-Grundschutz-Kompendium, Baustein ORP.4 Identitäts- und Berechtigungsmanagement
- ISO/IEC 27001:2022, Annex A controls A.5.15 and A.8.2
- SPIFFE / SPIRE specifications for workload identity (foundational for agent identity scenarios)

---

## Mapping to the Threat Catalog

After v1 of the controls library is populated, the following table summarizes which controls address which threats. This table is computed from the bidirectional mappings in `data/mappings.json` and updated whenever a control or threat changes.

| Threat | Primary controls | Secondary controls |
|---|---|---|
| AGT-001 (Prompt injection via tool outputs) | CTL-002, CTL-003 | CTL-001, CTL-005 |
| AGT-002 (Authorization confusion / deputy problem) | CTL-001, CTL-004 | CTL-003, CTL-005 |
| AGT-003 (Tool-chain abuse) | TBD when AGT-003 is drafted | TBD |
| AGT-004 through AGT-010 | TBD | TBD |

## Instructions for Claude Code

When this framework file is loaded into Claude Code as context, the following are the concrete next steps. Execute in order, with diff review and explicit confirmation between commits.

### Step 1: Place the framework document

Save this document as `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md` in the local repository. If `docs/frameworks/` does not exist, create it.

### Step 2: Update `data/controls.json`

Create or update `data/controls.json` with the v1 control library schema as specified in the per-control template. Populate CTL-001 fully using the worked example in this document. Create stub entries for CTL-002, CTL-003, CTL-004, and CTL-005 with the title and domain set, but the remaining fields marked `"status": "stub"`. Do not invent content for the stubs.

Reserved IDs (CTL-006 through CTL-015) are not added to `controls.json` yet; they will be populated as their corresponding threats are drafted.

### Step 3: Update AGT-001 and AGT-002 to reference consolidated control IDs

The previously placed AGT-001 and AGT-002 entries reference the original 11 specific control IDs. These must be updated to reference the consolidated v1 controls.

**For AGT-001:**

| Old reference | New reference |
|---|---|
| CTL-014 (tool-output isolation and tagging) | CTL-002 |
| CTL-021 (intent verification for high-impact actions) | CTL-003 |
| CTL-027 (out-of-band confirmation for state-changing operations) | CTL-003 (consolidated with CTL-021) |
| CTL-033 (provenance tracking for context content) | CTL-002 (consolidated with CTL-014) |

Final AGT-001 `recommended_controls`: `["CTL-002", "CTL-003"]` with optional secondary entries for CTL-001 and CTL-005 if the markdown supports a primary/secondary distinction.

**For AGT-002:**

| Old reference | New reference |
|---|---|
| CTL-008 (user-context propagation) | CTL-001 |
| CTL-009 (on-behalf-of authorization model) | CTL-001 (consolidated) |
| CTL-011 (tenant boundary enforcement at the agent layer) | CTL-001 (consolidated) |
| CTL-016 (delegation-context preservation) | CTL-001 (consolidated) |
| CTL-022 (per-user agent instances or per-request authorization scoping) | CTL-001 (consolidated) |
| CTL-029 (end-to-end audit traceability) | CTL-005 |
| CTL-031 (authorization-based output filtering) | CTL-004 |

Final AGT-002 `recommended_controls`: `["CTL-001", "CTL-004", "CTL-005"]` with optional secondary entries for CTL-003.

### Step 4: Update the source markdown files

Both `docs/sections/05-threat-model/AGT-001.md` and `docs/sections/05-threat-model/AGT-002.md` contain "Recommended controls" tables that list the old specific control IDs. Update those tables to reference the consolidated CTL-001 through CTL-005 IDs with their new titles. The descriptions in those tables should briefly explain what each consolidated control does in the context of that specific threat.

### Step 5: Update `data/mappings.json`

Remove the placeholder entries for the original 11 control IDs (CTL-008, CTL-009, CTL-011, CTL-014, CTL-016, CTL-021, CTL-022, CTL-027, CTL-029, CTL-031, CTL-033). Replace them with the consolidated CTL-001 through CTL-005 entries. CTL-001 should not have `"status": "referenced_but_not_yet_defined"` because it is now fully defined; the others retain that status until drafted.

Update the `control_mitigates_threat` mappings to reflect the consolidated IDs. Verify all mappings are bidirectional and consistent.

### Step 6: Update the canonical document

If `docs/main-document/EU-AI-Security-Mapping.md` already includes section 6 (controls), update the controls section to introduce CTL-001 through CTL-005 as the v1 library. If section 6 is still a stub, add a brief introduction (one paragraph stating the section presents a coarse-grained v1 control library of 10 to 15 controls organized by implementation domain) and include CTL-001 as the first fully written entry. Reference, do not embed, the framework document for methodology.

If section 5 (threat model) references control IDs in its threat entries, update those references to match the consolidated IDs.

### Step 7: Update CHANGELOG.md

Add an entry under the current unreleased version:

```
- Added v1 control library framework (docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md)
- Populated CTL-001 (Identity and authorization context propagation) as the reference control entry
- Created stubs for CTL-002 (Tool-output and context provenance), CTL-003 (Action verification at high-impact boundaries), CTL-004 (Authorization-aware output filtering), CTL-005 (End-to-end audit and accountability)
- Consolidated 11 specific control IDs from AGT-001 and AGT-002 into the new v1 library
- Updated AGT-001 and AGT-002 entries to reference consolidated control IDs
- Updated mappings.json to reflect new control IDs
```

### Step 8: Commit the work locally

Make the following atomic commits in order:

| Commit | Message |
|---|---|
| 1 | `Add control library framework document to docs/frameworks/` |
| 2 | `Populate CTL-001 in data/controls.json with full reference entry` |
| 3 | `Add stubs for CTL-002 through CTL-005` |
| 4 | `Update AGT-001 and AGT-002 source markdown to reference consolidated control IDs` |
| 5 | `Update threats.json entries for AGT-001 and AGT-002` |
| 6 | `Update mappings.json with consolidated control IDs` |
| 7 | `Update canonical document section 6 (controls) and any threat references` |
| 8 | `Update CHANGELOG with control library v1 changes` |

Show me the diff for each commit before executing it. If validation fails on any commit, stop and report the error rather than working around it.

### Step 9: Stop

Do not push to any remote (none is configured). Do not start drafting CTL-002 through CTL-005 fully. Wait for further instructions. The next session will populate one of CTL-002 through CTL-005 fully or move to AGT-003.

## Quality checks before completing

| Check | Action |
|---|---|
| `data/controls.json` is valid JSON | Run a JSON parse |
| CTL-001 matches the per-control template fully | Compare field names and types |
| CTL-002 through CTL-005 are stubs only, not auto-generated content | Verify status field and minimal field population |
| AGT-001 and AGT-002 no longer reference any old control IDs (CTL-008, 009, 011, 014, 016, 021, 022, 027, 029, 031, 033) | Search for these strings; report if found |
| `data/mappings.json` references only valid CTL-NNN IDs (CTL-001 through CTL-005) | Search for old IDs; report if found |
| The canonical document is internally consistent (control IDs match between sections 5 and 6) | Cross-reference |
| No em dashes anywhere | Search for em dash character |
| Local Git history is clean | `git log --oneline` shows new commits, no merge commits |

## Working Conventions Recap

| Convention | Rule |
|---|---|
| No em dashes | Use commas, semicolons, periods, or parentheses |
| Tables over bullet points | Default to tables for lists of three or more comparable items |
| Cite primary sources | NIST, ISO, BSI, regulation texts, RFCs |
| Voice | First-person practitioner perspective |
| Length discipline | v1 stays at 10 to 15 controls; do not add more without explicit decision |

## Open Questions for Future Sessions

| Question | When to resolve |
|---|---|
| Should CTL-001 be split in v2 (e.g., into separate identity propagation and tenant isolation controls)? | After AGT-007 and AGT-008 are drafted; may surface variants that justify split |
| Should `existing_standard_mappings` include CIS Controls v8 or other frameworks? | If customer engagements surface demand for them; v1 stays at NIST 800-53, ISO 27001, BSI |
| Should controls have a "verification" field listing how to confirm the control is implemented correctly? | Worth considering for v2 once v1 stability is established |
| Should the framework provide a "control selection guide" for organizations starting from scratch? | After v1 is published and customer feedback is available |
