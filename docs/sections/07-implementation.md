# 7. Implementation Considerations

The v1 control library and the threat catalog are useful only when they connect to an actual deployment program. This section addresses the operational realities of implementing the controls, the sequencing that tends to work, the integration with existing security programs, and the anti-patterns that recur across enterprises attempting this work.

The framework is opinionated where opinions help. It defers where context-specific judgment matters more than general guidance.

## 7.1 Operational realities

Several themes recur across the v1 controls. Practitioners planning implementation should design for these explicitly rather than discovering them mid-deployment.

### Performance overhead is real but bounded

Each of the v1 controls adds latency. CTL-001 (identity propagation) adds 10 to 50 ms per downstream call. CTL-002 (provenance envelopes) adds 5 to 15 ms per tool invocation. CTL-004 (output filtering) adds 20 to 100 ms per response. CTL-005 (audit) is asynchronous in most implementations but increases storage and SIEM ingestion costs.

In isolation, each is manageable. Cumulative across a multi-step agent workflow, the latency stacks. A workflow that invokes five tools and produces a filtered response can easily add 200 to 500 ms beyond the model invocation itself. This is acceptable for most enterprise use cases but breaks consumer-facing experiences with sub-second response expectations.

Plan for the cumulative cost, not the per-control cost. Where latency is critical, the strongest implementations push provenance and identity propagation into the protocol layer rather than the application layer.

### Legacy integration is the hardest part

Most enterprise systems were not designed for agent-mediated authorization. They authenticate against service accounts, they authorize against the calling identity rather than a propagated user identity, and they log against the agent rather than the originating user. Implementing CTL-001 against modern systems is mechanical. Implementing it against legacy systems requires either narrowing the agent's reach (so it does not need legacy integration) or accepting wider authorization scope on legacy paths (with compensating controls).

This is not an implementation defect of the framework. It is an enterprise architecture reality. Plan for it. A common pattern is to scope agent deployment phase one to systems that support user-context propagation, then expand to legacy systems with explicit risk acceptance for those paths.

### Reasoning provenance is structurally limited

CTL-005 captures decision provenance to the extent the model emits it. Current LLMs do not produce reliable explanations of their own reasoning. Implementations should capture chain-of-thought where models produce it and should not synthesize reasoning where models do not. This is not optional honesty; it is a structural property of the technology.

Practitioners who expect the audit to produce a complete causal chain from input to action will be disappointed. The audit produces what is captureable. For high-stakes decisions where complete reasoning provenance matters, human review at the action boundary (CTL-003) is the only fully reliable accountability mechanism.

### Configuration drift erodes coverage

Every v1 control is vulnerable to configuration drift. Initial deployment with correct authorization scoping, threshold definitions, output filters, and audit retention can degrade over months as new use cases are added, new tools are integrated, and new tenants are onboarded. The drift is rarely a single bad decision; it is the accumulation of small accommodations.

Build governance for periodic review into the deployment plan from the start. Treat the v1 controls as living configurations, not deployment-time decisions.

## 7.2 Sequencing recommendations

There is no universally correct order for implementing the v1 controls, but some controls depend on others. The dependency graph constrains where to start.

| Stage | Implement | Why this order |
|---|---|---|
| 1 | CTL-001 (Identity and authorization context propagation) | Foundational. User-context propagation is a prerequisite for meaningful application of CTL-004 (output filtering can only filter to user authorization if user context is propagated) and CTL-005 (audit can only attribute to the originating user if user context flows through the agent runtime). |
| 2 | CTL-005 (End-to-end audit and accountability) | Without audit, the other controls operate without visibility. Audit infrastructure also takes time to build (correlation, retention, access control on logs themselves), so starting early lets it mature alongside the other work. |
| 3 | CTL-002 (Tool-output and context provenance) | Provenance is independently valuable for AGT-001 defense and is a building block for CTL-005 (context provenance dimension) and downstream detection. |
| 4 | CTL-003 (Action verification at high-impact boundaries) | Builds on identity propagation (knowing who) and audit (knowing what happened). The hardest part of CTL-003 is defining the impact thresholds, which is policy work that should not block earlier technical work. |
| 5 | CTL-004 (Authorization-aware output filtering) | Builds on user-context propagation and provenance metadata. Often the last control implemented because it depends on the others being in place. |

This sequence is for organizations starting from scratch. Organizations with existing programs based on NIST, ISO, or BSI will have partial coverage of CTL-001 and CTL-005 already and should sequence based on gap analysis against the existing program rather than starting from stage 1.

### Pace expectations

A reasonable pace for an enterprise with an existing security program is one v1 control quarter. Faster is possible with dedicated resources; slower is common when controls compete for attention with other security priorities. Trying to implement all five in a single quarter risks shallow implementation across all of them rather than meaningful deployment of any.

## 7.3 Integration with existing security programs

The v1 controls are agent-specific extensions to established control frameworks. They do not replace those frameworks. Organizations operating under NIST SP 800-53, ISO/IEC 27001, or BSI grundschutz already have foundational identity, audit, and access control programs. The v1 controls extend those programs to the agent context.

### How to integrate

For each v1 control, the existing standard mapping section identifies the closest equivalent in NIST, ISO, and BSI. Use that mapping as the integration point. If the organization already has a mature implementation of NIST AC-3 (access enforcement), CTL-001 is an extension that applies AC-3 to agent runtime. The organizational ownership, the audit cadence, the policy documentation, and the control assessment processes already exist; they need to be extended, not duplicated.

If the organization does not yet have a mature implementation of the foundational control, address the foundation first. Implementing CTL-001 without solid identity propagation in the broader environment is building on sand.

### Where the framework adds value

The framework's specific contribution to existing programs is the agent-specific implementation pattern, the operational considerations, and the common failure modes documented for each control. These are the parts not present in NIST, ISO, or BSI catalogs because they were not designed with agents in mind. Practitioners can leverage existing program structure while adopting agent-specific guidance from the framework.

### Where the framework defers

Where existing controls adequately address an agent-specific concern, the framework defers rather than restating. Network segmentation, encryption at rest, key management, and similar foundational concerns are addressed by existing literature and not re-covered here. If an agent-specific concern reveals a gap in foundational security, address it with foundational controls.

## 7.4 Measurement and assurance

Measuring whether the v1 controls are operating as intended is harder than implementing them. Agent behavior is emergent. Configuration drift is silent. Detection signal is weak in current SIEM tooling.

A few approaches help:

| Approach | What it provides |
|---|---|
| Periodic configuration audit | Verify CTL-001 scope, CTL-003 thresholds, CTL-004 filter rules, and CTL-005 retention policies match documented policy; surface drift |
| Synthetic transaction testing | Generate agent interactions known to trigger high-impact actions, verify CTL-003 verification fires; generate interactions with sensitive content, verify CTL-004 filtering works |
| Audit log review at sample frequency | Periodic human review of agent action audit; surfaces patterns that automated detection misses |
| Red team or adversarial evaluation | Where feasible, controlled adversarial testing of agent deployments to surface gaps the controls did not anticipate |
| Cross-system correlation drills | Test the audit infrastructure by reconstructing specific past agent actions end-to-end; identify correlation breakdowns |

These are not novel measurement approaches; they are standard security practice applied to agent context. The framework does not specify metrics because metric design depends on what the organization needs to measure. The point is to plan for measurement explicitly rather than treating the controls as deploy-and-forget.

## 7.5 Anti-patterns

The following are recurring failure modes observed in enterprise agent deployments. Each is a way the framework can be applied incorrectly even when the controls are nominally implemented.

| Anti-pattern | Why it fails |
|---|---|
| Deploying CTL-005 without CTL-001 | Audit logs record agent actions but cannot attribute to originating users; accountability is broken at the foundation. Audit volume looks impressive but provides no forensic value. |
| Treating CTL-003 thresholds as a deployment-time decision | Thresholds set at deployment age quickly. Without periodic governance review, thresholds become rubber-stamping; reviewers process volumes too high to evaluate meaningfully. |
| Implementing CTL-002 only at the input boundary | Provenance is enforced when tool output enters the agent but stripped when the agent transforms it. Downstream the content is treated as agent-generated rather than tool-retrieved. The provenance signal is lost where it matters most. |
| Configuring CTL-004 to filter only direct quotation | The filter catches verbatim disclosure but misses paraphrase, summary, and composition. Inferential disclosure leaks at the rate the agent generates summaries, which is most of the time. |
| Treating the framework as a checklist | Practitioners implement all five v1 controls, declare agent security achieved, and stop. The controls are necessary but not sufficient; threats not covered by v1 (memory poisoning, tool-chain abuse, goal subversion) remain. |
| Skipping CTL-001 for legacy integrations | A pragmatic compromise becomes the new normal. Legacy paths retain broad authorization indefinitely. Risk acceptance is never revisited. |
| Treating provenance as model-enforced | CTL-002 is implemented via system prompt instructions telling the model to treat tool output as data. Models comply most of the time but not adversarially. Runtime enforcement is the only reliable implementation. |
| Confusing agent authorization with user authorization | Teams design the agent's service authorization carefully but never address user-context propagation. CTL-001 is partially implemented; CTL-002 through CTL-005 cannot function correctly. |
| Audit infrastructure that becomes a privacy incident | CTL-005 logs are retained without access control proportionate to their content. The audit infrastructure itself becomes a high-value target requiring its own protection. |
| Deploying agents to production before threshold policy exists | CTL-003 cannot meaningfully operate without thresholds. Deployments proceed with placeholder policies that do not match real risk tolerance. High-impact actions slip through. |

These are the patterns to watch for in your own deployment and in deployments you advise. They are not exhaustive. They are the ones that recur often enough to be worth naming.

## 7.6 Closing observation

The v1 control library is implementable. None of the controls requires technology that does not exist. None requires capabilities that mature enterprises do not already have in some form. What it requires is deliberate sequencing, sustained governance attention, and honesty about what the controls can and cannot do.

Most agent security failures will not come from the controls being technically inadequate. They will come from the controls being implemented partially, allowed to drift, or treated as a one-time deployment exercise rather than a sustained governance practice. The framework provides the structure. Sustained operational discipline provides the outcome.
