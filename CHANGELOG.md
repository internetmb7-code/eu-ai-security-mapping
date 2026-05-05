# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Initial repository scaffolding (directories, section stubs, JSON schemas, workflow placeholders).
- Optional Appendix A stub `docs/sections/10-appendix-servicenow-mapping.md` for mapping generic controls to ServiceNow products. Non-canonical; the main document remains regulation-agnostic.
- Optional `servicenow_mapping` field on the controls schema to support the appendix without coupling the core schema to any vendor.
- Added AGT-002 (Authorization Confusion / Deputy Problem) as fully populated threat entry. Covers excess privilege, cross-tenant deputy, and delegation ambiguity sub-patterns. References controls CTL-008, CTL-009, CTL-011, CTL-016, CTL-022, CTL-029, CTL-031 (defined in later phase).
