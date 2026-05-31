# 9. References

This section compiles the sources cited throughout the framework. References are organized by category for ease of navigation. Where multiple versions of a source exist, the most current consolidated text is cited.

## 9.1 EU Regulations and Directives

The four primary regulations addressed by the framework. Practitioners verifying compliance should consult these consolidated texts on EUR-Lex rather than the framework's interpretation.

| Source | Identifier | URL |
|---|---|---|
| Regulation (EU) 2024/1689 of the European Parliament and of the Council on AI (EU AI Act) | 2024/1689 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689 |
| Directive (EU) 2022/2555 on cybersecurity across the Union (NIS2 Directive) | 2022/2555 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555 |
| Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA) | 2022/2554 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554 |
| Regulation (EU) 2016/679 General Data Protection Regulation (GDPR) | 2016/679 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 |

Local copies of all four regulations are maintained in `data/regulations/` in the framework repository.

## 9.2 Information Security Control Frameworks

The established frameworks against which the v1 control library is mapped. Each v1 control documents its relationship to specific provisions in these frameworks.

| Framework | Version | Publisher |
|---|---|---|
| NIST Special Publication 800-53, Security and Privacy Controls for Information Systems and Organizations | Revision 5 (with updates through 2026) | National Institute of Standards and Technology, United States |
| ISO/IEC 27001, Information security, cybersecurity and privacy protection - Information security management systems | 2022 edition (Annex A) | International Organization for Standardization |
| BSI IT-Grundschutz-Kompendium | 2024 edition | Bundesamt für Sicherheit in der Informationstechnik, Germany |
| NIST Cybersecurity Framework | 2.0 (2024) | National Institute of Standards and Technology, United States |
| NIST Special Publication 800-207, Zero Trust Architecture | 2020 | National Institute of Standards and Technology, United States |
| NIST Special Publication 800-37, Risk Management Framework for Information Systems and Organizations | Revision 2 (2018) | National Institute of Standards and Technology, United States |
| NIST Special Publication 800-92, Guide to Computer Security Log Management | 2006 (current as of 2026) | National Institute of Standards and Technology, United States |
| NIST Special Publication 800-122, Guide to Protecting the Confidentiality of Personally Identifiable Information | 2010 (current as of 2026) | National Institute of Standards and Technology, United States |
| ISO/IEC 27018:2019, Code of practice for protection of personally identifiable information in public clouds | 2019 | International Organization for Standardization |
| ISO/IEC 27037:2012, Guidelines for identification, collection, acquisition and preservation of digital evidence | 2012 | International Organization for Standardization |
| ISO/IEC 38500:2024, Governance of information technology | 2024 | International Organization for Standardization |
| ISO/IEC 42001:2023, AI management system | 2023 | International Organization for Standardization |
| CIS Controls | Version 8 | Center for Internet Security |

## 9.3 AI and Agent Security References

Sources specifically addressing AI security, agent security, and adversarial machine learning.

| Source | Publisher or Author | Notes |
|---|---|---|
| NIST AI Risk Management Framework | NIST | NIST AI 100-1, January 2023 and subsequent updates |
| NIST AI 100-2 E2025, Adversarial Machine Learning Taxonomy | NIST | Updated periodically |
| MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) | MITRE | https://atlas.mitre.org |
| MITRE ATT&CK | MITRE | https://attack.mitre.org |
| MITRE D3FEND | MITRE | https://d3fend.mitre.org |
| OWASP Top 10 for LLM Applications | OWASP | https://owasp.org/www-project-top-10-for-large-language-model-applications |
| ENISA AI Cybersecurity Framework | European Union Agency for Cybersecurity | Multiple publications, 2023 and forward |
| Google Secure AI Framework (SAIF) | Google | https://safety.google/saif |
| Cloud Security Alliance AI Controls Matrix | Cloud Security Alliance | First edition 2024 |

## 9.4 Identity, Authentication, and Authorization

Technical specifications underlying the identity and authorization patterns referenced in the framework.

| Source | Identifier | Notes |
|---|---|---|
| The OAuth 2.0 Authorization Framework | RFC 6749 | IETF |
| OAuth 2.0 Token Exchange | RFC 8693 | IETF; foundational for on-behalf-of patterns in agent identity propagation |
| JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens | RFC 9068 | IETF |
| HTTP Message Signatures | RFC 9421 | IETF; relevant for verifiable provenance metadata |
| SPIFFE and SPIRE specifications | SPIFFE project | https://spiffe.io |

## 9.5 Research Literature

Peer-reviewed and well-cited research informing specific threat patterns. Not exhaustive; representative.

| Source | Notes |
|---|---|
| Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023) | Foundational paper on indirect prompt injection (AGT-001) |
| NIST IR 8269 (2019) and successors, taxonomies of adversarial machine learning | Background for the adversarial ML field as it relates to agents |

## 9.6 Incident Handling and Forensics

| Source | Identifier | Notes |
|---|---|---|
| NIST Special Publication 800-61, Computer Security Incident Handling Guide | Revision 2 (2012; current as of 2026) | NIST |

## 9.7 Sources Maintained Outside the Framework

The framework references several catalogs and standards that are continuously maintained. Practitioners should consult the current published version of each rather than relying on the framework's snapshot.

| Source | Why to consult the current version |
|---|---|
| MITRE ATLAS | New agentic AI techniques are added regularly |
| MITRE ATT&CK | Adversarial techniques are added and refined regularly |
| OWASP Top 10 for LLM Applications | Updated as the LLM threat landscape evolves |
| NIST SP 800-53 | Updated periodically with new control variants and refinements |
| EUR-Lex consolidated texts | Regulations are amended over time; the consolidated text on EUR-Lex reflects the current legal status |
| ENISA AI Cybersecurity Framework publications | Updated as ENISA issues new guidance |

## 9.8 Note on Citation Style

Where the framework cites a specific regulatory article (for example "EU AI Act Article 15"), the citation refers to the consolidated text version current at the framework's publication date. Where the framework cites a control identifier (for example "NIST AC-3"), the citation refers to NIST SP 800-53 Revision 5. Where the citation style does not make the version explicit, the most current consolidated version at the framework's publication date is intended.

Practitioners using the framework for compliance work should verify cited provisions against the current consolidated texts before relying on them.
