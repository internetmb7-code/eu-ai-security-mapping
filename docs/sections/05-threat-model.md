# 5. Agent-Specific Threat Model
<!-- Length budget: 4-6 pages -->

This section presents 10 agent-specific threats organized by the attack surface where each threat manifests most directly: input, model, tool-use, output, memory and persistence, and audit and provenance. Each entry follows a fixed template covering the threat's structural cause, a concrete attack scenario, the components affected, why traditional controls do not fully address it, the recommended controls from the framework's library, residual risk, detection and mitigation maturity, regulatory hooks, MITRE ATLAS mapping, and primary references. The catalog is deliberately bounded; threats outside this list are either covered adequately by existing frameworks (OWASP LLM Top 10, MITRE ATLAS technique-level entries) or out of the narrow agent scope defined in section 1.

This section is a guideline based on the author's interpretation of public regulatory texts and operational security experience. It is not legal advice. Readers should consult qualified legal counsel for compliance determinations specific to their organization.

---

### AGT-002: Authorization Confusion (Deputy Problem)

**Primary surface**: Tool-use
**Secondary surfaces**: Model, Audit and provenance

**Description**: An AI agent operates with an authorization scope that is decoupled from the authorization scope of the user it is serving. The agent's privileges, identity, and access to systems are configured at deployment time and persist across all user interactions. When a user asks the agent to act, the agent uses its own authorization context, not a constrained version derived from the user's. This creates a structural mismatch in which the agent can take actions the user is not authorized to perform, can access data the user is not authorized to see, or can act on behalf of users it is not serving in the current interaction. The threat is structural, not behavioral: it exists by design in many agent deployments and creates risk even when the agent is functioning correctly.

This entry covers three related sub-patterns that share the same root cause:

| Sub-pattern | Description |
|---|---|
| Excess privilege | The agent's authorization is broader than any individual user's, often because it must serve many users or perform many functions; users can cause actions through the agent that they could not perform directly |
| Cross-tenant deputy | In multi-tenant deployments, the agent's authorization spans tenants; an actor in one tenant can manipulate the agent to act in another |
| Delegation ambiguity | When an agent delegates to another agent or to a tool, the original user's authorization context is partially or fully lost; downstream systems see the agent's identity, not the user's |

These are facets of a single structural problem, not three separate threats.

**Attack scenario**: A workflow automation agent in a regulated DACH financial services enterprise is deployed to assist case officers across multiple business units. The agent is configured with read access to the full case management system, write access to specific case fields, and the ability to query an integrated KYC service. This authorization is granted at the system level and is constant across all user interactions, because configuring per-user authorization at the agent layer was deemed operationally complex during deployment.

A case officer in retail banking, who is authorized only for retail customer cases, asks the agent: "Summarize the open compliance flags for customer Schmidt." The agent retrieves the relevant cases. The case-management system performs its access check at the API layer using the agent's identity, not the user's, and returns all Schmidt-related cases including a private wealth management investigation that the retail officer is not authorized to see. The agent dutifully summarizes the content and presents it to the retail officer.

No traditional security control is bypassed. The agent's tool authorization is correct. The case-management API enforced its access policy correctly against the requesting identity. The user did not exploit a vulnerability. The harm comes from the agent being a deputy with broader authority than the user it served, and from the downstream system trusting the agent's identity rather than the user's.

The same scenario generalizes. In a cross-tenant variant, the agent serves customers across multiple tenants of a SaaS platform; an attacker in tenant A manipulates the agent into reading or writing in tenant B because the agent's authorization spans both. In a delegation-ambiguity variant, the case officer's request triggers the workflow agent to invoke a sub-agent for KYC enrichment; the sub-agent operates with its own service identity and has no record of which user originated the chain, so its actions are auditable to the sub-agent service account but not to the case officer.

**Affected components**:
- Agent runtime and its authorization configuration
- Identity and access management for agent service accounts
- Tool authorization layer between agent and external systems
- API gateways and downstream systems that perform access checks against the calling identity
- Multi-tenant data partitioning and isolation mechanisms
- Inter-agent communication and delegation infrastructure (where present)
- Audit logging systems that record actions against the agent's identity rather than the originating user

**Traditional controls and why insufficient**:

| Traditional control | Why insufficient |
|---|---|
| Role-based access control on the agent service account | The agent's role is correctly configured for what the agent must do, but that role is broader than any individual user's role; RBAC at the agent level cannot represent per-user constraints |
| Per-user authentication of the human caller | Authentication of the user works; the failure is in propagating that authenticated identity through the agent to downstream systems |
| Tool authorization (agent can only invoke specific tools) | The tools are the right tools for the agent; the issue is the data those tools return when called with the agent's identity rather than the user's |
| Multi-tenant data partitioning enforced at the database layer | Partitioning enforces tenant boundaries against the calling identity; if the agent's identity is permitted across tenants, partitioning does not protect against cross-tenant deputy attacks |
| Audit logging of agent actions | Logs record the agent acted; tracing back to the originating user requires correlation with upstream session logs that may not be retained or linkable |
| Session timeout and credential rotation | Address account compromise, not the structural decoupling of agent and user authorization |
| Network segmentation | The agent is operating within its expected network boundaries; the issue is logical authorization, not network reach |

**Recommended controls**:

| Control ID | Brief description |
|---|---|
| CTL-008 | User-context propagation: pass user identity and authorization claims through the agent to downstream systems, rather than relying on the agent's identity alone |
| CTL-009 | On-behalf-of authorization model: agent's effective authorization for any action is the intersection of its own authorization and the user's, not the union |
| CTL-011 | Tenant boundary enforcement at the agent layer: agents operating in multi-tenant contexts must include tenant identity in every downstream call, with refusal to cross tenant boundaries |
| CTL-016 | Delegation-context preservation: when an agent invokes another agent or a tool, the original user identity and authorization claims must be carried forward and verified at each step |
| CTL-022 | Per-user agent instances or per-request authorization scoping: where feasible, agents are instantiated or authorized per user rather than as shared service accounts |
| CTL-029 | End-to-end audit traceability: every agent action must be traceable to the originating user, the agent involved, the delegation chain, and the authorization basis |
| CTL-031 | Authorization-based output filtering: even when an agent retrieves data using broader authorization, output to the user is filtered to what the user is independently authorized to see |

**Residual risk**: User-context propagation and on-behalf-of models reduce but do not eliminate the threat. Several residual risks remain even with full implementation of recommended controls:

| Residual risk | Description |
|---|---|
| Performance and complexity costs | Per-user authorization scoping increases latency, complicates caching, and may force architectural choices that organizations resist |
| Legacy system integration | Many enterprise systems do not natively support user-context propagation; the agent must either widen its authorization or fail to perform required integrations |
| Inference vs retrieval distinction | Output filtering protects against direct data exposure but not against the agent inferring or summarizing protected information from data it had broad access to read |
| Delegation chain breaks | In multi-step workflows involving external services, the user's context may not survive the entire chain even when the controls are properly implemented at each agent boundary |
| Configuration drift | Authorization scoping correctly designed at deployment can degrade over time as new tools, users, or tenants are added without re-evaluating the model |

For high-stakes actions or in environments where user-context propagation is impractical, human approval at the action boundary is the only fully reliable mitigation. Organizations should treat broad-authority agents as elevated-privilege systems and apply the controls appropriate to that risk class, including monitoring, periodic authorization reviews, and minimum-necessary scope discipline.

**Detection maturity**: Emerging. Detection requires audit infrastructure that correlates user sessions, agent actions, and downstream system access across systems. Most enterprise SIEM and SOC tooling is not yet configured to surface authorization-confusion patterns; the signal of "agent acted on broader scope than user authorization" is not a standard detection rule. Some progress in 2025 to 2026 from agent-aware security platforms, but the field is early.

**Mitigation maturity**: Emerging. The architectural patterns (on-behalf-of, user-context propagation) exist in identity and OAuth ecosystems and are well understood for traditional service-to-service authorization. Their application to agent runtimes is recent and not consistently implemented. Major agent frameworks and platforms differ significantly in their support for user-context propagation, and many enterprise integrations require custom work.

**Regulatory hooks**:

| Regulation | Article or section | Relevance |
|---|---|---|
| EU AI Act | Art. 14 (Human oversight) | Where automated decisions can cause significant harm, human oversight is required; agents acting outside the user's authorization are operating without the oversight the regulation assumes |
| EU AI Act | Art. 15 (Accuracy, robustness, cybersecurity) | Cybersecurity requirements for high-risk AI systems include resilience to unauthorized use; structural authorization confusion is a form of unauthorized use even when no traditional control is bypassed |
| NIS2 | Art. 21 (Cybersecurity risk-management measures) | Includes access control policies and asset management; broad-authority agents are critical assets requiring proportionate controls |
| DORA | Art. 6 to 8 (ICT risk-management framework) | Operational resilience and ICT risk management requirements applicable to financial entities, including identity and access management |
| DORA | Art. 9 (Identification and classification of ICT supported business functions) | Agents serving multiple business functions across tenants or units must be classified and risk-assessed accordingly |
| GDPR | Art. 5(1)(f) (Integrity and confidentiality) | Personal data must be processed in a manner that ensures appropriate security; cross-user or cross-tenant data exposure via agent deputy patterns violates this principle |
| GDPR | Art. 22 (Automated individual decision-making) | Agent actions taken outside the data subject's authorization context may constitute unauthorized automated processing |
| GDPR | Art. 25 (Data protection by design and by default) | Agents that retrieve more data than the user is authorized for, even if filtered before output, may fail the data minimization requirement |
| GDPR | Art. 32 (Security of processing) | Appropriate technical measures including pseudonymization and access control are required; broad-authority agents bypassing per-user access control fail this standard |

**ATLAS mapping**: AML.T0070 (Indirect Prompt Injection), AML.T0072 (Reverse Shell). Pending agentic AI techniques in ATLAS v5.4.0 and later: mappings to be reviewed and added as the ATLAS agentic catalog matures.

**ATLAS mapping notes**: Authorization confusion as a structural threat does not yet have a dedicated ATLAS technique ID. ATLAS focuses primarily on attacker-driven techniques; the deputy problem is partly a deployment-architecture issue that creates exploitable conditions rather than a single attacker action. As ATLAS expands its agentic AI coverage through 2026, expect dedicated techniques for excess-privilege agents, cross-tenant agent abuse, and delegation context loss. This entry will be updated as those mappings become available.

**Realistic example**: To be populated. Candidate sources include public 2025 to 2026 disclosures of agent authorization issues in enterprise SaaS deployments, academic literature on confused deputy in OAuth and agent contexts, and anonymized scenarios from public regulatory enforcement actions involving cross-user data exposure. The example must be drawn from public sources only, in line with the framework's vendor-neutral and product-agnostic positioning.

**References**:

Primary sources:
- MITRE ATLAS, ATLAS Matrix v5.4.0, technique catalog as of February 2026
- EU AI Act, Regulation (EU) 2024/1689, Articles 14 and 15
- DORA, Regulation (EU) 2022/2554, Articles 6 to 9
- GDPR, Regulation (EU) 2016/679, Articles 5(1)(f), 22, 25, and 32
- NIS2 Directive, Directive (EU) 2022/2555, Article 21
- OAuth 2.0 Token Exchange, RFC 8693 (relevant for on-behalf-of patterns)
- NIST SP 800-207, Zero Trust Architecture (relevant for per-request authorization principles)

Practitioner and research literature:
- Hardt, "The OAuth 2.0 Authorization Framework," RFC 6749 (foundational for delegation patterns)
- Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023) (relevant for the attack vector that exploits AGT-002)
- Recent work on agent identity and authorization from 2025 to 2026 (specific citations to be selected during section drafting)
