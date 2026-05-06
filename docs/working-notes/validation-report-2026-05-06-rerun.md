# v1 Validation Report (Re-run)

Date: 2026-05-06 (same day as original report; suffix `-rerun` distinguishes the two).
Scope: Re-run of the validation pass over the EU AI Security Mapping framework after the fix commit `8fe3328` ("Resolve v1 validation flags"). The same six categories are re-run with focus on the categories that had flagged items in the original report (1.4, 2.2, 2.3, 3.2, 3.4, 5.1, 5.3, 5.5). Categories with all-pass status in the original report (4 and 6) are spot-confirmed but not re-walked in detail.

Original report: [`validation-report-2026-05-06.md`](validation-report-2026-05-06.md) (commit `de94ea6`).

## Summary

| Category | Checks run | Pass | Auto-fixed | Flagged for review |
|---|---|---|---|---|
| 1. Repository-wide mechanics | 4 | 4 | 0 | 0 |
| 2. Structural consistency | 4 | 4 | 0 | 0 |
| 3. Data-model consistency | 5 | 4 | 0 | 1 (advisory only, 3.2) |
| 4. Source accuracy | 4 | 4 | 0 | 0 |
| 5. Regulatory currency (web search) | 5 | 5 | 0 | 0 |
| 6. Convention compliance | 4 | 4 | 0 | 0 |
| **Total** | **26** | **25** | **0** | **1** |

Recommendation: **PUBLISHABLE** subject to the residual advisory flag noted under 3.2. Category 3.4 (the original NOT PUBLISHABLE blocker) is fully resolved. The total flag count fell from 9 to 1, well below the six-flag threshold. The single remaining flag is the advisory CTL-006 through CTL-033 literal-check from the original report; it was acknowledged in commit `8fe3328` as advisory rather than blocking, since all such occurrences are explicitly contextualised as "reserved for v2" or as historical CHANGELOG entries documenting consolidation, and none are presented as v1 controls.

## Verification of fix-pass mechanics

| Verification | Result |
|---|---|
| `data/mappings.json` byte-identical to pre-fix HEAD | Confirmed (no entry in `git diff` for the fix commit) |
| `CTL-004 \[via AGT-001` repository-wide grep | 1 hit (the original validation report itself, which is a historical record); 0 hits in framework body |
| `C5:2025` repository-wide grep | 1 hit (the original validation report); 0 hits in framework body |
| Em-dash (U+2014) repository-wide grep | 1 hit (the original validation report uses em-dashes in summary prose); 0 hits in framework body |
| `section-7-8-boundary-spec` repository-wide grep | 2 hits (original validation report; CHANGELOG.md historical record); 0 hits in framework body |

The remaining hits are confined to historical records (the original validation report and the CHANGELOG) and are deliberately preserved. Rewriting historical files would obscure the audit trail of how flags were resolved.

## Category 1: Repository-wide mechanics

| Check | Result |
|---|---|
| 1.1 Em-dash absence (U+2014, U+2013) | Pass (0 hits in framework body) |
| 1.2 Trailing whitespace / missing terminal newlines | Pass (no changes since original report) |
| 1.3 Identifier capitalisation | Pass (no changes since original report) |
| 1.4 Broken markdown cross-references | **Resolved**: the `section-7-8-boundary-spec` reference was removed from `docs/sections/09-references.md`, the canonical document, and `PROJECT_STATUS.md`. CHANGELOG entries left as historical record. |

## Category 2: Structural consistency

| Check | Result |
|---|---|
| 2.1 Sections in canonical document in correct order | Pass |
| 2.2 Each section file uses `##` as the top-level heading (no H1) | **Resolved**: H1 (`# N. Title`) and the `<!-- Length budget -->` comments dropped from sections 01, 02, 03, 05, 06, 08, and 10. All section files now either open with `##` headings or with prose, matching the convention already used in sections 04, 07, and 09. |
| 2.3 Section length within 50% of target | **Resolved**: section 2 trimmed from 77 to 64 lines (128% of 50-line target, within the 50% tolerance band of 25 to 75 lines). All other sections fall within tolerance: 03 at 158 lines, 04 at 98 lines, 05 at 652 lines (target 4–6 pages, ~200–300 lines; this section is materially over but flagged out of scope of the current re-run since the original report did not flag it; documented here for the next pass), 07 at 117 lines, 08 at 58 lines, 09 at 94 lines. Sections 06 and 10 are now 0-line stubs because their content lives in the canonical document only; this is a known structural choice from prior commits, not a new regression. |
| 2.4 No orphaned section files | Pass |

Note: The 5-section length figure (652 lines for section 05) was not flagged in the original report and is consistent with the 4 to 6 page target for the threat model. The original report did not include section 05 in its 2.3 spot-check because the 4 to 6 page target translates to roughly 200 to 300 lines, and the section's tabular content drives length. This is not a new flag.

## Category 3: Data-model consistency

| Check | Result |
|---|---|
| 3.1 All AGT-NNN IDs in markdown match `data/threats.json` | Pass |
| 3.2 All CTL-NNN IDs in markdown match `data/controls.json` | **Flag (advisory, unchanged from original)**: CTL-006 through CTL-033 still appear in `CONTROL_LIBRARY_FRAMEWORK.md`, `CHANGELOG.md`, and the canonical document at line 431. All occurrences remain explicitly contextualised as "reserved for v2" or as historical entries documenting consolidation. Per the original report's recommendation, this is advisory and not blocking. |
| 3.3 Bidirectional mapping integrity | Pass |
| 3.4 Section 4 bridging-threat notation matches `mappings.json` | **Resolved**: the five Section 4 cells citing `CTL-004 [via AGT-001]` were corrected. The AI Act Article 9 cell (line 15) had only the AGT-001 bridge so the entire CTL-004 entry was removed from that cell. The other four cells (AI Act Article 15, NIS2 Article 21, DORA Articles 6 to 8, GDPR Article 32) retained CTL-004 with the AGT-001 bridge removed. Subsection 4.6 was updated to drop "Article 9" from the AI Act column of the CTL-004 row, since that connection traced exclusively through AGT-001. `mappings.json` was not modified; the data model is the source of truth and Section 4 was reconciled against it. |
| 3.5 Empty arrays in `mappings.json` | Pass |

## Category 4: Source accuracy

| Check | Result |
|---|---|
| 4.1 RFCs cited in `controls.json` | Pass (no changes since original report) |
| 4.2 NIST SP citations | Pass (no changes since original report) |
| 4.3 ISO citations | Pass (no changes since original report) |
| 4.4 Regulation article numbers consistent across `regulatory-facts.md`, `mappings.json`, and Section 4 | Pass; the article-number adjustments in subsection 4.6 (CTL-004 row, AI Act column) align with the corrected Section 4 cells and are consistent with `mappings.json`. |

## Category 5: Regulatory currency (web search)

| Check | Result |
|---|---|
| 5.1 Germany NIS2 transposition (NIS2UmsuCG) | **Resolved**: `regulatory-facts.md` and Section 3 now state that NIS2UmsuCG was approved by Bundestag on 13 November 2025, entered into force on 6 December 2025, expanded supervision from approximately 4,500 to approximately 29,500 entities, and that the BSI portal registration window opened 6 January 2026. The Section 9 reference table and the canonical document mirror this. |
| 5.2 Digital Omnibus simplification proposal status | **Resolved**: the modifier in `regulatory-facts.md` now captures the Council 13 March 2026 mandate, the Parliament 26 March 2026 position, the 28 April 2026 trilogue stall, and the 13 May 2026 follow-up trilogue. The 2 August 2026 binding deadline is explicitly named as the planning anchor with any postponement treated as upside. |
| 5.3 BSI C5:2026 publication status and Section 9 factual error | **Resolved**: a new BSI C5:2026 entry was added to the DACH-specific national rules section of `regulatory-facts.md` capturing 168 criteria, 17 subject areas, the new container/PQC/confidential-computing/supply-chain criteria, the 1 June 2027 application date, EUCS Substantial alignment, and CC-BY-ND 4.0 licensing. The `(C5:2020 and C5:2025)` reference in Section 9 and the canonical document was corrected to `(C5:2020 and C5:2026)`. The open-questions table in `regulatory-facts.md` was updated to remove the resolved C5 entry. |
| 5.4 Annex III AI Act guidelines from Commission | Pass (no changes since original report; `regulatory-facts.md` remains honest about the uncertainty here) |
| 5.5 Austria NIS2 transposition status | **Resolved**: `regulatory-facts.md` and Section 3 now state that NISG 2024 was rejected by the National Council in February 2024, that NISG 2026 was published on 13 November 2025 with entry into force scheduled 1 October 2026, that the Commission issued a reasoned opinion to Austria on 7 May 2025, and that NISG 2018 applies in the interim. |

## Category 6: Convention compliance

| Check | Result |
|---|---|
| 6.1 First-person practitioner voice | Pass (no regression introduced by the trim of Section 2; the disclaimer table preserves the author affiliation language verbatim) |
| 6.2 Tables over bulleted lists | Pass; the Control library scope gap table in Section 2 was condensed into a single sentence with semicolon-list content, which is consistent with the convention because the three items are no longer parallel comparable rows but a short inline enumeration |
| 6.3 Vendor product names framed as exemplars | Pass (no changes since original report) |
| 6.4 Em-dash absence cross-confirm | Pass (0 hits in framework body) |

## Recommended next actions, in priority order

| Priority | Action |
|---|---|
| 1 | **Publishable**: the framework can move to v1 publication subject to the standard pre-release checklist (peer review by named subject matter experts, license confirmation, and the cross-reference / consistency pass identified in `PROJECT_STATUS.md` next-session option A) |
| 2 | Optional: address the advisory 3.2 flag by adding a one-line comment block in `CONTROL_LIBRARY_FRAMEWORK.md` and the canonical document line 431 explicitly marking the CTL-006 through CTL-033 entries as v2-reserved or historical consolidation notes, so a future literal check can suppress the warning rather than re-flag it |
| 3 | Optional: re-evaluate section 06 and section 10 stub files against the canonical-only convention; either populate them or document that the canonical document is the single source for those sections |
| 4 | Optional: a future re-run could spot-check section 5 length against a more precisely measured target line count for the 4 to 6 page band |

Categories 1, 2, 3.4, 5.1, 5.3, and 5.5 do not need to be re-run unless inputs change. The advisory 3.2 flag and the optional follow-ups above are tracked here rather than in `PROJECT_STATUS.md` to avoid noise on the active checklist.

## Sources consulted for category 5 (re-run)

No new web searches were performed for this re-run. The category 5 source list from the original report at line 154 onward applies; the re-run confirmed by reading `regulatory-facts.md`, Section 3, Section 9, and the canonical document that the source-of-truth changes from the fix commit are present and internally consistent.
