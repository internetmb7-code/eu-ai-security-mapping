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
| Phase 2: Threat model | Frame threats, draft all 10 entries | In progress (2 of 10 fully populated and committed) |
| Phase 3: Control library | Frame v1 library, draft entries | In progress (1 of 5 fully populated, 4 stubs) |
| Phase 4: Document drafting | Write all 9 sections of the practitioner guide | Not started |
| Phase 5: Regulatory crosswalk | Surface the regulatory mapping as a primary artifact | Partial (regulatory hooks accumulated through threats and controls) |
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
| `docs/frameworks/THREAT_MODEL_FRAMEWORK.md` | Done (v2 reframe pending application) |
| `docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md` | Done |
| `docs/frameworks/VENDOR_MAPPING_FRAMEWORK.md` | Deferred until controls library is more mature |
| `docs/frameworks/REGULATORY_MAPPING_FRAMEWORK.md` | Not yet |

### Threat model (10 threats total)

> **Note on framing**: As of the v2 framework reframe (pending application), these 10 threats are positioned as **exemplars** within the attack surface taxonomy, not as an exhaustive enumeration. Coverage of all 10 does not mean coverage of all agent threats. See `docs/frameworks/THREAT_MODEL_FRAMEWORK.md` for methodology on discovering threats specific to a deployment.

| ID | Title | Status |
|---|---|---|
| AGT-001 | Prompt injection via tool outputs | Fully populated, committed (standalone source markdown and JSON entry) |
| AGT-002 | Authorization confusion (deputy problem) | Fully populated, committed (exemplar_role field pending v2 reframe) |
| AGT-003 | Tool-chain abuse | Compressed draft ready, not yet committed |
| AGT-004 | Data exfiltration via legitimate channels | Compressed draft ready, not yet committed |
| AGT-005 | Audit and provenance failure | Compressed draft ready, not yet committed |
| AGT-006 | Memory and persistence poisoning | Compressed draft ready, not yet committed |
| AGT-007 | Inter-agent trust and delegation abuse | Compressed draft ready, not yet committed |
| AGT-008 | Output-channel injection | Compressed draft ready, not yet committed |
| AGT-009 | Goal subversion via context manipulation | Compressed draft ready, not yet committed |
| AGT-010 | Resource exhaustion via agent loops | Compressed draft ready, not yet committed |

### Control library (v1: 5 controls total)

| ID | Title | Status |
|---|---|---|
| CTL-001 | Identity and authorization context propagation | Fully populated, committed |
| CTL-002 | Tool-output and context provenance | Stub only |
| CTL-003 | Action verification at high-impact boundaries | Stub only |
| CTL-004 | Authorization-aware output filtering | Stub only |
| CTL-005 | End-to-end audit and accountability | Stub only |

### Practitioner guide sections (9 sections total)

| Section | Status |
|---|---|
| 1. Executive summary | Not started |
| 2. Scope and disclaimer | Not started |
| 3. Regulatory landscape | Not started |
| 4. Common-control crosswalk | Not started |
| 5. Threat model (renamed to "Agent Threat Patterns and Exemplars" pending v2 reframe) | Placeholder; AGT-001 and AGT-002 referenced; AGT-003 to AGT-010 not yet integrated |
| 6. Recommended controls | Partially populated (CTL-001 referenced; CTL-002 to CTL-005 not yet) |
| 7. Implementation considerations | Not started |
| 8. Gaps and open problems | Not started |
| 9. References | Not started |

### Data files

| File | Status |
|---|---|
| `data/threats.json` | AGT-001 and AGT-002 populated; AGT-003 to AGT-010 not yet present |
| `data/controls.json` | CTL-001 populated; CTL-002 to CTL-005 as stubs |
| `data/mappings.json` | Bidirectional mappings between AGT-001/AGT-002 and CTL-001 to CTL-005 |
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
| Foundation | Solid: framework documents done, 2 threats fully populated and committed, 1 control fully populated |
| Threat catalog completeness | 2 of 10 fully populated and committed; 8 of 10 compressed drafts ready but not yet committed |
| Control library completeness | 1 of 5 fully populated, 4 stubs |
| v2 framework reframe | Pending application |
| Document drafting | Not started |
| Web tool | Not started |
| Public visibility | Deferred until foundation is more mature |

**Time invested so far**: Approximately 12 to 15 substantive sessions across strategy, framework design, and content drafting.

**Time to publishable v1**: Estimated 12 to 18 more sessions.

## Next session options

| Option | What it produces | Recommendation |
|---|---|---|
| A. Apply the v2 framework reframe | Threat catalog reframed as exemplars within taxonomy; AGT-002 gets `exemplar_role` backfilled | Recommended next: closes the most important methodological loop |
| B. Commit AGT-003 through AGT-010 compressed drafts | Threat catalog populated at structural level | Defer until after the reframe |
| C. Populate CTL-002 through CTL-005 fully | v1 control library complete | Defer until after the reframe |
| D. Write executive summary and gaps section | Framing for the entire document | Strong second next step after the reframe |

## How to use this document

This file lives at the root of the repository. Update it at the end of each session to reflect what changed. It is the orientation document for any future session and the project record for anyone reviewing the work later.

When you come back to the project after a break, read this first. Then load the framework documents (`PROJECT_BRIEF.md`, `THREAT_MODEL_FRAMEWORK.md`, `CONTROL_LIBRARY_FRAMEWORK.md`) into Claude Code as context.
