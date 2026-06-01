# Threat Impact Assessment Methodologies

Huggins, T., Despeignes, S., and Trivedi, D.  
Department of Computer Science, Bowie State University, Bowie, Maryland, USA

*Related work presented at CCSC-Eastern 2025. This document extends the conference proceedings.*

---

## Abstract

As technology keeps advancing so do the actions of threat actors, and one of the most damaging attack types is the data breach -- a security incident in which unauthorized parties access sensitive or classified information, including personal and corporate data. Data breaches have threatened the viability of organizations across all sectors. To defend against them, cybersecurity professionals rely on threat impact assessment methodologies: structured approaches for analyzing, understanding, and prioritizing potential threats to an organization's information systems. This document surveys the top ten threat assessment methodologies, explains how each works, and provides guidance on selecting the right approach for a given organizational context.

---

## 1. Introduction

### 1.1 Motivating Incident: The LastPass Breach (2022)

In 2022, LastPass -- a widely used password manager -- experienced a significant security breach that illustrates the compounding nature of modern attacks. The first intrusion began on August 25, when threat actors gained unauthorized access to one of LastPass's developer environments. LastPass CEO Karim Toubba initially informed customers the issue was minor and no personal data had been stolen.

Three months later, on November 30, LastPass detected unusual activity through third-party cloud storage providers. Attackers had used credentials stolen in the August breach to pivot into LastPass's cloud backup infrastructure. By December 22, the scope became clear: attackers had accessed customer usernames, billing addresses, email addresses, phone numbers, IP addresses, and encrypted password vaults. Because master passwords were not compromised, direct credential theft was limited -- but the stolen metadata enabled targeted reconnaissance against organizations connected to LastPass.

This incident illustrates two critical lessons: (1) an initial breach that appears minor can enable a far more serious follow-on attack; and (2) third-party cloud storage creates supply chain risk exposure even for security-focused organizations.

### 1.2 Why Data Breaches Matter

The LastPass incident was relatively contained. Many breaches are not. Factors that can escalate a breach include compromised login credentials, unpatched vulnerabilities, insider threats, and poorly segmented networks. The potential impact operates at three levels:

- **User level:** Identity theft, credential exposure, financial loss.
- **Organization level:** Regulatory fines, reputational damage, operational disruption, litigation.
- **National level:** Compromise of critical infrastructure, government systems, or defense supply chains.

Regardless of when or how a breach is stopped, attackers typically have already exfiltrated data that can be sold or weaponized. The best defense is proactive: implementing threat impact assessment methodologies before an incident occurs.

### 1.3 Distinguishing Frameworks, Methodologies, and Tools

| Term | Definition | Flexibility |
|---|---|---|
| Framework | High-level guidance organized around principles, without prescribing specific steps. Example: NIST CSF 2.0. | High |
| Methodology | A structured, step-by-step process for a specific activity. Example: STRIDE threat modeling. | Moderate |
| Tool | Software or technique that automates or implements part of a methodology. Example: Microsoft Threat Modeling Tool. | Low (task-specific) |

Frameworks provide direction. Methodologies operationalize that direction into repeatable processes. Tools support specific steps within a methodology.

---

## 2. Threat Assessment Defined

Threat impact assessment involves analyzing, understanding, and prioritizing potential threats that could negatively affect an organization's security posture. Key factors considered include:

- **Likelihood:** How probable is the threat given current controls?
- **Technical performance:** Does the threat exploit a known, unpatched vulnerability?
- **Cost and schedule:** What is the recovery cost and downtime if the threat materializes?
- **Political and economic factors:** Could the incident damage the organization's reputation or trigger regulatory penalties?

Effective assessments prioritize risks to form a rational basis for resource allocation. As MITRE notes, "prioritizing risks is to form a basis for allocating resources" -- organizations cannot protect against all threats equally, so assessment methodologies help focus investment where it matters most.

---

## 3. Top 10 Threat Assessment Methodologies

### 3.1 STRIDE

**STRIDE -- Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege**

Developed in 1999 by Loren Kohnfelder and Praerit Garg at Microsoft, STRIDE is the most widely used threat modeling methodology. It provides a systematic checklist for identifying threats across six categories:

| Category | Definition | Example |
|---|---|---|
| Spoofing | Impersonating a user, process, or system | An attacker forges an email from a trusted domain to bypass phishing filters |
| Tampering | Unauthorized modification of data or code | An attacker modifies a software update package to inject malware |
| Repudiation | Denying that an action was performed | A user claims not to have transferred funds after a fraudulent wire transfer |
| Information Disclosure | Exposing data to unauthorized parties | A misconfigured S3 bucket exposes municipal financial records publicly |
| Denial of Service (DoS) | Preventing legitimate users from accessing a service | A volumetric DDoS attack takes a city's emergency services portal offline |
| Elevation of Privilege | Gaining capabilities beyond authorized permissions | An attacker exploits a kernel vulnerability to gain administrator access from a standard user account |

STRIDE is typically applied during system design using data flow diagrams to identify which threat categories apply to each component, data flow, and trust boundary.

### 3.2 PASTA -- Process for Attack Simulation and Threat Analysis

PASTA is a seven-stage, risk-centric threat modeling methodology that aligns business objectives with technical threat analysis:

1. Define objectives (business risk appetite)
2. Define technical scope (system components and data flows)
3. Application decomposition (identify attack surfaces)
4. Threat analysis (enumerate applicable threat scenarios)
5. Vulnerability and weakness analysis (map threats to existing vulnerabilities)
6. Attack modeling and simulation (model attacker paths)
7. Risk and impact analysis (quantify business impact and prioritize controls)

PASTA is more resource-intensive than STRIDE but produces risk-prioritized output directly tied to business impact -- valuable for executive decision-making.

### 3.3 DREAD -- Damage, Reproducibility, Exploitability, Affected Users, Discoverability

DREAD is a numerical risk-scoring methodology originally developed at Microsoft. Each of five dimensions is rated 1-10:

| Dimension | Definition |
|---|---|
| Damage | How much harm could the vulnerability cause? |
| Reproducibility | How easy is it to reproduce the exploit? |
| Exploitability | How much skill and effort does exploitation require? |
| Affected Users | What proportion of users would be impacted? |
| Discoverability | How easy is it for an attacker to find the vulnerability? |

The DREAD score is the average of these five ratings (or their sum). Higher scores indicate higher priority. DREAD has been criticized for subjectivity in scoring and has largely been replaced by CVSS for vulnerability scoring in enterprise contexts.

### 3.4 CVSS -- Common Vulnerability Scoring System

CVSS (maintained by FIRST -- Forum of Incident Response and Security Teams) provides a standardized numerical score (0.0-10.0) for software vulnerabilities. CVSS v3.1 scores are based on:

- **Base Score:** Inherent characteristics (attack vector, complexity, privileges required, user interaction, scope, confidentiality/integrity/availability impact)
- **Temporal Score:** Exploitability status and remediation level
- **Environmental Score:** Organizational context (modified metrics for the specific deployment)

CVSS is the standard used by the U.S. National Vulnerability Database (NVD) and is the most widely cited vulnerability scoring system for patch prioritization.

### 3.5 Attack Trees

Attack trees model attacker goals as the root of a tree, with sub-goals and attack steps as branches. Each leaf node represents an atomic attacker action. The tree structure enables:

- Combining AND and OR logic (all sub-goals must be achieved vs. any one suffices)
- Assigning probability and cost attributes to leaf nodes
- Computing aggregate attack probability and cost for entire paths

Attack trees are useful for analyzing complex multi-step attacks and comparing the relative cost of different attack paths versus the cost of countermeasures.

### 3.6 Trike

Trike is a threat modeling methodology that frames security analysis from a risk management perspective. It uses a requirements model (what should the system allow?) and an implementation model (what does the system actually do?) to derive a list of threats, where each threat is analyzed for its risk level and assigned to a stakeholder for mitigation.

Trike is notable for its explicit focus on acceptable risk: the analyst defines which threat scenarios are acceptable to the organization before identifying mitigation requirements, rather than treating all threats as unacceptable by default.

### 3.7 hTMM -- Hybrid Threat Modeling Method

The hybrid Threat Modeling Method (hTMM) combines elements of STRIDE, Security Cards, and SQUARE (Security Quality Requirements Engineering). It is designed to be more practical for agile development teams, using a structured workshop format rather than a comprehensive upfront analysis.

hTMM produces a prioritized threat list with associated mitigations in a format compatible with backlog-driven development practices.

### 3.8 Security Cards

Security Cards is a brainstorming methodology developed at the University of Washington. The deck consists of 42 cards covering human impacts, adversary motivations, resources, and attack methods. Teams use the cards to explore threat scenarios that might be missed by more structured methods like STRIDE.

Security Cards are particularly useful for uncovering non-obvious threats (e.g., attacks motivated by embarrassment rather than financial gain) and for facilitating threat modeling workshops with non-technical stakeholders.

### 3.9 OCTAVE -- Operationally Critical Threat, Asset, and Vulnerability Evaluation

OCTAVE was developed by Carnegie Mellon University's Software Engineering Institute (SEI). It emphasizes self-directed risk assessment, where internal teams (rather than outside consultants) drive the evaluation. OCTAVE exists in three variants:

- **OCTAVE** (original): Three-phase process for large organizations.
- **OCTAVE-S:** Simplified version for small organizations with limited IT staff.
- **OCTAVE Allegro:** Focuses on information assets rather than IT systems; suitable for cloud and distributed environments.

OCTAVE is a good fit for resource-constrained municipal governments because it is designed for self-assessment without requiring specialized security consultants.

### 3.10 Quantitative Threat Modeling Method

Quantitative threat modeling translates threat scenarios into financial terms, expressing risk as Expected Annual Loss (EAL) = Single Loss Expectancy (SLE) x Annual Rate of Occurrence (ARO). This approach aligns security investment decisions with financial risk management practices and enables direct comparison of the cost of a control versus the risk it mitigates.

Methods such as FAIR (Factor Analysis of Information Risk) provide a structured quantitative framework for this type of analysis.

---

## 4. Framework Comparison

### Choosing a Methodology

| Use Case | Recommended Methodology |
|---|---|
| System design (identifying threats early) | STRIDE or PASTA |
| Vulnerability prioritization and patch management | CVSS |
| Multi-step attack path analysis | Attack Trees |
| Financial risk quantification for executive reporting | Quantitative / FAIR |
| Small organizations or municipalities with limited staff | OCTAVE-S or OCTAVE Allegro |
| Agile development teams | hTMM |
| Workshop with non-technical stakeholders | Security Cards |
| Risk-centric, business-aligned assessment | PASTA or Trike |

### Frameworks vs. Methodologies in Practice

Threat assessment methodologies complement cybersecurity frameworks rather than replacing them. NIST CSF 2.0's Identify function explicitly requires risk assessment -- STRIDE, PASTA, or OCTAVE are the operational tools for satisfying that requirement. Similarly, the Govern function's supply chain risk management requirements (GV.SC) benefit from PASTA's vendor threat modeling capability.

---

## 5. Application to Municipal Government

Municipal governments typically have limited cybersecurity staff and IT budgets. This suggests the following approach:

1. **Start with STRIDE** during procurement and major system deployments to identify the most obvious threats without significant time investment.
2. **Apply OCTAVE Allegro** for annual self-assessments of critical information assets (citizen data, financial systems, emergency services platforms).
3. **Use CVSS** for vulnerability patch prioritization -- subscribe to CISA's Known Exploited Vulnerabilities (KEV) catalog and patch KEV entries first.
4. **Build toward PASTA** as staff capacity grows, particularly for supply chain risk assessments of major vendors.

---

## References

[B1] M. Syafrizal, S. R. Selamat, and N. A. Zakaria, "Analysis of Cybersecurity Standard and Framework Components," *IJCNIS*, vol. 12, no. 3, Apr. 2022. https://doi.org/10.17762/ijcnis.v12i3.4817

[B2] B. Bokan and J. Santos, "Managing Cybersecurity Risk Using Threat Based Methodology for Evaluation of Cybersecurity Architectures," *IEEE Xplore*, Apr. 2021.

[B3] R. Leszczyna, "Review of Cybersecurity Assessment Methods: Applicability Perspective," *Computers and Security*, vol. 108, p. 102376, 2021. https://doi.org/10.1016/j.cose.2021.102376

[B4] M. Toussaint, S. Krima, and H. Panetto, "Industry 4.0 Data Security: A Cybersecurity Frameworks Review," *Journal of Industrial Information Integration*, vol. 39, p. 100604, 2024. https://doi.org/10.1016/j.jii.2024.100604

[B5] P. Kirvan and J. Granneman, "Top 7 IT Security Frameworks and Standards Explained," *SearchSecurity*, Dec. 2021.

[B6] R. Ross and V. Pillitteri, "Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations -- NIST SP 800-171 Rev. 3," NIST, 2024.

[B7] IBM, "What is GRC?," 2024. https://www.ibm.com/topics/grc

[B8] Stefanini Group, "Cybersecurity Maturity Model," 2024.

[B9] S. Savas and S. Karatas, "Cyber Governance Studies in Ensuring Cybersecurity," *International Cybersecurity Law Review*, vol. 3, no. 1, 2022.

[B10] CISA, "Emergency Services Sector Cybersecurity Framework Implementation Guidance," Aug. 2021.
