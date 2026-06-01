# Cybersecurity Compliance Landscape

A reference guide to major cybersecurity compliance standards and frameworks, organized by category. Relevant for organizations selling to government, handling regulated data, or seeking to demonstrate security maturity.

---

## Overview

Cybersecurity compliance standards fall into five broad categories: broad information security standards, industry-specific regulations, government and defense requirements, privacy and data rights laws, and technical and authentication protocols. No single standard covers all risks; most organizations need to satisfy a combination of requirements depending on their sector, data types, and customer base.

---

## Broad Information Security Standards

These frameworks provide a general roadmap for managing an organization's overall security posture. They are applicable across industries and are often used as the foundation for more specific compliance programs.

**ISO/IEC 27001 -- International Organization for Standardization / International Electrotechnical Commission Standard 27001**
An international standard for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS). ISO/IEC 27001 certification requires an independent audit and is recognized globally.
*Example: A managed IT service provider seeking to serve European government clients obtains ISO/IEC 27001 certification to demonstrate systematic security risk management.*
*Citation: [C1, C3]*

**SOC 2 -- Service Organization Control 2**
Developed by the American Institute of Certified Public Accountants (AICPA), SOC 2 is specifically designed for service providers (particularly SaaS companies) that store or process customer data. It evaluates controls across five Trust Services Criteria: security, availability, processing integrity, confidentiality, and privacy. A SOC 2 Type II report covers a 6-12 month observation period, providing stronger assurance than a Type I point-in-time assessment.
*Example: A cloud-based payroll vendor used by a Maryland county provides its SOC 2 Type II report to satisfy the county's vendor security requirements.*
*Citation: [C1, C5]*

**NIST Cybersecurity Framework (CSF)**
A voluntary framework used primarily in the U.S. that organizes cybersecurity activities and outcomes into six functions: Govern, Identify, Protect, Detect, Respond, and Recover (CSF 2.0). CSF 2.0 was released in February 2024 and added the Govern function to the original five. Widely adopted by federal agencies, state governments, and critical infrastructure operators.
*Example: This repository maps Maryland government policies to NIST CSF 2.0's six functions to benchmark municipal cybersecurity readiness.*
*Citation: [C4, C6]*

---

## Industry-Specific Regulations

These are mandatory for organizations operating within certain sectors or handling specific types of data. Non-compliance can result in significant fines, operational restrictions, or contract disqualification.

**PCI DSS -- Payment Card Industry Data Security Standard**
Required for any organization that processes, stores, or transmits credit card data, regardless of size. Maintained by the PCI Security Standards Council (a consortium of card brands including Visa, Mastercard, and AmEx). Current version: PCI DSS 4.0 (released 2022, enforcement began 2024).
*Example: A county government that accepts online permit payments must comply with PCI DSS Requirement 6.3.3 (all software protected against known vulnerabilities) and Requirement 8.3.6 (multi-factor authentication for all system access).*
*Citation: [C1, C7]*

**HIPAA -- Health Insurance Portability and Accountability Act**
A U.S. law enacted in 1996 that establishes national standards for protecting sensitive patient health information (Protected Health Information, PHI). The HIPAA Security Rule specifically governs electronic PHI (ePHI) and requires administrative, physical, and technical safeguards. Healthcare providers, health plans, and their business associates are covered entities.
*Example: A Maryland county health department must encrypt ePHI at rest and in transit, implement audit controls, and train workforce members annually on HIPAA requirements.*
*Citation: [C1, C7]*

**NERC CIP -- North American Electric Reliability Corporation Critical Infrastructure Protection**
A set of mandatory cybersecurity standards for organizations that own or operate bulk electric power systems in North America, enforced by NERC and regional entities. Violations carry fines of up to $1 million per day per violation.
*Example: A utility operating high-voltage transmission infrastructure must comply with NERC CIP-007-6 (Systems Security Management), which requires patching critical assets within 35 days of a vendor patch release for high-impact systems.*
*Citation: [C6]*

---

## Government and Defense Requirements

Organizations working with U.S. government entities must meet these requirements to be eligible for federal contracts and to handle government information.

**FedRAMP -- Federal Risk and Authorization Management Program**
A government-wide program that provides a standardized security authorization process for cloud products and services used by federal agencies. FedRAMP authorizations are reusable across agencies -- a vendor authorized by one agency can reuse that authorization for contracts with other agencies.
*Example: A SaaS document management vendor seeking federal contracts must obtain FedRAMP Moderate authorization before any federal agency can procure its service for handling Controlled Unclassified Information (CUI).*
*Citation: [C6, C8]*

**CMMC -- Cybersecurity Maturity Model Certification**
A Department of Defense (DoD) program requiring defense contractors and subcontractors to achieve independent certification of their cybersecurity practices before handling Federal Contract Information (FCI) or Controlled Unclassified Information (CUI). CMMC 2.0 has three levels: Level 1 (basic cyber hygiene, self-assessment), Level 2 (advanced, maps to NIST SP 800-171, third-party assessment for most contractors), Level 3 (expert, government-led assessment).
*Example: A small IT services firm in the defense industrial base must achieve CMMC Level 2 -- demonstrated by a third-party assessment organization (C3PAO) -- before it can renew a subcontract involving CUI.*
*Citation: [C6, C8]*

**FISMA -- Federal Information Security Management Act**
A U.S. federal law (enacted 2002, modernized 2014) requiring federal agencies and their contractors to develop, document, and implement information security programs covering all information and systems supporting agency operations. FISMA compliance is measured through annual OMB reporting and independent Inspector General assessments.
*Example: Every federal agency must submit an annual FISMA report to OMB and DHS covering system inventories, plan of action and milestones (POA&Ms), and continuous monitoring program status.*
*Citation: [C6]*

---

## Privacy and Data Rights

While overlapping with cybersecurity, these frameworks focus primarily on user data privacy, consent, and legal rights.

**GDPR -- General Data Protection Regulation**
A comprehensive European Union data protection regulation (effective May 2018) that governs how any organization -- globally -- collects, processes, and stores personal data of EU residents. Key principles include data minimization, purpose limitation, storage limitation, and rights to access, rectification, and erasure. Fines can reach the greater of EUR 20 million or 4% of global annual revenue.
*Example: A U.S. university that hosts international students from EU countries must honor GDPR data subject access requests and report data breaches to supervisory authorities within 72 hours.*
*Citation: [C7]*

**CCPA / CPRA -- California Consumer Privacy Act / California Privacy Rights Act**
California laws that grant consumers rights over personal information collected by businesses: the right to know, the right to delete, the right to opt out of data sales, and (under CPRA) the right to correct inaccurate information. Enforceable by the California Privacy Protection Agency (CPPA) and private right of action for data breaches.
*Example: A Maryland government contractor with operations in California that collects employee personal data must provide a privacy notice disclosing data collection practices and honor deletion requests within 45 days.*
*Citation: [C6]*

---

## Technical and Authentication Protocols

Unlike broad audit frameworks, these focus on specific technical implementations and are often embedded as requirements within the broader standards above.

**FIDO2 -- Fast Identity Online 2**
An open authentication standard developed by the FIDO Alliance and W3C that enables users to authenticate using common devices -- hardware security keys, biometric sensors, or mobile devices -- rather than passwords. FIDO2 eliminates phishing risk because credentials are cryptographically bound to the originating website and never transmitted to the server.
*Example: A city employee logs into a tax administration portal using a FIDO2 hardware key (YubiKey). An attacker who steals the employee's password gains nothing because FIDO2 requires physical possession of the registered key.*
*Citation: [C9, C10]*

**CIS Controls -- Center for Internet Security Controls**
A prioritized set of 18 safeguards (organized into Implementation Groups 1, 2, and 3) for reducing the most common and impactful cyberattacks. CIS Controls v8 aligns with NIST CSF and MITRE ATT&CK.
*Example: A resource-constrained municipality starts with CIS IG1 (the "basic cyber hygiene" subset of 56 safeguards) as a practical entry point to improving its cybersecurity posture without requiring a full NIST CSF 2.0 implementation.*
*Citation: [C4]*

---

## Compliance Requirements for Selling to Government

Organizations seeking to sell products or services to U.S. government entities must typically satisfy a combination of the following:

| Requirement | When Required |
|---|---|
| FedRAMP (Moderate or High) | Cloud services to federal agencies |
| FISMA compliance | Any contractor handling federal information systems |
| CMMC Level 2 | DoD contracts involving CUI |
| NIST SP 800-171 | Non-federal systems handling CUI |
| StateRAMP | Cloud services to state and local governments (emerging) |
| SOC 2 Type II | State/local government vendor due diligence (common requirement) |
| NIST CSF 2.0 alignment | Increasingly required in state IT procurement templates |

For municipal government vendors specifically, the most common baseline requirements are SOC 2 Type II, NIST CSF alignment, and contract-specific cybersecurity clauses (incident notification, right to audit, and data handling requirements).

---

## References

[C1] SafeAeon, "Industries and Compliance Overview." https://www.safeaeon.com/industries/

[C2] What Is My IP Address, "Cybersecurity Compliance Guide." https://whatismyipaddress.com/cybersecurity-compliance-guide

[C3] Fractional CISO, "Cybersecurity Compliance Standards." https://fractionalciso.com/cybersecurity-compliance-standards/

[C4] ConnectWise, "11 Best Cybersecurity Frameworks." https://www.connectwise.com/blog/11-best-cybersecurity-frameworks

[C5] Drata, "Compliance and Security Frameworks." https://drata.com/learn/compliance/security-frameworks

[C6] Security Compass, "Regulatory Security Compliance Frameworks and Standards." https://www.securitycompass.com/blog/regulatory-security-compliance-frameworks-standards/

[C7] Sprinto, "Compliance Standards." https://sprinto.com/blog/compliance-standards/

[C8] Secureframe, "Security Frameworks." https://secureframe.com/blog/security-frameworks

[C9] Microsoft, "What is FIDO2?" https://www.microsoft.com/en-us/security/business/security-101/what-is-fido2

[C10] Ping Identity, "FIDO2 Passwordless Authentication." https://www.pingidentity.com/en/resources/blog/post/fido2-passwordless.html

[C11] NIST, "NIST Updates Privacy Framework," Apr. 2025. https://www.nist.gov/news-events/news/2025/04/nist-updates-privacy-framework-tying-it-recent-cybersecurity-guidelines
