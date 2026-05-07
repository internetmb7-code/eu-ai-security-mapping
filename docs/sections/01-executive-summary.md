This section is written for security leaders and CISOs who need to make decisions about AI agent deployments under EU regulatory pressure. It is longer than a typical executive summary because the decisions are not simple. Readers wanting a two-paragraph version can read the first two paragraphs and the overview table; everything else builds on that foundation.

## 1.1 The bottom line

If your organization is deploying AI agents (LLM-based, tool-using systems that take multi-step actions on behalf of users), you are accepting a class of risk that your current security program does not fully address. Most enterprise security programs are built around the assumption that systems act with their own service identity and that authorization decisions are made at fixed boundaries. AI agents violate both assumptions. They act on behalf of users (so authorization must propagate through them), and they make autonomous decisions between human approval points (so the authorization boundary moves with the agent, not with the architecture).

This framework is a practitioner's view of what to do about that, mapped to the EU regulations you are now subject to or will be soon. It is not legal advice; it is operational guidance grounded in regulatory text. The framework's central claim is simple: the agent-specific layer of your security program needs five technical controls to be defensible under EU AI Act, NIS2, DORA, and GDPR Article 22. None of the five replaces existing security infrastructure; all five extend it.

## 1.2 The five top exposures, in plain language

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

## 1.3 What to tell your board

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

## 1.4 What to do, in priority order

The framework has five v1 controls (CTL-001 through CTL-005). They are not equally urgent. The priority ordering below is based on three factors: structural dependency (some controls only work if others are in place), regulatory exposure (some obligations have current enforcement, others phase in), and practical leverage (some controls produce evidence that supports compliance for multiple obligations).

| Phase | Control | Why this priority | Criteria for moving to next phase |
|---|---|---|---|
| 1 | CTL-001 (Identity and authorization context propagation) | Structural foundation; without it, everything else either does not work or works on a weaker basis. This is also the control most enterprises fail on day one because their agents run as service accounts | Every agent action in production is associated with a verified user identity that propagates through downstream calls. Audit (CTL-005) shows this is true for at least 95% of actions over a 30-day window |
| 2 | CTL-005 (End-to-end audit and accountability) | Without audit, you cannot tell whether the other controls are working. CTL-005 also produces the evidence base for AI Act Art 12, NIS2 Art 23, DORA Art 17, GDPR Art 5(2), so its regulatory leverage is the highest of the five | Audit pipeline ingests agent events into the SIEM with sufficient detail to reconstruct any agent action. Retention period is set against the longest reporting cycle the organization is subject to (typically NIS2 Art 23 one-month cycle or DORA equivalent) |
| 3 | CTL-003 (Action verification at high-impact boundaries) | The structural mechanism for AI Act Art 14 (human oversight) and GDPR Art 22 (the human-review condition that takes a system out of "solely automated"). Cannot be effective without CTL-001 and CTL-005 in place | Approval queue is operational; thresholds are calibrated against actual operator override patterns; CTL-005 audit shows operator decisions are recorded with sufficient context for compliance |
| 4 | CTL-002 (Tool-output and context provenance) | Mitigates content-as-instruction (prompt injection). Less urgent than the first three because the worst impact of prompt injection (taking unauthorized actions) is bounded by CTL-001 and CTL-003 if those are in place | Provenance metadata is attached to content at ingest; agents distinguish content from instruction at every boundary; audit (CTL-005) shows no policy violations from injected content over a 30-day window |
| 5 | CTL-004 (Authorization-aware output filtering) | Defense-in-depth for the deputy problem and exfiltration; secondary to CTL-001 because if CTL-001 is correct, fewer cases reach CTL-004 | Pre-retrieval filtering is the primary mechanism (data layer enforces per-user authorization); post-retrieval filtering is a defense-in-depth layer for content classes where pre-retrieval cannot be enforced |

The criteria column matters as much as the ordering. Moving from one phase to the next without meeting the criteria is the failure mode that produces non-defensible deployments. Section 7 expands on the rollout patterns and the signals that indicate you should not move forward.

## 1.5 What this is going to cost

I am not going to give you a euro figure; that depends on your existing infrastructure, the scale of your agent deployment, and choices you have not yet made. I can tell you what categories of investment are involved.

| Investment category | Typical magnitude | Notes |
|---|---|---|
| Identity infrastructure changes for CTL-001 | Significant if you do not already have OAuth 2.0 token exchange or equivalent in production; modest if you do | The pattern of using a service account for the agent and re-authorizing per call is the most common starting point and the most expensive to migrate from |
| SIEM ingest capacity for CTL-005 | Moderate; agent audit events are higher cardinality than typical application logs | Underestimating this is common; budget for substantially higher per-user log volume than equivalent non-agent applications |
| Approval queue tooling for CTL-003 | Modest if you have existing workflow infrastructure (ServiceNow, Jira Service Management, custom workflow); higher if you are building from scratch | The expensive part is not the tooling; it is calibrating thresholds and training operators |
| Data layer authorization for CTL-004 | Highly variable; depends on how much of your data already has per-user authorization at the data layer | If your data lives behind systems that enforce per-user authorization (most modern SaaS, well-architected internal systems), this is mostly configuration. If your data lives in shared corpora (document stores, vector indexes without per-user metadata), this is structural |
| Provenance tooling for CTL-002 | Modest; primarily a runtime configuration and content-handling discipline | The cost here is not technical; it is operational discipline in how content enters the agent runtime |

The honest framing for budget conversations: the work is bounded and largely consists of extending what you already have, not buying new categories of tooling. The exception is identity infrastructure if you do not already have user-context propagation in production; that is a real architectural investment. Everything else is incremental.

## 1.6 What this framework will not do for you

I want to be explicit about the limits of this document, because over-reliance on a framework like this is itself a risk.

| The framework does not | What you still need |
|---|---|
| Address governance, organizational change, or culture | A separate program for AI risk governance, ethics review, and operator training |
| Cover detection and response controls (SIEM rules, anomaly detection on agent behavior) | Your existing SOC, augmented with agent-specific detection content; this is a v2 framework priority |
| Cover supply chain controls (model provenance, prompt template integrity) | Vendor risk management for your AI providers and your agent platform; this is a v2 framework priority |
| Cover regulatory obligations that are organizational (AI Act Art 17 QMS, Art 27 FRIA, contractual provisions under DORA Art 30) | Your compliance program; this framework is the technical layer underneath it |
| Constitute compliance certification | Validation by qualified counsel, your DPO, and the relevant supervisory authority before relying on this for compliance decisions |

The framework's contribution is the technical agent-specific layer. It is necessary but not sufficient.

## 1.7 How to read the rest of this document

The remaining sections are organized for two different ways of using the framework:

| If you want to | Read |
|---|---|
| Understand the regulatory landscape for agent deployments | Section 2 (scope and disclaimers), then Section 3 (regulatory landscape) |
| Find the right controls for a specific regulatory requirement | Section 4 (common-control crosswalk) |
| Understand the threat model in depth | Section 5 (threat patterns and exemplars) |
| Implement the v1 controls | Section 6 (control specifications) and Section 7 (implementation considerations) |
| Walk through a concrete deployment scenario | Annex B (worked example) |
| Understand what the framework does not cover | Section 8 (gaps and open problems) |

A practitioner deploying agents in a regulated DACH enterprise should read Section 1 (this section), Section 7 (implementation considerations), and Annex B (worked example) first. The other sections become useful when specific questions arise.

A regulator or auditor evaluating an agent deployment against the framework should read Sections 2, 3, 4, 5, 6, and 8. Sections 1 and 7 are practitioner-oriented and Annex B is illustrative; they are not the framework's primary content for compliance evaluation.
