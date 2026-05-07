A framework that overstates its coverage will be discovered by serious readers. The credibility of the rest of this document depends on this section being honest about what is missing and why. The categories below are the limits worth naming, with practical implications for how practitioners should use the framework today.

## 8.1 The threat catalog is not exhaustive

The 10 named threats in section 5 are exemplars within the attack surface taxonomy, not a complete enumeration. The durable contribution is the taxonomy and the threat-discovery methodology in section 5; the named threats illustrate the patterns. Practitioners who address all 10 exemplars have addressed 10 illustrative patterns, not agent security as a whole. Coverage requires applying the methodology to the specific deployment.

The catalog will grow as deployments mature and new patterns become recognizable. v2 of this framework will revisit the exemplar list based on field experience.

## 8.2 The v1 control library has known coverage gaps

The five v1 controls cover the threat catalog with deliberate honesty about where coverage is partial.

| Threat | Coverage in v1 | Gap |
|---|---|---|
| AGT-003 (tool-chain abuse) | Partial | CTL-003 was designed for individual high-impact actions; extension to composed actions requires runtime instrumentation v1 does not specify |
| AGT-006 (memory and persistence poisoning) | Partial | CTL-002 covers tool-output provenance; memory and vector store provenance follows similar principles but needs its own treatment |
| AGT-008 (output-channel injection) | Partial | Output sanitization for syntactic exploits in downstream parsers is not addressed by any v1 control |
| AGT-009 (goal subversion via context manipulation) | Weak | Genuinely hard to address with technical controls alone; v1 controls provide only partial coverage |
| AGT-010 (resource exhaustion via agent loops) | Partial | Resource governance is implicit in CTL-003 but not explicit |

These gaps are not implementation defects. They are design choices to keep v1 small and bounded. They are also the strongest candidates for v2 control work.

## 8.3 Reasoning provenance is fundamentally limited

CTL-005 captures audit and accountability across user attribution, agent attribution, context provenance, decision provenance, and authorization basis. One of these dimensions, model reasoning provenance, is fundamentally constrained by current LLM technology. Models do not produce reliable, deterministic explanations of their own decisions. Where models emit chain-of-thought, the audit can capture it. Where they do not, the audit cannot synthesize what was not produced.

This is a limit of the underlying technology, not a gap that v2 of this framework will close. Practitioners should treat agent decisions as partially opaque and design oversight assuming this constraint. For high-stakes decisions, human review at the action boundary is the only fully reliable accountability mechanism, which is why CTL-003 (action verification at high-impact boundaries) is the structural acknowledgment of this limit. Interpretability research may improve the situation in time, but the framework treats it as a constraint to design around rather than a gap to close.

## 8.4 The framework lacks documented incident examples

Each threat exemplar in section 5 includes a `realistic_example` field that is currently null. The framework is theoretically grounded in attack patterns and structural reasoning but does not yet illustrate threats with public incident data, anonymized customer scenarios, or documented breaches. This makes the framework less vivid for readers unfamiliar with agent security, and it makes the threats easier to dismiss as hypothetical even though the patterns are observed in research and in the field.

Populating realistic examples is a v2 priority. Sources will include public security research disclosures, anonymized scenarios from regulatory enforcement actions where available, and contributed examples from practitioner engagements where they can be sanitized for publication. Until v2, readers should treat the threat exemplars as well-grounded patterns awaiting evidentiary illustration in this specific document.

## 8.5 The vendor mapping interface is unproven

The framework is designed as a platform: vendor-specific control mappings are intended to be contributed by vendors and the community, not authored by the framework maintainer. The contribution interface is documented and the schema is defined, but no vendor mappings have been contributed as of v1 publication.

The platform model is unproven. Its value depends on adoption that has not yet happened. v2 evaluation will examine whether the contribution interface has produced meaningful mappings and what to adjust if not.

## 8.6 The framework does not address governance, culture, or organizational change

This framework is technical-practitioner-oriented. It addresses threats, controls, and regulatory mappings at the architectural and operational level. It does not address the organizational work of integrating AI security into procurement, shifting development culture, or building cross-functional governance. This is a deliberate scope choice. Most enterprise AI security failures will be governance failures as much as technical control failures, but addressing both in one document would dilute the focus and produce a less useful technical reference. Organizations should pair this framework with NIST AI RMF, ISO/IEC 42001, or ENISA AI cybersecurity guidance for the governance layer.

## 8.7 v1.1 commitments

The following items were intentionally deferred from v1 to keep the framework scope bounded and publishable. They are recorded here as commitments for the v1.1 release rather than v2, because they extend existing v1 content to parity rather than introducing new control or threat work.

| Commitment | What it covers | Why deferred from v1 |
|---|---|---|
| Populate AGT-003 through AGT-010 to parity with AGT-001 and AGT-002 | Add attack scenario depth, traditional controls and why insufficient, full residual-risk analysis, detection and mitigation maturity, and realistic deployment examples for the eight compressed exemplars in Section 5 | Time-bounded curation; the compressed form is sufficient for pattern recognition at v1, but practitioners using the framework for engagement-grade threat modeling need the deeper form |
| Merge full exemplar bodies into the canonical document | The canonical document at v1 contains the Section 5 framing only; exemplar bodies live in `docs/sections/05-threat-model.md`. v1.1 will inline the full bodies in the canonical document so the single-file artifact is self-contained | Avoided duplication while exemplar depth was uneven; defer to when AGT-003 through AGT-010 reach parity |
| Annex B (worked example) | A concrete deployment scenario walked through the threat model, the five v1 controls, and the regulatory crosswalk; intended to make the framework vivid for readers unfamiliar with agent security | The worked example requires a specific deployment context the framework does not yet have a sanitized example for; deferred rather than fabricated |

These commitments are bounded extensions of existing v1 content. They are distinct from v2 work, which extends the control library and expands the framework scope.

## What v2 will address

The gaps above produce a v2 control library priority list:

| Priority | Addresses |
|---|---|
| Memory and persistence provenance control | AGT-006 coverage gap |
| Runtime resource governance control | AGT-010 coverage gap |
| Output sanitization control or refinement | AGT-008 coverage gap |
| CTL-003 refinement for composed actions | AGT-003 coverage gap |

Beyond the control library, v2 will also populate realistic examples for the threat exemplars, evaluate the vendor mapping platform, and consider whether the methodology section needs strengthening for goal subversion (AGT-009), which remains the threat with the weakest v1 coverage.

v1 is bounded honestly to what it can defend. The framework is more useful for being explicit about that boundary than for pretending coverage it does not have.
