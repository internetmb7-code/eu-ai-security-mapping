# 1. Executive Summary
<!-- Length budget: 1-2 pages -->

This is a practitioner framework for the security of enterprise AI agent deployments under EU regulation. It maps the security-relevant requirements of the EU AI Act, NIS2, DORA, and GDPR to a concrete agent-specific threat catalog and to operational controls that extend, rather than replace, established security programs based on NIST SP 800-53, ISO/IEC 27001, and BSI grundschutz.

## What this framework is

Three interlinked artifacts:

| Artifact | Purpose |
|---|---|
| Threat catalog | Ten exemplar threats organized across six attack surfaces specific to agentic AI deployments, with concrete attack scenarios and recommended controls for each |
| Control library | Five v1 controls covering identity, runtime, data, governance, and audit dimensions, mapped to the threat catalog and to existing security standards |
| Regulatory crosswalk | Direct and reasoned mappings from the named EU regulations to the controls that address their requirements for agent deployments |

The framework is vendor-neutral and product-agnostic. It is intended to be useful regardless of which agent platform or AI provider an organization deploys.

## Why it exists

Practitioners in regulated DACH enterprises currently lack a consolidated reference for navigating the intersection of EU AI regulation and agent-specific security. Existing material is either legalistic and not actionable, technical and not regulation-aware, or vendor-specific and not interoperable. The framework fills that gap with structured, defensible content that integrates into existing security programs.

The framework treats threats as patterns within a finite attack surface taxonomy rather than as an exhaustive enumeration. The methodology for discovering threats in a specific deployment is the durable contribution; the named threats are exemplars.

## What this framework is not

It is not legal advice. It is not a complete defense for any agent deployment. It is not a replacement for existing security programs based on established standards. It is a guideline for practitioners, written from the perspective of fifteen years of operational security experience, that should be adapted to specific organizational contexts in consultation with qualified counsel and existing risk-management processes.

The author works at ServiceNow. The framework is independent practitioner work. No ServiceNow products or competitors are referenced in the threat catalog or control library. Vendor-specific mappings, if contributed in future, will be reviewed by independent reviewers when the contributing vendor is the author's employer.

## How to use it

Section 5 (threat patterns and exemplars) is the entry point for security architects evaluating an agent deployment. Section 6 (controls) is the entry point for security program leads integrating agent-specific controls into existing programs. Section 4 (regulatory crosswalk) is the entry point for compliance and regulatory leads. Section 8 (gaps and open problems) names what the framework does not yet do; readers should consult it before relying on the framework for high-stakes decisions.

The framework is best used as a working reference applied to a specific deployment, not as a checklist completed once. Threats and controls evolve; the framework will evolve with them.
