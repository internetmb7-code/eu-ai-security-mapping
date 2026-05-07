# v1 Validation Report (Final, 2026-05-07)

Date: 2026-05-07
Scope: Final validation pass following the v1 finalization session (commits `6668a0f`, `ddaa056`, `cd158e9`). Categories 1, 2, 3.4, 5.1, 5.3, 5.5 carried forward from the 2026-05-06 rerun (no inputs changed). New checks confirm the v1 scope decisions in Section 5, Section 8.7, and the (CTL-005, AGT-004) symmetry resolution. Annex B reference removal verified across Section 1 and the canonical document.

Predecessor reports:
- [`validation-report-2026-05-06.md`](validation-report-2026-05-06.md) (commit `de94ea6`): original report (9 flags, NOT PUBLISHABLE).
- [`validation-report-2026-05-06-rerun.md`](validation-report-2026-05-06-rerun.md) (commit `ed11bf0`): post-fix rerun (1 advisory flag, PUBLISHABLE).

## Summary

| Category | Checks run | Pass | Auto-fixed | Flagged for review |
|---|---|---|---|---|
| 1. Repository-wide mechanics | 4 | 4 | 0 | 0 |
| 2. Structural consistency | 4 | 4 | 0 | 0 |
| 3. Data-model consistency | 5 | 4 | 0 | 1 (advisory only, 3.2; carried forward) |
| 4. Source accuracy | 4 | 4 | 0 | 0 |
| 5. Regulatory currency (web search) | 5 | 5 | 0 | 0 |
| 6. Convention compliance | 4 | 4 | 0 | 0 |
| 7. v1-finalization deltas | 5 | 5 | 0 | 0 |
| **Total** | **31** | **30** | **0** | **1** |

Recommendation: **PUBLISHABLE**. The single residual flag (3.2 advisory) is unchanged from the 2026-05-06 rerun and was already accepted as advisory. All v1 finalization deltas verified.

## Category 7: v1-finalization deltas (new this pass)

| Check | Result |
|---|---|
| 7.1 Annex B references absent from Section 1 (file + canonical) | Pass. Section 1.7 reading-guide table no longer references Annex B; reading-order paragraphs no longer forward-reference an unwritten section. |
| 7.2 Section 5 "Note on v1 scope" present in section file before AGT-001 | Pass. The note distinguishes AGT-001/AGT-002 (fully populated) from AGT-003 through AGT-010 (compressed) and forward-references Section 8 commitments. |
| 7.3 Canonical document Section 5 "Note on completeness" replaced with honest "Note on v1 scope" | Pass. The misleading "exemplar entries below provide AGT-001..." phrasing is gone; the new note describes where exemplar bodies actually live (section file and `data/threats.json`) and records the v1.1 merge commitment. |
| 7.4 Section 8.7 "v1.1 commitments" present in section file and canonical document | Pass. Three deferrals recorded: AGT-003 through AGT-010 parity expansion, exemplar-body merge into the canonical document, Annex B (worked example). |
| 7.5 (CTL-005, AGT-004) symmetry: spec lists AGT-004 with relationship matching `data/mappings.json` (primary) | Pass. `docs/sections/06-controls/CTL-005.md` "Threats addressed" table has AGT-004 (primary). Canonical document line 917 lists `AGT-004 (primary)` in the inline threats-addressed line. `data/mappings.json` `control_mitigates_threat` has the same relationship. |

## Categories 1 to 6: Carried forward

No inputs changed for categories 1.1 to 1.4, 2.1 to 2.4, 3.1, 3.3 to 3.5, 4.1 to 4.4, 5.1 to 5.5, and 6.1 to 6.4 since the 2026-05-06 rerun. The em-dash check was rerun across all framework body files (including this session's edits to Section 5, Section 6 CTL-005, Section 8, and the canonical document) and confirmed zero hits in the framework body. The advisory 3.2 flag (CTL-006 through CTL-033 literal occurrences in `CONTROL_LIBRARY_FRAMEWORK.md`, `CHANGELOG.md`, and the canonical document line 431) is unchanged and remains advisory.

## Cross-references against Commit 1 work

Commits referenced in Commit 1 of the v1 finalization plan were already in `8fe3328` ("Resolve v1 validation flags") committed before this session. Re-verification:

| Verification | Result |
|---|---|
| Zero `CTL-004 [via AGT-001` in framework body | Confirmed (1 historical hit in `validation-report-2026-05-06.md` only) |
| Zero `C5:2025` in framework body | Confirmed (1 historical hit in `validation-report-2026-05-06.md` only) |
| Germany NIS2UmsuCG, Austria NISG 2026, BSI C5:2026 in `regulatory-facts.md` | Confirmed |
| Section 9 reads "C5:2020 and C5:2026" | Confirmed |
| Section 2 length within tolerance | Confirmed (64 lines) |

No further fixes were required for Commit 1 work; the corresponding session commit was therefore a no-op and was honestly omitted rather than fabricated.

## Recommended next actions

| Priority | Action |
|---|---|
| 1 | **Publishable**: framework v1 content is locked. Pre-release checklist (peer review by named SMEs, license confirmation, cross-reference pass) is the next step. |
| 2 | v1.1 work as recorded in Section 8.7: populate AGT-003 through AGT-010 to AGT-001/AGT-002 parity, merge full exemplar bodies into the canonical document, and write Annex B (worked example). |
| 3 | Optional: address the advisory 3.2 flag (CTL-006 through CTL-033 literal occurrences) by adding a one-line comment block marking those entries as v2-reserved or historical. |
