# 3. Regulatory Landscape

This section presents the four EU regulations that shape the security requirements for enterprise AI agent deployments: the EU AI Act, the NIS2 Directive, the Digital Operational Resilience Act (DORA), and the General Data Protection Regulation (GDPR). It describes what each regulation requires that is specifically relevant to agent security, and how they overlap in practice.

The framework treats these four together because they overlap. A regulated DACH enterprise deploying an agent will frequently be subject to all four simultaneously. Treating them in isolation produces fragmented compliance work; treating them together surfaces where one common control can satisfy obligations across multiple regulations.

This section operates at the article level. Citations identify specific provisions. Practitioners verifying compliance should consult the official consolidated texts on EUR-Lex (linked in section 9) and obtain legal counsel where the answer affects organizational decisions.

## 3.1 EU AI Act (Regulation 2024/1689)

The EU AI Act establishes harmonised rules for AI systems placed on the market, put into service, or used in the European Union. It applies a risk-based framework with different obligations for AI systems classified as prohibited, high-risk, limited-risk, or minimal-risk.

For enterprise AI agent deployments, the most consequential classification is **high-risk**. Many enterprise agents will fall into this category, particularly those involved in employment decisions, access to essential services, law enforcement, or critical infrastructure. Practitioners should determine classification before applying the requirements below.

The articles most relevant to agent security:

| Article | Subject | Relevance to agent security |
|---|---|---|
| Article 9 | Risk management system | High-risk AI systems must have a risk management system that identifies, analyses, and addresses risks. For agents, this includes foreseeable misuse and adversarial manipulation. |
| Article 10 | Data and data governance | Training, validation, and testing data must meet quality criteria. For deployed agents using retrieval, data governance extends to retrieval source quality and integrity. |
| Article 12 | Record-keeping | High-risk AI systems must automatically record events during operation. This is the regulatory basis for end-to-end audit (CTL-005). |
| Article 13 | Transparency and provision of information | Users must be provided sufficient information to interpret system output. For agents, this constrains how decisions are presented and explained. |
| Article 14 | Human oversight | High-risk AI systems must be designed to enable effective oversight by natural persons during operation. This is the regulatory basis for action verification at high-impact boundaries (CTL-003). |
| Article 15 | Accuracy, robustness, and cybersecurity | High-risk AI systems must achieve appropriate levels of accuracy, robustness, and cybersecurity throughout their lifecycle. Cybersecurity requirements include resilience against attempts by unauthorized third parties to alter use, outputs, or performance. This is the regulatory basis for most of the framework's threat-driven controls. |

The Act entered into force on 1 August 2024. Application is phased: prohibitions on prohibited AI systems apply from February 2025; obligations for general-purpose AI models from August 2025; obligations for high-risk AI systems from August 2026, with some provisions extending to August 2027.

For agent deployments, the most operationally relevant date is August 2026, when most high-risk system obligations begin to apply.

## 3.2 NIS2 Directive (Directive 2022/2555)

NIS2 establishes a common cybersecurity regulatory framework across the European Union, applicable to essential and important entities in sectors of high criticality including banking, financial market infrastructure, energy, transport, health, digital infrastructure, public administration, and several others.

Unlike the AI Act, NIS2 is a directive rather than a regulation: Member States transpose it into national law, and specific obligations may vary slightly across jurisdictions. Most Member States completed transposition by late 2024 to early 2025, though some remain incomplete as of 2026.

The article most relevant to agent security:

| Article | Subject | Relevance to agent security |
|---|---|---|
| Article 21 | Cybersecurity risk-management measures | Essential and important entities must take appropriate and proportionate technical, operational, and organizational measures to manage cybersecurity risks. The article enumerates ten specific measure categories including risk analysis policies, incident handling, business continuity, supply chain security, security in network and information systems acquisition and maintenance, policies on cryptography, human resources security, access control policies, and use of multi-factor authentication and secured communications. |
| Article 23 | Reporting obligations | Significant incidents must be reported to the competent authority. For agent deployments, this includes incidents arising from agent compromise or misuse. |

Article 21 is broad. For agent deployments, the relevant operational interpretation is that all ten measure categories must address the agent-specific risks introduced by autonomous AI systems with action capability. The framework's threat catalog (AGT-001 through AGT-010) and control library (CTL-001 through CTL-005) are positioned as the agent-specific extensions to existing NIS2 compliance programs.

## 3.3 Digital Operational Resilience Act (DORA, Regulation 2022/2554)

DORA establishes a uniform regulatory framework for the digital operational resilience of financial entities in the European Union. It applies to a broad range of financial entities including credit institutions, payment service providers, investment firms, insurance and reinsurance undertakings, crypto-asset service providers, and others.

DORA applies from 17 January 2025. For financial entities deploying AI agents, DORA is the most operationally specific of the four regulations.

The articles most relevant to agent security:

| Article | Subject | Relevance to agent security |
|---|---|---|
| Article 6 | ICT risk management framework | Financial entities must have a sound, comprehensive, and well-documented ICT risk management framework including strategies, policies, procedures, ICT protocols, and tools necessary to protect information assets. For agents, this framework must explicitly address agent-mediated ICT risks. |
| Article 7 | ICT systems, protocols, and tools | The technical requirements that ICT systems must meet, including resilience, redundancy, capacity, and information security. |
| Article 8 | Identification | Financial entities must identify, classify, and adequately document ICT-supported business functions, information assets, and ICT assets. Agents and the systems they integrate with fall in scope. |
| Article 9 | Protection and prevention | Specific protection requirements including access management, identity management, encryption, and configuration management. The basis for authorization and identity controls (CTL-001) in financial contexts. |
| Article 12 | Major ICT-related incidents | Financial entities must classify and report major ICT-related incidents. For agents, this includes incidents arising from agent-mediated harm. |
| Articles 28 to 30 | ICT third-party risk | Where AI agents integrate third-party services or AI providers, third-party risk management requirements apply. |

DORA is the most prescriptive of the four regulations regarding specific operational requirements. For financial entities, DORA effectively raises the operational baseline that the framework's controls must meet.

## 3.4 General Data Protection Regulation (GDPR, Regulation 2016/679)

The GDPR governs the processing of personal data of individuals in the European Union. It applies regardless of where the data controller or processor is established, if the processing relates to offering goods or services to data subjects in the EU or monitoring their behavior.

For agent deployments, GDPR applies whenever the agent processes personal data, which in most enterprise contexts is unavoidable. The articles most relevant to agent security:

| Article | Subject | Relevance to agent security |
|---|---|---|
| Article 5 | Principles relating to processing of personal data | Personal data must be processed lawfully, fairly, transparently, for specified purposes, in minimised quantities, accurately, and with integrity and confidentiality. Several principles are particularly relevant: purpose limitation (5(1)(b)), data minimisation (5(1)(c)), accuracy (5(1)(d)), and integrity and confidentiality (5(1)(f)). |
| Article 22 | Automated individual decision-making | Data subjects have the right not to be subject to decisions based solely on automated processing producing legal or similarly significant effects. For agents making consequential decisions about data subjects, this right constrains permissible deployment. |
| Article 25 | Data protection by design and by default | Data protection must be embedded in system design from the outset, with default settings that minimize processing. For agents, this affects retrieval scope, output filtering, and persistence design. |
| Article 30 | Records of processing activities | Controllers and processors must maintain records of processing activities. For agents, processing records must capture agent-mediated processing. |
| Article 32 | Security of processing | Appropriate technical and organizational measures including pseudonymisation, encryption, ensuring confidentiality and integrity, restoration capability, and regular testing. The article is broad and applies wherever personal data is processed, including by agents. |
| Article 35 | Data protection impact assessment | Where processing is likely to result in high risk to the rights of natural persons, a DPIA is required. Many agent deployments will trigger this requirement. |

The GDPR has been in force longer than the other three regulations and has the most developed body of case law, regulatory guidance, and supervisory authority enforcement. Practitioners should expect the GDPR provisions to be the most rigorously enforced in the short term.

## 3.5 How the regulations overlap

The four regulations were drafted independently and have different primary subjects, but they overlap substantially when applied to enterprise agent deployments.

| Overlap area | What it means in practice |
|---|---|
| Cybersecurity requirements | EU AI Act Article 15, NIS2 Article 21, DORA Articles 6 to 9, and GDPR Article 32 all establish cybersecurity obligations. They are not identical but are largely consistent. A single set of well-designed controls can satisfy all four simultaneously. |
| Risk management | EU AI Act Article 9, NIS2 Article 21, DORA Articles 6 to 8, and GDPR Article 25 all require structured risk management. Again, consistent in principle though differing in detail. |
| Incident reporting | EU AI Act Article 12, NIS2 Article 23, DORA Article 12, and GDPR Article 33 all impose incident-related obligations. Definitions of reportable incidents differ; reporting timelines differ; supervisory authorities differ. This is the area of greatest practical complexity. |
| Human oversight | EU AI Act Article 14 and GDPR Article 22 both constrain fully automated decision-making in different ways. EU AI Act focuses on system design for oversight; GDPR focuses on the data subject's right to human intervention. |
| Record-keeping and audit | EU AI Act Article 12, DORA Article 12, GDPR Article 30, and NIS2 (implicit in incident reporting) all require records. The records serve different purposes but overlap in content. |

The pragmatic implication is that organizations subject to multiple of these regulations should design controls once and document how they satisfy each regulation, rather than implementing separate compliance programs for each. The crosswalk in section 4 supports this approach.

## 3.6 Sectoral and national variations

Beyond the four regulations addressed here, additional requirements apply by sector or jurisdiction. A non-exhaustive list:

| Source | Relevance |
|---|---|
| BSI IT-Grundschutz (Germany) | German federal IT security standard; directly applicable to public sector and federally regulated entities; widely adopted in private sector |
| BaFin guidance (Germany) | Financial supervisory authority guidance applicable to BaFin-supervised institutions; layers on top of DORA |
| Sectoral cybersecurity acts in transposition | Some Member States have implemented NIS2 with sector-specific overlays |
| ePrivacy Directive and successor | Specific to electronic communications; relevant where agents interact with such communications |
| Medical Device Regulation (MDR) | Applies where agents are part of medical devices |

Full treatment of sectoral and national variations is out of scope for v1 of this framework. Practitioners operating in regulated sectors should expect their compliance work to include sectoral requirements in addition to the four addressed here.

## 3.7 What this section does not address

This section names the regulations and identifies the articles most relevant to agent security. It does not:

- Provide compliance determinations for specific deployments
- Replace legal counsel or formal compliance assessment
- Cover all provisions of each regulation
- Address the Member State transposition variations of NIS2
- Address regulatory developments after the framework's v1 publication date

The framework's regulatory mapping is current as of the v1 publication date. Regulations evolve; technical standards under DORA continue to be issued; AI Act guidance continues to develop. Practitioners should treat the regulatory landscape as moving and consult primary sources for current authoritative text.
