# 3. Regulatory Landscape
<!-- Length budget: 4-6 pages -->

Four EU instruments shape the security obligations of an enterprise AI agent deployment in the DACH region: the EU AI Act, the NIS2 Directive, DORA, and GDPR (specifically Article 22). They were drafted independently, on different timelines, and with different primary objectives. They overlap on operational security in ways that are not always obvious from the text. This section walks each instrument in turn at the depth a security practitioner needs to identify which articles apply to a given deployment and what they require operationally. Detailed control mappings are deferred to Sections 4 and 6; threat-level analysis to Section 5.

Verified citations, dates, and article numbers throughout this section are drawn from [`../frameworks/regulatory-facts.md`](../frameworks/regulatory-facts.md). Where legal interpretation is contested, I flag it; where the text is settled, I do not over-qualify.

## EU AI Act (Regulation (EU) 2024/1689)

The AI Act is the only one of the four instruments written specifically for AI systems. It was adopted on 13 June 2024, published in the Official Journal on 12 July 2024, and entered into force on 1 August 2024. Its substantive obligations apply on a staggered schedule.

| Application date | Provisions |
|---|---|
| 2 February 2025 | Prohibitions in Chapter II (e.g. social scoring, untargeted facial recognition scraping) and AI literacy obligations |
| 2 August 2025 | Governance provisions and obligations on general-purpose AI (GPAI) model providers (Chapter V) |
| 2 August 2026 | Most remaining provisions, including the Annex III high-risk obligations that affect typical enterprise agent deployments |
| 2 August 2027 | Article 6(1) high-risk systems (AI as safety components in products under Annex I sectoral law: medical devices, civil aviation, etc.) |

The Commission published a Digital Omnibus simplification proposal on 19 November 2025 that may extend the high-risk application timeline by up to 16 months pending availability of harmonised standards. This is a moving target; verify before relying on a specific date for compliance planning.

For agent security, the relevant articles cluster around risk management, data governance, oversight, and operational security:

| Article | Topic | Why it matters for agent security |
|---|---|---|
| Article 6 and Annex III | High-risk classification rules | Determines whether the deployment is high-risk and which obligations apply |
| Article 9 | Risk management system | Direct hook for threat modeling and control selection |
| Article 10 | Data and data governance | Training-data quality, bias mitigation, representativeness for high-risk systems |
| Article 12 | Record-keeping (logging) | Direct hook for audit and provenance controls (see CTL-005 in Section 6) |
| Article 13 | Transparency and information to deployers | Informs customer-facing security advisories |
| Article 14 | Human oversight | Direct hook for action-verification and approval-boundary controls (see CTL-003) |
| Article 15 | Accuracy, robustness, cybersecurity | The single most operationally relevant article; cited against most threats in Section 5 |
| Articles 16 to 22 | Provider obligations (QMS, technical documentation, automatically generated logs, corrective action, cooperation, authorised representatives) | Apply if the customer is the AI system provider |
| Article 26 | Deployer obligations for high-risk AI systems | Apply to most enterprise customers running purchased agents |
| Article 27 | Fundamental rights impact assessment | Required of public-sector deployers and certain private deployers |
| Article 50 | Transparency obligations for AI systems interacting with natural persons | Disclosure that the user is interacting with AI |
| Articles 53 to 55 | GPAI model provider obligations | Apply to model providers (OpenAI, Anthropic, Google, Mistral, Meta, etc.), not deployers |

The provider/deployer distinction matters operationally. A typical enterprise customer is a deployer of a purchased agent platform. Deployer obligations under Article 26 (use in line with provider instructions, monitoring, logging, human oversight, incident reporting) are the obligations that drive day-to-day operational security. Provider obligations under Articles 16 to 22 apply to the platform vendor; in practice, the customer inherits security properties from how well the provider implements them. If the customer builds the agent in-house on top of a foundation model, both sets of obligations may apply simultaneously.

**What this means for agent deployments**: The AI Act gives the framework its primary anchor. Article 9 (risk management) and Article 15 (cybersecurity, robustness, accuracy) are cited across the threat catalog in Section 5 because they make AI-specific operational security legally binding for the first time. Article 12 (logging) is the legal hook for audit controls that already exist as good engineering practice. Article 14 (human oversight) constrains how much autonomy an agent can have between approval points without violating the Act, which directly shapes the high-impact-action verification controls in Section 6. The August 2026 application date for Annex III obligations is the binding deadline for most enterprise deployments. The Article 6(1) date in August 2027 matters only for AI embedded as safety components in products covered by sectoral law (medical devices, civil aviation, automotive, etc.).

## NIS2 Directive (Directive (EU) 2022/2555)

NIS2 is the second-generation EU cybersecurity directive. It was adopted on 14 December 2022, entered into force on 16 January 2023, and member states were required to transpose it into national law by 17 October 2024. National measures became applicable from 18 October 2024 in member states that transposed on time. The original NIS Directive (Directive 2016/1148) was repealed on 18 October 2024.

NIS2 expanded the scope of the original directive substantially:

| Dimension | NIS1 | NIS2 |
|---|---|---|
| Sectors in scope | 7 | 18 (Annex I plus Annex II) |
| Estimated entities in scope | 10,000 to 15,000 across the EU | Approximately 160,000 (ENISA) |
| Entity classification | Operators of essential services / digital service providers | Essential entities / important entities |

The expansion catches enterprises that were previously out of NIS scope, including many that operate AI agents. Cloud computing service providers, data centre service providers, ICT service management (B2B), digital providers, and managed security services are explicitly named. Many DACH enterprises that did not previously identify as critical infrastructure now sit inside the directive's scope.

Three articles dominate the operational security analysis:

| Article | Topic |
|---|---|
| Article 21 | Cybersecurity risk-management measures: a 10-point list including risk analysis, incident handling, business continuity, supply chain security, vulnerability disclosure, basic cyber hygiene, encryption, access control, MFA, and security in network and information systems acquisition, development and maintenance |
| Article 23 | Reporting obligations: 24-hour early warning, 72-hour incident notification, one-month final report |
| Article 32 | Supervisory measures and penalties |

Article 21 is intentionally broad. It does not specify how to implement each measure; member states and competent authorities flesh that out through national law and guidance. This means Article 21 reads like a minimum expectation rather than a prescriptive control catalog. For agent security, the substantive content is in supply-chain security (Article 21(2)(d)), incident handling (Article 21(2)(b)), access control and MFA (Article 21(2)(i) and (j)), and encryption (Article 21(2)(h)).

### DACH transposition status

Transposition is uneven. As of early 2026:

| Country | Status | Note |
|---|---|---|
| Germany | Not yet transposed | NIS2UmsuCG (NIS-2-Umsetzungs- und Cybersicherheitsstärkungsgesetz) draft is in parliamentary process; the European Commission issued a reasoned opinion on 7 May 2025 for delayed transposition |
| Austria | Transposed | Verify current Austrian implementing law before relying on specific national obligations |
| Switzerland | Out of scope | Not an EU member; relevant only to Swiss entities providing services into the EU |

For Germany specifically, this is operationally awkward: the directive entered into force in 2023, transposition was due in October 2024, and as of this writing the implementing law has not been adopted. Enterprises preparing for NIS2 are working from the directive text and the draft transposition law concurrently, with the expectation that the German law will tighten or extend specific obligations. Verify the current state with qualified counsel before relying on this section for compliance decisions.

**What this means for agent deployments**: NIS2 supplies the general cybersecurity baseline that AI agents inherit by virtue of running inside an in-scope enterprise. It is not AI-specific. Article 21's 10-point list maps cleanly onto traditional security controls; the agent-specific overlay (prompt injection, authorization confusion, tool-chain abuse, etc.) sits on top of that baseline rather than replacing it. The supply-chain security obligation (Article 21(2)(d)) is the most relevant for agent deployments because it pulls foundation model providers, agent platform vendors, and tool integrations into the scope of the customer's NIS2 risk assessment. Incident reporting timelines under Article 23 are tight; agent-specific incidents (prompt-injection-driven exfiltration, authorization-confusion-driven actions) can trigger them just like traditional incidents.

## DORA (Regulation (EU) 2022/2554)

DORA is the EU's digital operational resilience regulation for the financial sector. It was adopted on 14 December 2022 (the same day as NIS2), entered into force on 16 January 2023, and applies from 17 January 2025. A companion directive (Directive (EU) 2022/2556) had a transposition deadline of 17 January 2025. Unlike NIS2, DORA is a regulation, so it applies directly without national transposition.

DORA is structured around five pillars:

| Pillar | Articles |
|---|---|
| ICT risk management | Articles 5 to 16 |
| ICT-related incident management, classification, reporting | Articles 17 to 23 |
| Digital operational resilience testing | Articles 24 to 27 |
| ICT third-party risk management | Articles 28 to 30 |
| Information and intelligence sharing | Article 45 |

For agent security in financial entities, the high-leverage articles are:

| Article | Topic |
|---|---|
| Article 6 | ICT risk management framework (the umbrella requirement) |
| Article 9 | Protection and prevention (security controls baseline) |
| Articles 17 and 18 | ICT incident classification and major-incident reporting |
| Article 28 | General principles for ICT third-party risk |
| Article 30 | Mandatory contractual provisions for ICT services supporting critical or important functions |

The third-party risk pillar deserves particular attention for agent deployments. Article 30 specifies contractual provisions that financial entities must include in agreements with ICT service providers supporting critical or important functions: rights to audit, exit strategies, security and incident notification obligations, sub-contracting restrictions, and assistance during incidents. Foundation model providers, agent platform vendors, and major tool integrations sit inside this scope when an agent supports a critical or important function.

The Commission designated the first 19 critical ICT third-party providers (CTPPs) on 18 November 2025, including AWS, Microsoft, Google Cloud, IBM, Bloomberg, LSEG, TCS, and Orange. CTPP designation triggers direct EU oversight under Articles 31 to 44, including the right of EU lead overseers to conduct on-site inspections at the provider. Foundation model providers are not currently on the list; that does not mean they cannot be added in subsequent rounds.

**What this means for agent deployments**: For financial entities, DORA's third-party risk obligations make the foundation model provider, the agent platform vendor, and major tool integrations into named, contractually constrained, regulator-visible elements of the deployment. This is the most operationally specific of the four instruments for agents in financial services. Articles 17 and 18 incident reporting overlap with NIS2 Article 23 reporting; the entity-specific question is which regulator gets the report first and whether a single submission discharges both obligations (this is jurisdiction-specific; verify with national authorities). Article 9's protection and prevention requirements map onto the same operational controls as the AI Act's Article 15 cybersecurity obligation, with finance-specific accent on resilience and continuity.

## GDPR Article 22 (Regulation (EU) 2016/679)

GDPR has applied since 25 May 2018. Most of its provisions are well-traveled by now. For agent security specifically, Article 22 is the article that matters and the only one I cover here in any depth.

Article 22(1) states:

> "The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her."

Article 22(2) specifies the conditions under which a solely automated decision is permitted:

| Basis | Reference |
|---|---|
| Necessary for entering into or performance of a contract between data subject and controller | Article 22(2)(a) |
| Authorised by Union or Member State law with suitable safeguards | Article 22(2)(b) |
| Based on the data subject's explicit consent | Article 22(2)(c) |

In cases (a) and (c), Article 22(3) requires the controller to implement suitable measures to safeguard the data subject's rights, at minimum: the right to obtain human intervention, to express their point of view, and to contest the decision.

The operationally critical word in Article 22(1) is "solely". An automated decision is in scope only if no meaningful human review takes place. The threshold for "meaningful" review is set by EDPB Guidelines on Automated Decision-Making (WP251rev.01): the human reviewer must have the authority and competence to override the decision. Rubber-stamp human approval that always confirms the algorithmic recommendation does not qualify. A reviewer who lacks the data, expertise, or organizational authority to disagree does not qualify either.

This is exactly where agentic AI creates new risk. An agent that "recommends" an action that is then "approved" by a human one-click reviewer is, in practice, making a solely automated decision dressed up as a human one. The Article 22 risk is not theoretical; supervisory authorities have shown willingness to look through the form to the substance.

**What this means for agent deployments**: Article 22 is the legal lever for the human-oversight design pattern that runs through Section 6 (specifically CTL-003: Action Verification at High-Impact Boundaries). The framework's position is that high-impact actions (financial transactions, hiring or termination, credit or lending, access to services with legal effects) require human approval that is meaningful, not nominal. The control library specifies what meaningful means operationally: independent context, override authority, sufficient time, and audit of overrides. Article 22 also limits how aggressive an agent can be in autonomy progression: every increment in autonomy reduces the share of decisions that get meaningful human review, and at some point the system crosses into "solely automated" territory. The crossing is not always obvious; it deserves explicit design and legal review.

## DACH-specific national rules

Two German national rules deserve mention because they intersect with agent deployments in specific sectors.

### BSI C5 Equivalence Regulation (C5-Gleichwertigkeitsverordnung, C5GleichwV)

The C5 Equivalence Regulation was published on 19 March 2025 (BGBl. 2025 I Nr. 91) with retroactive effect from 1 July 2024. Its statutory basis is § 393 Abs. 4 Satz 4 SGB V, introduced by the DigiG (22 March 2024). Scope: cloud computing services processing social or health data for healthcare providers, statutory health insurers, and their processors. Mechanism: it permits alternative certifications (ISO 27001 auf Basis IT-Grundschutz, SOC 2) as temporarily equivalent to a C5-Type-1 testat, for a maximum of two years, conditional on a documented gap-closure plan toward C5-Type-2. Relevance to agent security is narrow: it affects healthcare-sector cloud and AI deployments in Germany specifically.

### BSI IT-Grundschutz

IT-Grundschutz is the German national security baseline framework, maintained by the Bundesamt für Sicherheit in der Informationstechnik (BSI). Its annual IT-Grundschutz-Kompendium serves as a national reference catalog of building blocks (Bausteine), threats (Gefährdungen), and security requirements. The framework treats it as a translation aid alongside NIST SP 800-53 and ISO 27001 Annex A, not as a primary regulatory anchor.

**What this means for agent deployments**: The DACH-specific rules narrow the framework's relevance for two specific cases (German healthcare cloud; mappings to a German national baseline) without changing the primary EU-level analysis. Practitioners working in those contexts should treat the DACH section as a hook into more specialized guidance from BSI and the national supervisory authorities; it is not a substitute for that guidance.

## How the four instruments interact

The four instruments are layered, not parallel:

| Layer | Instrument | What it adds |
|---|---|---|
| AI-specific | EU AI Act | Risk classification, AI-specific obligations on data, oversight, accuracy, robustness, cybersecurity |
| Sectoral cybersecurity | NIS2 | Cybersecurity baseline for in-scope entities; supply chain and incident reporting |
| Sectoral cybersecurity (financial) | DORA | Operational resilience for financial entities; ICT third-party risk; CTPP regime |
| Data protection | GDPR Article 22 | Human oversight requirement for solely automated decisions affecting individuals |

A given deployment can sit inside two, three, or all four scopes simultaneously. A high-risk AI agent deployed by a German bank to make credit decisions on retail customers triggers all four: AI Act (high-risk classification under Annex III), NIS2 (banking is a NIS2 essential entity sector), DORA (banks are explicitly in scope), and GDPR Article 22 (credit decisions are solely automated decisions with legal or similarly significant effects). The framework's Section 4 maps where the four instruments converge on common controls, which is what makes integrated compliance tractable rather than four parallel projects.

The more general point: a security practitioner who understands the agent-specific threat model in Section 5 and applies the controls in Section 6 will satisfy a substantial portion of the operational obligations across all four instruments. The remainder is process, documentation, and governance work outside the operational security scope of this framework.
