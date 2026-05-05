# Vendor Mappings

This directory holds contributor-attested mappings of specific vendor products to the framework's vendor-neutral control library.

## Status

The vendor mapping contribution interface is not yet open. It will be activated only after the threat model and controls library are mature (see Phase 5 in `PROJECT_BRIEF.md`). Mapping IDs may still change before that point, so early submissions are not accepted.

## How mappings will work (preview)

| Aspect | Position |
|---|---|
| Eligibility | Vendor-submitted mappings preferred; community-submitted mappings accepted with disclosure |
| Schema compliance | Mandatory; validated automatically via CI |
| Quality criteria | Must reference framework control IDs, cite vendor documentation, declare scope, include last-reviewed date |
| Independence safeguards | The framework author works at ServiceNow and recuses from reviewing any ServiceNow-submitted mapping; an independent reviewer is arranged at submission time |
| Currency | Mappings marked stale after 12 months without review; archived after 24 months |
| Conflict resolution | Vendor mappings take precedence over third-party mappings for the same product |

## Files

| File | Purpose |
|---|---|
| `_template.json` | Schema template for new mapping submissions (to be authored once the schema is defined) |
| `<vendor>-<product>.json` | One file per vendor product, named in lowercase with hyphens |

## Index of accepted mappings

None yet.
