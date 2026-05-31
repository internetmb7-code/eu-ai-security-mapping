# EU AI Security Mapping

A practitioner's mapping of EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments.

> **Status:** scaffolding. No content drafted yet.
>
> **Disclaimer:** This document is a guideline based on the author's interpretation of public regulatory texts and operational security experience. It is **not legal advice**.

---

## Table of Contents

1. [Executive Briefing](#1-executive-briefing)
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

## 1. Executive Briefing

<!-- Source: docs/sections/01-executive-summary.md (4-6 pages) -->

This section is written for security leaders and CISOs who need to make decisions about AI agent deployments under EU regulatory pressure. It is longer than a typical executive summary because the decisions are not simple. Readers wanting a two-paragraph version can read the first two paragraphs and the overview table; everything else builds on that foundation.

### 1.1 The bottom line

If your organization is deploying AI agents (LLM-based, tool-using systems that take multi-step actions on behalf of users), you are accepting a class of risk that your current security program does not fully address. Most enterprise security programs are built around the assumption that systems act with their own service identity and that authorization decisions are made at fixed boundaries. AI agents violate both assumptions. They act on behalf of users (so authorization must propagate through them), and they make autonomous decisions between human approval points (so the authorization boundary moves with the agent, not with the architecture).

This framework is a practitioner's view of what to do about that, mapped to the EU regulations you are now subject to or will be soon. It is not legal advice; it is operational guidance grounded in regulatory text. The framework's central claim is simple: the agent-specific layer of your security program needs five technical controls to be defensible under EU AI Act, NIS2, DORA, and GDPR Article 22. None of the five replaces existing security infrastructure; all five extend it.

### 1.2 The five top exposures, in plain language

These are the patterns I see consistently in enterprise agent deployments. They are not the framework's full threat catalog (Section 5 has all ten); they are the ones a CISO will encounter first.

| Top exposure | What it actually means | What addresses it (in priority order) | Effort to baseline | What regulators care about |
|---|---|---|---|---|
| Agent over-privilege | Your agent runs as a service account with broad rights and acts with those rights regardless of which user is asking | CTL-001 (identity propagation), CTL-003 (action verification at high-impact boundaries) | High; structural change to identity architecture | AI Act Art 14 (oversight), GDPR Art 22 (automated decisions), Art 32 (security of processing), NIS2 Art 21 (access control) |
| Content-as-instruction (prompt injection) | Untrusted text the agent reads (emails, web pages, documents, tool outputs) hijacks its behavior because the agent cannot reliably distinguish content from instruction | CTL-002 (provenance), CTL-003 (verification), CTL-004 (output filtering as defense-in-depth) | Medium; pattern-based, not architectural | AI Act Art 15 (cybersecurity, robustness), GDPR Art 32 |
| Authorization confusion (the deputy problem) | Your agent acts on behalf of users incorrectly: serves data from one user to another, or acts with privileges the requesting user does not have | CTL-001 (the structural fix), CTL-004 (output filtering as defense-in-depth) | High; structural | GDPR Art 5(1)(f) (integrity, confidentiality), Art 22, Art 32 |
| Audit incompleteness | When something goes wrong, you cannot reconstruct what the agent did, why it did it, or who is accountable | CTL-005 (end-to-end audit) | Medium; tooling investment | AI Act Art 12 (record-keeping), NIS2 Art 23 (incident reporting), DORA Art 17 (incident management), GDPR Art 5(2) (accountability) |
| Decision opacity | You cannot explain why the agent made a specific decision; this becomes a regulatory problem the moment a data subject contests one | CTL-002 (provenance), CTL-005 (audit) | Hard; partially solvable in current architectures | GDPR Art 22(3) (right to explanation), AI Act Art 13 (transparency to deployers) |

Two clarifications worth flagging up front:

| Clarification | Detail |
|---|---|
| This is curated, not exhaustive | Section 5 documents ten threat exemplars across six attack surfaces. The five exposures above are the patterns most enterprises will hit first; they are not a complete threat model |
| "What addresses it" lists controls in priority order | The control listed first is the structural fix; the others are defense-in-depth. Skipping the first and relying on the others is the failure mode I see most often |

**Where these come from**: The five exposures are curated from the framework's ten threat exemplars in Section 5. The exemplars are organized by attack surface (input, model, tool-use, output, memory, audit) and tagged with MITRE ATLAS techniques where applicable. They overlap substantially with the OWASP Top 10 for LLM Applications and draw on academic work on indirect prompt injection (Greshake et al., 2023), but the structural claim of the framework, that agent threats are bounded by a finite set of attack surfaces, is the framework's own contribution. Section 5 documents the methodology for discovering deployment-specific threats that may not match the named exemplars.

### 1.3 What to tell your board

Three sentences that convey the situation accurately without overclaiming or underclaiming:

| Audience signal | Talking point |
|---|---|
| The risk is real and measurable | "We are deploying AI agents that take actions in our systems. Our existing security controls were designed for systems that act with their own identity; agents act on behalf of users. This is a structural gap, not a tooling gap." |
| The regulatory pressure is concrete | "EU AI Act, NIS2, DORA, and GDPR all impose obligations that intersect with how we deploy agents. Most of these obligations are already in force; the AI Act high-risk obligations apply from August 2026. Our agent deployments are within scope of at least three of these regulations" |
| The work is bounded and technical | "There are five technical controls that, together, bring our agent deployments to defensible. We can build a phased plan to implement them. The work is bounded; we know what done looks like" |

The corresponding things not to say to your board, because they are either not true or unhelpfully alarming:

| Do not say | Why not |
|---|---|
| "AI agents are fundamentally insecure" | Not true; they are securable with specific controls. The blanket statement is the kind of claim that gets challenged and undermines the rest of the briefing |
| "We need to halt all AI agent deployments until we are compliant" | Almost never the right answer; staged deployment with the right controls is achievable and most regulations do not require pre-deployment certification for non-high-risk uses |
| "This is just like cloud security; we have done this before" | Wrong analogy; the deputy problem and content-as-instruction are genuinely new. Underclaiming undermines the case for investment |

### 1.4 What to do, in priority order

The framework has five v1 controls (CTL-001 through CTL-005). They are not equally urgent. The priority ordering below is based on three factors: structural dependency (some controls only work if others are in place), regulatory exposure (some obligations have current enforcement, others phase in), and practical leverage (some controls produce evidence that supports compliance for multiple obligations).

| Phase | Control | Why this priority | Criteria for moving to next phase |
|---|---|---|---|
| 1 | CTL-001 (Identity and authorization context propagation) | Structural foundation; without it, everything else either does not work or works on a weaker basis. This is also the control most enterprises fail on day one because their agents run as service accounts | Every agent action in production is associated with a verified user identity that propagates through downstream calls. Audit (CTL-005) shows this is true for at least 95% of actions over a 30-day window |
| 2 | CTL-005 (End-to-end audit and accountability) | Without audit, you cannot tell whether the other controls are working. CTL-005 also produces the evidence base for AI Act Art 12, NIS2 Art 23, DORA Art 17, GDPR Art 5(2), so its regulatory leverage is the highest of the five | Audit pipeline ingests agent events into the SIEM with sufficient detail to reconstruct any agent action. Retention period is set against the longest reporting cycle the organization is subject to (typically NIS2 Art 23 one-month cycle or DORA equivalent) |
| 3 | CTL-003 (Action verification at high-impact boundaries) | The structural mechanism for AI Act Art 14 (human oversight) and GDPR Art 22 (the human-review condition that takes a system out of "solely automated"). Cannot be effective without CTL-001 and CTL-005 in place | Approval queue is operational; thresholds are calibrated against actual operator override patterns; CTL-005 audit shows operator decisions are recorded with sufficient context for compliance |
| 4 | CTL-002 (Tool-output and context provenance) | Mitigates content-as-instruction (prompt injection). Less urgent than the first three because the worst impact of prompt injection (taking unauthorized actions) is bounded by CTL-001 and CTL-003 if those are in place | Provenance metadata is attached to content at ingest; agents distinguish content from instruction at every boundary; audit (CTL-005) shows no policy violations from injected content over a 30-day window |
| 5 | CTL-004 (Authorization-aware output filtering) | Defense-in-depth for the deputy problem and exfiltration; secondary to CTL-001 because if CTL-001 is correct, fewer cases reach CTL-004 | Pre-retrieval filtering is the primary mechanism (data layer enforces per-user authorization); post-retrieval filtering is a defense-in-depth layer for content classes where pre-retrieval cannot be enforced |

The criteria column matters as much as the ordering. Moving from one phase to the next without meeting the criteria is the failure mode that produces non-defensible deployments. Section 7 expands on the rollout patterns and the signals that indicate you should not move forward.

### 1.5 What this is going to cost

I am not going to give you a euro figure; that depends on your existing infrastructure, the scale of your agent deployment, and choices you have not yet made. I can tell you what categories of investment are involved.

| Investment category | Typical magnitude | Notes |
|---|---|---|
| Identity infrastructure changes for CTL-001 | Significant if you do not already have OAuth 2.0 token exchange or equivalent in production; modest if you do | The pattern of using a service account for the agent and re-authorizing per call is the most common starting point and the most expensive to migrate from |
| SIEM ingest capacity for CTL-005 | Moderate; agent audit events are higher cardinality than typical application logs | Underestimating this is common; budget for substantially higher per-user log volume than equivalent non-agent applications |
| Approval queue tooling for CTL-003 | Modest if you have existing workflow infrastructure (ServiceNow, Jira Service Management, custom workflow); higher if you are building from scratch | The expensive part is not the tooling; it is calibrating thresholds and training operators |
| Data layer authorization for CTL-004 | Highly variable; depends on how much of your data already has per-user authorization at the data layer | If your data lives behind systems that enforce per-user authorization (most modern SaaS, well-architected internal systems), this is mostly configuration. If your data lives in shared corpora (document stores, vector indexes without per-user metadata), this is structural |
| Provenance tooling for CTL-002 | Modest; primarily a runtime configuration and content-handling discipline | The cost here is not technical; it is operational discipline in how content enters the agent runtime |

The honest framing for budget conversations: the work is bounded and largely consists of extending what you already have, not buying new categories of tooling. The exception is identity infrastructure if you do not already have user-context propagation in production; that is a real architectural investment. Everything else is incremental.

### 1.6 What this framework will not do for you

I want to be explicit about the limits of this document, because over-reliance on a framework like this is itself a risk.

| The framework does not | What you still need |
|---|---|
| Address governance, organizational change, or culture | A separate program for AI risk governance, ethics review, and operator training |
| Cover detection and response controls (SIEM rules, anomaly detection on agent behavior) | Your existing SOC, augmented with agent-specific detection content; this is a v2 framework priority |
| Cover supply chain controls (model provenance, prompt template integrity) | Vendor risk management for your AI providers and your agent platform; this is a v2 framework priority |
| Cover regulatory obligations that are organizational (AI Act Art 17 QMS, Art 27 FRIA, contractual provisions under DORA Art 30) | Your compliance program; this framework is the technical layer underneath it |
| Constitute compliance certification | Validation by qualified counsel, your DPO, and the relevant supervisory authority before relying on this for compliance decisions |

The framework's contribution is the technical agent-specific layer. It is necessary but not sufficient.

### 1.7 How to read the rest of this document

The remaining sections are organized for two different ways of using the framework:

| If you want to | Read |
|---|---|
| Understand the regulatory landscape for agent deployments | Section 2 (scope and disclaimers), then Section 3 (regulatory landscape) |
| Find the right controls for a specific regulatory requirement | Section 4 (common-control crosswalk) |
| Understand the threat model in depth | Section 5 (threat patterns and exemplars) |
| Implement the v1 controls | Section 6 (control specifications) and Section 7 (implementation considerations) |
| Understand what the framework does not cover | Section 8 (gaps and open problems) |

A practitioner deploying agents in a regulated DACH enterprise should read Section 1 (this section) and Section 7 (implementation considerations) first. The other sections become useful when specific questions arise.

A regulator or auditor evaluating an agent deployment against the framework should read Sections 2, 3, 4, 5, 6, and 8. Sections 1 and 7 are practitioner-oriented; they are not the framework's primary content for compliance evaluation.

## 2. Scope and Disclaimer

<!-- Source: docs/sections/02-scope-disclaimer.md (1 page) -->

### What this framework addresses

This framework addresses the security of enterprise AI agent deployments under EU regulation. It focuses on the intersection of four named regulations (the EU AI Act, NIS2, DORA, and GDPR) and the security-relevant operational concerns specific to agentic AI systems. Where these concerns overlap with general information security, the framework defers to established practice. The contribution is in the agent-specific layer that existing security frameworks do not cover.

### What counts as an agent

The framework's claims apply to systems meeting all four of the following criteria:

| Criterion | Description |
|---|---|
| 1. Natural language instruction | The system accepts instructions in natural language as its primary control interface |
| 2. Autonomous tool selection | The system decides which tools or actions to invoke without human approval at each step |
| 3. Real-world effect | The system executes those actions against external systems with effect beyond the model's own context |
| 4. Multi-step operation | The system operates over multiple steps within a single workflow |

This definition is deliberately narrow. It distinguishes agents from related systems that share some characteristics but not all.

#### In scope

| System type | Examples |
|---|---|
| Workflow automation agents | Agents creating, modifying, or routing enterprise records autonomously |
| Customer-facing agents with action authority | Agents that issue refunds, file tickets, update accounts |
| Developer copilots with execution access | Agents with shell or repository write access |
| Multi-agent systems with delegation | Orchestrator agents that delegate to sub-agents across workflows |
| Autonomous research and analysis agents | Agents that retrieve, summarize, and act on findings |

#### Out of scope

| System type | Reason for exclusion |
|---|---|
| Single-shot LLM calls (chat without tools) | No autonomous action; covered by general content-security practice |
| Retrieval-augmented generation without action capability | Read-only; covered by data-access controls |
| Classifier or recommendation models | Adversarial ML literature and MITRE ATLAS apply directly |
| Workflow automation with AI-assisted steps and human approval at each action | Human-in-the-loop addresses most agent-specific risks |

Organizations operating systems outside these criteria may still find the threat patterns useful, but the framework's specific claims about controls and regulatory mapping are calibrated to in-scope systems.

### Audience

The primary audience is CISOs and security program leads responsible for AI deployments in regulated enterprises, particularly in the DACH region. The framework assumes the reader operates within an established security program (typically based on NIST SP 800-53, ISO/IEC 27001, BSI grundschutz, or equivalent) and is integrating AI-specific concerns into that program.

The secondary audience is enterprise security architects designing agent deployments, and compliance or regulatory leads navigating the intersection of AI security and EU regulation.

Readers who are new to AI security generally, or who do not operate within an existing security program, will find the framework dense and presupposing. The framework does not teach foundational security concepts; it builds on them.

### Disclaimer

This framework is a guideline. It is not legal advice. It reflects the author's interpretation of public regulatory texts, the author's operational experience, and current public research on agent security. None of these are substitutes for qualified legal counsel, formal compliance assessment, or organizational risk management decisions.

Readers should treat the framework as a structured starting point for their own analysis, not as an authoritative determination of compliance or sufficiency. Where the framework cites specific regulatory articles, readers verifying compliance should consult the official consolidated texts on EUR-Lex and seek legal counsel where the answer matters.

The framework is offered without warranty. The author and contributors are not responsible for outcomes arising from its application.

### Author affiliation and independence

The author works at ServiceNow. The framework is independent practitioner work. No ServiceNow products, services, or proprietary information are referenced in the threat catalog or control library. No ServiceNow competitor is referenced either.

The framework is designed to accept contributed vendor-specific control mappings under the contribution interface described in CONTRIBUTING.md. If a ServiceNow mapping is submitted, the author will recuse from its review. An independent reviewer will be arranged at submission time. The recusal policy applies specifically to ServiceNow content; the author retains responsibility for the framework's threat catalog, control library, and methodology.

This separation is structural, not cosmetic. The framework's threat and control content exists independently of any vendor's product capabilities.

### Vendor mapping disclaimer

Vendor mappings, where they exist in `data/vendor-mappings/`, are contributor-attested representations of how specific vendor products implement framework controls. They are not framework-verified. Readers evaluating a specific vendor product against the framework should verify mapping claims against current vendor documentation and the vendor's own attestations.

As of v1, no vendor mappings have been contributed.

## 3. Regulatory Landscape

<!-- Source: docs/sections/03-regulatory-landscape.md (4-6 pages) -->

This section presents the four EU regulations that shape the security requirements for enterprise AI agent deployments: the EU AI Act, the NIS2 Directive, the Digital Operational Resilience Act (DORA), and the General Data Protection Regulation (GDPR). It describes what each regulation requires that is specifically relevant to agent security, and how they overlap in practice.

The framework treats these four together because they overlap. A regulated DACH enterprise deploying an agent will frequently be subject to all four simultaneously. Treating them in isolation produces fragmented compliance work; treating them together surfaces where one common control can satisfy obligations across multiple regulations.

This section operates at the article level. Citations identify specific provisions. Practitioners verifying compliance should consult the official consolidated texts on EUR-Lex (linked in section 9) and obtain legal counsel where the answer affects organizational decisions.

### 3.1 EU AI Act (Regulation 2024/1689)

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

### 3.2 NIS2 Directive (Directive 2022/2555)

NIS2 establishes a common cybersecurity regulatory framework across the European Union, applicable to essential and important entities in sectors of high criticality including banking, financial market infrastructure, energy, transport, health, digital infrastructure, public administration, and several others.

Unlike the AI Act, NIS2 is a directive rather than a regulation: Member States transpose it into national law, and specific obligations may vary slightly across jurisdictions. Most Member States completed transposition by late 2024 to early 2025, though some remain incomplete as of 2026.

The article most relevant to agent security:

| Article | Subject | Relevance to agent security |
|---|---|---|
| Article 21 | Cybersecurity risk-management measures | Essential and important entities must take appropriate and proportionate technical, operational, and organizational measures to manage cybersecurity risks. The article enumerates ten specific measure categories including risk analysis policies, incident handling, business continuity, supply chain security, security in network and information systems acquisition and maintenance, policies on cryptography, human resources security, access control policies, and use of multi-factor authentication and secured communications. |
| Article 23 | Reporting obligations | Significant incidents must be reported to the competent authority. For agent deployments, this includes incidents arising from agent compromise or misuse. |

Article 21 is broad. For agent deployments, the relevant operational interpretation is that all ten measure categories must address the agent-specific risks introduced by autonomous AI systems with action capability. The framework's threat catalog (AGT-001 through AGT-010) and control library (CTL-001 through CTL-005) are positioned as the agent-specific extensions to existing NIS2 compliance programs.

### 3.3 Digital Operational Resilience Act (DORA, Regulation 2022/2554)

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

### 3.4 General Data Protection Regulation (GDPR, Regulation 2016/679)

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

### 3.5 How the regulations overlap

The four regulations were drafted independently and have different primary subjects, but they overlap substantially when applied to enterprise agent deployments.

| Overlap area | What it means in practice |
|---|---|
| Cybersecurity requirements | EU AI Act Article 15, NIS2 Article 21, DORA Articles 6 to 9, and GDPR Article 32 all establish cybersecurity obligations. They are not identical but are largely consistent. A single set of well-designed controls can satisfy all four simultaneously. |
| Risk management | EU AI Act Article 9, NIS2 Article 21, DORA Articles 6 to 8, and GDPR Article 25 all require structured risk management. Again, consistent in principle though differing in detail. |
| Incident reporting | EU AI Act Article 12, NIS2 Article 23, DORA Article 12, and GDPR Article 33 all impose incident-related obligations. Definitions of reportable incidents differ; reporting timelines differ; supervisory authorities differ. This is the area of greatest practical complexity. |
| Human oversight | EU AI Act Article 14 and GDPR Article 22 both constrain fully automated decision-making in different ways. EU AI Act focuses on system design for oversight; GDPR focuses on the data subject's right to human intervention. |
| Record-keeping and audit | EU AI Act Article 12, DORA Article 12, GDPR Article 30, and NIS2 (implicit in incident reporting) all require records. The records serve different purposes but overlap in content. |

The pragmatic implication is that organizations subject to multiple of these regulations should design controls once and document how they satisfy each regulation, rather than implementing separate compliance programs for each. The crosswalk in section 4 supports this approach.

### 3.6 Sectoral and national variations

Beyond the four regulations addressed here, additional requirements apply by sector or jurisdiction. A non-exhaustive list:

| Source | Relevance |
|---|---|
| BSI IT-Grundschutz (Germany) | German federal IT security standard; directly applicable to public sector and federally regulated entities; widely adopted in private sector |
| BaFin guidance (Germany) | Financial supervisory authority guidance applicable to BaFin-supervised institutions; layers on top of DORA |
| Sectoral cybersecurity acts in transposition | Some Member States have implemented NIS2 with sector-specific overlays |
| ePrivacy Directive and successor | Specific to electronic communications; relevant where agents interact with such communications |
| Medical Device Regulation (MDR) | Applies where agents are part of medical devices |

Full treatment of sectoral and national variations is out of scope for v1 of this framework. Practitioners operating in regulated sectors should expect their compliance work to include sectoral requirements in addition to the four addressed here.

### 3.7 What this section does not address

This section names the regulations and identifies the articles most relevant to agent security. It does not:

- Provide compliance determinations for specific deployments
- Replace legal counsel or formal compliance assessment
- Cover all provisions of each regulation
- Address the Member State transposition variations of NIS2
- Address regulatory developments after the framework's v1 publication date

The framework's regulatory mapping is current as of the v1 publication date. Regulations evolve; technical standards under DORA continue to be issued; AI Act guidance continues to develop. Practitioners should treat the regulatory landscape as moving and consult primary sources for current authoritative text.

## 4. Common-Control Crosswalk

<!-- Source: docs/sections/04-crosswalk.md (3-4 pages) -->

This section presents the consolidated view of how the four EU regulations addressed by the framework map to the v1 controls. It is the practitioner-facing summary that supports two common questions:

- "We are subject to regulation X; which controls in this framework address its requirements?"
- "We have implemented control Y; which regulatory requirements does it help us satisfy?"

The crosswalk is summary-level. Specific article-level citations and the per-control regulatory basis live in the threat entries (section 5) and the control entries (section 6). Section 4 is the entry point; sections 5 and 6 are the detailed reference.

### 4.1 Methodology

The crosswalk is constructed from the regulatory hooks documented in each threat entry (AGT-001 through AGT-010) and the regulatory basis documented in each control entry (CTL-001 through CTL-005). These hooks are practitioner-attested interpretations of which regulatory provisions a given control or threat addresses. They are defensible but not authoritative.

Two views of the same underlying data are presented:

| View | What it shows | When to use it |
|---|---|---|
| Direct view | Regulation to control mappings, organized by regulation | Compliance-oriented work; quick reference for which controls support which regulatory provisions |
| Reasoned view | Regulation to threat to control chain, organized by regulation | Defensive-reasoning work; explains *why* each control satisfies the regulation by identifying the threat pattern it addresses |

The direct view is faster. The reasoned view is more defensible when challenged by an auditor or regulator. Practitioners should be comfortable with both.

### 4.2 Direct view: which controls support which regulations

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

### 4.3 Reasoned view: regulation to threat to control

The reasoned view explains why each control addresses the regulatory requirement by identifying the threat pattern the regulation implicitly requires defense against. This view is defensible when an auditor or regulator asks "How does this control satisfy the requirement?"

Four reasoned chains are presented as worked examples. Practitioners can construct additional chains for any of the regulatory provisions in the direct view above using the same pattern.

#### Chain 1: EU AI Act Article 15 (Cybersecurity)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 15 requires high-risk AI systems to achieve appropriate levels of accuracy, robustness, and cybersecurity, including resilience against attempts by unauthorised third parties to alter use, outputs, or performance. |
| Threat patterns implied | The article implicitly requires defense against agent-specific threats including indirect adversarial input (AGT-001), authorisation manipulation (AGT-002), tool-chain abuse (AGT-003), and goal subversion (AGT-009). These are the "alteration attempts" the article addresses for agent systems specifically. |
| Controls that address those threats | CTL-002 (tool-output provenance) addresses AGT-001. CTL-001 (identity propagation) addresses AGT-002. CTL-003 (action verification) addresses AGT-003 and AGT-009. CTL-005 (audit) supports detection across all. |
| Why this combination satisfies the article | The combination provides the resilience the article requires by preventing, detecting, and enabling response to the specific threats that constitute "alteration attempts" in the agent context. No single control is sufficient; the combination is. |

#### Chain 2: DORA Article 9 (Protection and prevention)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 9 requires financial entities to implement specific protection measures including access management, identity management, encryption, and configuration management. |
| Threat patterns implied | The article implicitly requires defense against authorisation decoupling (AGT-002) and data exfiltration through legitimate channels (AGT-004), among others. These are the access and identity threats specifically relevant to agent deployments. |
| Controls that address those threats | CTL-001 (identity and authorisation context propagation) directly satisfies the identity management requirement for agents. CTL-004 (authorisation-aware output filtering) addresses the data protection dimension. |
| Why this combination satisfies the article | CTL-001 brings user-level identity into the agent runtime in a way that traditional service identity does not. CTL-004 closes the output gap that traditional access management does not see. Together they extend the protection requirements of Article 9 to the agent context. |

#### Chain 3: GDPR Article 22 (Automated decision-making)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 22(1) gives data subjects the right not to be subject to decisions based solely on automated processing producing legal or similarly significant effects. Where such processing occurs, Article 22(3) requires the controller to implement suitable measures including the right to obtain human intervention. |
| Threat patterns implied | The article implicitly requires that automated agent decisions affecting data subjects can be subject to human intervention, which means the system must recognise when such a decision is being taken and pause for review. |
| Controls that address those threats | CTL-003 (action verification at high-impact boundaries) is the structural mechanism by which agent decisions can be paused for human review. CTL-005 (audit and accountability) supports the right by enabling reconstruction of how a decision was reached. |
| Why this combination satisfies the article | CTL-003 provides the procedural mechanism for human intervention. CTL-005 provides the basis for the data subject to meaningfully exercise that right by understanding what decision was made and why. Without both, Article 22 cannot be operationalised for agents. |

#### Chain 4: NIS2 Article 21 (Cybersecurity risk-management measures)

| Layer | Content |
|---|---|
| Regulatory requirement | Article 21 requires essential and important entities to take appropriate and proportionate measures across ten enumerated categories including risk analysis, incident handling, business continuity, supply chain security, access control, and others. |
| Threat patterns implied | The article is broad. For agent deployments, the implicit threat patterns span the full attack surface: input (AGT-001), tool-use (AGT-002, AGT-003), output (AGT-004, AGT-008), and audit (AGT-005). |
| Controls that address those threats | All five v1 controls contribute. The article's breadth means the framework's controls are most usefully understood as a coherent set that addresses the agent dimension across the ten measure categories. |
| Why this combination satisfies the article | NIS2 Article 21 is not satisfied by any single control. It is satisfied by demonstrating that the agent-specific dimensions of the ten measure categories are addressed. The v1 controls collectively do this; gaps remain (per section 8) but the foundation is in place. |

### 4.4 How to use the crosswalk in practice

The crosswalk supports several workflows that practitioners actually perform.

| Workflow | How to use the crosswalk |
|---|---|
| Regulatory readiness assessment | Start from the regulation column in section 4.2. Identify which v1 controls are listed as primary for the applicable provisions. Cross-reference to section 6 for implementation patterns and operational considerations. Identify gaps where the framework lists no primary controls. |
| Control program design | Start from the controls in section 6. For each control already implemented or planned, cross-reference to section 4.2 to identify which regulatory provisions are supported. Use this to scope compliance documentation. |
| Auditor engagement | For any regulatory provision questioned by the auditor, use the reasoned view in section 4.3 to construct the defense: regulation, threat pattern, control, why the combination is sufficient. Apply the same pattern to provisions not worked out in section 4.3. |
| Threat-driven program design | Start from the threat catalog in section 5. For each threat the deployment is exposed to, cross-reference to section 4.2 to understand which regulatory provisions implicitly require defense against it. |

### 4.5 Limitations of the crosswalk

The crosswalk is summary-level. Practitioners should be aware of three limitations:

| Limitation | Implication |
|---|---|
| Mappings are practitioner-attested, not regulator-attested | The mappings represent defensible interpretations of which controls address which provisions. They are not authoritative compliance determinations. Practitioners verifying compliance should obtain legal counsel. |
| The crosswalk reflects v1 framework coverage | Where the framework has known gaps (section 8), the crosswalk does not artificially close them by listing inadequate controls as primary. |
| Sectoral and national variations are not reflected | The crosswalk addresses the four named regulations at the EU level. Member State transposition variations, sectoral overlays (BSI grundschutz, BaFin guidance, MDR for medical contexts), and similar are out of scope for v1. |

These limitations are not defects. They are properties of any practitioner crosswalk constructed at a defensible level of generality. Practitioners adapt the crosswalk to their specific organisational context.

## 5. Agent Threat Patterns and Exemplars

<!-- Source: docs/sections/05-threat-model.md (4-6 pages) -->

This section presents the framework's view of agent-specific threats. It is structured in three layers, each playing a distinct role.

The first layer is an attack surface taxonomy. Agents have a bounded set of attack surfaces (input, model, tool-use, output, memory and persistence, audit and provenance), and each surface produces recognizable threat patterns. The taxonomy is the durable structural claim of the framework: it is finite, derived from the architectural components every agent has, and stable across deployments.

The second layer is a set of ten named threat exemplars (AGT-001 through AGT-010), one or two illustrative threats per attack surface. Each exemplar is documented with an attack scenario, an analysis of why traditional controls are insufficient, recommended controls from the v1 library, residual risk, detection and mitigation maturity, regulatory hooks, and MITRE ATLAS mappings. The exemplars are not an exhaustive enumeration of agent threats. They illustrate patterns concretely enough that practitioners can recognize variants in their own deployments.

The third layer is methodology for discovering threats specific to a deployment that may not match the named exemplars. The methodology is essential: threats are infinite, no catalog can be complete, and the framework's value lies in the taxonomy and the structured way of thinking, not in the specific list of named threats. The methodology is documented in `docs/frameworks/THREAT_MODEL_FRAMEWORK.md`; this section references it rather than restating it.

### Provenance of the threat catalog

The framework's threat catalog draws on multiple sources, each playing a different role:

| Source | Role in the catalog |
|---|---|
| Attack surface taxonomy (input, model, tool-use, output, memory, audit) | Framework-original. The structural claim that agent threats are bounded by a finite set of architectural surfaces is the framework's primary contribution and is not adopted from any specific external catalog |
| MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) | Secondary tagging on each exemplar where applicable. ATLAS provides technique-level adversarial-ML reference; this framework uses ATLAS technique IDs as cross-references but does not adopt ATLAS taxonomy as the primary structure |
| OWASP Top 10 for LLM Applications | Substantial overlap with several exemplars (notably AGT-001 prompt injection, AGT-004 data exfiltration). OWASP Top 10 is the most widely-recognized agent-relevant catalog among practitioners; the framework's exemplars overlap intentionally to ease cross-referencing, but the catalog is not derived from OWASP |
| Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," AISec '23 | Specific influence on AGT-001 (prompt injection via tool outputs). Cited in the exemplar as the canonical academic reference for the indirect-injection pattern |
| Author's practitioner experience in DACH regulated enterprises | The curation choice: which threats made the cut as exemplars, which residual risks were highlighted, and which regulatory hooks were emphasized. This influence is unavoidable in any practitioner framework and is acknowledged here rather than disguised |
| Cross-references to MITRE ATT&CK and NIST AI 100-2 (Adversarial Machine Learning) | Applied where threats overlap with general adversarial-ML or general-IT-security patterns; cited in individual exemplars rather than as primary structure |

The framework's claim is not that these ten threats are the complete or correct set; it is that the attack surface taxonomy is bounded and that the methodology for discovering deployment-specific threats is the durable contribution. Practitioners using this section should not interpret coverage of the ten exemplars as completion of agent threat work. Coverage of the exemplars is necessary but not sufficient. The actual security work is in applying the taxonomy and methodology to the specific deployment, complemented by external catalogs (MITRE ATLAS, OWASP LLM Top 10, MITRE ATT&CK, NIST AI 100-2) for technique-level detail.

**Note on v1 scope**: The canonical document at v1 contains the framing above; the exemplar bodies are not inlined here. AGT-001 (Prompt injection via tool outputs) and AGT-002 (Authorization confusion) are fully populated in `docs/sections/05-threat-model.md`, with attack scenario, traditional controls and why insufficient, recommended controls, residual risk, detection and mitigation maturity, regulatory hooks, and MITRE ATLAS mappings. AGT-003 through AGT-010 are present as compressed exemplars in the same section file and in `data/threats.json`: they cover attack scenario, recommended controls, and regulatory hooks but defer realistic deployment examples and full residual-risk analysis. Practitioners requiring depth equivalent to AGT-001 and AGT-002 should treat AGT-003 through AGT-010 as patterns to recognize rather than fully-documented exemplars at v1. Section 8 records the v1.1 commitments to populate AGT-003 through AGT-010 to parity and to merge full exemplar bodies into the canonical document.

## 6. Recommended Controls and Patterns

<!-- Source: docs/sections/06-controls.md (6-10 pages) -->

This section presents a coarse-grained v1 control library of 10 to 15 controls organized by implementation domain (identity, runtime, data, governance, audit and accountability) and tagged by function (preventive, detective, corrective, deterrent). Each control is mapped to the threats it addresses, to relevant articles of the EU AI Act, NIS2, DORA, and GDPR, and to the closest equivalents in NIST SP 800-53 Rev. 5, ISO 27001 Annex A, and BSI grundschutz. The intent is breadth and readability: a CISO should be able to scan the library in one sitting and identify which controls are relevant to their deployment.

The methodology, per-control template, taxonomy, and consolidation rules are documented in `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md`. That framework is the authoritative reference for how the library is structured and how new controls are added or refined. This section presents the controls themselves; the framework explains why they look the way they do.

The current v1 library status: CTL-001, CTL-002, CTL-003, CTL-004, and CTL-005 are all fully populated (presented below). The v1 control library is complete at five controls. CTL-006 through CTL-015 are reserved IDs that will be populated in v2 as the library expands beyond the initial five.

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

### CTL-004: Authorization-Aware Output Filtering

**Domain**: Data
**Function**: Preventive
**Maturity**: Emerging

**Description**: Agent outputs are filtered against the requesting user's authorization context before delivery, regardless of what the agent retrieved. The control closes the gap between agent retrieval scope and user authorization. Even when an agent has retrieved data using broader privileges than the user holds (a common operational reality), the output the user receives is constrained to what they are independently authorized to see.

The control operates at the output boundary, downstream of agent reasoning. It is structurally distinct from retrieval authorization: retrieval determines what the agent can read, output filtering determines what the user can see. Both are needed because in many enterprise deployments the agent must read broadly to perform its task, but users served by the agent have differentiated authorization.

**Implementation pattern**: After the agent has composed its proposed response and before delivery to the user, an output filter applies the user authorization context to the response. The filter has access to the user identity, the user's authorization claims (roles, group memberships, tenant, sensitivity clearances), and the data sources or content elements that contributed to the response.

Three implementation styles are common:

| Style | How it works |
|---|---|
| Source-based filtering | Each content element in the proposed output is tagged with its source; the filter removes elements from sources the user is not authorized to access |
| Attribute-based filtering | Output content is classified at filter time (PII type, sensitivity level, regulatory category); the filter compares classifications against user authorization and redacts non-authorized content |
| Hybrid filtering | Source tags provide the primary signal; attribute-based filtering catches inferential disclosure where source attribution is insufficient |

The filter must handle three distinct disclosure modes: direct quotation (content from a non-authorized source appears verbatim, which source-based filtering catches reliably); paraphrase or summary (content is rephrased but conveys the same protected information, which source-based filtering may miss and attribute-based filtering may catch); and inferential disclosure (content composed from authorized sources reveals protected information through inference, for example aggregating individually permitted records into a profile that would not have been permitted directly; both filtering styles struggle here, and this is where CTL-004 has known limits).

For high-stakes deployments, the filter extends to non-user-facing output channels: log entries, telemetry, audit records, and persistence to memory or vector stores. Output filtering at the user boundary alone is insufficient if the same content reaches other systems unfiltered.

**Operational considerations**:

| Consideration | Description |
|---|---|
| Performance overhead | Output filtering adds latency, typically 20 to 100 ms per response depending on filter complexity; cumulative for streaming or multi-turn responses |
| User context dependency | Filtering requires the user authorization context to be available at the output boundary; if CTL-001 is not implemented, the filter has insufficient information |
| Inferential disclosure limits | Current filtering technology cannot reliably detect when a paraphrased or composed response reveals protected information; this is a known limit, not an implementation defect |
| Content classification accuracy | Attribute-based filtering depends on classifiers (PII detectors, sensitivity classifiers); their accuracy varies and false negatives produce real disclosure |
| Channel coverage | Filtering only the user-facing channel leaves logs, telemetry, audit records, and persisted state unfiltered; full coverage requires deliberate channel inventory |
| Authorization model complexity | Enterprises with role-based, attribute-based, or relationship-based authorization need filter logic that mirrors the production authorization model; mismatches produce inconsistent behavior |
| Streaming output | Real-time streaming responses are harder to filter than complete responses; partial filtering during streaming risks revealing protected content before the filter completes |

**Common failure modes**:

| Failure mode | Description |
|---|---|
| Filtering only direct quotes | The filter catches verbatim disclosure but misses paraphrase and summary; the agent reveals protected information in its own words |
| Inference leaks | Composed responses reveal protected information through inference even when no individual content element is unauthorized |
| Channel bypass | Output filtering applies to the user response but logs, telemetry, audit records, or persistence include the unfiltered content |
| User context unavailable at filter time | The filter runs but cannot evaluate authorization because the user identity or claims were not propagated; the filter fails open or fails closed inconsistently |
| Classifier false negatives | Attribute-based filters miss content the classifier was not trained for; novel sensitive categories evade detection |
| Authorization model drift | Filter logic was implemented against a production authorization model; the production model evolves but the filter logic does not |
| Permission-denied notice as oracle | When the filter redacts content, the resulting permission-denied notice itself reveals that protected content existed; this can be a disclosure in regulated contexts |

**Threats addressed**: AGT-002 (primary), AGT-004 (primary), AGT-008 (secondary).

**Regulatory basis**:

| Regulation | Article or section | Relevance |
|---|---|---|
| GDPR | Art. 5(1)(c) | Data minimization; the regulatory anchor for output filtering as a data protection principle |
| GDPR | Art. 25 | Data protection by design and by default; design-level requirement to filter outputs to the minimum necessary |
| GDPR | Art. 32 | Security of processing; technical measures including access control at output |
| EU AI Act | Art. 10 | Data and data governance; output filtering enforces data governance at the agent output boundary |
| EU AI Act | Art. 15 | Cybersecurity; filtering reduces unauthorized disclosure as a security outcome |
| NIS2 | Art. 21 | Cybersecurity risk-management measures; output filtering is a structural confidentiality control |
| DORA | Art. 6 to 8 | ICT risk management; operational resilience including confidentiality controls at agent output |

**Existing standard mappings**:

| Standard | Control ID | Relationship |
|---|---|---|
| NIST SP 800-53 Rev. 5 | AC-3 (Access Enforcement) | Refinement: AC-3 establishes access enforcement; CTL-004 extends enforcement to the output boundary as a distinct point of control |
| NIST SP 800-53 Rev. 5 | AC-21 (Information Sharing) | Refinement: information-sharing decisions enforced at the agent output boundary |
| NIST SP 800-53 Rev. 5 | SC-8 (Transmission Confidentiality and Integrity) | Adjacent: confidentiality of transmission extended to filtering of agent outputs |
| NIST SP 800-53 Rev. 5 | SI-15 (Information Output Filtering) | Direct equivalent: SI-15 is specifically about output filtering; CTL-004 is its application to agent runtimes |
| ISO 27001 Annex A | A.5.10 (Acceptable use of information) | Refinement: acceptable use enforced at the output boundary of agent systems |
| ISO 27001 Annex A | A.8.12 (Data leakage prevention) | Refinement: data leakage prevention applied to agent-mediated output |
| BSI grundschutz | CON.6 (Löschen und Vernichten von Daten) | Adjacent: data minimization principles extended to output filtering |
| BSI grundschutz | CON.2 (Datenschutz) | Refinement: data protection principles applied to agent output |

**Related controls**:

| Control | Relationship |
|---|---|
| CTL-001 (Identity and authorization context propagation) | Dependent: filter operation requires the user authorization context that CTL-001 propagates; without CTL-001, the filter has insufficient information |
| CTL-002 (Tool-output and context provenance) | Complementary: provenance metadata helps the filter identify which content elements came from which sources for source-based filtering |
| CTL-005 (End-to-end audit and accountability) | Complementary: filter decisions (what was filtered, why, for whom) are themselves auditable events that CTL-005 captures |

**References**:

- NIST SP 800-53 Rev. 5, controls AC-3, AC-21, SC-8, SI-15
- NIST SP 800-122, Guide to Protecting the Confidentiality of Personally Identifiable Information
- ISO/IEC 27001:2022, Annex A controls A.5.10 and A.8.12
- ISO/IEC 27018:2019, Code of practice for protection of personally identifiable information in public clouds
- BSI IT-Grundschutz-Kompendium, Bausteine CON.2 and CON.6
- GDPR, Article 5(1)(c) (Data minimization), as the regulatory anchor for output filtering as a data protection principle
- GDPR, Article 25 (Data protection by design and by default), for design-level requirement to filter outputs to the minimum necessary
- GDPR, Article 32 (Security of processing), for technical measures including access control at output

### CTL-005: End-to-End Audit and Accountability

**Domain**: Audit and accountability
**Function**: Detective, Corrective
**Maturity**: Emerging (operational logs); Experimental (reasoning provenance)

**Description**: Every agent action is traceable to the originating user, the agent involved, the delegation chain (where applicable), the data and context that informed the decision, and the authorization basis on which the action was taken. The control enables forensic review, regulatory reporting, accountability for agent-mediated harm, and the detection of patterns that span multiple actions or users.

The control is detective and corrective rather than preventive: it does not stop bad things from happening, but it makes them visible after the fact and provides the basis for remediation. In agent contexts this matters more than in traditional systems because agent behavior is emergent and individual actions may look benign in isolation. Without end-to-end audit, organizations cannot answer fundamental accountability questions when something goes wrong.

The control distinguishes itself from traditional logging by capturing five dimensions of provenance simultaneously: who initiated the action (user attribution), what acted (agent attribution including delegation chain), what informed the decision (context provenance, retrieved data, instructions), what reasoning produced the action (model reasoning where available), and on what authority (authorization basis).

**Implementation pattern**: Audit records are structured to capture the full provenance chain for each agent action. A typical record includes:

| Dimension | What is captured |
|---|---|
| User attribution | Verified user identity, session identifier, authentication method, request that initiated the chain |
| Agent attribution | Agent service identity, agent version or model identifier, delegation chain if multiple agents are involved |
| Context provenance | Tools invoked, tool outputs received with their provenance metadata (from CTL-002), retrieved documents with version or revision identifiers, system prompts active at the time |
| Decision provenance | Model reasoning where available (chain-of-thought, tool selection rationale), policy decisions consulted, alternative paths considered |
| Authorization basis | The user authorization context that applied (from CTL-001), the verification that occurred at action boundaries (from CTL-003), the output filter decisions that were made (from CTL-004) |
| Action and outcome | The action taken, the system that received it, the result, and any downstream effects |

Records are correlated across systems through consistent identifiers: session ID, request ID, agent invocation ID, tool call ID. Without correlation, forensic reconstruction becomes prohibitively expensive.

For high-stakes deployments, audit extends to memory and persistence operations: every write to memory or vector stores is logged with the user, agent, and context that produced it, enabling later investigation when persisted content influences subsequent agent behavior.

The control acknowledges a fundamental limit: model reasoning provenance is partially opaque. Current LLMs do not produce reliable, deterministic explanations of their own decisions. Audit records should capture what reasoning the model emitted (where it produces chain-of-thought) but should not fabricate reasoning where none was emitted. This is a documented limit, not an implementation defect.

**Operational considerations**:

| Consideration | Description |
|---|---|
| Log volume | Provenance-rich records are substantially larger than traditional application logs; storage costs grow accordingly, often by an order of magnitude |
| SIEM ingestion cost | Most enterprise SIEMs are priced by ingestion volume; agent audit records compound the cost |
| Correlation infrastructure | Cross-system correlation requires consistent identifier propagation, which often requires retrofit of existing logging infrastructure |
| Reasoning provenance limits | Where the model does not emit reasoning, the audit record cannot synthesize it; this must be documented honestly rather than papered over |
| Retention policy alignment | Regulatory retention requirements (GDPR data subject rights, DORA incident reconstruction, sector-specific audit retention) drive retention, not internal preference |
| Privacy of audit records | Audit records often contain personal data and sensitive content; the audit infrastructure itself becomes a high-value target requiring its own access control |
| Detection at scale | Surfacing useful patterns from agent audit volumes requires detection rules tuned for agent behavior, which most enterprise SOC tooling does not yet have |
| Real-time vs batch | Real-time logging affects performance; batch logging risks loss during incidents; deployments must choose deliberately |

**Common failure modes**:

| Failure mode | Description |
|---|---|
| Logs fragmented across systems | Each component logs to its own destination with no common correlation key; reconstruction requires manual joins that are infeasible at scale |
| User attribution lost when CTL-001 is not implemented | Logs record the agent acted but cannot link to the originating user; accountability is broken at the foundation |
| Reasoning provenance fabricated | Implementations that synthesize plausible-sounding reasoning when the model did not emit any; gives false confidence in interpretability |
| Retention policies inconsistent with regulatory requirements | Logs are retained per IT policy rather than per regulatory obligation; data subject rights or incident-reconstruction requests cannot be fulfilled |
| Memory and persistence operations not audited | Direct user-facing actions are logged but writes to vector stores or long-term memory are not; later investigation cannot trace influence back to origin |
| Audit records exposed | Logs are stored without access control proportionate to their content; the audit infrastructure becomes a privacy or security incident in itself |
| Detection rules absent | Logs exist but no detection logic surfaces patterns; audit becomes forensic-only, not preventive |
| Volume-induced sampling | Cost pressures lead to sampling that breaks reconstruction integrity; sampling must be deliberate and documented, not silent |

**Threats addressed**: AGT-005 (primary), AGT-004 (primary), AGT-001 (secondary), AGT-002 (secondary), AGT-003 (secondary), AGT-006 (secondary), AGT-007 (secondary), AGT-009 (secondary), AGT-010 (secondary).

**Regulatory basis**:

| Regulation | Article or section | Relevance |
|---|---|---|
| EU AI Act | Art. 12 | Record-keeping; AI-specific logging requirements applicable to high-risk systems |
| EU AI Act | Art. 13 | Transparency; the information-about-system-operation requirement that audit supports |
| GDPR | Art. 5(2) | Accountability; the foundational requirement that audit enables |
| GDPR | Art. 30 | Records of processing activities; formal record-keeping obligation that overlaps with agent audit |
| NIS2 | Art. 21 | Cybersecurity risk-management measures; logging and monitoring as structural controls |
| NIS2 | Art. 23 | Incident reporting; reporting obligations depend on audit data being available |
| DORA | Art. 12 | Major ICT-related incidents; regulatory anchor for incident reconstruction obligations |
| DORA | Art. 17 to 19 | ICT-related incident management, classification, and reporting; all depend on audit |

**Existing standard mappings**:

| Standard | Control ID | Relationship |
|---|---|---|
| NIST SP 800-53 Rev. 5 | AU-2 (Event Logging) | Refinement: event logging extended to agent actions and decisions |
| NIST SP 800-53 Rev. 5 | AU-3 (Content of Audit Records) | Refinement: audit content extended to capture user, agent, context, and reasoning provenance |
| NIST SP 800-53 Rev. 5 | AU-6 (Audit Record Review, Analysis, and Reporting) | Refinement: review extended to agent-specific patterns |
| NIST SP 800-53 Rev. 5 | AU-9 (Protection of Audit Information) | Refinement: audit protection acknowledging audit records contain sensitive agent context |
| NIST SP 800-53 Rev. 5 | AU-12 (Audit Record Generation) | Refinement: record generation across agent runtime, tools, model invocations, and persistence |
| NIST SP 800-53 Rev. 5 | IR-4 (Incident Handling) | Adjacent: incident handling depends on the audit data CTL-005 produces |
| ISO 27001 Annex A | A.8.15 (Logging) | Refinement: logging extended to agent provenance |
| ISO 27001 Annex A | A.8.16 (Monitoring activities) | Refinement: monitoring extended to agent behavior patterns |
| ISO 27001 Annex A | A.5.28 (Collection of evidence) | Refinement: evidence collection extended to agent reasoning and provenance |
| BSI grundschutz | OPS.1.1.5 (Protokollierung) | Refinement: logging principles extended to agent runtime |
| BSI grundschutz | DER.1 (Detektion von sicherheitsrelevanten Ereignissen) | Refinement: detection extended to agent-specific patterns |

**Related controls**:

| Control | Relationship |
|---|---|
| CTL-001 (Identity and authorization context propagation) | Dependent: user attribution in audit records requires identity propagation; without CTL-001, audit cannot attribute reliably |
| CTL-002 (Tool-output and context provenance) | Dependent: context provenance in audit records requires the metadata that CTL-002 produces |
| CTL-003 (Action verification at high-impact boundaries) | Complementary: verification decisions are audit events; CTL-005 captures them |
| CTL-004 (Authorization-aware output filtering) | Complementary: filter decisions are audit events; CTL-005 captures them |

**References**:

- NIST SP 800-53 Rev. 5, AU family controls (AU-2, AU-3, AU-6, AU-9, AU-12), IR-4
- NIST SP 800-92, Guide to Computer Security Log Management
- NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide
- ISO/IEC 27001:2022, Annex A controls A.5.28, A.8.15, A.8.16
- ISO/IEC 27037:2012, Guidelines for identification, collection, acquisition and preservation of digital evidence
- BSI IT-Grundschutz-Kompendium, Bausteine OPS.1.1.5 and DER.1
- DORA, Article 12 (Major ICT-related incidents), as the regulatory anchor for incident reconstruction obligations
- EU AI Act, Article 12 (Record-keeping), for AI-specific logging requirements applicable to high-risk systems
- EU AI Act, Article 13 (Transparency), for the information-about-system-operation requirement that audit supports
- GDPR, Article 5(2) (Accountability), as the foundational requirement that audit enables
- GDPR, Article 30 (Records of processing activities), for the formal record-keeping obligation that overlaps with agent audit

## 7. Implementation Considerations

This section addresses how to deploy the v1 controls in environments that already have an established security program. The five subsections track the high-leverage decisions: where the controls plug into existing architecture, how to design the human review surface, where to place output filtering, how to roll out controls without exposing the organization to unnecessary risk, and how the controls produce evidence for regulatory obligations. Known gaps in the v1 control library are documented in Section 8 and are not revisited here.

### 7.1 Mapping controls to existing security architecture

Most organizations subject to NIS2 or DORA already operate identity, audit, and content security infrastructure. The v1 controls do not replace any of it; they extend it across the agent execution boundary. The integration patterns that work consistently in practice are:

| v1 control | Integrates with | Integration pattern |
|---|---|---|
| CTL-001 (Identity and authorization context propagation) | Existing IdP (Entra ID, Okta, Ping); existing OAuth / token-exchange infrastructure | The agent runtime acts as a downstream service in the token-exchange chain. The originating user's authorization context is carried forward as a delegated assertion (RFC 8693 token exchange or equivalent) rather than replaced with an agent service identity. The pattern that fails: the agent uses a service account with broad authorization and re-authorizes per call. The pattern that works: the agent inherits user context and the downstream tools enforce per-user authorization on retrieval. |
| CTL-002 (Tool-output and context provenance) | Existing data classification and DLP infrastructure | Provenance metadata is attached to content at ingest into the agent runtime and persisted through the execution. The agent runtime is responsible for distinguishing instruction from content; downstream consumers (including the model itself in subsequent turns) read the provenance tags. The pattern that fails: provenance lives only in agent logs after the fact. The pattern that works: provenance is part of the in-flight context and structurally distinguishes content from instruction at every boundary. |
| CTL-005 (End-to-end audit and accountability) | Existing SIEM (Splunk, Sentinel, Elastic); existing log retention infrastructure | Agent audit events flow into the existing SIEM as a new log source with a defined schema. The schema must include user attribution, tool invocation, retrieval scope, and decision provenance. The pattern that fails: agent logs as opaque blobs that the SOC cannot correlate with other security events. The pattern that works: agent logs as first-class structured events that the SOC can query alongside identity, network, and endpoint logs. |

The integration questions worth answering during design rather than discovering during operation:

| Question | Why it matters |
|---|---|
| Does the agent runtime have a service identity that the IdP can recognize as a delegated principal? | If not, CTL-001 cannot be implemented correctly; the agent will run with broad authorization and the deputy problem becomes structural |
| Does the SIEM ingest schema accommodate the cardinality of agent audit events? | A single user request can produce dozens of agent audit events; the SIEM must handle the volume without dropping or downsampling |
| Does the existing data classification taxonomy distinguish content origin? | If not, CTL-002 has no taxonomy to attach to; provenance becomes a parallel system rather than an extension of the existing one |

CTL-003 and CTL-004 integrate with workflow and content systems respectively; their integration considerations are covered in subsections 7.2 and 7.3.

### 7.2 Approval queue design for high-impact actions

CTL-003 places verification at high-impact action boundaries. The control specification does not prescribe the user experience; that is an operational decision with two failure modes.

The first failure mode is over-broad approval scope. If every agent action requires approval, operators ignore the queue. The agent provides no efficiency benefit and the organization has merely added a slow human step to a workflow that did not need automation. This is alert fatigue applied to approvals.

The second failure mode is under-broad approval scope. If only the most consequential actions require approval (large fund transfers, account deletions), the agent operates autonomously across a large surface where authorization confusion (AGT-002), tool-chain abuse (AGT-003), and goal drift (AGT-009) can produce harm without verification. The threshold appears to be set conservatively but is in fact the lower bound below which technical controls must work alone.

The patterns that hold up in practice:

| Approach | When it works | When it does not |
|---|---|---|
| Threshold based on action type alone (e.g., all fund transfers above EUR 10,000) | Actions are individually meaningful and the threshold reflects organizational risk tolerance | Actions compose; no single action exceeds the threshold but the composite does |
| Threshold based on cumulative effect (CTL-003's composition tracking) | Action composition is the dominant risk; AGT-003 is in scope | Operators cannot interpret cumulative thresholds; the queue surfaces opaque "cumulative limit reached" alerts |
| Threshold based on confidence (the agent's stated certainty about the action) | The model is well-calibrated and produces honest confidence signals | Models tend to be overconfident; thresholds based on stated confidence underapprove |
| Threshold based on user-context delta (the action affects users beyond the originating user) | AGT-002 (deputy problem) is the dominant risk | Single-user agents where the user always affects only themselves |

The approval surface itself is a design problem distinct from the threshold. Three properties worth designing for:

| Property | Why |
|---|---|
| The operator can see what the agent intends to do without re-reading the full conversation | Approvals must be possible in seconds, not minutes; the action description is the unit of decision |
| The operator can see the bridging context that makes the action high-impact | Why is this action surfacing for approval? Cumulative threshold? User-context delta? Without this, the operator cannot calibrate intuition over time |
| The operator can deny the action without ending the agent session | Hard-stop denial is rarely the right answer; "deny this action, propose an alternative" is. The approval surface must support negotiation |

Approval queue design is where the framework most acutely depends on factors outside its scope (operator training, organizational risk tolerance, audit retention policy). Subsection 4.7 of the crosswalk and Section 8 acknowledge that human factors are out of scope for v1; this subsection treats the approval surface as a technical artifact while flagging that the human side is the dominant determinant of effectiveness.

### 7.3 Output filtering placement decisions

CTL-004 (authorization-aware output filtering) produces a structural choice: where in the request lifecycle does filtering apply?

The two viable placements:

| Placement | Mechanism | Tradeoffs |
|---|---|---|
| Pre-retrieval filtering | The agent's retrieval calls are scoped to the user's authorization at the data layer (database row-level security, vector store metadata filters, search index ACLs) | Strongest guarantee; the agent cannot retrieve what it cannot see. Requires the data layer to enforce per-user authorization, which is often the existing access control architecture. Works only when the agent's retrieval interface respects the authorization model |
| Post-retrieval filtering | The agent retrieves with broad authorization and the output is filtered against the user's authorization before delivery | Weaker guarantee; the agent has temporarily seen content the user cannot see, creating residual risk through caching, logging, and side effects. Necessary when the data layer cannot enforce per-user authorization (e.g., document corpora with no per-user metadata) |

The combination that works: pre-retrieval filtering as the primary mechanism, post-retrieval filtering as a defense-in-depth layer for content classes where pre-retrieval cannot be enforced. The combination that creates the deputy problem at scale: post-retrieval filtering only, with the agent operating against a corpus that includes content for many users.

A practical signal that the placement is wrong: the audit trail (CTL-005) shows the agent retrieving content the user is not authorized for, even though the user never saw it. This is structurally equivalent to AGT-004 (data exfiltration via legitimate channels) at the model layer; the model has been exposed to the content and may surface it in subsequent turns through paraphrase or summarization that defeats post-retrieval filtering.

### 7.4 Phased rollout patterns

Agent deployments fail more often through scope expansion than through technical inadequacy. The pattern: a successful pilot with narrow tool authorization expands to broader tool authorization, broader user populations, or higher-stakes use cases without the corresponding investment in CTL-001 and CTL-003. The framework cannot prevent this organizationally, but the rollout phasing can make the expansion decision visible.

The phasing that works in regulated environments:

| Phase | Tool authorization | User population | Action surface | What gets validated |
|---|---|---|---|---|
| Pilot | Read-only against a single domain | Internal users with administrator visibility into agent behavior | Information retrieval; no consequential actions | CTL-001 propagation; CTL-005 audit completeness |
| Expansion 1 | Read-only across multiple domains; structured write to a single domain | Broader internal users | Limited consequential actions, all under CTL-003 verification | CTL-002 provenance under cross-domain retrieval; CTL-003 threshold calibration |
| Expansion 2 | Structured write across multiple domains | Internal users in operational roles | Consequential actions with selective CTL-003 verification based on calibrated thresholds | CTL-004 output filtering under broader authorization scopes; CTL-001 under multi-tenant or cross-organizational contexts |
| Production | Full deployed scope | Production user population | Full action surface | Continuous monitoring against the audit baseline established in earlier phases |

The decision criteria for moving between phases are organization-specific and not prescribed here. The decision criteria for not moving between phases are universal:

| Signal | What it indicates |
|---|---|
| CTL-005 audit shows authorization context drift across the pilot phase | CTL-001 implementation is incomplete; expansion will compound the gap |
| CTL-003 approval queue shows operator override patterns inconsistent with declared thresholds | Threshold calibration is wrong; expansion will produce alert fatigue |
| CTL-002 provenance failures are present in the audit trail | The agent is treating content as instruction in some path; expansion increases AGT-001 exposure |
| CTL-004 post-retrieval filtering is catching unauthorized content at non-trivial rate | Pre-retrieval filtering is not working; the data layer authorization model needs to be addressed before expansion |

Rollback triggers are simpler. Any of the four signals above, observed at production scale, is a rollback trigger to the previous phase. Rolling back is not a failure; rolling forward through the signals is.

### 7.5 Regulatory evidence collection

The crosswalk in Section 4 maps regulatory requirements to v1 controls. This subsection addresses the operational counterpart: what evidence the controls produce, and how that evidence connects to specific regulatory obligations.

Evidence is produced as a byproduct of correct operation, not as a separate compliance activity. If the controls are operating, the evidence exists. If the evidence does not exist, the controls are not operating. This is the structural relationship that makes the framework useful for compliance work; it is not a guarantee that the evidence is sufficient for any specific obligation, which depends on the regulator's interpretation and the deployer's broader compliance program.

| Regulatory obligation | Evidence the v1 controls produce | Operational source |
|---|---|---|
| EU AI Act Article 12 (record-keeping) | Automatically generated logs over the system lifecycle, including user attribution, tool invocation, retrieval scope, and decision provenance | CTL-005 audit stream; CTL-001 user attribution; CTL-002 retrieval and reasoning provenance |
| EU AI Act Article 14 (human oversight) | Approval queue records showing actions surfaced for human review, the operator decision (approve, deny, modify), and the timestamps for both | CTL-003 approval queue logs; CTL-005 audit of operator actions |
| EU AI Act Article 15 (accuracy, robustness, cybersecurity) | Audit-derived metrics on agent behavior under varied inputs; provenance trail for incidents involving content manipulation | CTL-002 provenance; CTL-005 audit; CTL-003 verification outcomes |
| NIS2 Article 21 (cybersecurity risk-management measures) | Evidence of access control enforcement (CTL-001), audit completeness (CTL-005), and operational monitoring derived from the audit stream | CTL-001 propagation logs; CTL-005 audit stream feeding the SIEM |
| NIS2 Article 23 (incident reporting) | Audit data sufficient to reconstruct events for the 24-hour, 72-hour, and one-month reporting cycles | CTL-005 audit retention with structured event schema |
| DORA Article 12 (major ICT-related incidents) | Audit data sufficient to reconstruct incident events; user and agent attribution for affected actions | CTL-005 with retention aligned to DORA reporting timelines |
| DORA Articles 28 to 30 (ICT third-party risk) | Audit and provenance data covering sub-agent and third-party tool invocations | CTL-001 across third-party tool boundaries; CTL-002 provenance across sub-agent outputs; CTL-005 audit of delegation chains |
| GDPR Article 5(2) (accountability) | End-to-end audit trail demonstrating compliance with processing principles | CTL-005 audit; CTL-002 provenance |
| GDPR Article 22 (automated individual decision-making) | Approval queue records demonstrating that decisions are not "solely" automated where Article 22 applies; audit trail supporting data subject contestability rights | CTL-003 approval queue; CTL-005 audit |
| GDPR Article 32 (security of processing) | Evidence of access control enforcement, output filtering, and incident audit consistent with appropriate technical measures | CTL-001, CTL-004, CTL-005 |

The evidence-collection decisions worth making during design:

| Decision | Why it matters |
|---|---|
| Audit retention period | Must accommodate the longest reporting cycle the organization is subject to (typically DORA's structured incident reporting or NIS2 Article 23's one-month final report). Under-retention forecloses compliance options |
| Schema versioning for audit events | Regulatory requirements evolve; audit schemas must accommodate evolution without re-deriving evidence from the past. Schema-versioned events are queryable across schema generations |
| Separation of audit data from operational data | Operational logs are often retained on a different cycle and with different access controls than compliance audit. Treating these as the same store creates retention conflicts and access-control conflicts |
| Read-only access for compliance and audit functions | Compliance reviewers need access to the audit stream that does not require operational privileges. The access pattern that fails: compliance asks operations for a one-time data extract, which then ages and is not reproducible |

For the cross-reference between specific articles and specific controls, see Section 4 (Common-control crosswalk). For known gaps in the v1 control library that affect what evidence can be produced, see Section 8 (Gaps and open problems).

## 8. Gaps and Open Problems

<!-- Source: docs/sections/08-gaps.md (2-3 pages) -->

A framework that overstates its coverage will be discovered by serious readers. The credibility of the rest of this document depends on this section being honest about what is missing and why. The categories below are the limits worth naming, with practical implications for how practitioners should use the framework today.

### 8.1 The threat catalog is not exhaustive

The 10 named threats in section 5 are exemplars within the attack surface taxonomy, not a complete enumeration. The durable contribution is the taxonomy and the threat-discovery methodology in section 5; the named threats illustrate the patterns. Practitioners who address all 10 exemplars have addressed 10 illustrative patterns, not agent security as a whole. Coverage requires applying the methodology to the specific deployment.

The catalog will grow as deployments mature and new patterns become recognizable. v2 of this framework will revisit the exemplar list based on field experience.

### 8.2 The v1 control library has known coverage gaps

The five v1 controls cover the threat catalog with deliberate honesty about where coverage is partial.

| Threat | Coverage in v1 | Gap |
|---|---|---|
| AGT-003 (tool-chain abuse) | Partial | CTL-003 was designed for individual high-impact actions; extension to composed actions requires runtime instrumentation v1 does not specify |
| AGT-006 (memory and persistence poisoning) | Partial | CTL-002 covers tool-output provenance; memory and vector store provenance follows similar principles but needs its own treatment |
| AGT-008 (output-channel injection) | Partial | Output sanitization for syntactic exploits in downstream parsers is not addressed by any v1 control |
| AGT-009 (goal subversion via context manipulation) | Weak | Genuinely hard to address with technical controls alone; v1 controls provide only partial coverage |
| AGT-010 (resource exhaustion via agent loops) | Partial | Resource governance is implicit in CTL-003 but not explicit |

These gaps are not implementation defects. They are design choices to keep v1 small and bounded. They are also the strongest candidates for v2 control work.

### 8.3 Reasoning provenance is fundamentally limited

CTL-005 captures audit and accountability across user attribution, agent attribution, context provenance, decision provenance, and authorization basis. One of these dimensions, model reasoning provenance, is fundamentally constrained by current LLM technology. Models do not produce reliable, deterministic explanations of their own decisions. Where models emit chain-of-thought, the audit can capture it. Where they do not, the audit cannot synthesize what was not produced.

This is a limit of the underlying technology, not a gap that v2 of this framework will close. Practitioners should treat agent decisions as partially opaque and design oversight assuming this constraint. For high-stakes decisions, human review at the action boundary is the only fully reliable accountability mechanism, which is why CTL-003 (action verification at high-impact boundaries) is the structural acknowledgment of this limit. Interpretability research may improve the situation in time, but the framework treats it as a constraint to design around rather than a gap to close.

### 8.4 The framework lacks documented incident examples

Each threat exemplar in section 5 includes a `realistic_example` field that is currently null. The framework is theoretically grounded in attack patterns and structural reasoning but does not yet illustrate threats with public incident data, anonymized customer scenarios, or documented breaches. This makes the framework less vivid for readers unfamiliar with agent security, and it makes the threats easier to dismiss as hypothetical even though the patterns are observed in research and in the field.

Populating realistic examples is a v2 priority. Sources will include public security research disclosures, anonymized scenarios from regulatory enforcement actions where available, and contributed examples from practitioner engagements where they can be sanitized for publication. Until v2, readers should treat the threat exemplars as well-grounded patterns awaiting evidentiary illustration in this specific document.

### 8.5 The vendor mapping interface is unproven

The framework is designed as a platform: vendor-specific control mappings are intended to be contributed by vendors and the community, not authored by the framework maintainer. The contribution interface is documented and the schema is defined, but no vendor mappings have been contributed as of v1 publication.

The platform model is unproven. Its value depends on adoption that has not yet happened. v2 evaluation will examine whether the contribution interface has produced meaningful mappings and what to adjust if not.

### 8.6 The framework does not address governance, culture, or organizational change

This framework is technical-practitioner-oriented. It addresses threats, controls, and regulatory mappings at the architectural and operational level. It does not address the organizational work of integrating AI security into procurement, shifting development culture, or building cross-functional governance. This is a deliberate scope choice. Most enterprise AI security failures will be governance failures as much as technical control failures, but addressing both in one document would dilute the focus and produce a less useful technical reference. Organizations should pair this framework with NIST AI RMF, ISO/IEC 42001, or ENISA AI cybersecurity guidance for the governance layer.

### 8.7 v1.1 commitments

The following items were intentionally deferred from v1 to keep the framework scope bounded and publishable. They are recorded here as commitments for the v1.1 release rather than v2, because they extend existing v1 content to parity rather than introducing new control or threat work.

| Commitment | What it covers | Why deferred from v1 |
|---|---|---|
| Populate AGT-003 through AGT-010 to parity with AGT-001 and AGT-002 | Add attack scenario depth, traditional controls and why insufficient, full residual-risk analysis, detection and mitigation maturity, and realistic deployment examples for the eight compressed exemplars in Section 5 | Time-bounded curation; the compressed form is sufficient for pattern recognition at v1, but practitioners using the framework for engagement-grade threat modeling need the deeper form |
| Merge full exemplar bodies into the canonical document | The canonical document at v1 contains the Section 5 framing only; exemplar bodies live in `docs/sections/05-threat-model.md`. v1.1 will inline the full bodies in the canonical document so the single-file artifact is self-contained | Avoided duplication while exemplar depth was uneven; defer to when AGT-003 through AGT-010 reach parity |
| Annex B (worked example) | A concrete deployment scenario walked through the threat model, the five v1 controls, and the regulatory crosswalk; intended to make the framework vivid for readers unfamiliar with agent security | The worked example requires a specific deployment context the framework does not yet have a sanitized example for; deferred rather than fabricated |

These commitments are bounded extensions of existing v1 content. They are distinct from v2 work, which extends the control library and expands the framework scope.

### What v2 will address

The gaps above produce a v2 control library priority list:

| Priority | Addresses |
|---|---|
| Memory and persistence provenance control | AGT-006 coverage gap |
| Runtime resource governance control | AGT-010 coverage gap |
| Output sanitization control or refinement | AGT-008 coverage gap |
| CTL-003 refinement for composed actions | AGT-003 coverage gap |

Beyond the control library, v2 will also populate realistic examples for the threat exemplars, evaluate the vendor mapping platform, and consider whether the methodology section needs strengthening for goal subversion (AGT-009), which remains the threat with the weakest v1 coverage.

v1 is bounded honestly to what it can defend. The framework is more useful for being explicit about that boundary than for pretending coverage it does not have.

## 9. References

### How references are organized

This section consolidates the sources cited throughout the practitioner guide. It is a working reference list, not an academic bibliography. Entries are short-form (title, publisher, identifier or URL where applicable) and grouped by source type. Where a source is cited in multiple sections, it appears only once.

For verified dates, article references, and citation specifics for the four primary EU regulatory instruments, see also [`../frameworks/regulatory-facts.md`](../frameworks/regulatory-facts.md) in this repository, which is the source-of-truth reference file maintained alongside this guide.

### EU regulations

| Citation | Source |
|---|---|
| Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence (Artificial Intelligence Act) | EUR-Lex, https://eur-lex.europa.eu/eli/reg/2024/1689/oj |
| Directive (EU) 2022/2555 of the European Parliament and of the Council on measures for a high common level of cybersecurity across the Union (NIS2 Directive) | EUR-Lex, https://eur-lex.europa.eu/eli/dir/2022/2555/oj |
| Regulation (EU) 2022/2554 of the European Parliament and of the Council on digital operational resilience for the financial sector (Digital Operational Resilience Act, DORA) | EUR-Lex, https://eur-lex.europa.eu/eli/reg/2022/2554/oj |
| Regulation (EU) 2016/679 of the European Parliament and of the Council on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation, GDPR) | EUR-Lex, https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| Directive (EU) 2022/2556 (DORA Directive, companion to Regulation 2022/2554) | EUR-Lex, https://eur-lex.europa.eu/eli/dir/2022/2556/oj |

### EU institutional guidance

| Citation | Source |
|---|---|
| European Commission, AI Act implementation guidance | digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |
| AI Act Service Desk, Article-level guidance | ai-act-service-desk.ec.europa.eu |
| European Data Protection Board (EDPB), Guidelines on Automated Individual Decision-Making and Profiling, WP251rev.01 | edpb.europa.eu |
| European Supervisory Authorities (EBA, EIOPA, ESMA), DORA Regulatory Technical Standards on ICT risk management, incident reporting, and third-party risk | esas-joint-committee.europa.eu |
| ESAs, Designated Critical ICT Third-Party Providers under DORA (first list, 18 November 2025) | Joint ESA publication |
| ENISA, NIS2 Directive guidance and sector taxonomies | enisa.europa.eu |

### National and sector-specific rules (DACH)

| Citation | Source |
|---|---|
| BSI, Cloud Computing Compliance Criteria Catalogue (C5:2020 and C5:2026) | bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5 |
| C5-Gleichwertigkeitsverordnung (Verordnung über gleichwertige Sicherheitsnachweise zum C5-Standard für Cloud-Computing-Dienste im Gesundheitswesen), 19 March 2025, BGBl. 2025 I Nr. 91 | gesetze-im-internet.de/c5gleichwv |
| § 393 SGB V (Fünftes Buch Sozialgesetzbuch), introduced by the Digital-Gesetz (DigiG), 22 March 2024 | gesetze-im-internet.de/sgb_5 |
| BSI, IT-Grundschutz-Kompendium (current edition) | bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/IT-Grundschutz-Kompendium |
| BSI IT-Grundschutz, Baustein ORP.1 (Organisation), ORP.4 (Identitäts- und Berechtigungsmanagement), CON.2 (Datenschutz), CON.6 (Löschen und Vernichten), CON.10 (Entwicklung von Webanwendungen), DER.1 (Detektion), OPS.1.1.5 (Protokollierung), OPS.1.2.4 (Telearbeit) | BSI IT-Grundschutz-Kompendium |
| Germany NIS2 transposition (NIS2-Umsetzungs- und Cybersicherheitsstärkungsgesetz, NIS2UmsuCG), in force 6 December 2025 | Bundesgesetzblatt 2025; bsi.bund.de |

### International standards and frameworks

| Citation | Source |
|---|---|
| NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations | nist.gov/publications |
| NIST SP 800-37 Rev. 2, Risk Management Framework for Information Systems and Organizations | nist.gov/publications |
| NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide | nist.gov/publications |
| NIST SP 800-92, Guide to Computer Security Log Management | nist.gov/publications |
| NIST SP 800-122, Guide to Protecting the Confidentiality of Personally Identifiable Information | nist.gov/publications |
| NIST SP 800-207, Zero Trust Architecture | nist.gov/publications |
| NIST SP 800-218, Secure Software Development Framework (SSDF) | nist.gov/publications |
| NIST AI 100-1, AI Risk Management Framework (AI RMF 1.0) | nist.gov/itl/ai-risk-management-framework |
| NIST AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations | nist.gov/publications |
| ISO/IEC 27001:2022, Information security, cybersecurity and privacy protection, Information security management systems, Requirements | iso.org |
| ISO/IEC 27018:2019, Code of practice for protection of personally identifiable information in public clouds acting as PII processors | iso.org |
| ISO/IEC 27037:2012, Guidelines for identification, collection, acquisition and preservation of digital evidence | iso.org |
| ISO/IEC 38500:2024, Governance of information technology | iso.org |
| ISO/IEC 42001:2023, Information technology, Artificial intelligence, Management system | iso.org |
| ISO 22301:2019, Security and resilience, Business continuity management systems | iso.org |
| MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems), Matrix v5.4.0 | atlas.mitre.org |
| OWASP Top 10 for Large Language Model Applications | owasp.org/www-project-top-10-for-large-language-model-applications |

### IETF and protocol specifications

| Citation | Source |
|---|---|
| RFC 6749, The OAuth 2.0 Authorization Framework | datatracker.ietf.org/doc/html/rfc6749 |
| RFC 8693, OAuth 2.0 Token Exchange | datatracker.ietf.org/doc/html/rfc8693 |
| RFC 9068, JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens | datatracker.ietf.org/doc/html/rfc9068 |
| RFC 9421, HTTP Message Signatures | datatracker.ietf.org/doc/html/rfc9421 |
| SPIFFE (Secure Production Identity Framework For Everyone) and SPIRE specifications | spiffe.io |

### Academic and practitioner sources

| Citation | Source |
|---|---|
| Greshake, K., et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec '23), 2023 | dl.acm.org or arxiv.org/abs/2302.12173 |
| AI Safety Institute (UK AISI) and partners, evaluation guidance for foundation models | aisi.gov.uk |

### Repository internal references

| Item | Path |
|---|---|
| Project brief | `PROJECT_BRIEF.md` |
| Threat model framework | `docs/frameworks/THREAT_MODEL_FRAMEWORK.md` |
| Control library framework | `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md` |
| Regulatory facts (source of truth for dates and article references) | `docs/frameworks/regulatory-facts.md` |
| Threat catalog (data) | `data/threats.json` |
| Control library (data) | `data/controls.json` |
| Bidirectional mappings | `data/mappings.json` |

### Notes on currency and verification

Regulatory citations were verified against EUR-Lex and Commission sources in May 2026. Specific application dates, transposition status, and Article references are subject to change as member-state implementation progresses and as the Digital Omnibus simplification proposal (published 19 November 2025) advances. For the current state of these items, consult [`../frameworks/regulatory-facts.md`](../frameworks/regulatory-facts.md), which is updated as part of repository maintenance, and verify directly against EUR-Lex and the relevant national supervisory authority before relying on any citation here for compliance decisions.

Threat-specific citations in `data/threats.json` include placeholders ("Recent work on indirect prompt injection from 2024 to 2026 (specific citations to be selected during section drafting)" and similar). These placeholders persist into v1 and will be filled during the v2 expansion of the threat catalog. They are noted here for transparency rather than included as references.

## Appendix A. ServiceNow Mapping (Optional)

<!-- Source: docs/sections/10-appendix-servicenow-mapping.md -->
<!-- Optional, non-canonical overlay mapping the generic controls in section 6 to ServiceNow products. -->
_Placeholder._
