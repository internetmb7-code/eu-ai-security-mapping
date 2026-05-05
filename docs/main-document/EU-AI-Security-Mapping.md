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

The current v1 library status: CTL-001 is fully populated as the reference entry (presented below). CTL-002 through CTL-005 are reserved with title and domain assigned and full population deferred to subsequent sessions. CTL-006 through CTL-015 are reserved IDs that will be populated as the remaining threats (AGT-003 through AGT-010) are drafted.

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

### CTL-002 through CTL-005: forthcoming

The following entries are reserved with title and domain assigned. Full population is deferred to subsequent sessions.

| ID | Title | Domain | Function | Status |
|---|---|---|---|---|
| CTL-002 | Tool-output and context provenance | Runtime | Preventive, Detective | Stub |
| CTL-003 | Action verification at high-impact boundaries | Governance | Preventive | Stub |
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
