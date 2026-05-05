# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Initial repository scaffolding (directories, section stubs, JSON schemas, workflow placeholders).
- Optional Appendix A stub `docs/sections/10-appendix-servicenow-mapping.md` for mapping generic controls to ServiceNow products. Non-canonical; the main document remains regulation-agnostic.
- Optional `servicenow_mapping` field on the controls schema to support the appendix without coupling the core schema to any vendor.
- Added AGT-002 (Authorization Confusion / Deputy Problem) as fully populated threat entry. Covers excess privilege, cross-tenant deputy, and delegation ambiguity sub-patterns. References controls CTL-008, CTL-009, CTL-011, CTL-016, CTL-022, CTL-029, CTL-031 (defined in later phase).
- Added v1 control library framework document `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md`. Establishes scope, the per-control template, the implementation domain taxonomy, and the relationship between controls and existing security standards (NIST SP 800-53, ISO 27001 Annex A, BSI grundschutz).
- Populated CTL-001 (Identity and Authorization Context Propagation) in `data/controls.json` as the reference control entry. Domain: identity. Function: preventive. Maturity: emerging. Includes operational considerations, common failure modes, regulatory basis (EU AI Act, NIS2, DORA, GDPR), existing standard mappings, and references.
- Added stub entries for CTL-002 (Tool-output and context provenance), CTL-003 (Action verification at high-impact boundaries), CTL-004 (Authorization-aware output filtering), CTL-005 (End-to-end audit and accountability) with title and domain assigned; full population deferred to subsequent sessions.
- Consolidated 11 placeholder control IDs from prior AGT-002 work (CTL-008, CTL-009, CTL-011, CTL-016, CTL-022, CTL-029, CTL-031, plus CTL-014, CTL-021, CTL-027, CTL-033 reserved for AGT-001) into the v1 library (CTL-001 through CTL-005). The retired IDs are no longer referenced anywhere in the repository.
- Updated AGT-002 entry in `data/threats.json`, `docs/sections/05-threat-model/AGT-002.md`, `docs/sections/05-threat-model.md`, and `docs/main-document/EU-AI-Security-Mapping.md` section 5 to reference the consolidated control IDs (CTL-001 primary, CTL-004 primary, CTL-005 primary, CTL-003 secondary).
- Replaced retired control IDs in `data/mappings.json` `control_mitigates_threat`. Replaced the legacy `control_placeholders` entries with stub markers for CTL-002 through CTL-005.
- Added section 6 (Recommended Controls and Patterns) to the canonical document `docs/main-document/EU-AI-Security-Mapping.md` with introductory paragraph and the CTL-001 reference entry. CTL-002 through CTL-005 listed as forthcoming stubs.

- Added AGT-001 (Prompt Injection via Tool Outputs) as fully populated threat entry. Covers the indirect injection vector where adversarial instructions reach the agent through legitimate tool outputs (retrieval, web fetch, document, knowledge base, inter-agent communication). Source markdown placed at `docs/sections/05-threat-model/AGT-001.md`. References v1 controls CTL-002 (primary), CTL-003 (primary), CTL-001 (secondary), CTL-005 (secondary). Includes `exemplar_role` text anticipating the v2 threat model reframe.
- Populated AGT-001 entry in `data/threats.json` with consolidated v1 controls. Entry placed as the first array element so AGT-001 precedes AGT-002 in document order.
- Added AGT-001 mappings in `data/mappings.json`: 7 `threat_addresses_requirement` entries (EU AI Act Art. 9, 14, 15; NIS2 Art. 21; DORA Art. 6 to 8; GDPR Art. 22, 32), 4 `control_mitigates_threat` entries (CTL-002 primary, CTL-003 primary, CTL-001 secondary, CTL-005 secondary), and 5 outgoing `threat_related_to_threat` entries (AGT-002, AGT-003, AGT-006, AGT-008, AGT-009). The pre-existing AGT-002 to AGT-001 reverse relationship is retained.
- Added AGT-001 entry to `docs/sections/05-threat-model.md` immediately before AGT-002, following the same template as AGT-002.
- Added PROJECT_STATUS.md at repository root: living checklist of project scope, status, decisions, and next-session options. Reflects current state including AGT-001 and AGT-002 committed, control library v1 with CTL-001 populated, and the pending v2 framework reframe.

### Deferred

- v2 threat model framework reframe (positioning the 10 named threats as exemplars within the attack surface taxonomy, plus an `exemplar_role` field on threat entries) is not yet applied. AGT-001 already includes the `exemplar_role` text in its source markdown and threats.json entry; AGT-002 still needs the field backfilled when the v2 reframe is applied.
