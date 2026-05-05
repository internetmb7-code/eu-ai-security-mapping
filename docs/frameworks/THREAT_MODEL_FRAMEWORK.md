# Threat Model Framework: Enterprise AI Agent Security (v2 Reframe)

This document defines the framework used in Section 5 of the practitioner guide. It establishes the attack surface taxonomy, the role of named threats as exemplars, the methodology for discovering threats in specific deployment contexts, and the per-threat template. It is the foundational artifact for `data/threats.json` and shapes the controls library and the web tool's threat browser.

This is a v2 reframe of the original framework. The substantive content (attack surfaces, threats, template) is preserved. What changes is the **status** of the threat catalog: it is now positioned as a set of exemplars within a taxonomy plus methodology, not as a comprehensive enumeration of agent threats.

## What changed and why

| Element | v1 framing | v2 framing |
|---|---|---|
| Status of the 10 named threats | Implicit catalog of "the threats agents face" | Explicit exemplars illustrating threat patterns at each attack surface |
| Primary structural claim | The threat catalog | The attack surface taxonomy |
| Position on completeness | Implicit; reader could infer the list was authoritative | Explicit; the list is not exhaustive and cannot be |
| External catalog references | Mentioned as related work | Positioned as continuously-maintained sources for specific techniques |
| Methodology for new deployments | Not addressed | Explicit guidance on threat discovery |

The reason for the reframe: threats are infinite. Any catalog of named threats will be incomplete, will become stale, and will create false confidence in coverage. Mature threat-driven frameworks (MITRE ATT&CK, MITRE ATLAS, STRIDE) do not claim completeness. They claim usefulness. The reframe brings this framework into line with that practice.

## Purpose

To provide CISOs and security program leads with:

| Goal | How the framework achieves it |
|---|---|
| A durable, finite structural model for thinking about agent threats | The attack surface taxonomy: agents have a bounded number of attack surfaces, and each surface produces recognizable threat patterns |
| Concrete exemplars that illustrate the patterns | Ten named threats (AGT-001 through AGT-010), one or two per surface, fully documented with attack scenarios and recommended controls |
| Methodology for discovering threats in specific contexts | Explicit guidance on how to identify threats in a specific deployment that may not match the named exemplars |
| Pointers to continuously-maintained external catalogs | MITRE ATLAS, OWASP LLM Top 10, MITRE ATT&CK as references for specific techniques as they emerge |

The framework is not a checklist. A practitioner who confirms "we have controls against all 10 named threats" has not confirmed they have addressed agent security. They have confirmed they have addressed ten illustrative patterns. The actual security work is in applying the taxonomy and methodology to their specific deployment.

## Audience and Reading Mode

| Aspect | Choice |
|---|---|
| Primary audience | CISOs and security program leads |
| Secondary audience | Enterprise security architects, regulatory and compliance leads |
| Reading mode | Risk-first, prioritization-oriented |
| Expected use | Read the taxonomy and methodology in full; reference exemplar threats during program design or customer engagement |

## Scope: What Counts as an Agent

For the purposes of this framework, an **AI agent** is an LLM-based system that meets all four of the following criteria:

1. Takes instructions in natural language
2. Decides which tools or actions to invoke without human approval at each step
3. Executes those actions against external systems with real-world effect
4. Operates over multiple steps within a single workflow

### In scope

| System type | Example |
|---|---|
| Workflow agents acting on enterprise records | Agents creating, modifying, or routing records |
| Customer service agents with action authority | Agents that file tickets, issue refunds, or update accounts |
| Code-execution agents | Developer copilots with shell or repository access |
| Multi-agent systems with delegation | Orchestrator agents that delegate to sub-agents |
| Autonomous research and analysis agents | Agents that browse, fetch, summarize, and act |

### Out of scope

| System type | Reason for exclusion |
|---|---|
| Single-shot LLM calls (chat without tools) | No autonomy over actions; covered by traditional content-security frameworks |
| RAG systems without action capability | Read-only; covered by data-access controls |
| Classifier or recommendation models | Covered by adversarial ML literature and standard MITRE ATLAS techniques |
| Workflow automation with AI-assisted steps and human approval at each action | Human-in-the-loop neutralizes most agent-specific risks |

## The Attack Surface Taxonomy

This is the durable structural claim of the framework. Agents have a bounded set of attack surfaces, regardless of specific deployment. Each surface produces recognizable threat patterns that can be reasoned about and defended.

### The six attack surfaces

| Surface | Description | Typical threat patterns at this surface |
|---|---|---|
| 1. Input | Channels through which content enters the agent's context | Adversarial content in user prompts, retrieved documents, or tool outputs that re-enter context |
| 2. Model | The LLM itself and its decision-making behavior | Goal interpretation drift, instrumental goal pursuit, emergent misalignment |
| 3. Tool-use | The interface between the model's decisions and external actions | Authorization decoupling, tool-chain composition, delegation context loss, resource exhaustion |
| 4. Output | Channels through which the agent's outputs leave the system | Data exfiltration via legitimate channels, downstream system exploitation, output-as-instruction in receiving systems |
| 5. Memory and persistence | State that persists across agent interactions or sessions | Memory poisoning, cross-session influence, vector-store contamination |
| 6. Audit and provenance | Mechanisms for understanding what the agent did and why | Attribution loss, reasoning opacity, context provenance failure |

The taxonomy is the **systematic** part of the framework. Practitioners can use it to ask: "What threats exist at each of these surfaces in our deployment?" That question is finite and answerable. The taxonomy works even when specific named threats do not match the deployment.

### Why these six surfaces

The surfaces are derived from the architectural components every agent has: it receives input, has a model that reasons, invokes tools, produces output, may have persistent state, and is observed by audit systems. This is bounded by architecture, not by attacker creativity. New attack patterns at these surfaces will continue to emerge; the surfaces themselves are stable.

If a deployment introduces a genuinely new architectural component (for example, a cryptographic enclave that mediates model decisions, or a federated coordinator across organizational boundaries), the taxonomy may need extension. This is a deliberate design choice: extending the taxonomy is a meaningful act, not an everyday occurrence.

## Threat Exemplars

The framework includes ten named threats, designated AGT-001 through AGT-010. They are **exemplars**, not an exhaustive catalog. Their purpose is to illustrate the threat patterns at each attack surface in enough depth that practitioners can recognize variants in their own deployments.

### What "exemplar" means in practice

| Statement | Truth |
|---|---|
| "These are the 10 threats agents face" | Not true. There are far more. |
| "These are 10 representative threat patterns at each attack surface" | True. |
| "If we have controls against these 10, we are secure against agent threats" | Not true. Coverage of the exemplars is necessary but not sufficient. |
| "These 10 illustrate the patterns; use the taxonomy and methodology to identify threats specific to your deployment" | True, and this is how the framework should be used. |

### How exemplars are selected

The 10 exemplars are chosen to:

1. Cover all six attack surfaces (at least one exemplar per surface)
2. Illustrate genuinely distinct threat patterns rather than variations of the same pattern
3. Be concrete enough to ground discussion of attack scenarios and recommended controls
4. Be common enough in real deployments that practitioners will recognize them

Exemplars may be added, retired, or refined over time as the field matures. Adding an exemplar does not mean a new threat has been discovered; it means a previously underrepresented pattern has been formalized.

### Master exemplar list

| ID | Threat | Primary surface | ATLAS mapping (initial) |
|---|---|---|---|
| AGT-001 | Prompt injection via tool outputs | Input | AML.T0051, AML.T0070 |
| AGT-002 | Authorization confusion (deputy problem) | Tool-use | Mapping under review |
| AGT-003 | Tool-chain abuse | Tool-use | Mapping under review |
| AGT-004 | Data exfiltration via legitimate channels | Output | AML.T0024, AML.T0057 |
| AGT-005 | Audit and provenance failure | Audit and provenance | Mapping under review |
| AGT-006 | Memory and persistence poisoning | Memory and persistence | AML.T0020 (adapted) |
| AGT-007 | Inter-agent trust and delegation abuse | Tool-use | Newly tracked in ATLAS 2026 updates |
| AGT-008 | Output-channel injection | Output | Mapping under review |
| AGT-009 | Goal subversion via context manipulation | Model | Related to AML.T0051 indirect prompt injection |
| AGT-010 | Resource exhaustion via agent loops | Tool-use | Operational, partial mapping |

## Methodology: Discovering Threats in Your Deployment

The exemplars are starting points. The framework provides explicit methodology for identifying threats specific to a deployment that may not match the named exemplars.

### The four-step discovery method

| Step | Question | Output |
|---|---|---|
| 1. Map the deployment to the surfaces | "What does our agent receive at each attack surface? What components implement each surface?" | A surface inventory: for each of the six surfaces, the specific components, channels, data flows, and trust relationships in this deployment |
| 2. Identify exemplar applicability | "Which of the named exemplars (AGT-001 through AGT-010) directly apply to our deployment, and which need adaptation?" | A subset of exemplars that apply directly, plus notes on adaptations needed |
| 3. Look for surface-specific variants | "At each surface, what threat patterns exist that are not covered by the directly applicable exemplars? What architectural choices in our deployment create attack surfaces the exemplars do not anticipate?" | A list of deployment-specific threats, named locally, mapped to the surface taxonomy |
| 4. Cross-reference external catalogs | "What does MITRE ATLAS, OWASP LLM Top 10, or MITRE ATT&CK have to say about the patterns at each surface?" | Pointers to specific techniques in external catalogs that complement the framework's exemplars |

### When the methodology produces a candidate new threat archetype

If a deployment surfaces a threat pattern that:

- Is genuinely distinct from existing exemplars
- Recurs across multiple deployments or contexts
- Is not adequately covered by external catalogs

it is a candidate for addition to the exemplar list in a future framework version. Practitioners are encouraged to propose such candidates through the framework's contribution process. Discovery in the field is the primary mechanism for keeping the exemplar list relevant.

### What the methodology does not do

| Claim | Truth |
|---|---|
| "The methodology will surface all threats in your deployment" | Not true. No methodology can. |
| "The methodology will surface the most important threats in your deployment" | Often true, but depends on the rigor of application. |
| "The methodology replaces threat modeling expertise" | Not true. It structures it. |
| "The methodology produces a finite, complete list of threats" | Not true. It produces a context-aware threat inventory that should be treated as a working document, not a finished one. |

The honest position: this methodology is one tool among several. Practitioners should also consult external catalogs continuously, engage red-team or adversarial-evaluation activity where feasible, and treat agent security as an ongoing concern rather than a one-time exercise.

## Per-Threat Exemplar Template

Each exemplar in `data/threats.json` and Section 5 of the document follows this template. The template is unchanged from v1.

| Field | Type | Description |
|---|---|---|
| `id` | string | Internal identifier, format `AGT-NNN` |
| `title` | string | Short, action-oriented threat name |
| `primary_surface` | enum | One of: input, model, tool-use, output, memory, audit |
| `secondary_surfaces` | array of enums | Other surfaces touched |
| `description` | string | Plain-language explanation in 2 to 4 sentences |
| `attack_scenario` | string | Concrete walkthrough of how the attack happens, in narrative form |
| `affected_components` | array of strings | Specific system components or roles involved |
| `traditional_controls` | array of objects | Existing controls that partially address this; for each: `control`, `why_insufficient` |
| `recommended_controls` | array of strings | Control IDs from the controls library (`CTL-NNN`) |
| `residual_risk` | string | What remains uncontrolled even with recommended mitigations |
| `detection_maturity` | enum | One of: experimental, emerging, established, mature |
| `mitigation_maturity` | enum | Same scale |
| `regulatory_hooks` | array of objects | For each: `regulation`, `article_or_section`, `relevance` |
| `atlas_mapping` | array of strings | MITRE ATLAS technique IDs, may be empty if no current mapping exists |
| `atlas_mapping_notes` | string | Explanation of mapping choice or why no mapping exists |
| `realistic_example` | string or null | Anonymized customer scenario or public incident; null if not yet documented |
| `references` | array of objects | Citations: standards, papers, public incidents, regulatory guidance |
| `exemplar_role` | string | Brief note on what threat pattern this exemplar illustrates and at which surface |

The `exemplar_role` field is new in v2. It makes explicit what pattern each named threat is meant to exemplify. This is the JSON manifestation of the reframe.

### Template field rules

| Rule | Reason |
|---|---|
| `description` and `attack_scenario` must be readable by a non-technical CISO | Audience requirement |
| `traditional_controls` must explain *why* existing controls are insufficient, not just list them | This is the differentiated insight of the framework |
| `recommended_controls` references the controls library; controls are defined once and reused | Avoids duplication, supports the web tool's filtering |
| `regulatory_hooks` should cite specific articles, not regulations in the abstract | Reinforces the crosswalk and protects against vague claims |
| `realistic_example` may be null but should be populated where possible | Examples make the threat memorable; absence of example is honest |
| `atlas_mapping` may be empty; this is acceptable for genuinely new agent threats | Honest about where ATLAS coverage lags |
| `exemplar_role` is required | Anchors the exemplar in its illustrative purpose |
| Severity and likelihood scoring are deliberately omitted | Subjective, dates poorly, encourages false precision |

## Relationship to Existing Frameworks

The framework is explicit about its relationship to existing work. The exemplar reframe makes this relationship clearer than v1: external catalogs are not "competitors" but continuously-maintained sources that complement the framework.

| Framework | Relationship in v2 |
|---|---|
| MITRE ATLAS | Continuously-maintained source for adversarial ML and agent technique IDs. The framework references ATLAS as the technique-level catalog and uses ATLAS IDs as a secondary attribute on exemplars. |
| MITRE ATT&CK | Continuously-maintained source for general adversarial techniques. Relevant when agent threats overlap with traditional adversarial patterns. |
| OWASP Top 10 for LLM Applications | Continuously-maintained source for LLM application risks at the component level. Complements the framework by addressing risks below the agent runtime layer. |
| NIST AI 100-2 / AI RMF | Risk-management framing and adversarial ML taxonomy. The framework's risk discussion aligns with NIST principles. |
| Google SAIF | Closest peer in scope but broader. The framework focuses on EU regulatory mapping where SAIF does not. |
| Anthropic agentic misalignment research | Research-grade insight informing the framework. The framework operates at the enterprise-deployment level; research operates at the model-behavior level. |
| STRIDE | Threat-modeling taxonomy that influenced this framework's surface-based approach. STRIDE is general; this framework is agent-specific. |

The framework's value is in three things that no individual external source provides together: the agent-specific attack surface taxonomy, the EU regulatory mapping, and the practitioner-grade implementation guidance. External catalogs are referenced for the technique-level detail the framework deliberately does not duplicate.

## Working Conventions Recap

| Convention | Rule |
|---|---|
| No em dashes anywhere | Use commas, semicolons, periods, or parentheses |
| Tables over bullet points | Default to tables for any list of three or more comparable items |
| Cite primary sources | Regulation texts, NIST, MITRE, ENISA, BSI, original research |
| Acknowledge uncertainty | Where ATLAS mapping is unclear, where detection is immature, where examples are not yet documented, say so |
| Voice | First-person practitioner perspective; the reader should feel they are learning from someone who has done this work |
| Length discipline | The framework as a whole (Section 5 of the practitioner guide) is 4 to 6 pages including introduction and the threat exemplars; the methodology section adds 1 to 2 pages |

## Implications of the Reframe for Other Framework Documents

The reframe affects several adjacent documents and decisions. Each is addressed below.

### Practitioner guide section 5

Section 5 is renamed from "Agent-Specific Threat Model" to **"Agent Threat Patterns and Exemplars"**. The section opens with the attack surface taxonomy as the primary structural claim, follows with the methodology for threat discovery, and presents the 10 named threats as exemplars within this structure. The exemplars themselves are unchanged in content.

### Section 4 (regulatory crosswalk)

The crosswalk gains a layered presentation: regulations map directly to attack surfaces (the durable structural claim), and exemplar threats provide the reasoned defense. This addresses the earlier concern about regulation-to-control crosswalks being too compliance-checklist-shaped.

### Section 8 (gaps and open problems)

Section 8 explicitly acknowledges:

- The exemplar list is not exhaustive
- The control library is bounded and there are gaps
- The regulatory mapping reflects current understanding and will evolve
- Threat discovery in specific deployments is essential and cannot be replaced by the framework

This framing was already planned for v1 publication. The reframe makes it more explicit and defensible.

### Web tool

The web tool's primary navigation gains the attack surface taxonomy as the top-level entry point. Practitioners can:

1. Browse by attack surface
2. Browse by exemplar threat
3. Browse by regulation
4. Browse by control
5. Use a guided "discover threats in your deployment" flow that walks the four-step methodology

The fifth navigation mode is a v2 enhancement that can be deferred but is now part of the design vocabulary.

### Vendor mapping interface

Vendor mappings continue to map to controls, not to exemplars. The reframe does not affect the contribution interface. Vendors describe how their products implement controls; controls address threat patterns; threat patterns are illustrated by exemplars.

## Open Questions for Future Sessions

| Question | Why it matters | When to resolve |
|---|---|---|
| Should the methodology section include a worked example of applying it to a hypothetical deployment? | Makes the methodology concrete; risks dating quickly | When drafting section 5 of the practitioner guide |
| Should exemplars include explicit "variant" subsections for common adaptations? | Bridges the gap between exemplars and deployment-specific threats | After section 5 is drafted; revisit based on feedback |
| Should the framework adopt or define a notation for deployment-specific threats (e.g., "DEP-NNN")? | Helps practitioners document their own findings | Likely v3 concern; deferred |
| How does the methodology interact with formal threat modeling techniques (STRIDE, PASTA)? | Practitioners may want to combine approaches | Address in section 7 (implementation considerations) |

## Summary of the Reframe

The framework is now positioned as: **an attack surface taxonomy plus methodology, illustrated by exemplar threats, complemented by external catalogs, and mapped to EU regulatory requirements through a control library.**

The phrase "the threats agents face" is replaced by "exemplars of agent threat patterns." This single change of framing makes the framework defensible against the completeness criticism and more useful to practitioners who must reason about threats in their specific deployments.

No threat content needs to change. The data files, the exemplars, the control mappings, the regulatory hooks all remain valid. What changes is the framing and the addition of the methodology section.
