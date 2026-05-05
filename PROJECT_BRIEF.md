# EU AI Security Mapping Project

A practitioner's mapping of EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments.

## Project Goal

Produce two interlinked artifacts:

1. **Practitioner Guide** (primary output): A 25 to 40 page technical document mapping EU regulatory requirements (EU AI Act, NIS2, DORA, relevant GDPR articles) to concrete security controls for enterprise AI and agent deployments. Includes an agent-specific threat model and implementation patterns.
2. **Interactive Web Tool** (supporting output): A searchable web interface that exposes the regulatory mapping, control library, and threat model as a queryable, filterable, exportable resource. Hosted publicly via GitHub.

The combined output positions the author as a credible practitioner voice in DACH AI security advisory, suitable for conference talks, customer engagements, and senior advisory roles at AI labs, hyperscalers, regulators, or client-side CISO functions.

## Author's Perspective and Disclaimer

Written from the perspective of a senior security practitioner with 14 years of operational security experience, including current customer-facing advisory work in the DACH region.

The document is a guideline based on the author's interpretation of public regulatory texts and operational security experience. It is **not legal advice**. Readers should consult qualified legal counsel for compliance determinations. Primary sources are cited extensively so readers can follow the reasoning chain and form their own conclusions.

## Scope

### In scope
- EU AI Act, with focus on Articles 9 (risk management), 10 (data governance), 14 (human oversight), and 15 (accuracy, robustness, cybersecurity)
- NIS2 Directive, focusing on technical security obligations relevant to AI systems
- DORA, focusing on ICT risk management and third-party risk for financial services
- GDPR Article 22 (automated decision-making) where it intersects with AI agent autonomy
- Agent-specific threat model covering risks not adequately addressed by traditional security controls
- Operational controls and implementation patterns for enterprise security programs

### Out of scope
- Non-EU regulatory regimes (US Executive Orders, NIST AI RMF except as referenced)
- Sector-specific regulations beyond general DORA financial services scope (no deep dive into MaRisk, MDR, etc., though hooks for sectoral extension are noted)
- Legal interpretation of ambiguous regulatory language
- Model alignment, capability evaluations, or frontier AI safety research
- Generative AI content moderation policy

### Scoping rationale
The crosswalk approach (multiple regulations, common controls, agent-specific threats) addresses real customer pain in DACH enterprises navigating overlapping obligations. Sectoral extensions are hooks rather than full treatments to keep the scope finishable.

## Document Structure

| Section | Content | Approx. length |
|---|---|---|
| 1. Executive summary | Core thesis, audience, key findings | 1 to 2 pages |
| 2. Scope and disclaimer | What is and isn't covered, guideline-not-legal-advice framing | 1 page |
| 3. Regulatory landscape | Overview of EU AI Act, NIS2, DORA, GDPR Art. 22 with focus on technical security obligations | 4 to 6 pages |
| 4. Common-control crosswalk | Where the regulations overlap on actual security requirements | 3 to 4 pages |
| 5. Agent-specific threat model | Risk classes traditional controls don't fully address: prompt injection via tool outputs, authorization confusion, tool-chain abuse, data exfiltration via legitimate channels, audit and provenance, memory and persistence | 4 to 6 pages |
| 6. Recommended controls and patterns | Concrete control recommendations mapped to threats and regulatory requirements | 6 to 10 pages |
| 7. Implementation considerations | What this looks like in practice, including reference architecture sketches | 4 to 6 pages |
| 8. Gaps and open problems | Honest discussion of where regulations are unclear or inadequate, and where industry practice is still evolving | 2 to 3 pages |
| 9. References | Primary sources, standards, related work | 2 to 3 pages |

## Source of Truth

The **canonical document** lives at `docs/main-document/EU-AI-Security-Mapping.md` in the GitHub repository. This is the master file where all final, quality-checked content is consolidated.

Section drafts live in `docs/sections/` and are merged into the canonical document only after review. Word, PDF, and HTML exports are generated from the markdown source via the build pipeline; they are derived artifacts, never edited directly.

The repository is the single source of truth. Local files should always be synced via Git.

## Repository Structure

```
eu-ai-security-mapping/
├── README.md                          # Project overview, status, how to contribute
├── PROJECT_BRIEF.md                   # This file: scope, goals, methodology
├── LICENSE                            # CC BY 4.0 for document, MIT for code
├── CHANGELOG.md                       # Version history of the document
├── .gitignore
│
├── docs/
│   ├── main-document/
│   │   └── EU-AI-Security-Mapping.md  # CANONICAL DOCUMENT, single source of truth
│   ├── sections/                      # Section drafts before merge
│   │   ├── 01-executive-summary.md
│   │   ├── 02-scope-disclaimer.md
│   │   ├── 03-regulatory-landscape.md
│   │   ├── 04-crosswalk.md
│   │   ├── 05-threat-model.md
│   │   ├── 06-controls.md
│   │   ├── 07-implementation.md
│   │   ├── 08-gaps.md
│   │   └── 09-references.md
│   ├── diagrams/                      # Reference architecture, threat model diagrams (mermaid or SVG)
│   └── exports/                       # Generated outputs (PDF, DOCX, HTML), not hand-edited
│
├── data/
│   ├── regulations/                   # Source regulation texts (EU AI Act, NIS2, DORA, GDPR)
│   ├── requirements.json              # Structured database of requirements extracted from regulations
│   ├── controls.json                  # Control library with mappings
│   ├── threats.json                   # Agent-specific threat catalog
│   └── mappings.json                  # Cross-references: regulation → control → threat
│
├── tool/                              # Web GUI (built in Phase 4)
│   ├── README.md
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── ...
│
├── scripts/                           # Helper scripts
│   ├── extract-requirements.py        # Parse regulation texts into structured data
│   ├── validate-citations.py          # Check citation integrity
│   ├── build-document.sh              # Compile sections into canonical document
│   └── export-formats.sh              # Generate PDF, DOCX, HTML
│
└── .github/
    ├── workflows/
    │   ├── validate.yml               # CI: validate JSON schemas, check citations
    │   └── build.yml                  # CI: build exports on tag
    └── ISSUE_TEMPLATE/
```

## Phased Workflow

The work is split across Claude.ai chat (strategic and writing dialogue) and Claude Code (filesystem, code, repository management). Use each tool for what it's good at.

### Phase 1: Strategic and Structural (Claude.ai chat)

| Task | Status |
|---|---|
| Refine scope and ToC | Done (this brief) |
| Decide depth per regulation | Done (Articles 9, 10, 14, 15 prioritized for AI Act) |
| Develop threat model framework | To do, in chat |
| Sharpen executive summary thesis | To do, in chat |
| Review and challenge sections as drafted | Ongoing, in chat |

### Phase 2: Research and Source Gathering (Claude Code)

| Task | Tool |
|---|---|
| Pull and store full text of regulations into `data/regulations/` | Claude Code |
| Build `requirements.json` schema, populate from regulation texts | Claude Code, possibly with research sub-agents in parallel |
| Cross-reference NIST publications, BSI grundschutz, ENISA guidance | Claude Code |
| Build initial `controls.json` and `threats.json` schemas | Claude Code |
| Validate citations and check for outdated references | Claude Code |

### Phase 3: Drafting (mixed)

| Task | Tool |
|---|---|
| Write substantive section drafts in author's voice | Claude.ai chat with author driving |
| Generate first drafts of repetitive structured content (mapping tables) from `data/*.json` | Claude Code |
| Iterate on threat model and control recommendations | Claude.ai chat |
| Polish prose and citations | Either |
| Merge approved sections into canonical document | Claude Code |

### Phase 4: Web Tool (Claude Code)

| Feature | Priority |
|---|---|
| Searchable regulation requirements database (filter by regulation, article, security domain, control type) | High |
| Control mapping view (requirement → control → threat) | High |
| Threat model browser (agent-specific threats linked to controls and regulations) | High |
| Coverage dashboard (visualize how a security program maps to regulatory requirements) | Medium |
| Export filtered reports | Medium |
| Update mechanism for regulation changes | Low (post-launch) |

**Suggested stack** (subject to confirmation in Phase 4):
- Frontend: SvelteKit or Next.js
- Data: SQLite or static JSON (the dataset is not large)
- Hosting: Vercel, Cloudflare Pages, or GitHub Pages (free tier sufficient)
- No backend required initially; fully static is fine

### Phase 5: Publication and Distribution

| Channel | Action |
|---|---|
| GitHub | Public repository with all artifacts |
| LinkedIn | Long-form post announcing the work |
| Conferences | Submit talks to BSI events, IAPP DACH, heise security conferences, RSA EU, Black Hat EU |
| Blog | Companion blog post explaining the methodology |
| ServiceNow internal | Share with OCISO leadership and account teams covering DACH regulated enterprises |

## Quality Standards

| Dimension | Standard |
|---|---|
| Citations | Every regulatory claim cites the specific article, recital, or paragraph. NIST, BSI, ENISA references include document number and version. |
| Voice | First-person practitioner perspective. Avoid passive voice and corporate filler. The reader should feel they're learning from someone who has actually done this work. |
| Disclaimer | Each major section that touches legal interpretation includes a brief reminder that this is a guideline, not legal advice. |
| Threat model rigor | Each threat includes: description, attack scenario, affected components, traditional controls (and why insufficient), recommended controls, residual risk |
| Control recommendations | Each control includes: regulatory basis, threats addressed, implementation pattern, operational considerations, common failure modes |
| Examples | Wherever possible, include concrete examples from realistic enterprise scenarios. Avoid abstraction without illustration. |
| Length discipline | Section length budgets in the structure table are firm targets. If a section is running long, ruthlessly cut. |

## Working Conventions

| Convention | Rule |
|---|---|
| No em dashes (—) anywhere in the document | Use commas, semicolons, periods, or parentheses instead |
| Tables over bullet points | Default to tables for any list of three or more comparable items |
| Cite primary sources | Regulation texts, NIST publications, BSI grundschutz, ENISA guidance, original research |
| Acknowledge uncertainty | If something is contested, evolving, or unclear in the regulation, say so rather than feigning certainty |
| Version control discipline | Each section draft is a Git branch. Merges to main require self-review against the quality standards above. |

## Local-First Workflow for Initial Setup

The repository is built and reviewed entirely locally before any push to GitHub. This avoids cluttering the public commit history with exploratory changes and ensures the first impression of the public repository is intentional.

### Workflow principles

| Principle | Rule |
|---|---|
| Build locally first | All scaffolding, schemas, stubs, and structure are created on the local machine before GitHub is involved |
| Use local Git from day one | `git init` runs immediately; commits are made locally as work progresses, providing rollback capability |
| No remote connection until ready | Do not add a GitHub remote or push until the local foundation is reviewed and approved |
| Single considered first push | The first push to GitHub presents a clean, intentional repository, not a messy exploration history |
| Branch-and-PR workflow only after the initial push | The simple direct-commit model is fine for the local setup phase; switch to feature branches once the project is on GitHub |

### Initial Tasks for Claude Code

When this brief is loaded into Claude Code, the first concrete actions are:

1. Confirm the working directory is the intended local project directory (e.g., `~/projects/eu-ai-security-mapping`) and that no Git remote exists
2. Run `git init` to initialize a local Git repository
3. Create the basic `.gitignore` (Node, Python, OS, IDE artifacts) as the first file
4. Create stub `README.md` and `CHANGELOG.md`
5. Create the directory structure as specified in the Repository Structure section
6. Create empty section files in `docs/sections/` with the section title and length budget as a comment header
7. Create the canonical document at `docs/main-document/EU-AI-Security-Mapping.md` with the full ToC and section placeholders
8. Initialize `data/regulations/` with a README explaining what source documents will be stored there
9. Create JSON schema files for `requirements.json`, `controls.json`, `threats.json`, and `mappings.json` with documented field definitions
10. Create initial GitHub Actions workflow stubs in `.github/workflows/` (placeholders, to be filled out later)
11. Make an initial local commit: `git add .` then `git commit -m "Initial project scaffolding"`
12. **Stop here.** Do not add a remote. Do not push. Do not start writing content.

### Author's review checkpoint

After the initial setup is complete locally, the author reviews:

| Check | What to verify |
|---|---|
| Directory structure matches the brief | All folders and stub files present |
| `.gitignore` is appropriate | No accidental commits of secrets, dependencies, or OS artifacts will occur |
| JSON schemas are reasonable | Field definitions make sense for downstream use |
| Section files have only title and length budget headers | Claude Code did not auto-generate placeholder content |
| `README.md` is minimal and accurate | No marketing language, no auto-filled boilerplate |
| Local Git history is clean | One initial commit, no junk |

If anything is wrong, fix it locally and amend the commit (`git commit --amend`) before proceeding.

### Connecting to GitHub when ready

Only after the local review passes:

1. Create an empty repository on GitHub via the web UI (no README, no .gitignore, no license; the repository must be empty)
2. Note the repository URL (SSH format preferred: `git@github.com:username/eu-ai-security-mapping.git`)
3. Add the remote: `git remote add origin <url>`
4. Push the local repository: `git push -u origin main`
5. On GitHub, configure branch protection on `main` to require pull requests for future changes

### Workflow after the initial push

From this point forward, switch to the feature-branch and pull-request workflow:

| Step | Command |
|---|---|
| Create a branch for new work | `git checkout -b feature/<descriptive-name>` |
| Make changes and commit locally | Normal Claude Code workflow |
| Push the branch | `git push -u origin feature/<descriptive-name>` |
| Open a Pull Request on GitHub | Via web UI |
| Self-review the PR diff | Read every change in GitHub's UI |
| Merge to main when satisfied | Standard merge or squash-merge |

After the initial setup, do not start writing content. Confirm the structure is correct, then return to Claude.ai chat for Phase 1 strategic work on the threat model framework and executive summary thesis before drafting begins.

## Success Criteria

The project is successful if:

1. The practitioner guide is published on GitHub with full text, references, and exports (PDF, DOCX, HTML)
2. The web tool is publicly accessible and demonstrably useful for navigating the regulatory mapping
3. At least one conference talk or substantial public presentation is delivered based on the work
4. The artifact is referenced or shared by at least three independent practitioners or organizations within six months of publication
5. The author can defend every claim in the document and every architectural decision in the tool against expert questioning

## Out of Scope for This Brief

The following decisions are deferred to later phases:

- Specific licensing terms beyond the high-level "CC BY 4.0 for document, MIT for code"
- Whether to seek peer review from named subject matter experts before publication
- Whether to translate the document or tool into German for DACH audiences
- Long-term maintenance commitment beyond initial publication
- Whether to extend the work into additional regulations, sectors, or jurisdictions

These are real questions but should not block initial repository setup or Phase 2 work.
