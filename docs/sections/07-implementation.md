This section addresses how to deploy the v1 controls in environments that already have an established security program. The five subsections track the high-leverage decisions: where the controls plug into existing architecture, how to design the human review surface, where to place output filtering, how to roll out controls without exposing the organization to unnecessary risk, and how the controls produce evidence for regulatory obligations. Known gaps in the v1 control library are documented in Section 8 and are not revisited here.

## 7.1 Mapping controls to existing security architecture

Most organizations subject to NIS2 or DORA already operate identity, audit, and content security infrastructure. The v1 controls do not replace any of it; they extend it across the agent execution boundary. The integration patterns that work consistently in practice are:

| v1 control | Integrates with | Integration pattern |
|---|---|---|
| CTL-001 (Identity and authorization context propagation) | Existing IdP (Entra ID, Okta, Ping); existing OAuth / token-exchange infrastructure | The agent runtime acts as a downstream service in the token-exchange chain. The originating user's authorization context is carried forward as a delegated assertion (RFC 8693 token exchange or equivalent) rather than replaced with an agent service identity. The pattern that fails: the agent uses a service account with broad authorization and re-authorizes per call. The pattern that works: the agent inherits user context and the downstream tools enforce per-user authorization on retrieval. |
| CTL-002 (Tool-output and context provenance) | Existing data classification and DLP infrastructure | Provenance metadata is attached to content at ingest into the agent runtime and persisted through the execution. The agent runtime is responsible for distinguishing instruction from content; downstream consumers (including the model itself in subsequent turns) read the provenance tags. The pattern that fails: provenance lives only in agent logs after the fact. The pattern that works: provenance is part of the in-flight context and structurally distinguishes content from instruction at every boundary. |
| CTL-005 (End-to-end audit and accountability) | Existing SIEM (Splunk, Sentinel, Elastic); existing log retention infrastructure | Agent audit events flow into the existing SIEM as a new log source with a defined schema. The schema must include user attribution, tool invocation, retrieval scope, and decision provenance. The pattern that fails: agent logs as opaque blobs that the SOC cannot correlate with other security events. The pattern that works: agent logs as first-class structured events that the SOC can query alongside identity, network, and endpoint logs. |

The integration questions worth answering during design rather than discovering during operation:

| Question | Why it matters |
|---|---|
| Does the agent runtime have a service identity that the IdP can recognize as a delegated principal? | If not, CTL-001 cannot be implemented correctly; the agent will run with broad authorization and the deputy problem becomes structural |
| Does the SIEM ingest schema accommodate the cardinality of agent audit events? | A single user request can produce dozens of agent audit events; the SIEM must handle the volume without dropping or downsampling |
| Does the existing data classification taxonomy distinguish content origin? | If not, CTL-002 has no taxonomy to attach to; provenance becomes a parallel system rather than an extension of the existing one |

CTL-003 and CTL-004 integrate with workflow and content systems respectively; their integration considerations are covered in subsections 7.2 and 7.3.

## 7.2 Approval queue design for high-impact actions

CTL-003 places verification at high-impact action boundaries. The control specification does not prescribe the user experience; that is an operational decision with two failure modes.

The first failure mode is over-broad approval scope. If every agent action requires approval, operators ignore the queue. The agent provides no efficiency benefit and the organization has merely added a slow human step to a workflow that did not need automation. This is alert fatigue applied to approvals.

The second failure mode is under-broad approval scope. If only the most consequential actions require approval (large fund transfers, account deletions), the agent operates autonomously across a large surface where authorization confusion (AGT-002), tool-chain abuse (AGT-003), and goal drift (AGT-009) can produce harm without verification. The threshold appears to be set conservatively but is in fact the lower bound below which technical controls must work alone.

The patterns that hold up in practice:

| Approach | When it works | When it does not |
|---|---|---|
| Threshold based on action type alone (e.g., all fund transfers above EUR 10,000) | Actions are individually meaningful and the threshold reflects organizational risk tolerance | Actions compose; no single action exceeds the threshold but the composite does |
| Threshold based on cumulative effect (CTL-003's composition tracking) | Action composition is the dominant risk; AGT-003 is in scope | Operators cannot interpret cumulative thresholds; the queue surfaces opaque "cumulative limit reached" alerts |
| Threshold based on confidence (the agent's stated certainty about the action) | The model is well-calibrated and produces honest confidence signals | Models tend to be overconfident; thresholds based on stated confidence underapprove |
| Threshold based on user-context delta (the action affects users beyond the originating user) | AGT-002 (deputy problem) is the dominant risk | Single-user agents where the user always affects only themselves |

The approval surface itself is a design problem distinct from the threshold. Three properties worth designing for:

| Property | Why |
|---|---|
| The operator can see what the agent intends to do without re-reading the full conversation | Approvals must be possible in seconds, not minutes; the action description is the unit of decision |
| The operator can see the bridging context that makes the action high-impact | Why is this action surfacing for approval? Cumulative threshold? User-context delta? Without this, the operator cannot calibrate intuition over time |
| The operator can deny the action without ending the agent session | Hard-stop denial is rarely the right answer; "deny this action, propose an alternative" is. The approval surface must support negotiation |

Approval queue design is where the framework most acutely depends on factors outside its scope (operator training, organizational risk tolerance, audit retention policy). Subsection 4.7 of the crosswalk and Section 8 acknowledge that human factors are out of scope for v1; this subsection treats the approval surface as a technical artifact while flagging that the human side is the dominant determinant of effectiveness.

## 7.3 Output filtering placement decisions

CTL-004 (authorization-aware output filtering) produces a structural choice: where in the request lifecycle does filtering apply?

The two viable placements:

| Placement | Mechanism | Tradeoffs |
|---|---|---|
| Pre-retrieval filtering | The agent's retrieval calls are scoped to the user's authorization at the data layer (database row-level security, vector store metadata filters, search index ACLs) | Strongest guarantee; the agent cannot retrieve what it cannot see. Requires the data layer to enforce per-user authorization, which is often the existing access control architecture. Works only when the agent's retrieval interface respects the authorization model |
| Post-retrieval filtering | The agent retrieves with broad authorization and the output is filtered against the user's authorization before delivery | Weaker guarantee; the agent has temporarily seen content the user cannot see, creating residual risk through caching, logging, and side effects. Necessary when the data layer cannot enforce per-user authorization (e.g., document corpora with no per-user metadata) |

The combination that works: pre-retrieval filtering as the primary mechanism, post-retrieval filtering as a defense-in-depth layer for content classes where pre-retrieval cannot be enforced. The combination that creates the deputy problem at scale: post-retrieval filtering only, with the agent operating against a corpus that includes content for many users.

A practical signal that the placement is wrong: the audit trail (CTL-005) shows the agent retrieving content the user is not authorized for, even though the user never saw it. This is structurally equivalent to AGT-004 (data exfiltration via legitimate channels) at the model layer; the model has been exposed to the content and may surface it in subsequent turns through paraphrase or summarization that defeats post-retrieval filtering.

## 7.4 Phased rollout patterns

Agent deployments fail more often through scope expansion than through technical inadequacy. The pattern: a successful pilot with narrow tool authorization expands to broader tool authorization, broader user populations, or higher-stakes use cases without the corresponding investment in CTL-001 and CTL-003. The framework cannot prevent this organizationally, but the rollout phasing can make the expansion decision visible.

The phasing that works in regulated environments:

| Phase | Tool authorization | User population | Action surface | What gets validated |
|---|---|---|---|---|
| Pilot | Read-only against a single domain | Internal users with administrator visibility into agent behavior | Information retrieval; no consequential actions | CTL-001 propagation; CTL-005 audit completeness |
| Expansion 1 | Read-only across multiple domains; structured write to a single domain | Broader internal users | Limited consequential actions, all under CTL-003 verification | CTL-002 provenance under cross-domain retrieval; CTL-003 threshold calibration |
| Expansion 2 | Structured write across multiple domains | Internal users in operational roles | Consequential actions with selective CTL-003 verification based on calibrated thresholds | CTL-004 output filtering under broader authorization scopes; CTL-001 under multi-tenant or cross-organizational contexts |
| Production | Full deployed scope | Production user population | Full action surface | Continuous monitoring against the audit baseline established in earlier phases |

The decision criteria for moving between phases are organization-specific and not prescribed here. The decision criteria for not moving between phases are universal:

| Signal | What it indicates |
|---|---|
| CTL-005 audit shows authorization context drift across the pilot phase | CTL-001 implementation is incomplete; expansion will compound the gap |
| CTL-003 approval queue shows operator override patterns inconsistent with declared thresholds | Threshold calibration is wrong; expansion will produce alert fatigue |
| CTL-002 provenance failures are present in the audit trail | The agent is treating content as instruction in some path; expansion increases AGT-001 exposure |
| CTL-004 post-retrieval filtering is catching unauthorized content at non-trivial rate | Pre-retrieval filtering is not working; the data layer authorization model needs to be addressed before expansion |

Rollback triggers are simpler. Any of the four signals above, observed at production scale, is a rollback trigger to the previous phase. Rolling back is not a failure; rolling forward through the signals is.

## 7.5 Regulatory evidence collection

The crosswalk in Section 4 maps regulatory requirements to v1 controls. This subsection addresses the operational counterpart: what evidence the controls produce, and how that evidence connects to specific regulatory obligations.

Evidence is produced as a byproduct of correct operation, not as a separate compliance activity. If the controls are operating, the evidence exists. If the evidence does not exist, the controls are not operating. This is the structural relationship that makes the framework useful for compliance work; it is not a guarantee that the evidence is sufficient for any specific obligation, which depends on the regulator's interpretation and the deployer's broader compliance program.

| Regulatory obligation | Evidence the v1 controls produce | Operational source |
|---|---|---|
| EU AI Act Article 12 (record-keeping) | Automatically generated logs over the system lifecycle, including user attribution, tool invocation, retrieval scope, and decision provenance | CTL-005 audit stream; CTL-001 user attribution; CTL-002 retrieval and reasoning provenance |
| EU AI Act Article 14 (human oversight) | Approval queue records showing actions surfaced for human review, the operator decision (approve, deny, modify), and the timestamps for both | CTL-003 approval queue logs; CTL-005 audit of operator actions |
| EU AI Act Article 15 (accuracy, robustness, cybersecurity) | Audit-derived metrics on agent behavior under varied inputs; provenance trail for incidents involving content manipulation | CTL-002 provenance; CTL-005 audit; CTL-003 verification outcomes |
| NIS2 Article 21 (cybersecurity risk-management measures) | Evidence of access control enforcement (CTL-001), audit completeness (CTL-005), and operational monitoring derived from the audit stream | CTL-001 propagation logs; CTL-005 audit stream feeding the SIEM |
| NIS2 Article 23 (incident reporting) | Audit data sufficient to reconstruct events for the 24-hour, 72-hour, and one-month reporting cycles | CTL-005 audit retention with structured event schema |
| DORA Article 12 (major ICT-related incidents) | Audit data sufficient to reconstruct incident events; user and agent attribution for affected actions | CTL-005 with retention aligned to DORA reporting timelines |
| DORA Articles 28 to 30 (ICT third-party risk) | Audit and provenance data covering sub-agent and third-party tool invocations | CTL-001 across third-party tool boundaries; CTL-002 provenance across sub-agent outputs; CTL-005 audit of delegation chains |
| GDPR Article 5(2) (accountability) | End-to-end audit trail demonstrating compliance with processing principles | CTL-005 audit; CTL-002 provenance |
| GDPR Article 22 (automated individual decision-making) | Approval queue records demonstrating that decisions are not "solely" automated where Article 22 applies; audit trail supporting data subject contestability rights | CTL-003 approval queue; CTL-005 audit |
| GDPR Article 32 (security of processing) | Evidence of access control enforcement, output filtering, and incident audit consistent with appropriate technical measures | CTL-001, CTL-004, CTL-005 |

The evidence-collection decisions worth making during design:

| Decision | Why it matters |
|---|---|
| Audit retention period | Must accommodate the longest reporting cycle the organization is subject to (typically DORA's structured incident reporting or NIS2 Article 23's one-month final report). Under-retention forecloses compliance options |
| Schema versioning for audit events | Regulatory requirements evolve; audit schemas must accommodate evolution without re-deriving evidence from the past. Schema-versioned events are queryable across schema generations |
| Separation of audit data from operational data | Operational logs are often retained on a different cycle and with different access controls than compliance audit. Treating these as the same store creates retention conflicts and access-control conflicts |
| Read-only access for compliance and audit functions | Compliance reviewers need access to the audit stream that does not require operational privileges. The access pattern that fails: compliance asks operations for a one-time data extract, which then ages and is not reproducible |

For the cross-reference between specific articles and specific controls, see Section 4 (Common-control crosswalk). For known gaps in the v1 control library that affect what evidence can be produced, see Section 8 (Gaps and open problems).
