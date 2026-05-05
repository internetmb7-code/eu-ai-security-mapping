# EU AI Security Mapping

A vendor-neutral practitioner framework mapping EU AI Act, NIS2, and DORA security requirements to operational controls for enterprise AI agent deployments. Includes a defined contribution interface for vendor-specific control mappings.

**Status:** scaffolding. No content drafted yet.

## What this is

The project produces three interlinked artifacts:

1. **Practitioner Guide**: a 25 to 40 page technical document mapping EU regulatory requirements (EU AI Act, NIS2, DORA, GDPR Art. 22) to concrete, vendor-neutral security controls for enterprise AI and agent deployments, with an agent-specific threat model.
2. **Interactive Web Tool**: a multi-entry-point navigator for the framework, hosted publicly via GitHub.
3. **Vendor Mapping Contribution Interface**: a documented schema and process by which vendors and community contributors can submit mappings of their products to the framework's control library. Mappings live alongside the framework but are clearly attributed to their contributors.

## Vendor neutrality

The core framework is vendor-neutral. The threat model, controls library, and main document contain no vendor names, products, or branding. Vendor-specific content lives only in the separated mapping layer under `data/vendor-mappings/`, contributed by vendors or community members and clearly attributed.

This is a deliberate platform-style design. The framework is intended to be defensible as independent practitioner work in any external context, including AI labs, regulators, and conferences, while still providing a useful place for vendors and the community to publish product-specific mappings.

## Maintainer affiliation disclosure

The maintainer works at ServiceNow. This project is independent practitioner work and does not represent ServiceNow positions. The maintainer will recuse from reviewing any ServiceNow-submitted vendor mapping; an independent reviewer will be arranged for those submissions.

## Disclaimer

The framework is a guideline based on the maintainer's interpretation of public regulatory texts and operational security experience. It is **not legal advice**. Readers should consult qualified legal counsel for compliance determinations.

Vendor mappings, when present, are contributor-attested representations of how a specific product implements framework controls. They are not framework-verified. Readers evaluating a specific vendor product should verify mapping claims against current vendor documentation.

## Repository layout

| Path | Purpose |
|---|---|
| `PROJECT_BRIEF.md` | Scope, methodology, structure, phased workflow |
| `docs/main-document/` | Canonical practitioner guide (single source of truth) |
| `docs/sections/` | Section drafts before merge |
| `docs/frameworks/` | Methodology reference documents (threat model, control library, regulatory mapping, vendor mapping) |
| `data/regulations/` | Source regulation texts |
| `data/*.json` | Structured requirements, controls, threats, mappings |
| `data/vendor-mappings/` | Contributed vendor mappings (interface opens in Phase 5) |
| `tool/` | Web GUI (Phase 4) |
| `scripts/` | Helper scripts |
| `CONTRIBUTING.md` | Contribution interface (stub; expanded in Phase 5) |
| `CODE_OF_CONDUCT.md` | Contributor expectations (stub) |

See [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) for the full scope, methodology, and document structure.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The vendor mapping contribution interface is not yet open; it will be activated once the threat model and controls library are mature enough for stable mapping.
