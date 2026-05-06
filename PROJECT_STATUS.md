# Project Status: EU AI Security Mapping

A living checklist of what we are building, why, and where we are. Updated as the project progresses.

## What we are building

A vendor-neutral practitioner framework mapping EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments. Three deliverables:

| Deliverable | Purpose |
|---|---|
| 1. Practitioner guide (markdown document, exported to PDF/DOCX/HTML) | The primary written artifact; 25 to 40 pages; published on GitHub |
| 2. Interactive web tool | Multi-entry-point navigator for CISOs and security architects to traverse the framework starting from any layer |
| 3. Vendor mapping contribution interface | Defined schema and process by which vendors and community contributors can submit product-specific mappings to the framework |

## Why we are building it

| Reason | Detail |
|---|---|
| Real customer need | DACH regulated enterprises lack a clear practitioner-grade reference for navigating overlapping EU AI regulations as they deploy agentic AI |
| Career positioning | Establishes the author as a credible practitioner voice in DACH AI security; portable across employers, regulators, AI labs |
| Differentiated work | Most existing material is either legalistic and not actionable, or technical and not regulation-aware; this fills the gap |
| Regulatory timing | EU AI Act enforcement begins August 2026; NIS2, DORA, GDPR Art. 22 already in force |
| Platform model (Option D) | Vendor mappings as community contributions rather than author-produced content; positions the work as infrastructure rather than a single document |

## High-level project plan

| Phase | Description | Status |
|---|---|---|
| Phase 1: Strategy and scaffolding | Define scope, audience, structure, set up repository | Done |
| Phase 2: Threat model | Frame threats, draft all 10 entries | In progress (2 of 10 fully populated, 8 of 10 compressed drafts committed; realistic examples deferred) |
| Phase 3: Control library | Frame v1 library, draft entries | Done (5 of 5 fully populated; v1 control library complete) |
| Phase 4: Document drafting | Write all 9 sections of the practitioner guide | In progress (sections 1, 2, 3, 4, 5, 6, and 8 drafted; sections 7 and 9 not started) |
| Phase 5: Regulatory crosswalk | Surface the regulatory mapping as a primary artifact | Drafted (regulatory landscape narrative in section 3; regulatory facts reference file at `docs/frameworks/regulatory-facts.md`; common-control crosswalk in section 4 reconciled against `data/mappings.json` with bridging-threat notation) |
| Phase 6: Web tool | Build the multi-entry-point navigator | Not started |
| Phase 7: Vendor mapping interface | Define contribution schema and process | Deferred (until controls library is mature) |
| Phase 8: Publication | Push to GitHub, distribute, conference submissions | Deferred |

## Detailed checklist

### Repository and tooling

| Item | Status |
|---|---|
| Local Git repository initialized | Done |
| Directory structure scaffolded | Done |
| `.gitignore`, `README.md`, `CHANGELOG.md` | Done |
| GitHub repository created and pushed | Not yet (deliberate; staying local until foundation is more mature) |
| Branch protection rules on main | Not yet (will configure when going public) |
| CI/CD workflows | Not yet |

### Foundational documents

| Item | Status |
|---|---|
| `PROJECT_BRIEF.md` (Option D platform model, public + product-agnostic) | Done |
| `docs/frameworks/THREAT_MODEL_FRAMEWORK.md` | Done (v2 reframe applied) |
| `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md` | Done |
| `docs/frameworks/VENDOR_MAPPING_FRAMEWORK.md` | Deferred until controls library is more mature |
| `docs/frameworks/REGULATORY_MAPPING_FRAMEWORK.md` | Not yet |
| `docs/frameworks/regulatory-facts.md` (source-of-truth reference for regulatory dates, article numbers, and citations) | Done (initial v1; verified May 2026) |

### Threat model (10 threats total)

> **Note on framing**: As of the v2 framework reframe, these 10 threats are positioned as **exemplars** within the attack surface taxonomy, not as an exhaustive enumeration. Coverage of all 10 does not mean coverage of all agent threats. See `docs/frameworks/THREAT_MODEL_FRAMEWORK.md` for methodology on discovering threats specific to a deployment.

| ID | Title | Status |
|---|---|---|
| AGT-001 | Prompt injection via tool outputs | Fully populated, committed (standalone source markdown and JSON entry) |
| AGT-002 | Authorization confusion (deputy problem) | Fully populated, committed (exemplar_role field backfilled per v2 reframe) |
| AGT-003 | Tool-chain abuse | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-004 | Data exfiltration via legitimate channels | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-005 | Audit and provenance failure | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-006 | Memory and persistence poisoning | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-007 | Inter-agent trust and delegation abuse | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-008 | Output-channel injection | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-009 | Goal subversion via context manipulation | Compressed draft committed (schema-faithful; realistic example deferred) |
| AGT-010 | Resource exhaustion via agent loops | Compressed draft committed (schema-faithful; realistic example deferred) |

### Control library (v1: 5 controls total)

| ID | Title | Status |
|---|---|---|
| CTL-001 | Identity and authorization context propagation | Fully populated, committed |
| CTL-002 | Tool-output and context provenance | Fully populated, committed |
| CTL-003 | Action verification at high-impact boundaries | Fully populated, committed |
| CTL-004 | Authorization-aware output filtering | Fully populated, committed |
| CTL-005 | End-to-end audit and accountability | Fully populated, committed |

### Practitioner guide sections (9 sections total)

| Section | Status |
|---|---|
| 1. Executive summary | Drafted (section file and canonical document populated) |
| 2. Scope and disclaimer | Drafted (section file and canonical document populated) |
| 3. Regulatory landscape | Drafted (section file and canonical document populated; uses `docs/frameworks/regulatory-facts.md` as spine; one subsection per instrument with bridging "what this means for agent deployments" paragraphs) |
| 4. Common-control crosswalk | Drafted (section file and canonical document populated; reconciled against `data/mappings.json`) |
| 5. Agent Threat Patterns and Exemplars (renamed per v2 reframe) | Merged section file contains all 10 threats: AGT-001 and AGT-002 in full, AGT-003 through AGT-010 as compressed entries |
| 6. Recommended controls | Fully populated for v1 (CTL-001 through CTL-005 all inserted; v1 control library complete) |
| 7. Implementation considerations | Not started |
| 8. Gaps and open problems | Drafted (section file and canonical document populated) |
| 9. References | Not started |

### Data files

| File | Status |
|---|---|
| `data/threats.json` | All 10 threats present: AGT-001 and AGT-002 fully populated; AGT-003 through AGT-010 as compressed drafts (status: `compressed_draft`, `realistic_example_status: to_be_populated`) |
| `data/controls.json` | CTL-001 through CTL-005 all populated; v1 control library complete |
| `data/mappings.json` | Bidirectional mappings for all 10 threats against CTL-001 to CTL-005 (56 threat-to-requirement entries, 33 control-to-threat entries, 25 threat-to-threat entries) |
| `data/regulations/` | Source regulation texts not yet collected |
| `data/vendor-mappings/` | Folder structure exists; no contributions yet (deferred) |

### Web tool

| Item | Status |
|---|---|
| Design framework | Discussed; multi-entry-point navigator confirmed |
| Stack decisions | Suggested (SvelteKit or Next.js, static, GitHub Pages) |
| Data model for traversal | Schema in place via `data/mappings.json` |
| Implementation | Not started |

### Publication

| Item | Status |
|---|---|
| Push to GitHub | Deferred |
| LinkedIn announcement post | Not yet |
| Conference submissions (BSI, IAPP DACH, heise, RSA EU, Black Hat EU) | Not yet |
| Companion blog post | Not yet |

## Decisions locked in (do not revisit without explicit reason)

| Decision | Choice |
|---|---|
| Audience | CISOs and security program leads (primary); architects, compliance leads (secondary) |
| Scope of "agent" | Narrow (LLM-based, tool-using, multi-step, autonomous between human approvals) |
| Threat categorization | By attack surface (input, model, tool-use, output, memory, audit) |
| Threat catalog source | MITRE ATLAS as secondary attribute; custom AGT-NNN IDs as primary |
| Threat catalog size | Bounded at 10 threats |
| Threat catalog status | Exemplars within attack surface taxonomy, not exhaustive enumeration |
| Deliverable model | Public only, product-agnostic (Option D platform model) |
| Vendor mappings | Community contributions; author recuses from reviewing ServiceNow submissions |
| Control library granularity | Coarse-grained v1 (10 to 20 target; currently 5; honest about gaps) |
| Control categorization | Implementation domain primary, function secondary |
| External standard mappings | NIST SP 800-53, ISO 27001 Annex A, BSI grundschutz |
| Working conventions | No em dashes; tables over bullet points; cite primary sources; first-person practitioner voice |
| Workflow | Local-first until foundation is mature; switch to feature branches and PRs after first push |

## Open questions deferred to later sessions

| Question | When to resolve |
|---|---|
| Specific licensing terms (CC BY 4.0 + MIT confirmed at high level) | Before publication |
| Peer review by named subject matter experts | Before publication |
| German translation | Post-launch decision |
| Long-term maintenance commitment | Post-launch |
| v2 expansion to additional regulations or jurisdictions | After v1 ships |
| v2 expansion of control library (specific gap-fillers identified) | After customer engagement feedback on v1 |

## Where we are right now

| Element | Status |
|---|---|
| Foundation | Solid: framework documents done, 2 threats fully populated, 8 threats committed as compressed drafts, 5 controls fully populated; v1 control library complete |
| Threat catalog completeness | 2 of 10 fully populated; 8 of 10 committed as compressed drafts (realistic examples deferred); structural completeness reached at the exemplar level |
| Control library completeness | 5 of 5 fully populated; v1 control library complete |
| v2 framework reframe | Applied |
| Document drafting | Sections 1, 2, 3, 4, 5, 6, and 8 drafted; sections 7 and 9 not started |
| Web tool | Not started |
| Public visibility | Deferred until foundation is more mature |

**Time invested so far**: Approximately 12 to 15 substantive sessions across strategy, framework design, and content drafting.

**Time to publishable v1**: Estimated 12 to 18 more sessions.

## Next session options

| Option | What it produces | Recommendation |
|---|---|---|
| A. Draft practitioner guide sections 7 (Implementation considerations) and 9 (References) | Remaining unwritten sections of the practitioner guide | Recommended next: sections 1, 2, 3, 4, 5, 6, and 8 are drafted; closing sections 7 and 9 gives a complete v1 document. |
| B. Populate realistic examples for AGT-003 through AGT-010 | Threat catalog reaches parity with AGT-001 and AGT-002 | Strong parallel work to section drafting |
| C. Begin regulatory mapping framework | Surfaces the regulatory crosswalk as a primary artifact | Natural feeder into section 4 once sections 2 and 3 are stable |
| D. Plan the web tool | Multi-entry-point navigator scoped against the now-stable schema | Defer until practitioner guide is closer to v1 publishable |

## How to use this document

This file lives at the root of the repository. Update it at the end of each session to reflect what changed. It is the orientation document for any future session and the project record for anyone reviewing the work later.

When you come back to the project after a break, read this first. Then load the framework documents (`PROJECT_BRIEF.md`, `THREAT_MODEL_FRAMEWORK.md`, `CONTROL_LIBRARY_FRAMEWORK.md`) into Claude Code as context.
