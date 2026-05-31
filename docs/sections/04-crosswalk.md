# 4. Common-Control Crosswalk

This section presents the consolidated view of how the four EU regulations addressed by the framework map to the v1 controls. It is the practitioner-facing summary that supports two common questions:

- "We are subject to regulation X; which controls in this framework address its requirements?"
- "We have implemented control Y; which regulatory requirements does it help us satisfy?"

The crosswalk is summary-level. Specific article-level citations and the per-control regulatory basis live in the threat entries (section 5) and the control entries (section 6). Section 4 is the entry point; sections 5 and 6 are the detailed reference.

## 4.1 Methodology

The crosswalk is constructed from the regulatory hooks documented in each threat entry (AGT-001 through AGT-010) and the regulatory basis documented in each control entry (CTL-001 through CTL-005). These hooks are practitioner-attested interpretations of which regulatory provisions a given control or threat addresses. They are defensible but not authoritative.

Two views of the same underlying data are presented:

| View | What it shows | When to use it |
|---|---|---|
| Direct view | Regulation to control mappings, organized by regulation | Compliance-oriented work; quick reference for which controls support which regulatory provisions |
| Reasoned view | Regulation to threat to control chain, organized by regulation | Defensive-reasoning work; explains *why* each control satisfies the regulation by identifying the threat pattern it addresses |

The direct view is faster. The reasoned view is more defensible when challenged by an auditor or regulator. Practitioners should be comfortable with both.

## 4.2 Direct view: which controls support which regulations

The following table summarises which v1 controls address requirements under each named regulation. A control listed as "primary" is a substantive answer to the regulatory requirement. A control listed as "supporting" contributes to the requirement but is not the central control.

| Regulation and provision | Primary controls | Supporting controls |
|---|---|---|
| EU AI Act Art. 9 (Risk management) | CTL-003 | CTL-005 |
| EU AI Act Art. 12 (Record-keeping) | CTL-005 | CTL-001, CTL-002 |
| EU AI Act Art. 13 (Transparency) | CTL-005 | CTL-002 |
| EU AI Act Art. 14 (Human oversight) | CTL-003 | CTL-001, CTL-005 |
| EU AI Act Art. 15 (Cybersecurity, robustness) | CTL-001, CTL-002, CTL-003, CTL-004 | CTL-005 |
| NIS2 Art. 21 (Cybersecurity risk-management measures) | CTL-001, CTL-002, CTL-003, CTL-004, CTL-005 | All v1 controls contribute |
| NIS2 Art. 23 (Reporting obligations) | CTL-005 | None |
| DORA Art. 6 (ICT risk management framework) | CTL-001, CTL-003, CTL-005 | CTL-002, CTL-004 |
| DORA Art. 7 (ICT systems, protocols, tools) | CTL-001, CTL-002 | CTL-003 |
| DORA Art. 8 (Identification) | CTL-005 | CTL-001 |
| DORA Art. 9 (Protection and prevention) | CTL-001, CTL-004 | CTL-002 |
| DORA Art. 12 (Major incident reporting) | CTL-005 | None |
| DORA Arts. 28 to 30 (Third-party risk) | Out of scope for v1; vendor mapping addresses this | None |
| GDPR Art. 5(1)(b) Purpose limitation | CTL-003 | None |
| GDPR Art. 5(1)(c) Data minimisation | CTL-004 | CTL-001 |
| GDPR Art. 5(1)(f) Integrity and confidentiality | CTL-001, CTL-002, CTL-004 | CTL-005 |
| GDPR Art. 22 (Automated decision-making) | CTL-003, CTL-005 | CTL-001 |
| GDPR Art. 25 (Data protection by design) | CTL-001, CTL-004 | CTL-002, CTL-003 |
| GDPR Art. 30 (Records of processing) | CTL-005 | None |
| GDPR Art. 32 (Security of processing) | CTL-001, CTL-002, CTL-004 | CTL-003, CTL-005 |
| GDPR Art. 35 (DPIA) | Process-level; CTL-005 supports | All v1 controls inform DPIA content |

The table reflects current v1 coverage. Where a regulatory provision is not addressed by any v1 control (DORA third-party risk, GDPR DPIA process), this is noted explicitly rather than implied. Section 8 (Gaps and open problems) addresses where v1 coverage is partial or absent.

## 4.3 Reasoned view: regulation to threat to control

The reasoned view explains why each control addresses the regulatory requirement by identifying the threat pattern the regulation implicitly requires defense against. This view is defensible when an auditor or regulator asks "How does this control satisfy the requirement?"

Four reasoned chains are presented as worked examples. Practitioners can construct additional chains for any of the regulatory provisions in the direct view above using the same pattern.

### Chain 1: EU AI Act Article 15 (Cybersecurity)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 15 requires high-risk AI systems to achieve appropriate levels of accuracy, robustness, and cybersecurity, including resilience against attempts by unauthorised third parties to alter use, outputs, or performance. |
| Threat patterns implied | The article implicitly requires defense against agent-specific threats including indirect adversarial input (AGT-001), authorisation manipulation (AGT-002), tool-chain abuse (AGT-003), and goal subversion (AGT-009). These are the "alteration attempts" the article addresses for agent systems specifically. |
| Controls that address those threats | CTL-002 (tool-output provenance) addresses AGT-001. CTL-001 (identity propagation) addresses AGT-002. CTL-003 (action verification) addresses AGT-003 and AGT-009. CTL-005 (audit) supports detection across all. |
| Why this combination satisfies the article | The combination provides the resilience the article requires by preventing, detecting, and enabling response to the specific threats that constitute "alteration attempts" in the agent context. No single control is sufficient; the combination is. |

### Chain 2: DORA Article 9 (Protection and prevention)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 9 requires financial entities to implement specific protection measures including access management, identity management, encryption, and configuration management. |
| Threat patterns implied | The article implicitly requires defense against authorisation decoupling (AGT-002) and data exfiltration through legitimate channels (AGT-004), among others. These are the access and identity threats specifically relevant to agent deployments. |
| Controls that address those threats | CTL-001 (identity and authorisation context propagation) directly satisfies the identity management requirement for agents. CTL-004 (authorisation-aware output filtering) addresses the data protection dimension. |
| Why this combination satisfies the article | CTL-001 brings user-level identity into the agent runtime in a way that traditional service identity does not. CTL-004 closes the output gap that traditional access management does not see. Together they extend the protection requirements of Article 9 to the agent context. |

### Chain 3: GDPR Article 22 (Automated decision-making)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 22(1) gives data subjects the right not to be subject to decisions based solely on automated processing producing legal or similarly significant effects. Where such processing occurs, Article 22(3) requires the controller to implement suitable measures including the right to obtain human intervention. |
| Threat patterns implied | The article implicitly requires that automated agent decisions affecting data subjects can be subject to human intervention, which means the system must recognise when such a decision is being taken and pause for review. |
| Controls that address those threats | CTL-003 (action verification at high-impact boundaries) is the structural mechanism by which agent decisions can be paused for human review. CTL-005 (audit and accountability) supports the right by enabling reconstruction of how a decision was reached. |
| Why this combination satisfies the article | CTL-003 provides the procedural mechanism for human intervention. CTL-005 provides the basis for the data subject to meaningfully exercise that right by understanding what decision was made and why. Without both, Article 22 cannot be operationalised for agents. |

### Chain 4: NIS2 Article 21 (Cybersecurity risk-management measures)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 21 requires essential and important entities to take appropriate and proportionate measures across ten enumerated categories including risk analysis, incident handling, business continuity, supply chain security, access control, and others. |
| Threat patterns implied | The article is broad. For agent deployments, the implicit threat patterns span the full attack surface: input (AGT-001), tool-use (AGT-002, AGT-003), output (AGT-004, AGT-008), and audit (AGT-005). |
| Controls that address those threats | All five v1 controls contribute. The article's breadth means the framework's controls are most usefully understood as a coherent set that addresses the agent dimension across the ten measure categories. |
| Why this combination satisfies the article | NIS2 Article 21 is not satisfied by any single control. It is satisfied by demonstrating that the agent-specific dimensions of the ten measure categories are addressed. The v1 controls collectively do this; gaps remain (per section 8) but the foundation is in place. |

## 4.4 How to use the crosswalk in practice

The crosswalk supports several workflows that practitioners actually perform.

| Workflow | How to use the crosswalk |
|---|---|
| Regulatory readiness assessment | Start from the regulation column in section 4.2. Identify which v1 controls are listed as primary for the applicable provisions. Cross-reference to section 6 for implementation patterns and operational considerations. Identify gaps where the framework lists no primary controls. |
| Control program design | Start from the controls in section 6. For each control already implemented or planned, cross-reference to section 4.2 to identify which regulatory provisions are supported. Use this to scope compliance documentation. |
| Auditor engagement | For any regulatory provision questioned by the auditor, use the reasoned view in section 4.3 to construct the defense: regulation, threat pattern, control, why the combination is sufficient. Apply the same pattern to provisions not worked out in section 4.3. |
| Threat-driven program design | Start from the threat catalog in section 5. For each threat the deployment is exposed to, cross-reference to section 4.2 to understand which regulatory provisions implicitly require defense against it. |

## 4.5 Limitations of the crosswalk

The crosswalk is summary-level. Practitioners should be aware of three limitations:

| Limitation | Implication |
|---|---|
| Mappings are practitioner-attested, not regulator-attested | The mappings represent defensible interpretations of which controls address which provisions. They are not authoritative compliance determinations. Practitioners verifying compliance should obtain legal counsel. |
| The crosswalk reflects v1 framework coverage | Where the framework has known gaps (section 8), the crosswalk does not artificially close them by listing inadequate controls as primary. |
| Sectoral and national variations are not reflected | The crosswalk addresses the four named regulations at the EU level. Member State transposition variations, sectoral overlays (BSI grundschutz, BaFin guidance, MDR for medical contexts), and similar are out of scope for v1. |

These limitations are not defects. They are properties of any practitioner crosswalk constructed at a defensible level of generality. Practitioners adapt the crosswalk to their specific organisational context.
