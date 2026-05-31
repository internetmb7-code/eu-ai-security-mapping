# 2. Scope and Disclaimer

## What this framework addresses

This framework addresses the security of enterprise AI agent deployments under EU regulation. It focuses on the intersection of four named regulations (the EU AI Act, NIS2, DORA, and GDPR) and the security-relevant operational concerns specific to agentic AI systems. Where these concerns overlap with general information security, the framework defers to established practice. The contribution is in the agent-specific layer that existing security frameworks do not cover.

## What counts as an agent

The framework's claims apply to systems meeting all four of the following criteria:

| Criterion | Description |
|---|---|
| 1. Natural language instruction | The system accepts instructions in natural language as its primary control interface |
| 2. Autonomous tool selection | The system decides which tools or actions to invoke without human approval at each step |
| 3. Real-world effect | The system executes those actions against external systems with effect beyond the model's own context |
| 4. Multi-step operation | The system operates over multiple steps within a single workflow |

This definition is deliberately narrow. It distinguishes agents from related systems that share some characteristics but not all.

### In scope

| System type | Examples |
|---|---|
| Workflow automation agents | Agents creating, modifying, or routing enterprise records autonomously |
| Customer-facing agents with action authority | Agents that issue refunds, file tickets, update accounts |
| Developer copilots with execution access | Agents with shell or repository write access |
| Multi-agent systems with delegation | Orchestrator agents that delegate to sub-agents across workflows |
| Autonomous research and analysis agents | Agents that retrieve, summarize, and act on findings |

### Out of scope

| System type | Reason for exclusion |
|---|---|
| Single-shot LLM calls (chat without tools) | No autonomous action; covered by general content-security practice |
| Retrieval-augmented generation without action capability | Read-only; covered by data-access controls |
| Classifier or recommendation models | Adversarial ML literature and MITRE ATLAS apply directly |
| Workflow automation with AI-assisted steps and human approval at each action | Human-in-the-loop addresses most agent-specific risks |

Organizations operating systems outside these criteria may still find the threat patterns useful, but the framework's specific claims about controls and regulatory mapping are calibrated to in-scope systems.

## Audience

The primary audience is CISOs and security program leads responsible for AI deployments in regulated enterprises, particularly in the DACH region. The framework assumes the reader operates within an established security program (typically based on NIST SP 800-53, ISO/IEC 27001, BSI grundschutz, or equivalent) and is integrating AI-specific concerns into that program.

The secondary audience is enterprise security architects designing agent deployments, and compliance or regulatory leads navigating the intersection of AI security and EU regulation.

Readers who are new to AI security generally, or who do not operate within an existing security program, will find the framework dense and presupposing. The framework does not teach foundational security concepts; it builds on them.

## Disclaimer

This framework is a guideline. It is not legal advice. It reflects the author's interpretation of public regulatory texts, the author's operational experience, and current public research on agent security. None of these are substitutes for qualified legal counsel, formal compliance assessment, or organizational risk management decisions.

Readers should treat the framework as a structured starting point for their own analysis, not as an authoritative determination of compliance or sufficiency. Where the framework cites specific regulatory articles, readers verifying compliance should consult the official consolidated texts on EUR-Lex and seek legal counsel where the answer matters.

The framework is offered without warranty. The author and contributors are not responsible for outcomes arising from its application.

## Author affiliation and independence

The author works at ServiceNow. The framework is independent practitioner work. No ServiceNow products, services, or proprietary information are referenced in the threat catalog or control library. No ServiceNow competitor is referenced either.

The framework is designed to accept contributed vendor-specific control mappings under the contribution interface described in CONTRIBUTING.md. If a ServiceNow mapping is submitted, the author will recuse from its review. An independent reviewer will be arranged at submission time. The recusal policy applies specifically to ServiceNow content; the author retains responsibility for the framework's threat catalog, control library, and methodology.

This separation is structural, not cosmetic. The framework's threat and control content exists independently of any vendor's product capabilities.

## Vendor mapping disclaimer

Vendor mappings, where they exist in `data/vendor-mappings/`, are contributor-attested representations of how specific vendor products implement framework controls. They are not framework-verified. Readers evaluating a specific vendor product against the framework should verify mapping claims against current vendor documentation and the vendor's own attestations.

As of v1, no vendor mappings have been contributed.
