# Regulatory Facts: Source-of-Truth Reference

Internal reference file for the EU AI Security Mapping framework. Provides verified citations and dates for the four regulatory instruments in scope, plus DACH-specific national rules. Update when source positions change. Cite this file from Section 3 (Regulatory landscape) and from threat or control specifications that reference dates or article numbers.

Last verified: 6 May 2026.

## EU AI Act (Regulation (EU) 2024/1689)

| Attribute | Value | Source |
|---|---|---|
| Full title | Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence | EUR-Lex |
| Adopted | 13 June 2024 | EUR-Lex |
| Published in OJ | 12 July 2024 | EUR-Lex |
| Entered into force | 1 August 2024 | digital-strategy.ec.europa.eu |
| Application: prohibitions (Chapter II) and AI literacy obligations | 2 February 2025 | digital-strategy.ec.europa.eu |
| Application: governance and GPAI model obligations (Chapter V) | 2 August 2025 | digital-strategy.ec.europa.eu |
| Application: most remaining provisions including Annex III high-risk obligations | 2 August 2026 | digital-strategy.ec.europa.eu |
| Application: Article 6(1) high-risk systems (AI as safety components in products under Annex I, e.g. medical devices, civil aviation) | 2 August 2027 | digital-strategy.ec.europa.eu, Mayer Brown |
| Pending modifier | Digital Omnibus simplification proposal published 19 November 2025 may extend high-risk application timeline by up to 16 months pending availability of harmonised standards | bakermckenzie.com |

### Article map for security practitioners

| Article range | Topic | Relevance to agent security |
|---|---|---|
| Article 6 and Annex III | High-risk classification rules | Determines whether an agent deployment falls under high-risk obligations |
| Article 9 | Risk management system | Direct mapping to threat modeling and control selection |
| Article 10 | Data and data governance | Training data quality, bias mitigation |
| Article 12 | Record-keeping (logging) | Direct mapping to CTL-005 (audit) |
| Article 13 | Transparency and information to deployers | Customer-facing security advisory implications |
| Article 14 | Human oversight | Direct mapping to CTL-003 (action verification) |
| Article 15 | Accuracy, robustness, cybersecurity | Direct mapping to most operational threats |
| Articles 16-22 | Provider obligations (general, QMS, documentation, logs, corrective action, cooperation, authorised representatives) | Apply if your customer is an AI system provider |
| Article 26 | Deployer obligations for high-risk AI systems | Apply to most enterprise customers running agents |
| Article 27 | Fundamental rights impact assessment | Required of public-sector and certain private deployers |
| Article 50 | Transparency obligations for AI systems interacting with natural persons | Disclosure that user is interacting with AI |
| Articles 53-55 | GPAI model provider obligations | Apply to model providers (OpenAI, Anthropic, Google, etc.), not deployers |

## NIS2 Directive (Directive (EU) 2022/2555)

| Attribute | Value | Source |
|---|---|---|
| Full title | Directive (EU) 2022/2555 on measures for a high common level of cybersecurity across the Union | EUR-Lex |
| Adopted | 14 December 2022 | digital-strategy.ec.europa.eu |
| Entered into force | 16 January 2023 | digital-strategy.ec.europa.eu |
| Member-state transposition deadline | 17 October 2024 | digital-strategy.ec.europa.eu |
| National measures applicable from | 18 October 2024 (where transposed) | nis-2-directive.com |
| NIS1 (Directive 2016/1148) repealed | 18 October 2024 | digital-strategy.ec.europa.eu |
| Estimated entities in scope | Approximately 160,000 across the EU (up from 10,000 to 15,000 under NIS1) | ENISA |
| Sectors in scope | 18 (Annex I plus Annex II), up from 7 under NIS1 | compliquest.com |

### DACH transposition status (verify before customer-facing use)

| Country | Status as of early 2026 | Source |
|---|---|---|
| Germany | Not yet transposed; NIS2UmsuCG (NIS-2-Umsetzungs- und Cybersicherheitsstärkungsgesetz) draft in parliamentary process; Commission reasoned opinion issued 7 May 2025 | nis-2-directive.com |
| Austria | Transposed (verify current status before citing) | gtlaw.com (general status) |
| Switzerland | Not in EU; not subject to NIS2 directly; relevant only via cross-border service obligations | n/a |

### Key NIS2 articles for agent security

| Article | Topic |
|---|---|
| Article 21 | Cybersecurity risk-management measures (the operative obligations: 10-point list including supply chain security, incident handling, access control, MFA) |
| Article 23 | Reporting obligations (24-hour early warning, 72-hour incident notification, one-month final report) |
| Article 32 | Supervisory measures and penalties |

## DORA (Regulation (EU) 2022/2554)

| Attribute | Value | Source |
|---|---|---|
| Full title | Regulation (EU) 2022/2554 on digital operational resilience for the financial sector | EUR-Lex |
| Adopted | 14 December 2022 | EUR-Lex |
| Entered into force | 16 January 2023 | EUR-Lex |
| Applies from | 17 January 2025 | EUR-Lex, hunton.com |
| Companion directive | Directive (EU) 2022/2556 (DORA Directive), transposition deadline 17 January 2025 | EUR-Lex |
| First CTPP designations | 18 November 2025 (19 critical ICT third-party providers including AWS, Microsoft, Google Cloud, IBM, Bloomberg, LSEG, TCS, Orange) | orbiqhq.com |

### Five pillars

| Pillar | Articles |
|---|---|
| ICT risk management | Articles 5 to 16 |
| ICT-related incident management, classification, reporting | Articles 17 to 23 |
| Digital operational resilience testing | Articles 24 to 27 |
| ICT third-party risk management | Articles 28 to 30 |
| Information and intelligence sharing | Article 45 |

### Key DORA articles for agent security in financial entities

| Article | Topic |
|---|---|
| Article 6 | ICT risk management framework |
| Article 9 | Protection and prevention (security controls baseline) |
| Article 17-18 | ICT incident classification and major-incident reporting |
| Article 28 | General principles for ICT third-party risk |
| Article 30 | Mandatory contractual provisions for ICT services supporting critical or important functions |

## GDPR (Regulation (EU) 2016/679)

| Attribute | Value | Source |
|---|---|---|
| Full title | Regulation (EU) 2016/679 (General Data Protection Regulation) | EUR-Lex |
| Applies from | 25 May 2018 | EUR-Lex |
| Article 22 wording (paragraph 1) | "The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her" | gdpr.algolia.com |

### Article 22 conditions for permissibility (paragraph 2)

A solely automated decision is permissible only when one of the following applies:

| Basis | Article 22(2) reference |
|---|---|
| Necessary for entering into or performance of a contract between data subject and controller | Article 22(2)(a) |
| Authorised by Union or Member State law with suitable safeguards | Article 22(2)(b) |
| Based on the data subject's explicit consent | Article 22(2)(c) |

In cases (a) and (c), Article 22(3) requires the controller to implement suitable measures to safeguard the data subject's rights, at minimum: the right to obtain human intervention, to express their point of view, and to contest the decision.

### Practical interpretation note

Article 22 applies only to "solely" automated decisions. Meaningful human review takes a system out of Article 22 scope. The threshold for "meaningful": the human reviewer must have authority and competence to override the decision; rubber-stamp review does not count. (EDPB Guidelines on Automated Decision-Making, WP251rev.01.)

## DACH-specific national rules

### BSI C5 Equivalence Regulation (C5-Gleichwertigkeitsverordnung, C5GleichwV)

| Attribute | Value | Source |
|---|---|---|
| Full title | Verordnung über gleichwertige Sicherheitsnachweise zum C5-Standard für Cloud-Computing-Dienste im Gesundheitswesen | gesetze-im-internet.de |
| Published | 19 March 2025 (BGBl. 2025 I Nr. 91) | gesetze-im-internet.de |
| Effective date (retroactive) | 1 July 2024 | gesetze-im-internet.de |
| Statutory basis | § 393 Abs. 4 Satz 4 SGB V (introduced by DigiG, 22 March 2024) | gesetze-im-internet.de |
| Scope | Cloud computing services processing social or health data for healthcare providers, statutory health insurers, and their processors | bsi.bund.de |
| Mechanism | Permits alternative certifications (e.g., ISO 27001 auf Basis IT-Grundschutz, SOC 2) as temporarily equivalent to a C5-Type-1 testat for a maximum of two years, conditional on a documented gap-closure plan | activemind.de |
| Hard deadline | C5-Type-2 testat ultimately required; equivalence period maximum two years from gap-plan creation | curacon.de |

Relevance to agent security framework: narrow. Affects healthcare-sector cloud and AI deployments in Germany specifically. Worth a short reference in Section 3 or a footnote, not a primary regulatory pillar.

### BSI IT-Grundschutz

| Attribute | Value |
|---|---|
| Status | German national security baseline framework, maintained by BSI (Bundesamt für Sicherheit in der Informationstechnik) |
| Latest compendium | IT-Grundschutz-Kompendium (annual editions; verify current edition before citing) |
| Relevance | Used as a control-mapping target alongside NIST SP 800-53 and ISO 27001 Annex A |

## Source quality notes

| Source category | Use for |
|---|---|
| EUR-Lex (eur-lex.europa.eu) | Primary source for regulation text and article wording. Use for any direct citation. |
| European Commission digital-strategy.ec.europa.eu | Official commentary on AI Act, NIS2, DORA. Reliable for dates and high-level scope. |
| ENISA | Authoritative for NIS2 implementation, scope estimates, sector taxonomy |
| EDPB (edpb.europa.eu) | Authoritative for GDPR interpretation, including Article 22 guidelines |
| Major law firms (Baker McKenzie, White & Case, Mayer Brown, DLA Piper, Jones Day) | Use for synthesis and timeline summaries; cross-check against primary sources |
| Vendor blogs and consultancy sites | Use only for orientation; never as a primary citation |

## Open questions for resolution before publication

| Question | Status |
|---|---|
| Final wording of Digital Omnibus simplification proposal and its impact on AI Act high-risk timeline | Pending; check Commission status quarterly |
| Germany NIS2 transposition (NIS2UmsuCG) entry into force | Pending; check parliamentary status quarterly |
| C5:2026 publication and superseding of C5:2020 | Referenced in BSI FAQ; verify current status before citing |
| First Annex III guidelines from Commission (originally expected by 2 February 2026) | Verify publication status |
