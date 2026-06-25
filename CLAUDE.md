# CLAUDE.md

Instructions and context for AI assistants working on the EU AI Security Mapping project.

## Project Overview

This is a vendor-neutral practitioner framework mapping EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments. The project produces three deliverables:

1. **Practitioner Guide**: 25-40 page technical document with threat model, control library, and regulatory crosswalk
2. **Interactive Web Tool**: Multi-entry-point navigator for the framework
3. **Vendor Mapping Contribution Interface**: Schema and process for vendors to submit product mappings

**Current Phase**: Document drafting (Phase 4) approaching v1-publishable status. All nine sections drafted.

## Critical Positioning Constraints

### Vendor Neutrality (Non-Negotiable)

The core framework is **strictly vendor-neutral**. This is a fundamental architectural principle:

- **NO vendor names** in threat model, control library, or main document
- **NO product names** or branding in core framework
- **NO ServiceNow references** in practitioner guide
- Vendor-specific content lives ONLY in `data/vendor-mappings/` (contribution interface opens Phase 5)

The maintainer works at ServiceNow but this is independent practitioner work. The framework must be defensible as unbiased in any external context (AI labs, regulators, conferences).

### Maintainer Recusal Policy

- Maintainer recuses from reviewing any ServiceNow-submitted vendor mapping
- Independent reviewer will be arranged for ServiceNow submissions
- This policy is documented in README.md and must not be altered

## Repository Structure

```
eu-ai-security-mapping/
├── docs/
│   ├── main-document/
│   │   └── EU-AI-Security-Mapping.md    # CANONICAL DOCUMENT (single source of truth)
│   ├── sections/                         # Section drafts before merge
│   │   ├── 01-executive-summary.md
│   │   ├── 02-scope-disclaimer.md
│   │   └── ... (9 sections total)
│   └── frameworks/                       # Methodology reference documents
│       ├── THREAT_MODEL_FRAMEWORK.md
│       ├── CONTROL_LIBRARY_FRAMEWORK.md
│       └── regulatory-facts.md
├── data/
│   ├── threats.json                      # 10 agent-specific threats (AGT-001 to AGT-010)
│   ├── controls.json                     # 5 controls in v1 library (CTL-001 to CTL-005)
│   ├── mappings.json                     # Bidirectional threat/control/requirement mappings
│   ├── regulations/                      # Source regulation PDFs
│   └── vendor-mappings/                  # Contributed vendor mappings (Phase 5)
└── tool/                                 # Web GUI (Phase 6, not started)
```

### Source of Truth Hierarchy

1. **`docs/main-document/EU-AI-Security-Mapping.md`** is the canonical document
2. Section drafts in `docs/sections/` are merged into canonical after review
3. Structured data in `data/*.json` feeds both document and web tool
4. Word, PDF, HTML exports are derived artifacts (never edit directly)

## Working Conventions (Strictly Enforced)

| Convention | Rule |
|---|---|
| **No em dashes** | Use commas, semicolons, periods, or parentheses instead |
| **Tables over bullet points** | Default to tables for any list of 3+ comparable items |
| **Cite primary sources** | Regulation texts, NIST, BSI, ENISA, original research |
| **First-person practitioner voice** | Avoid passive voice and corporate filler |
| **Acknowledge uncertainty** | If something is contested/evolving/unclear, say so |
| **Length discipline** | Section length budgets are firm; cut ruthlessly if over |

### Quality Standards

- **Citations**: Every regulatory claim cites specific article/recital/paragraph
- **Disclaimer**: Each section touching legal interpretation includes guideline-not-legal-advice reminder
- **Examples**: Include concrete examples from realistic enterprise scenarios
- **No marketing language**: This is practitioner work, not promotional material

## Document Structure (9 Sections)

| Section | Length | Status |
|---|---|---|
| 1. Executive briefing | 4-6 pages | Drafted |
| 2. Scope and disclaimer | 1 page | Rewritten |
| 3. Regulatory landscape | 4-6 pages | Rewritten |
| 4. Common-control crosswalk | 3-4 pages | Rewritten |
| 5. Agent threat patterns | 4-6 pages | Drafted (10 threats) |
| 6. Recommended controls | 6-10 pages | Fully populated (5 controls) |
| 7. Implementation considerations | 4-6 pages | Rewritten |
| 8. Gaps and open problems | 2-3 pages | Drafted |
| 9. References | 2-3 pages | Rewritten |

## Threat Model

10 threats total (AGT-001 to AGT-010), framed as **exemplars within attack surface taxonomy** (not exhaustive):

- AGT-001: Prompt injection via tool outputs (fully populated)
- AGT-002: Authorization confusion (deputy problem) (fully populated)
- AGT-003 to AGT-010: Compressed drafts committed; realistic examples deferred to v1.1

Attack surfaces: input, model, tool-use, output, memory, audit

MITRE ATLAS is secondary attribute; AGT-NNN IDs are primary.

## Control Library

5 controls in v1 (CTL-001 to CTL-005), all fully populated:

- CTL-001: Identity and authorization context propagation
- CTL-002: Tool-output and context provenance
- CTL-003: Action verification at high-impact boundaries
- CTL-004: Authorization-aware output filtering
- CTL-005: End-to-end audit and accountability

v1 control library is deliberately coarse-grained and honest about gaps.

## Data Files

- **`data/threats.json`**: All 10 threats; AGT-001/002 fully populated, AGT-003 to 010 compressed
- **`data/controls.json`**: CTL-001 to CTL-005 all populated
- **`data/mappings.json`**: 56 threat-to-requirement, 33 control-to-threat, 25 threat-to-threat entries

These files are authoritative for structured data and feed into both document and web tool.

## Known Outstanding Work (Before v1 Publication)

From PROJECT_STATUS.md "Next session options":

1. **Final assembly review** (Option A): Full-document read-through, cross-reference audit, consistency pass
2. **Citation verification pass** (Option B): Verify article numbers and dates against PDFs in `data/regulations/`
3. **Known cleanup items** (Option C):
   - (CTL-005, AGT-004) mapping asymmetry
   - PDF filename normalization
   - Merge AGT-001 to AGT-010 exemplar bodies into canonical document
4. **Publication decision** (Option D): License confirmation, peer review, GitHub push

## Things to Watch Out For

### Do Not Do These Things

- **Do not** add vendor names or product references to core framework
- **Do not** alter the maintainer recusal policy
- **Do not** use em dashes in prose
- **Do not** expand scope beyond EU regulations (no US Executive Orders, etc.)
- **Do not** auto-generate placeholder content in section files
- **Do not** edit derived artifacts (PDF, DOCX, HTML) directly

### Common Patterns

- When referencing threats, use AGT-NNN format
- When referencing controls, use CTL-NNN format
- Regulation citations format: "EU AI Act Article 9(2)(a)" or "NIS2 Article 21"
- All paths should be absolute when using tools
- Git workflow: feature branches after initial push; local-first during setup

### File Editing Discipline

- **Read before editing**: Always read a file with the Read tool before editing
- **Section files vs canonical**: Section files in `docs/sections/` are working drafts; merge to `docs/main-document/EU-AI-Security-Mapping.md` after review
- **JSON schema compliance**: Changes to `data/*.json` must validate against documented schemas

## Current Status Summary

- **Foundation**: Solid (framework documents done, data schemas populated)
- **Threat catalog**: 2 of 10 fully populated, 8 of 10 compressed drafts (structural completeness reached)
- **Control library**: 5 of 5 populated; v1 complete
- **Document drafting**: All 9 sections drafted; structurally complete
- **Pre-publication**: Approaching v1-publishable status pending final assembly review
- **Web tool**: Not started (Phase 6)
- **Public visibility**: Still local; not yet pushed to GitHub

## Key Documents to Review

Before working on this project, review:

1. **PROJECT_BRIEF.md**: Scope, methodology, phased workflow
2. **PROJECT_STATUS.md**: Current status, decisions locked in, next session options
3. **docs/frameworks/THREAT_MODEL_FRAMEWORK.md**: Threat modeling methodology
4. **docs/frameworks/CONTROL_LIBRARY_FRAMEWORK.md**: Control library structure
5. **docs/frameworks/regulatory-facts.md**: Source-of-truth regulatory citations

## Workflow Guidance

### Local-First During Setup

- Repository is built and reviewed locally before any GitHub push
- First push will present clean, intentional history
- Currently in this phase; no remote configured yet

### After Initial Push

- Switch to feature-branch and pull-request workflow
- Branch naming: `feature/<descriptive-name>`
- Self-review all PRs in GitHub UI before merge

## Success Criteria

The project is successful if:

1. Practitioner guide published on GitHub with full text and exports
2. Web tool publicly accessible and useful for multi-entry-point navigation
3. Vendor mapping interface documented and at least one external mapping contributed within 12 months
4. At least one conference talk delivered
5. Referenced by at least three independent practitioners/organizations within 6 months
6. Maintainer can defend every claim and architectural decision

## Questions or Ambiguity?

When in doubt:

1. Check PROJECT_BRIEF.md for scoping decisions
2. Check PROJECT_STATUS.md for current status and locked decisions
3. Check framework documents for methodology
4. Preserve vendor neutrality above all else
5. Ask the user before making structural changes

## License

- Document: CC BY 4.0 (to be confirmed before publication)
- Code: MIT (to be confirmed before publication)

Last updated: 2026-06-02
