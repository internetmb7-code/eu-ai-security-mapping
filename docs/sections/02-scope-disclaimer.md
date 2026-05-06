# 2. Scope and Disclaimer
<!-- Length budget: 1 page -->

## What this document covers

This guide addresses the security of **enterprise AI agent deployments** under EU regulatory pressure. By "agent" I mean a specific class of system, not the broader marketing category.

| Attribute | In scope |
|---|---|
| Reasoning core | LLM-based |
| Capability | Tool-using (calls APIs, queries data sources, invokes other systems) |
| Execution model | Multi-step (plans and executes sequences of actions) |
| Autonomy | Operates autonomously between human approval points |
| Deployment context | Enterprise environments subject to EU AI Act, NIS2, DORA, or GDPR Article 22 |

The threats and controls in this document assume all five attributes hold. Systems missing one or more attributes have different threat surfaces and different control needs.

## What this document does not cover

| Out of scope | Why excluded |
|---|---|
| Classical robotic process automation (RPA) without an LLM reasoning core | Different threat model; deterministic rule-based execution; established control frameworks already exist |
| Single-shot LLM calls (chatbots, summarization, classification) without tool use | No tool-chain attack surface; no autonomy between approvals; existing AI risk frameworks (NIST AI RMF, ISO 42001) address these adequately |
| Fully supervised copilots where every action requires explicit human approval | Human approval is the dominant control; agent-specific threats like authorization confusion and tool-chain abuse are bounded |
| Foundation model training, fine-tuning, and pre-deployment safety evaluation | Different lifecycle phase; covered by AI provider obligations under EU AI Act Articles 16 to 29 and frameworks like the AISI evaluation guidance |
| Consumer-facing AI products and general-purpose AI assistants | Different regulatory regime, different threat model, different audience |
| Adversarial machine learning research (model extraction, membership inference, evasion) | Active research field with its own literature; orthogonal to operational deployment security |
| Physical-world agents (robotics, autonomous vehicles, embedded systems) | Different regulatory frameworks (Machinery Regulation, type approval); different threat surfaces |

The boundary that matters most: this document is about **operational security of agents already deployed in enterprise environments**, not about the safety properties of the underlying models or the design of agent architectures from scratch.

## Regulatory scope

The framework maps to four EU instruments:

| Instrument | Relevance |
|---|---|
| EU AI Act (Regulation 2024/1689) | High-risk AI system obligations; general-purpose AI model obligations; enforcement begins August 2026 for high-risk systems |
| NIS2 Directive (Directive 2022/2555) | Cybersecurity obligations for essential and important entities; in force since October 2024 |
| DORA (Regulation 2022/2554) | ICT risk management for financial entities; in force since January 2025 |
| GDPR Article 22 | Automated decision-making with legal or similarly significant effects; in force since 2018 |

Mappings to non-EU frameworks (NIST SP 800-53, ISO 27001 Annex A, BSI IT-Grundschutz) are provided as a translation aid, not as primary coverage. The framework is EU-regulation-anchored.

## Threat catalog scope

The 10 threats in Section 5 are **exemplars within an attack surface taxonomy**, not an exhaustive enumeration. Coverage of all 10 does not mean coverage of all agent threats. Section 5 documents the methodology for discovering threats specific to a deployment; the methodology is the durable contribution, not the catalog.

## Control library scope

The 5 controls in Section 6 are a **coarse-grained v1**. They cover the high-leverage operational decisions. They do not cover:

| Gap | Status |
|---|---|
| Detection and response controls (SIEM integration, anomaly detection on agent behavior) | Acknowledged in Section 8; v2 priority |
| Supply chain controls (model provenance, prompt template integrity) | Acknowledged in Section 8; v2 priority |
| Human factors controls (operator training, alert fatigue management) | Acknowledged in Section 8; v2 priority |

Honest gap acknowledgment beats false comprehensiveness. The control library will expand in v2 based on customer engagement feedback on v1.

## Disclaimer and author affiliation

I am a Senior Staff Information Security Analyst in the Office of the CISO at ServiceNow, based in Munich. This framework is independent practitioner work. It is vendor-neutral and product-agnostic.

Specifically:

| Statement | Meaning |
|---|---|
| The framework names no vendor products in threat descriptions, control specifications, or mappings | The body of the work is product-agnostic by construction |
| Vendor-specific mappings are accepted as community contributions through a defined schema and process (see Vendor Mapping Framework) | The author does not produce vendor mappings as part of the core framework |
| The author recuses from reviewing ServiceNow submissions to the vendor mapping interface | A separate reviewer chain handles ServiceNow contributions to avoid conflict of interest |
| Nothing in this document constitutes legal advice, certification of compliance, or regulatory interpretation binding on any authority | This is practitioner guidance; binding interpretation comes from regulators, courts, and qualified counsel |
| Views expressed are the author's own and do not represent ServiceNow's official positions, product commitments, or regulatory interpretations | Standard separation between employer and independent practitioner work |

Readers using this framework in regulated contexts should validate findings with qualified counsel, their data protection officer, and the relevant supervisory authority before relying on it for compliance decisions.
