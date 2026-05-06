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
| Classical RPA without an LLM reasoning core | Different threat model; established control frameworks cover it |
| Single-shot LLM calls (chatbots, summarization, classification) without tool use | No tool-chain attack surface; existing AI risk frameworks (NIST AI RMF, ISO 42001) cover them |
| Fully supervised copilots where every action requires explicit human approval | Human approval is the dominant control; agent-specific threats are bounded |
| Foundation model training, fine-tuning, and pre-deployment safety evaluation | Different lifecycle phase; covered by AI Act Articles 16 to 29 and AISI evaluation guidance |
| Consumer-facing AI products and general-purpose AI assistants | Different regulatory regime, different audience |
| Adversarial ML research (model extraction, membership inference, evasion) | Active research field with its own literature; orthogonal to operational deployment security |
| Physical-world agents (robotics, autonomous vehicles, embedded systems) | Different regulatory frameworks (Machinery Regulation, type approval) |

The boundary that matters most: this document is about **operational security of agents already deployed in enterprise environments**, not the safety properties of the underlying models or agent architecture design from scratch.

## Regulatory scope

The framework maps to four EU instruments:

| Instrument | Relevance |
|---|---|
| EU AI Act (Regulation 2024/1689) | High-risk AI system and GPAI obligations; high-risk enforcement from August 2026 |
| NIS2 Directive (Directive 2022/2555) | Cybersecurity obligations for essential and important entities; in force since October 2024 |
| DORA (Regulation 2022/2554) | ICT risk management for financial entities; in force since January 2025 |
| GDPR Article 22 | Solely automated decisions with legal or similarly significant effects |

Mappings to non-EU frameworks (NIST SP 800-53, ISO 27001 Annex A, BSI IT-Grundschutz) are translation aids. Verified citations and dates are maintained in [`../frameworks/regulatory-facts.md`](../frameworks/regulatory-facts.md), from which Section 3 draws.

## Threat catalog scope

The 10 threats in Section 5 are **exemplars within an attack surface taxonomy**, not an exhaustive enumeration. Coverage of all 10 does not mean coverage of all agent threats. Section 5 documents the methodology for discovering threats specific to a deployment; the methodology is the durable contribution, not the catalog.

## Control library scope

The 5 controls in Section 6 are a **coarse-grained v1**. Detection and response (SIEM integration, behavioral anomaly detection), supply-chain controls (model provenance, prompt-template integrity), and human-factors controls (operator training, alert-fatigue management) are acknowledged gaps in Section 8 and are v2 priorities. Honest gap acknowledgment beats false comprehensiveness; the library will expand in v2 based on customer engagement feedback.

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
