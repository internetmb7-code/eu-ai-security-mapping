## How to read this section

This section maps regulatory requirements to the controls in this framework's v1 control library (CTL-001 through CTL-005). It is a navigation aid, not a compliance certification. A cell that names a control means the control contributes substantively to satisfying the requirement; it does not mean the control alone discharges the obligation. Most regulatory requirements are satisfied by a combination of controls, organizational measures, and operational evidence that fall outside the technical scope of this framework.

The mappings below connect requirements to controls through the bridging threat that puts the requirement at risk. The bracketed `[via AGT-NNN]` notation cites the threat. This reflects how [`../../data/mappings.json`](../../data/mappings.json) actually models the relationship: a regulatory requirement does not connect to a control directly; the connection runs through a specific agent threat that the control mitigates and that the requirement either explicitly or implicitly addresses. The bridging-threat notation makes the evidence chain visible.

The primary view is requirement-to-control. A summary table at the end (subsection 4.6) presents the inverse view for readers navigating from the control library.

Honest gaps in the v1 crosswalk are documented in subsection 4.7.

## EU AI Act: requirements and matching controls

| AI Act requirement | Bridging threats | v1 controls (with bridge) |
|---|---|---|
| Article 9 (Risk management system) | AGT-001, AGT-003, AGT-009 | CTL-001 [via AGT-001, AGT-003], CTL-002 [via AGT-001, AGT-009], CTL-003 [via AGT-001, AGT-003, AGT-009], CTL-005 [via AGT-001, AGT-003, AGT-009] |
| Article 10 (Data and data governance) | AGT-006 | None in v1 (this is primarily a provider-side training-data obligation; v1 controls do not address training data quality. Memory poisoning under AGT-006 is the closest agent-deployment connection) |
| Article 12 (Record-keeping) | AGT-005 | CTL-005 [via AGT-005, primary], CTL-001 [via AGT-005, primary], CTL-002 [via AGT-005, primary] |
| Article 13 (Transparency to deployers) | AGT-005 | CTL-001 [via AGT-005], CTL-002 [via AGT-005], CTL-005 [via AGT-005] |
| Article 14 (Human oversight) | AGT-001, AGT-002, AGT-003, AGT-005, AGT-007, AGT-009 | CTL-003 [via AGT-001, AGT-002, AGT-003, AGT-007, AGT-009; primary across most], CTL-002 [via AGT-005, AGT-007, AGT-009], CTL-005 [via AGT-005, AGT-009] |
| Article 15 (Accuracy, robustness, cybersecurity) | AGT-001, AGT-002, AGT-004, AGT-006, AGT-007, AGT-008, AGT-009, AGT-010 | CTL-001 [via most], CTL-002 [via AGT-001, AGT-006, AGT-007, AGT-008, AGT-009], CTL-003 [via most], CTL-004 [via AGT-002, AGT-004, AGT-008], CTL-005 [via most] (all five v1 controls contribute; cybersecurity is addressed by the entire library) |

**What this means for agent deployments**: The v1 control library covers the technical core of AI Act compliance for agent deployments, with strongest coverage of Articles 12 (logging), 14 (oversight), and 15 (cybersecurity). Coverage of data governance (Article 10) and process obligations (QMS, FRIA) is intentionally out of scope. Deployers should treat this framework as the technical layer of a broader compliance program, not as the program itself.

## NIS2: requirements and matching controls

NIS2 mappings in `mappings.json` reference Article 21 at the article level rather than the sub-paragraph level. The crosswalk preserves that granularity.

| NIS2 requirement | Bridging threats | v1 controls (with bridge) |
|---|---|---|
| Article 21 (Cybersecurity risk-management measures, general) | AGT-001, AGT-002, AGT-004, AGT-005, AGT-006, AGT-007, AGT-008, AGT-010 | CTL-001 [via most], CTL-002 [via AGT-001, AGT-005, AGT-006, AGT-007, AGT-008], CTL-003 [via most], CTL-004 [via AGT-002, AGT-004, AGT-008], CTL-005 [via most] (NIS2 Art 21 is the universal cybersecurity baseline; the full v1 library contributes through the threats it mitigates) |

**What this means for agent deployments**: NIS2 Article 21 sets the cybersecurity risk-management baseline. The v1 controls address the agent-specific layer that sits on top of foundational cybersecurity baselines (cryptography, MFA, backup, network segmentation, supply chain). Entities subject to NIS2 should treat this framework as agent-specific reinforcement of an existing NIS2 program, not as a substitute for it. Sub-paragraph-level coverage of Article 21 (for example, 21(2)(a) policies, 21(2)(d) supply chain, 21(2)(g) hygiene and training) is documented in subsection 4.7.

## DORA: requirements and matching controls

| DORA requirement | Bridging threats | v1 controls (with bridge) |
|---|---|---|
| Articles 6 to 8 (ICT risk-management framework) | AGT-001, AGT-002, AGT-003, AGT-004, AGT-008, AGT-010 | CTL-001 [via most], CTL-002 [via AGT-001, AGT-008], CTL-003 [via AGT-001, AGT-002, AGT-003, AGT-008], CTL-004 [via AGT-002, AGT-004, AGT-008], CTL-005 [via most] (the v1 controls form the technical agent-specific layer of the ICT risk management framework) |
| Article 9 (Identification and classification of ICT-supported business functions) | AGT-002 | CTL-001 [via AGT-002, primary], CTL-003 [via AGT-002, primary], CTL-004 [via AGT-002, primary], CTL-005 [via AGT-002] |
| Article 12 (Major ICT-related incidents) | AGT-005 | CTL-005 [via AGT-005, primary], CTL-001 [via AGT-005, primary], CTL-002 [via AGT-005, primary] |
| Articles 28 to 30 (ICT third-party risk) | AGT-007 | CTL-001 [via AGT-007, primary], CTL-002 [via AGT-007, primary], CTL-003 [via AGT-007, primary], CTL-005 [via AGT-007] (third-party risk applies when sub-agents integrate third-party services; contractual provisions under Article 30 are organizational and not addressed by v1 technical controls) |

**What this means for agent deployments**: DORA's five-pillar structure means the v1 controls primarily address Pillar 1 (ICT risk management) and parts of Pillar 4 (third-party risk via sub-agent delegation). Pillars 2 (incident reporting), 3 (resilience testing), and 5 (information sharing) are largely organizational. Financial entities deploying agents should treat this framework as the technical agent-specific component of Pillars 1 and 4, integrated into the broader DORA programme.

## GDPR: requirements and matching controls

GDPR coverage extends beyond Article 22. The crosswalk includes the GDPR articles named in `mappings.json` because all of them are directly relevant to enterprise agent deployments.

| GDPR requirement | Bridging threats | v1 controls (with bridge) |
|---|---|---|
| Article 5(1)(b) (Purpose limitation) | AGT-009 | CTL-002 [via AGT-009], CTL-003 [via AGT-009], CTL-005 [via AGT-009] |
| Article 5(1)(c) (Data minimization) | AGT-003, AGT-009 | CTL-001 [via AGT-003], CTL-003 [via AGT-003, AGT-009], CTL-005 [via AGT-003, AGT-009] |
| Article 5(1)(d) (Accuracy) | AGT-006 | CTL-002 [via AGT-006, primary], CTL-003 [via AGT-006], CTL-005 [via AGT-006] |
| Article 5(1)(f) (Integrity and confidentiality) | AGT-002, AGT-004 | CTL-001 [via AGT-002, AGT-004; primary], CTL-003 [via AGT-002], CTL-004 [via AGT-002, AGT-004; primary], CTL-005 [via AGT-002, AGT-004] |
| Article 5(2) (Accountability) | AGT-005, AGT-007 | CTL-001 [via AGT-005, AGT-007], CTL-002 [via AGT-005, AGT-007], CTL-005 [via AGT-005, primary; AGT-007] |
| Article 17 (Right to erasure) | AGT-006 | CTL-002 [via AGT-006, primary], CTL-005 [via AGT-006] (erasure is more complex when persisted state has influenced agent behavior; provenance and audit are necessary but not sufficient) |
| Article 22 (Automated individual decision-making) | AGT-001, AGT-002, AGT-005 | CTL-001 [via AGT-002], CTL-003 [via AGT-001, AGT-002; the structural mechanism for ensuring decisions are not "solely" automated], CTL-004 [via AGT-002], CTL-005 [via AGT-005; supports the right-to-explanation by providing auditable decision provenance] |
| Article 25 (Data protection by design and by default) | AGT-002, AGT-003, AGT-009 | CTL-001 [via AGT-002, AGT-003], CTL-003 [via AGT-003, AGT-009], CTL-005 [via AGT-009] |
| Article 32 (Security of processing) | AGT-001, AGT-002, AGT-004, AGT-008 | CTL-001 [via AGT-002, AGT-004; primary], CTL-002 [via AGT-001, AGT-008], CTL-003 [via AGT-001, AGT-002, AGT-008], CTL-004 [via AGT-002, AGT-004, AGT-008; primary] |

**What this means for agent deployments**: GDPR coverage in the v1 controls is broader than Article 22 alone. Article 32 (security of processing) is satisfied substantively by CTL-001, CTL-003, and CTL-004 across multiple threats. Article 5(1)(f) (integrity and confidentiality) is the principle-level anchor for the deputy and exfiltration patterns. Article 22 specifically applies only when the agent makes solely automated decisions producing legal or similarly significant effects on individuals; CTL-003 is the structural mechanism for placing meaningful human review at the decision boundary. Where Article 22 applies, deployers should pair CTL-003 with the organizational measures (lawful basis assessment, data subject communication, contestability process) that the v1 control library does not address.

## Common-control summary: control-to-requirement view

This subsection presents the inverse of the requirement-to-control crosswalk. For each v1 control, the table indicates which regulatory requirements it contributes to (across all bridging threats). This view is intended for readers navigating from the control library rather than from a regulatory question.

| Control | EU AI Act | NIS2 | DORA | GDPR |
|---|---|---|---|---|
| CTL-001 (Identity and authorization context propagation) | Articles 9, 12, 13, 14, 15 | Article 21 | Articles 6 to 8, 9, 12, 28 to 30 | Articles 5(1)(c), 5(1)(f), 5(2), 22, 25, 32 |
| CTL-002 (Tool-output and context provenance) | Articles 9, 12, 13, 14, 15 | Article 21 | Articles 6 to 8, 12, 28 to 30 | Articles 5(1)(b), 5(1)(d), 5(2), 17, 32 |
| CTL-003 (Action verification at high-impact boundaries) | Articles 9, 14, 15 | Article 21 | Articles 6 to 8, 9, 28 to 30 | Articles 5(1)(b), 5(1)(c), 5(1)(d), 5(1)(f), 22, 25, 32 |
| CTL-004 (Authorization-aware output filtering) | Article 15 | Article 21 | Articles 6 to 8, 9 | Articles 5(1)(f), 22, 32 |
| CTL-005 (End-to-end audit and accountability) | Articles 9, 12, 13, 14, 15 | Article 21 | Articles 6 to 8, 9, 12, 28 to 30 | Articles 5(1)(b), 5(1)(c), 5(1)(d), 5(1)(f), 5(2), 17, 22, 25 |

The pattern: CTL-005 carries the broadest regulatory weight because logging, audit, and accountability are universal requirements across all four instruments. CTL-001 and CTL-003 are the structural anchors for human-oversight and access-control requirements. CTL-002 is the specialized control for provenance-related obligations (transparency, accuracy, erasure). CTL-004 has the narrowest direct mapping but is decisive for confidentiality and Article 22 contexts.

## Honest gaps in the crosswalk

Several requirements in the four instruments have no direct match in the v1 control library because no v1 threat bridges them to a v1 control. These gaps are intentional; v1 is scoped to the agent-specific operational security layer, not to the foundational cybersecurity baseline or the organizational compliance program.

| Requirement | Why no v1 match | Where it belongs |
|---|---|---|
| AI Act Article 10 (training-data governance) | Provider-side obligation focused on training data; AGT-006 (memory poisoning) is the closest agent-deployment bridge but does not satisfy the full obligation | Outside v1 scope; AI Act provider compliance frameworks |
| AI Act Article 16 (provider obligations, general); Article 17 (QMS); Article 19 (provider log retention); Article 26 (deployer obligations); Article 27 (FRIA) | Process and organizational obligations; v1 controls provide the technical substrate (especially CTL-005 for logging) but the obligations themselves are not satisfied by technical controls alone | Outside v1 scope; covered by AI Act compliance program guidance |
| NIS2 Article 21(2)(c) (business continuity, backup, crisis management) | Foundational ICT continuity controls | Assumed to exist independently; ISO 22301, NIST SP 800-34 |
| NIS2 Article 21(2)(d) (supply chain security) | Out of scope per Section 8 | Flagged for v2 expansion |
| NIS2 Article 21(2)(e) (secure development, vulnerability handling) | SDLC controls outside v1 scope; CTL-002 (provenance) contributes partially | Outside v1 scope; covered by SSDLC frameworks |
| NIS2 Article 21(2)(g) (cyber hygiene, training) | Human factors out of scope per Section 8 | Flagged for v2 expansion |
| NIS2 Article 21(2)(h) (cryptography and encryption) | Foundational control assumed | NIST SP 800-53, BSI IT-Grundschutz |
| NIS2 Article 21(2)(i, j) (HR security, access control, MFA) | Foundational identity and access controls; CTL-001 depends on these being in place | Assumed to exist; identity provider frameworks |
| NIS2 Article 23 (incident reporting) | Reporting process is organizational; CTL-005 provides the underlying audit data | Outside v1 scope; covered by SOC and incident response frameworks |
| DORA Article 10 (detection) | First-class detection controls out of scope per Section 8 | Flagged for v2 expansion |
| DORA Article 11 (response and recovery); Article 12 (backup) | Foundational ICT continuity | Assumed to exist; ISO 22301 |
| DORA Article 17 to 18 (incident classification and reporting) | Reporting and classification process is organizational | Outside v1 scope |
| DORA Article 30 (mandatory contractual provisions) | Contractual, not technical | Outside v1 scope |
| GDPR Articles 13(2)(f), 14(2)(g), 15(1)(h) (transparency about automated decision-making logic) | Data subject communication is organizational; CTL-002 (provenance) contributes the logic substrate | Outside v1 scope; covered by privacy notice and data subject request processes |

For the gaps flagged as v2 expansion priorities (detection, supply chain, human factors), see Section 8. For the gaps that are intentional foundations of an existing security program, this framework assumes the foundations are in place and addresses only the agent-specific layer that sits on top.
