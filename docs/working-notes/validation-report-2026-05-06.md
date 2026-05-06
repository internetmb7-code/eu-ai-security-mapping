# v1 Validation Report

Date: 2026-05-06.
Scope: Quality and validation pass over the EU AI Security Mapping framework before public release. Six categories: repository-wide mechanics, structural consistency, data-model consistency, source accuracy, regulatory currency, convention compliance. Auto-fix categories were considered first; flagged items are documented below.

## Summary

| Category | Checks run | Pass | Auto-fixed | Flagged for review |
|---|---|---|---|---|
| 1. Repository-wide mechanics | 4 | 3 | 0 | 1 |
| 2. Structural consistency | 4 | 1 | 0 | 3 |
| 3. Data-model consistency | 5 | 3 | 0 | 2 (one critical, 3.4) |
| 4. Source accuracy | 4 | 4 | 0 | 0 |
| 5. Regulatory currency (web search) | 5 | 2 | 0 | 3 |
| 6. Convention compliance | 4 | 4 | 0 | 0 |
| **Total** | **26** | **17** | **0** | **9** |

Recommendation: **NOT PUBLISHABLE**. Driven by category 3.4 (broken Section 4 mappings) per the exit policy, and reinforced by the total flag count exceeding the six-flag threshold. The 3.4 issue is the highest-priority blocker; categories 5.1 and 5.5 are second-order (factual currency) and should be addressed before any public release. The remaining flags are smaller-scale corrections that can be batched.

## Note on the missing mechanical-fixes commit

The auto-fix pass produced zero changes. Em-dashes (U+2014), en-dashes (U+2013), trailing whitespace, missing terminal newlines, and broken identifier capitalisation each returned no hits across the 28 markdown files in scope. The "C5:2025" reference described under flag 5.3 was considered for auto-fix as an identifier issue, but it represents a factual currency error, not a capitalisation error, and is correctly flagged under category 5 rather than silently rewritten. No "Mechanical fixes from v1 validation pass" commit was created because there was nothing to fix.

## Category 1: Repository-wide mechanics

| Check | Result |
|---|---|
| 1.1 Em-dash absence (U+2014, U+2013) | Pass (0 hits) |
| 1.2 Trailing whitespace / missing terminal newlines | Pass (0 hits) |
| 1.3 Identifier capitalisation (AGT/CTL uppercase, "EU AI Act", "NIS2", "DORA", "GDPR") | Pass (apparent hits were the official German legal name `NIS-2-Umsetzungs-` with hyphens, lowercase filenames `nis2.md`, `dora.md`, `gdpr-art-22.md`, and the URL `gdpr.algolia.com` — all legitimate) |
| 1.4 Broken markdown cross-references | **Flag**: see below |

### Flag 1.4: Broken cross-reference to `docs/working-notes/section-7-8-boundary-spec.md`

Referenced from four locations: canonical document line 1165, `docs/sections/09-references.md` line 86, `PROJECT_STATUS.md`, and `CHANGELOG.md`. The `docs/working-notes/` directory did not exist before this report was written; the boundary-spec file does not exist. Either create the file (and check it in) or remove the references. Removing is the lower-effort option since Section 7 is already drafted and the boundary spec served as a working note rather than a published artifact.

## Category 2: Structural consistency

| Check | Result |
|---|---|
| 2.1 Sections in canonical document in correct order (1 through 9 plus Appendix A) | Pass |
| 2.2 Each section file uses `##` as the top-level heading (no H1) | **Flag**: see below |
| 2.3 Section length within 50% of target | **Flag**: see below |
| 2.4 No orphaned section files in `docs/sections/` | Pass |

### Flag 2.2: Heading-depth inconsistency across section files

Sections 01, 02, 03, 05, 06, 08, and 10 use `# N. Title` (H1) plus a `<!-- Length budget -->` comment. Sections 04, 07, and 09 use `##` directly with no length-budget comment. The convention check requires `##` as the top-level heading in section files; the canonical document supplies the H1. Either update the seven non-conforming files to drop the H1 and the length-budget comment, or formalise the inconsistency by documenting that section files retain their own H1 for standalone readability and the canonical document strips them on insertion.

### Flag 2.3: Section 2 over length budget

Section 2 (Scope and disclaimer) is 77 lines against a target of approximately 1 page (50 lines). At 154% of target this is just over the 50% deviation tolerance and warrants a tightening pass. All other sections fall within tolerance: section 3 at 161 lines (target 4–6 pages), section 4 at 98 lines (target 3–4 pages), section 7 at 117 lines (target 4–6 pages), section 9 at 95 lines (target 2–3 pages).

## Category 3: Data-model consistency

| Check | Result |
|---|---|
| 3.1 All AGT-NNN IDs in markdown match `data/threats.json` | Pass |
| 3.2 All CTL-NNN IDs in markdown match `data/controls.json` | **Flag** (low priority): see below |
| 3.3 Bidirectional mapping integrity (`recommended_controls` symmetry with `control_mitigates_threat`) | Pass (zero asymmetries) |
| 3.4 Section 4 bridging-threat notation matches `mappings.json` | **Flag (CRITICAL)**: see below |
| 3.5 Empty arrays in `mappings.json` (`requirement_to_controls`, `control_to_threats`) | Pass (empty by design; bridge through threats) |

### Flag 3.2: CTL IDs beyond CTL-005 referenced in markdown

CTL-006 through CTL-033 appear in `CONTROL_LIBRARY_FRAMEWORK.md`, `CHANGELOG.md`, and the canonical document at line 431. All occurrences are explicitly contextualised as "reserved for v2" or as historical entries documenting consolidation; none are presented as v1 controls. The literal check fails but the underlying content is correct. Recommended action: leave as-is and treat the literal check as advisory rather than blocking.

### Flag 3.4 (CRITICAL): Section 4 cites `CTL-004 [via AGT-001]` in five cells without supporting mapping

Section 4 cites `CTL-004 [via AGT-001]` in the following cells:

| Section 4 location | Line | Citation |
|---|---|---|
| AI Act Article 9 row | 15 | `CTL-004 [via AGT-001]` |
| AI Act Article 15 row | 20 | `CTL-004 [via AGT-001, AGT-002, AGT-004, AGT-008]` |
| NIS2 Article 21 row | 30 | `CTL-004 [via AGT-001, AGT-002, AGT-004, AGT-008]` |
| DORA Articles 6 to 8 row | 38 | `CTL-004 [via AGT-001, AGT-002, AGT-004, AGT-008]` |
| GDPR Article 32 row | 59 | `CTL-004 [via AGT-001, AGT-002, AGT-004, AGT-008]` |

The pair `(CTL-004, AGT-001)` is not present in `data/mappings.json` `control_mitigates_threat`. CTL-004 (Authorization-aware output filtering) is mapped only to AGT-002, AGT-004, and AGT-008. The bridging-threat notation in Section 4 therefore claims a relationship that the data model does not back.

Two reconciliation options:

1. **Remove `AGT-001` from the bridge list in those five cells.** Lowest data-model risk. Section 4 still has the other bridge threats and CTL-002, CTL-003, CTL-005 to do the cross-walk work for those rows.
2. **Add `(CTL-004, AGT-001)` to `control_mitigates_threat` in `mappings.json`** if a defensible rationale exists (CTL-004 contains injected instructions that originated from prompt injection; the relationship is "partial" or "secondary"). Higher data-model effort and requires a written justification in the mapping entry's `rationale` field.

This is the single highest-priority finding in the report and the reason the recommendation is NOT PUBLISHABLE. Per the exit policy, any flag in 3.4 forces NOT PUBLISHABLE regardless of total count.

## Category 4: Source accuracy

| Check | Result |
|---|---|
| 4.1 RFCs cited in `controls.json` (RFC 8693, 9068, 9421) | Pass; all match Section 9 references |
| 4.2 NIST SP citations (800-37r2, 800-53r5, 800-61r2, 800-92, 800-122, 800-207, 800-218) | Pass; all match Section 9 references |
| 4.3 ISO citations (27001:2022, 27018:2019, 27037:2012, 38500:2024) | Pass; all match Section 9 references |
| 4.4 Regulation article numbers consistent across `regulatory-facts.md`, `mappings.json`, and Section 4 | Pass (the apparent inconsistencies between "Articles 6 to 8" plural and `Art. 6 to 8` abbreviated are surface-form differences, not citation errors) |

## Category 5: Regulatory currency (web search)

| Check | Result |
|---|---|
| 5.1 Germany NIS2 transposition (NIS2UmsuCG) entry into force | **Flag**: stale |
| 5.2 Digital Omnibus simplification proposal status | Pass (with minor note below) |
| 5.3 BSI C5:2026 publication status | **Flag**: stale + factual error |
| 5.4 Annex III AI Act guidelines from Commission | Pass (status text in `regulatory-facts.md` is honest about uncertainty) |
| 5.5 Austria NIS2 transposition status | **Flag**: incorrect |

### Flag 5.1: Germany NIS2 status is stale

`regulatory-facts.md` line 55 says "Not yet transposed; NIS2UmsuCG draft in parliamentary process". The Bundestag approved NIS2UmsuCG on 13 November 2025 and it entered into force on 6 December 2025 with promulgation in the Federal Law Gazette. Update `regulatory-facts.md` to reflect entry into force on 6 December 2025, the expansion from approximately 4,500 to approximately 29,500 supervised entities, and the new BSI portal registration window opening 6 January 2026.

### Flag 5.2: Digital Omnibus current status (minor note)

`regulatory-facts.md` line 19 currently captures the proposal correctly. Optional addition: the second trilogue on 28 April 2026 ended without agreement; a follow-up trilogue was scheduled for 13 May 2026. The 2 August 2026 deadline therefore remains the binding planning anchor and any postponement should be treated as upside, not a baseline. Worth adding to the regulatory-facts file but not a publication blocker.

### Flag 5.3: BSI C5:2026 status is stale and Section 9 contains a factual error

Two sub-issues:

| Sub-issue | Location | Detail |
|---|---|---|
| Section 9 cites a non-existent "C5:2025" | `docs/sections/09-references.md` line 32; canonical document line 1111 | The published versions are C5:2020 and C5:2026 (final version released end of March 2026). C5:2025 is not a published BSI catalogue. |
| `regulatory-facts.md` open question 5 is stale | `regulatory-facts.md` line 163 | Says "verify current status before citing"; C5:2026 is now published with 168 criteria, application from 1 June 2027. Update the open-questions table and add C5:2026 to the DACH-specific national rules section. |

Recommended fix in Section 9: change "(C5:2020 and C5:2025)" to "(C5:2020 and C5:2026)" in both the section file and the canonical document. This is a one-line factual correction.

### Flag 5.5: Austria NIS2 status is incorrect

`regulatory-facts.md` line 56 says "Austria | Transposed (verify current status before citing)". This is incorrect. The first draft (NISG 2024) was rejected by the National Council in February 2024. A new draft (NISG 2026) was published on 13 November 2025 and is set to enter into force on 1 October 2026. Until that date, the existing NISG 2018 regime applies. The European Commission sent Austria a reasoned opinion for failure to transpose on 7 May 2025. Replace the table cell with: "Not yet transposed; NISG 2026 draft published 13 November 2025; entry into force scheduled 1 October 2026; Commission reasoned opinion issued 7 May 2025; NISG 2018 applies in the interim".

## Category 6: Convention compliance

| Check | Result |
|---|---|
| 6.1 First-person practitioner voice (no "I", "my", "we" except where authorial voice is intentional) | Pass (one acceptable usage in section 2 opening) |
| 6.2 Tables over bulleted lists for comparable items | Pass (spot-checks across sections 4, 6, 7 confirm tables are used for parallel content) |
| 6.3 Vendor product names framed as exemplars rather than endorsements | Pass (Splunk, Sentinel, Elastic, Entra ID, Okta, Ping all appear in parenthetical exemplar lists with multiple alternatives) |
| 6.4 Em-dash absence cross-confirm | Pass (0 hits across all sources) |

## Recommended next actions, in priority order

| Priority | Action |
|---|---|
| 1 | Resolve the category 3.4 issue: either remove `AGT-001` from the five Section 4 cells citing `CTL-004 [via AGT-001]`, or add the `(CTL-004, AGT-001)` mapping to `control_mitigates_threat` with a documented rationale |
| 2 | Update `regulatory-facts.md` for Germany NIS2 (now in force), Austria NIS2 (NISG 2026 entry into force 1 October 2026), BSI C5:2026 (now published) |
| 3 | Fix the "C5:2025" → "C5:2026" reference in Section 9 and the canonical document |
| 4 | Resolve the working-notes boundary-spec cross-reference (either commit the file or remove the references) |
| 5 | Decide on heading-depth convention for section files (uniform `##` opening, or formalise the per-section variation) |
| 6 | Tighten Section 2 toward the 1-page target |
| 7 | Optional: add a note to `regulatory-facts.md` capturing the 28 April 2026 trilogue stall on Digital Omnibus |

After these are addressed, re-run categories 1, 2, and 3.4 to confirm the publishable status. Categories 4, 5 (5.2, 5.4 only), and 6 do not need to be re-run unless inputs change.

## Sources consulted for category 5

| Item | Sources |
|---|---|
| Germany NIS2 (5.1) | nis-2-directive.com (Germany page); openkritis.de; Reed Smith blog; usd.de; Deloitte Legal; McDermott |
| Digital Omnibus (5.2) | digital-strategy.ec.europa.eu; europarl.europa.eu (legislative train and press); IAPP; Bird & Bird; Slaughter and May; Pinsent Masons; Morrison Foerster; DLA Piper |
| BSI C5:2026 (5.3) | bsi.bund.de (C5:2026 page); 2b-advice.com; certhub.de; grclab.com; AWS, Microsoft compliance pages |
| Annex III guidelines (5.4) | ai-act-service-desk.ec.europa.eu; digital-strategy.ec.europa.eu; legalnodes.com; secureprivacy.ai |
| Austria NIS2 (5.5) | nis-2-directive.com (Austria page); copla.com; docusnap.com; ECSO; nis-solutions.eu; digital-strategy.ec.europa.eu (Austria page); Baker McKenzie; Wavestone |
