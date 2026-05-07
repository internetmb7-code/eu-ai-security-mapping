# v1 Final State Report

Date: 2026-05-07
Purpose: Single-document summary of where the EU AI Security Mapping framework stands at v1 content lock, what was decided versus deferred, and the bounded list of next steps.

## v1 publication status

| Dimension | State |
|---|---|
| Validation flags | 1 (advisory only; carried forward; not blocking). See `validation-report-2026-05-07-final.md`. |
| Section completeness | All canonical sections (1 through 9) present and within tolerance. Section 5 exemplar bodies live in `docs/sections/05-threat-model.md`; canonical document holds framing only at v1, with the v1.1 merge recorded. |
| Control library | CTL-001 through CTL-005 fully populated. CTL-006 through CTL-033 are reserved IDs for v2. |
| Threat catalog | AGT-001 and AGT-002 fully populated. AGT-003 through AGT-010 are compressed exemplars at v1; v1.1 commitment recorded for parity. |
| Regulatory currency | NIS2UmsuCG (Germany, in force 2025-12-06), NISG 2026 (Austria, in force 2026-10-01), BSI C5:2026, Digital Omnibus trilogue state, all current as of 2026-05-07. |
| Recommendation | PUBLISHABLE |

## What this session locked

| Decision | Where recorded |
|---|---|
| Annex B (worked example) deferred to v1.1; all forward-references removed from Section 1 | `docs/sections/01-executive-summary.md`, `docs/main-document/EU-AI-Security-Mapping.md`, `PROJECT_STATUS.md`, `CHANGELOG.md`. Commit `ddaa056`. |
| AGT-003 through AGT-010 remain compressed exemplars at v1; parity expansion deferred to v1.1 | `docs/sections/05-threat-model.md` ("Note on v1 scope" before AGT-001), `docs/sections/08-gaps.md` (subsection 8.7), canonical document Section 5 framing and Section 8.7. Commit `cd158e9`. |
| Canonical document Section 5 holds framing only at v1; exemplar-body merge deferred to v1.1 | Canonical document Section 5 "Note on v1 scope", Section 8.7 commitments. Commit `cd158e9`. |
| (CTL-005, AGT-004) symmetry resolved: spec aligned with `data/mappings.json` (primary) | `docs/sections/06-controls/CTL-005.md`, canonical document CTL-005 spec line 917. Commit `cd158e9`. |
| Section 1 rewritten as CISO executive briefing; Section 5 provenance subsection added | Commit `6668a0f` (preceding this finalization session). |
| All Commit 1 validation-flag work (Section 4 bridging-threat fixes, regulatory currency, structural fixes) | Commit `8fe3328` (preceding this finalization session). Verified still in place. |

## What was honestly omitted rather than fabricated

| Item | Why |
|---|---|
| A fresh "Commit 1" in this session resolving validation flags | The flags from `validation-report-2026-05-06.md` were already resolved in `8fe3328` and confirmed in `validation-report-2026-05-06-rerun.md`. Creating an empty commit would have manufactured fake activity. The rerun and this final report record the actual provenance. |

## v1.1 commitments (bounded extensions of v1 content)

Recorded in Section 8.7 of both the section file and the canonical document:

| Commitment | What it covers |
|---|---|
| Populate AGT-003 through AGT-010 to parity with AGT-001 and AGT-002 | Add attack scenario depth, traditional controls and why insufficient, full residual-risk analysis, detection and mitigation maturity, and realistic deployment examples. |
| Merge full exemplar bodies into the canonical document | The single-file artifact becomes self-contained once exemplar parity is reached. |
| Annex B (worked example) | Concrete deployment scenario walked through threat model, five v1 controls, regulatory crosswalk. Requires sanitized deployment context. |

These are distinct from v2 work (Section 8 "What v2 will address"), which extends the control library and expands the framework scope.

## v1 advisory flags (not blocking)

| Flag | Description | Disposition |
|---|---|---|
| 3.2 | CTL-006 through CTL-033 literal occurrences in `CONTROL_LIBRARY_FRAMEWORK.md`, `CHANGELOG.md`, and canonical document line 431 | Advisory only. All occurrences are explicitly contextualised as "reserved for v2" or as historical CHANGELOG entries documenting consolidation. None presented as v1 controls. Optional cleanup: add a one-line comment block marking the entries as v2-reserved so future literal checks can suppress the warning. |

## Pre-release checklist (suggested, not part of this session's scope)

| Item | Notes |
|---|---|
| Peer review by named subject-matter experts | The framework's curation choices (which threats are exemplars, which controls are v1) benefit from independent practitioner review. |
| License confirmation | Confirm the published license (CC-BY-SA, MIT, or similar) and add a `LICENSE` file. |
| Cross-reference / consistency pass | Identified in `PROJECT_STATUS.md` next-session option A; one final read-through to catch any cross-section drift introduced during the rapid finalization. |
| DOI or stable identifier | If publishing as a citable artifact, mint a DOI via Zenodo or equivalent. |

## Session commit chain

| Commit | Purpose |
|---|---|
| `6668a0f` | Rewrite Section 1 as CISO executive briefing; add Section 5 provenance (preceding finalization session) |
| `ddaa056` | Remove Annex B references from Section 1; defer worked example to v1.1 |
| `cd158e9` | Lock v1 scope: compressed AGT note, Section 8.7, CTL-005 AGT-004 |
| (this commit) | Add final validation report and v1 final state report |

## Where to read what

| Topic | File |
|---|---|
| Final validation results | `docs/working-notes/validation-report-2026-05-07-final.md` |
| v1 publishable confirmation (post-fix rerun) | `docs/working-notes/validation-report-2026-05-06-rerun.md` |
| Original validation flags (historical) | `docs/working-notes/validation-report-2026-05-06.md` |
| Project state and active work | `PROJECT_STATUS.md` |
| Per-session change log | `CHANGELOG.md` |
| v1.1 commitments | `docs/sections/08-gaps.md` subsection 8.7 |
| v2 priorities | `docs/sections/08-gaps.md` "What v2 will address" |
