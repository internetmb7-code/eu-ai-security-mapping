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

### Deferred

- AGT-001 (Prompt injection via tool outputs) is not yet ported. The v1 control library work assumed AGT-001 was committed; prerequisite was unmet, so AGT-001-touching steps from the original control library prompt (source markdown update, threats.json entry update) were skipped. To be addressed in a subsequent session.
- v2 threat model framework reframe (positioning the 10 named threats as exemplars within the attack surface taxonomy, plus an `exemplar_role` field on threat entries) is not yet applied. To be addressed after AGT-001 is ported.
