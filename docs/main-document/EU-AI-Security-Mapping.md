# EU AI Security Mapping

A practitioner's mapping of EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments.

> **Status:** scaffolding. No content drafted yet.
>
> **Disclaimer:** This document is a guideline based on the author's interpretation of public regulatory texts and operational security experience. It is **not legal advice**.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Scope and Disclaimer](#2-scope-and-disclaimer)
3. [Regulatory Landscape](#3-regulatory-landscape)
4. [Common-Control Crosswalk](#4-common-control-crosswalk)
5. [Agent Threat Patterns and Exemplars](#5-agent-threat-patterns-and-exemplars)
6. [Recommended Controls and Patterns](#6-recommended-controls-and-patterns)
7. [Implementation Considerations](#7-implementation-considerations)
8. [Gaps and Open Problems](#8-gaps-and-open-problems)
9. [References](#9-references)
- [Appendix A. ServiceNow Mapping (Optional)](#appendix-a-servicenow-mapping-optional)

---

## 1. Executive Summary

<!-- Source: docs/sections/01-executive-summary.md (1-2 pages) -->
_Placeholder. Content will be merged from the section draft._

## 2. Scope and Disclaimer

<!-- Source: docs/sections/02-scope-disclaimer.md (1 page) -->
_Placeholder._

## 3. Regulatory Landscape

<!-- Source: docs/sections/03-regulatory-landscape.md (4-6 pages) -->
_Placeholder._

## 4. Common-Control Crosswalk

<!-- Source: docs/sections/04-crosswalk.md (3-4 pages) -->
_Placeholder._

## 5. Agent Threat Patterns and Exemplars

<!-- Source: docs/sections/05-threat-model.md (4-6 pages) -->

This section presents the framework's view of agent-specific threats. It is structured in three layers, each playing a distinct role.

The first layer is an attack surface taxonomy. Agents have a bounded set of attack surfaces (input, model, tool-use, output, memory and persistence, audit and provenance), and each surface produces recognizable threat patterns. The taxonomy is the durable structural claim of the framework: it is finite, derived from the architectural components every agent has, and stable across deployments.

The second layer is a set of ten named threat exemplars (AGT-001 through AGT-010), one or two illustrative threats per attack surface. Each exemplar is documented with an attack scenario, an analysis of why traditional controls are insufficient, recommended controls from the v1 library, residual risk, detection and mitigation maturity, regulatory hooks, and MITRE ATLAS mappings. The exemplars are not an exhaustive enumeration of agent threats. They illustrate patterns concretely enough that practitioners can recognize variants in their own deployments.

The third layer is methodology for discovering threats specific to a deployment that may not match the named exemplars. The methodology is essential: threats are infinite, no catalog can be complete, and the framework's value lies in the taxonomy and the structured way of thinking, not in the specific list of named threats. The methodology is documented in `docs/frameworks/THREAT_MODEL_FRAMEWORK.md`; this section references it rather than restating it.

Practitioners using this section should not interpret coverage of the ten exemplars as completion of agent threat work. Coverage of the exemplars is necessary but not sufficient. The actual security work is in applying the taxonomy and methodology to the specific deployment, complemented by external catalogs (MITRE ATLAS, OWASP LLM Top 10, MITRE ATT&CK) for technique-level detail.

_The exemplar entries (AGT-001 through AGT-010) will be merged from the section drafts during document drafting (Phase 4). AGT-001 and AGT-002 are the populated exemplars to date; AGT-003 through AGT-010 are drafted but not yet committed._

## 6. Recommended Controls and Patterns

<!-- Source: docs/sections/06-controls.md (6-10 pages) -->

This section presents a coarse-grained v1 control library of 10 to 15 controls organized by implementation domain (identity, runtime, data, governance, audit and accountability) and tagged by function (preventive, detective, corrective, deterrent). Each control is mapped to the threats it addresses, to relevant articles of the EU AI Act, NIS2, DORA, and GDPR, and to the closest equivalents in NIST SP 800-53 Rev. 5, ISO 27001 Annex A, and BSI grundschutz. The intent is breadth and readability: a CISO should be able to scan the library in one sitting and identify which controls are relevant to their deployment.

The methodology, per-control template, taxonomy, and consolidation rules are documented in `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md`. That framework is the authoritative reference for how the library is structured and how new controls are added or refined. This section presents the controls themselves; the framework explains why they look the way they do.

The current v1 library status: CTL-001, CTL-002, and CTL-003 are fully populated (presented below). CTL-004 and CTL-005 are reserved with title and domain assigned and full population deferred to subsequent sessions. CTL-006 through CTL-015 are reserved IDs that will be populated as the remaining threats (AGT-003 through AGT-010) are drafted.

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

**Threats addressed**: AGT-002 (primary), AGT-001 (secondary, by limiting blast radius), AGT-005 (secondary, by enabling cleaner attribution).

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
- SPIFFE / SPIRE specifications for workload identity

### CTL-002: Tool-Output and Context Provenance

**Domain**: Runtime
**Function**: Preventive, Detective
**Maturity**: Emerging

**Description**: Content returned by tools is structurally distinguished from instructions the agent should follow. The control creates an architectural boundary between data the agent processes and instructions the agent treats as authoritative. Without this boundary, adversarial content embedded in tool outputs (documents, web pages, retrieval results, sub-agent responses) can override the agent's original task. With it, the agent runtime maintains provenance metadata that prevents content from being elevated to instruction status.

The control exists because LLMs do not natively distinguish between content and instruction. Both arrive in the same context window as text. The distinction must be enforced at the runtime layer, not relied upon as a model behavior.

**Implementation pattern**: Tool outputs are wrapped in a structured envelope before entering the agent context. The envelope preserves provenance metadata: source tool identity, retrieval timestamp, source URL or document identifier, content type, and trust level (e.g., internal-trusted, internal-untrusted, external). The agent runtime processes wrapped content as data, not as authoritative instruction.

Three implementation styles are common:

| Style | How it works |
|---|---|
| Tagged context | Tool outputs are inserted into the agent context with explicit markers (e.g., `<tool_output source="web_fetch" trust="external">`); the system prompt instructs the model to treat content within these markers as data, not instruction |
| Structured envelope | Tool outputs are passed to the agent as structured objects (JSON, typed records) with provenance fields; the agent reasoning operates over the structure, not raw text |
| Runtime mediation | A runtime layer between the model and tool calls inspects outputs and either rejects, transforms, or annotates them before they reach the model context |

The strongest implementations combine all three: structured envelopes at the runtime level, tagged context within the model prompt, and active runtime mediation for high-trust environments. For high-stakes deployments, the control extends to memory and persistence (memory writes carry provenance), to delegation chains (sub-agent outputs preserve their provenance through the chain), and to output channels (provenance metadata is referenced in audit logs).

**Operational considerations**:

| Consideration | Description |
|---|---|
| Performance overhead | Envelope wrapping and provenance tracking add per-call overhead, typically 5 to 15 ms per tool invocation; cumulative across multi-tool workflows |
| Complexity of cross-tool aggregation | When the agent reasons across outputs from multiple tools, provenance must be preserved through aggregation; naive transformation strips it |
| Trust level definition | Defining what counts as internal-trusted versus external requires policy work; over-broad trust labels weaken the control |
| Model cooperation | Tagged-context approaches depend on the model respecting the markers; current LLMs do this imperfectly, especially under adversarial pressure |
| Audit volume | Provenance-rich logs are larger than traditional tool-call logs; storage and SIEM costs grow accordingly |
| Backward compatibility | Existing agent integrations may not pass provenance through; integration retrofits are real work |

**Common failure modes**:

| Failure mode | Description |
|---|---|
| Envelope stripping during transformation | The agent summarizes, translates, or otherwise transforms tool output, and the transformation removes provenance metadata; downstream the content is treated as agent-generated rather than tool-retrieved |
| Provenance loss across delegation chains | A sub-agent receives content with provenance, processes it, and emits output without preserving the original source attribution |
| Reliance on model self-discipline | Implementations that depend on model instructions to treat retrieved content as data rather than instruction without runtime enforcement; models comply most of the time but not adversarially |
| Trust label drift | Initial deployment labels external content as untrusted; over time, internal sources are added that should also be untrusted but are labeled as internal-trusted |
| Inconsistent envelope formats | Different tools wrap output differently; the agent runtime must normalize, and normalization can introduce errors |
| Memory bypass | Provenance is enforced at retrieval but stripped before content is written to memory; persisted content loses its provenance and is later retrieved as agent-authored |

**Threats addressed**: AGT-001 (primary), AGT-006 (primary), AGT-008 (secondary), AGT-009 (secondary).

**Regulatory basis**:

| Regulation | Article or section | Relevance |
|---|---|---|
| EU AI Act | Art. 15 | Cybersecurity; resilience to manipulation through tool-output channels requires runtime-level provenance |
| EU AI Act | Art. 14 | Human oversight; provenance metadata supports the reviewability that meaningful oversight requires |
| EU AI Act | Art. 10 | Data and data governance; provenance is a data-quality control extended to runtime context |
| NIS2 | Art. 21 | Cybersecurity risk-management measures; agent runtimes processing variable-trust content fall within the directive's scope |
| DORA | Art. 6 to 8 | ICT risk management; operational resilience for financial entities including resilience to runtime manipulation |
| GDPR | Art. 32 | Security of processing; technical measures including resilience to manipulation of context content |
| GDPR | Art. 5(1)(d) | Accuracy; provenance is a precondition for assessing and maintaining accuracy of content the agent operates over |

**Existing standard mappings**:

| Standard | Control ID | Relationship |
|---|---|---|
| NIST SP 800-53 Rev. 5 | SC-8 (Transmission Confidentiality and Integrity) | Refinement: SC-8 establishes integrity protection for transmissions; CTL-002 extends to integrity-of-attribution for tool outputs within agent runtimes |
| NIST SP 800-53 Rev. 5 | SI-10 (Information Input Validation) | Refinement: SI-10 covers input validation generally; CTL-002 extends to the specific case of tool outputs as inputs to model reasoning |
| NIST SP 800-53 Rev. 5 | SI-15 (Information Output Filtering) | Adjacent: SI-15 addresses output filtering; CTL-002 addresses input handling but uses similar provenance principles |
| ISO 27001 Annex A | A.8.26 (Application security requirements) | Refinement: application security extended to agent runtime requirements |
| ISO 27001 Annex A | A.8.28 (Secure coding) | Adjacent: secure coding principles applied to agent runtime envelope handling |
| BSI grundschutz | CON.10 (Webanwendungen und Webservices) | Adjacent: web application security extended to retrieval-tool integrations |
| BSI grundschutz | OPS.1.2.4 (Schutz vor Schadprogrammen) | Refinement: extended to agent-context-level content evaluation |

**Related controls**:

| Control | Relationship |
|---|---|
| CTL-001 (Identity and authorization context propagation) | Complementary: provenance addresses what content is; identity propagation addresses who the action is for |
| CTL-003 (Action verification at high-impact boundaries) | Complementary: when provenance flags untrusted content as influencing a high-impact action, action verification provides a checkpoint |
| CTL-005 (End-to-end audit and accountability) | Dependent: forensic review of injection-driven actions requires the provenance metadata that CTL-002 produces |

**References**:

- NIST SP 800-53 Rev. 5, controls SC-8, SI-10, SI-15
- NIST SP 800-218 (Secure Software Development Framework), relevant for runtime input handling
- ISO/IEC 27001:2022, Annex A controls A.8.26 and A.8.28
- BSI IT-Grundschutz-Kompendium, Bausteine CON.10 and OPS.1.2.4
- IETF RFC 9421 (HTTP Message Signatures), relevant pattern for verifiable provenance metadata
- OWASP Top 10 for LLM Applications, LLM01 (Prompt Injection) and LLM03 (Training Data Poisoning) for context on the threat landscape
- MITRE ATLAS, AML.T0070 (Indirect Prompt Injection)
- Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)

### CTL-003: Action Verification at High-Impact Boundaries

**Domain**: Governance
**Function**: Preventive
**Maturity**: Emerging

**Description**: Before an agent executes an action that exceeds defined impact thresholds, the action is verified through an explicit checkpoint that is independent of the agent reasoning. The control inserts a governance boundary between agent intent and consequential action. Where automated controls cannot fully prevent a threat, this checkpoint is often the only fully reliable mitigation.

The control is governance-domain because the central work is policy: defining what counts as high-impact, how verification happens, who or what performs it, and what triggers escalation. The technical enforcement is straightforward once policy is clear; the policy itself requires deliberate organizational decisions that cannot be automated.

**Implementation pattern**: Define impact thresholds across multiple dimensions: financial (transaction value, cumulative cost), reputational (external communications, customer-facing decisions), regulatory (actions touching regulated data or processes), irreversibility (data deletion, contract execution, public statements), and cumulative composition (sequences of individually small actions producing high-impact outcomes).

For any action exceeding a threshold, the agent must obtain verification before proceeding. Verification can take several forms:

| Verification mode | Use case |
|---|---|
| Human approval (human-in-the-loop) | Highest-stakes actions; irreversible decisions; regulated environments where automation alone is not permitted |
| Out-of-band confirmation | User confirms via secondary channel (email, push notification, signed token); appropriate where the user is the originating actor |
| Secondary agent review | A second agent with different prompts, different context, or different authorization reviews the proposed action; useful at scale where human approval does not |
| Policy engine check | Automated rule evaluation against a policy; appropriate for well-defined, repeatable threshold tests |
| Multi-step delay with notification | Action is queued for a defined window during which it can be canceled; appropriate for moderate-impact actions where review is desirable but not essential |

The control extends to composed actions. A sequence of low-impact actions that together produce a high-impact outcome must be detected and verified at the composition boundary, not only at the individual action level. This requires the agent runtime to track cumulative effect, not just per-call thresholds. For high-stakes deployments, verification is layered: a policy engine handles the high-volume routine cases, secondary agent review handles the medium-volume novel cases, and human approval handles the low-volume highest-stakes cases.

**Operational considerations**:

| Consideration | Description |
|---|---|
| Latency | Verification adds latency, ranging from milliseconds (policy engine) to hours or days (human approval); this directly affects user experience and must be designed into the workflow |
| Threshold calibration | Thresholds must be tuned to organizational risk tolerance; too low and verification becomes routine and ignored, too high and meaningful actions slip through |
| Verification fatigue | Reviewers exposed to many verifications develop rubber-stamping behavior; design must include sampling, randomization, or explicit attention prompts |
| Cumulative effect tracking | Tracking composed actions requires runtime instrumentation that many agent platforms do not natively support |
| Threshold drift | Policy thresholds set at deployment can become stale as products, regulations, and risk environment evolve; periodic governance review is essential |
| Workaround risk | Agents under instruction or pressure may find paths to achieve the same outcome through actions that individually fall below thresholds; CTL-003 alone does not prevent this |
| Cross-organization variance | What counts as high-impact varies dramatically across regulated sectors; the control framework requires sector-specific policy work |

**Common failure modes**:

| Failure mode | Description |
|---|---|
| Threshold definitions becoming stale | Initial thresholds reflect deployment-time assumptions; product changes, regulatory changes, and threat landscape evolution make them inadequate over time |
| Rubber-stamping | Reviewers process too many verifications too quickly; the verification becomes formal rather than meaningful |
| Per-action thresholds without composition | Thresholds catch single high-impact actions but miss sequences of low-impact actions producing similar outcomes |
| Verification path bypass | Agents discover paths that achieve the goal through tools or sequences not covered by threshold rules |
| Policy engine staleness | Automated rules are written once and not maintained; new action types fall outside the rules and proceed without verification |
| Out-of-band channel compromise | Confirmation channels (email, SMS) are themselves attackable; under sophisticated attack, the confirmation step can be defeated |
| Misaligned verification authority | The reviewer lacks the context, authority, or training to evaluate the action meaningfully; the verification is procedural rather than substantive |

**Threats addressed**: AGT-001 (primary), AGT-002 (primary), AGT-003 (primary), AGT-008 (primary), AGT-009 (secondary), AGT-010 (secondary).

**Regulatory basis**:

| Regulation | Article or section | Relevance |
|---|---|---|
| EU AI Act | Art. 14 | Human oversight; the regulatory anchor for human-in-the-loop verification at high-impact boundaries |
| EU AI Act | Art. 15 | Cybersecurity; resilience to manipulation requires verification gates for consequential actions |
| EU AI Act | Art. 9 | Risk management system; high-impact actions require proportionate verification controls |
| NIS2 | Art. 21 | Cybersecurity risk-management measures; action-boundary verification is a structural risk control |
| DORA | Art. 6 to 9 | ICT risk management and identification of critical functions requiring proportionate verification |
| GDPR | Art. 22 | Automated individual decision-making; verification is the structural mechanism for the right to human review |
| GDPR | Art. 32 | Security of processing; verification at high-impact boundaries is a technical and organizational measure |

**Existing standard mappings**:

| Standard | Control ID | Relationship |
|---|---|---|
| NIST SP 800-53 Rev. 5 | AC-3 (Access Enforcement) | Refinement: AC-3 establishes the principle of enforcing approved authorizations; CTL-003 extends to action-level verification beyond identity-based authorization |
| NIST SP 800-53 Rev. 5 | CA-7 (Continuous Monitoring) | Refinement: continuous monitoring extended to agent action streams |
| NIST SP 800-53 Rev. 5 | AC-21 (Information Sharing) | Adjacent: information-sharing decisions are a class of high-impact action that CTL-003 covers |
| NIST SP 800-53 Rev. 5 | SI-4 (System Monitoring) | Adjacent: system monitoring extended to agent action patterns |
| ISO 27001 Annex A | A.5.36 (Compliance with policies, rules and standards) | Refinement: policy compliance enforced at the action boundary |
| ISO 27001 Annex A | A.8.7 (Protection against malware) | Adjacent: extended to protection against agent-driven actions exceeding authorization scope |
| BSI grundschutz | ORP.1 (Organisation) | Refinement: organizational governance extended to agent action governance |
| BSI grundschutz | ORP.4 (Identitäts- und Berechtigungsmanagement) | Adjacent: identity and authorization management extended to action verification |

**Related controls**:

| Control | Relationship |
|---|---|
| CTL-001 (Identity and authorization context propagation) | Complementary: CTL-001 limits what the agent is authorized to do; CTL-003 verifies high-impact actions within that authorization |
| CTL-002 (Tool-output and context provenance) | Complementary: provenance metadata informs the verification decision; untrusted-content-influenced actions warrant stricter verification |
| CTL-005 (End-to-end audit and accountability) | Dependent: verification decisions must be auditable; CTL-005 captures the verification record |

**References**:

- NIST SP 800-53 Rev. 5, controls AC-3, AC-21, CA-7, SI-4
- NIST SP 800-37 Rev. 2, Risk Management Framework, for governance context
- ISO/IEC 27001:2022, Annex A controls A.5.36 and A.8.7
- ISO/IEC 38500:2024, Governance of information technology, for organizational governance principles applicable to agent governance
- BSI IT-Grundschutz-Kompendium, Bausteine ORP.1 and ORP.4
- EU AI Act, Article 14 (Human oversight), as the regulatory anchor for human-in-the-loop verification at high-impact boundaries
- DORA, Articles 6 to 9, for ICT risk management and identification of critical functions requiring proportionate verification

### CTL-004 and CTL-005: forthcoming

The following entries are reserved with title and domain assigned. Full population is deferred to subsequent sessions.

| ID | Title | Domain | Function | Status |
|---|---|---|---|---|
| CTL-004 | Authorization-aware output filtering | Data | Preventive | Stub |
| CTL-005 | End-to-end audit and accountability | Audit and accountability | Detective | Stub |

## 7. Implementation Considerations

<!-- Source: docs/sections/07-implementation.md (4-6 pages) -->
_Placeholder._

## 8. Gaps and Open Problems

<!-- Source: docs/sections/08-gaps.md (2-3 pages) -->
_Placeholder._

## 9. References

<!-- Source: docs/sections/09-references.md (2-3 pages) -->
_Placeholder._

## Appendix A. ServiceNow Mapping (Optional)

<!-- Source: docs/sections/10-appendix-servicenow-mapping.md -->
<!-- Optional, non-canonical overlay mapping the generic controls in section 6 to ServiceNow products. -->
_Placeholder._
