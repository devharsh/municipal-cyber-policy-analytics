# Acronyms and Definitions

All acronyms used across this repository, expanded with a one-sentence definition and a concrete example drawn from the Maryland corpus or related literature.

---

## Frameworks and Standards

**AI -- Artificial Intelligence**
Software systems that perform tasks normally requiring human intelligence, such as reading comprehension, classification, and reasoning.
*Example: Claude Sonnet 4.6 (an AI model) classifies a 12,000-character government PDF excerpt and decides whether it covers the NIST CSF Protect function.*

**CIS -- Center for Internet Security**
A nonprofit organization that publishes the CIS Controls, a prioritized set of 18 safeguards for reducing the most common cyberattacks.
*Example: The MD Judicial Information Security Policy explicitly cites CIS Controls alongside NIST CSF as its governance references.*

**CMMC -- Cybersecurity Maturity Model Certification**
A U.S. Department of Defense program requiring defense contractors to demonstrate compliance with cybersecurity standards before receiving federal contracts.
*Example: A defense subcontractor bidding on a DoD IT services contract must obtain CMMC Level 2 certification, which maps to NIST SP 800-171 controls.*

**CSF -- Cybersecurity Framework**
A voluntary framework published by NIST that organizes cybersecurity activities and outcomes into functions, categories, and subcategories.
*Example: NIST CSF 2.0 adds a sixth function (Govern) to the original five functions of CSF 1.1.*

**CVSS -- Common Vulnerability Scoring System**
An open standard for rating the severity of software security vulnerabilities on a scale of 0.0 to 10.0.
*Example: The Log4Shell vulnerability (CVE-2021-44228) received a CVSS score of 10.0 (Critical), prompting emergency patching across thousands of organizations.*

**DREAD -- Damage, Reproducibility, Exploitability, Affected Users, Discoverability**
A risk-scoring methodology where each of the five components is rated 1-10 and averaged to prioritize threats.
*Example: A buffer overflow in a publicly exposed API might score Damage=9, Reproducibility=8, Exploitability=7, Affected Users=9, Discoverability=8 for a DREAD total of 8.2.*

**EO -- Executive Order**
A directive issued by the U.S. President that has the force of law for federal agencies.
*Example: EO 14028 (2021) directed federal agencies to adopt zero-trust architectures and improve software supply chain security.*

**F1 (F1 Score) -- Harmonic Mean of Precision and Recall**
A single metric that balances precision and recall, computed as 2 x (precision x recall) / (precision + recall). Ranges from 0 (worst) to 1 (best).
*Example: Method 1 achieves F1 = 0.353; Method 2 achieves F1 = 0.737. The 2x improvement reflects the reduction in false positives from 21 to 5.*

**FIDO2 -- Fast Identity Online 2**
An open authentication standard developed by the FIDO Alliance and W3C that replaces passwords with cryptographic keys stored on hardware security keys or biometric devices.
*Example: A municipal employee logs into a city portal using a YubiKey hardware token, which sends a cryptographic response instead of a typed password -- eliminating phishing risk.*

**FISMA -- Federal Information Security Management Act**
A U.S. law requiring federal agencies to develop, document, and implement information security programs.
*Example: Every federal agency must file an annual FISMA report with OMB covering the maturity of its information security program.*

**FedRAMP -- Federal Risk and Authorization Management Program**
A U.S. government program that provides a standardized security authorization process for cloud products used by federal agencies.
*Example: A SaaS vendor selling email archiving to a federal agency must obtain FedRAMP Authorization before the agency can procure the service.*

**GDPR -- General Data Protection Regulation**
A European Union regulation that governs how organizations collect, process, and store personal data of EU residents, with fines up to 4% of global revenue.
*Example: A U.S. municipality that provides online services to EU citizens (e.g., a tourism portal) must honor GDPR data subject access requests.*

**GRC -- Governance, Risk, and Compliance**
An integrated approach to aligning organizational strategy with risk management and regulatory requirements.
*Example: A city IT department implements a GRC platform to consolidate policy management, risk registers, and audit evidence in one system.*

**HIPAA -- Health Insurance Portability and Accountability Act**
A U.S. law that establishes national standards for protecting sensitive patient health information.
*Example: A Maryland county health department must encrypt patient records at rest and in transit to satisfy HIPAA's Security Rule requirements.*

**ISMS -- Information Security Management System**
A set of policies and procedures for systematically managing an organization's sensitive data, as defined in ISO/IEC 27001.
*Example: An organization that achieves ISO/IEC 27001 certification has demonstrated a functioning ISMS covering risk assessment, access control, and incident management.*

**ISO/IEC 27001 -- International Organization for Standardization / International Electrotechnical Commission Standard 27001**
An international standard for establishing, implementing, maintaining, and continually improving an Information Security Management System.
*Example: A cloud provider seeking to serve European government clients obtains ISO/IEC 27001 certification to demonstrate information security maturity.*

**LLM -- Large Language Model**
A neural network trained on large text corpora that can generate, classify, summarize, and reason about text.
*Example: Claude Sonnet 4.6 is the LLM used in Method 2 to classify government PDFs against NIST CSF 2.0 functions.*

**MD5 -- Message Digest Algorithm 5**
A hash function that produces a 128-bit fingerprint of any input file. Identical files produce identical MD5 hashes.
*Example: Four duplicate PDFs in the Maryland corpus were identified by comparing MD5 hashes; once matched, three copies were removed.*

**NERC CIP -- North American Electric Reliability Corporation Critical Infrastructure Protection**
Mandatory cybersecurity standards for organizations that own or operate bulk electric power systems in North America.
*Example: A utility operating a high-voltage transmission substation must comply with NERC CIP-007 (Systems Security Management), requiring patching within 35 days of a vendor patch release.*

**NIST -- National Institute of Standards and Technology**
A U.S. federal agency that develops measurement standards and guidelines, including widely adopted cybersecurity frameworks.
*Example: NIST published CSF 2.0 in February 2024, expanding the framework to include a Govern function for organizational oversight.*

**NIST SP 800-53 -- NIST Special Publication 800-53**
A catalog of security and privacy controls for federal information systems and organizations, organized into 20 control families.
*Example: A federal agency classifying a system as "High" impact under FIPS 199 must implement all SP 800-53 High baseline controls, including CM-6 (Configuration Settings).*

**OCR -- Optical Character Recognition**
Technology that converts scanned images of text into machine-readable characters.
*Example: Three documents in the Maryland corpus were scanned images with garbled OCR output, returning zero usable characters when processed by PyMuPDF.*

**PASTA -- Process for Attack Simulation and Threat Analysis**
A seven-step, risk-centric threat modeling methodology that aligns business objectives with technical threat analysis.
*Example: A financial services firm uses PASTA to model an attacker's path from a phishing email to accessing core banking systems, then prioritizes controls by estimated business impact.*

**PCI DSS -- Payment Card Industry Data Security Standard**
A security standard required of any organization that processes, stores, or transmits credit card data, maintained by the PCI Security Standards Council.
*Example: A county government that accepts online payments for permits must comply with PCI DSS Requirement 6.3.3, which mandates patching all software against known vulnerabilities.*

**RMF -- Risk Management Framework**
NIST's six-step process (Categorize, Select, Implement, Assess, Authorize, Monitor) for managing security risk in information systems, mandatory for U.S. federal agencies.
*Example: A federal IT system goes through RMF Authorize, where an Authorizing Official reviews the security assessment report and formally accepts residual risk before the system goes live.*

**SaaS -- Software as a Service**
A software distribution model in which applications are hosted in the cloud and accessed via the internet, rather than installed locally.
*Example: A municipality using a cloud-hosted payroll system (SaaS) must ensure the vendor has FedRAMP or SOC 2 certification to satisfy supply chain risk requirements.*

**SDLC -- Software Development Lifecycle**
A structured process for planning, creating, testing, and deploying software, with security checkpoints at each phase when following a "secure SDLC."
*Example: The MD DOIT System and Network Security Policy mandates a secure SDLC, requiring security testing before any internally developed application is deployed to production.*

**SOC 2 -- Service Organization Control 2**
An auditing standard developed by the American Institute of Certified Public Accountants (AICPA) that evaluates a service provider's controls for security, availability, processing integrity, confidentiality, and privacy.
*Example: A cloud backup vendor used by a Maryland agency presents its SOC 2 Type II report to demonstrate 12 months of continuous compliance with security controls.*

**STRIDE -- Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege**
A threat categorization model developed at Microsoft in 1999 to systematically identify security threats during system design.
*Example: A development team uses STRIDE to analyze a new municipal API: Spoofing (can an attacker impersonate a user?), Tampering (can data in transit be modified?), and so on for each of the six threat types.*

---

## NIST CSF 2.0 Functions and Sub-Functions

**GV -- Govern**
The NIST CSF 2.0 function covering organizational cybersecurity strategy, risk management policy, roles and responsibilities, and supply chain risk management. Introduced in CSF 2.0; absent from CSF 1.1.
*Example: A municipality publishing a formal cybersecurity risk appetite statement and assigning a CISO with executive authority addresses the Govern function.*

**GV.SC -- Govern: Supply Chain Risk Management**
A sub-function of Govern covering policies and processes for managing cybersecurity risks from third-party vendors and service providers.
*Example: Requiring all software vendors to submit a Software Bill of Materials (SBOM) as a condition of contract award addresses GV.SC.*

**ID -- Identify**
The NIST CSF 2.0 function covering asset inventory, risk assessment, and planning for improvement.
*Example: A county maintaining a complete inventory of all servers, workstations, and cloud subscriptions -- with assigned data classifications -- satisfies the Identify function.*

**PR -- Protect**
The NIST CSF 2.0 function covering identity management, access control, awareness training, data security, and platform security.
*Example: Requiring multi-factor authentication for all remote access and conducting annual security awareness training satisfies core Protect requirements.*

**PR.PS -- Protect: Platform Security**
The sub-function covering secure configuration and management of hardware and software platforms.
*Example: Maintaining an approved-software list and blocking unapproved executables addresses PR.PS.*

**PR.IR -- Protect: Infrastructure Resilience**
The sub-function covering the security and resilience of networks, systems, and infrastructure.
*Example: Implementing network segmentation between operational technology and enterprise IT networks addresses PR.IR.*

**DE -- Detect**
The NIST CSF 2.0 function covering continuous monitoring and analysis of adverse events.
*Example: A security operations center (SOC) that monitors network traffic 24/7 and classifies anomalous events within defined thresholds addresses the Detect function.*

**DE.CM -- Detect: Continuous Monitoring**
The sub-function requiring ongoing monitoring of networks, physical environments, personnel, and external service providers.
*Example: The MD DOIT Continuous Monitoring Policy explicitly maps to DE.CM, requiring monitoring of user activity, network traffic, and cloud service providers.*

**DE.AE -- Detect: Adverse Events Analysis**
The sub-function covering investigation and analysis of potentially adverse events to understand their nature and potential impact.
*Example: Correlating multiple failed login attempts from the same IP address within a 10-minute window and classifying it as a brute-force attempt addresses DE.AE.*

**RS -- Respond**
The NIST CSF 2.0 function covering incident management, analysis, communication, and mitigation.
*Example: A city maintaining a documented incident response plan with defined roles, communication templates, and escalation thresholds addresses the Respond function.*

**RC -- Recover**
The NIST CSF 2.0 function covering restoration of operations following cybersecurity incidents.
*Example: A municipality with verified offsite backups, a tested disaster recovery plan, and defined recovery time objectives addresses the Recover function.*

---

## Maryland-Specific Acronyms

**DHMH -- Department of Health and Mental Hygiene**
The former name of the Maryland agency responsible for public health programs; reorganized as MDH (Maryland Department of Health).
*Example: MD DHMH IT Security Policy v4.0 (2014) establishes access control and incident response requirements for DHMH IT systems.*

**DOIT -- Department of Information Technology**
The Maryland state agency responsible for enterprise IT governance, standards, and cybersecurity policy.
*Example: DOIT issued three cybersecurity policies in 2026 (Cyber Risk Management, Continuous Monitoring, System and Network Security) that form the core of the Maryland state cybersecurity governance framework.*

**eMMA -- eMaryland Marketplace Advantage**
Maryland's electronic procurement portal where state agencies post solicitations and award contracts.
*Example: Procurement documents retrieved from eMMA contain high keyword counts for supply chain terms (vendor, contractor) but no cybersecurity requirements, contributing to the supply chain risk gap identified in the paper.*

**MCE -- Maryland Correctional Enterprises**
A division of the Maryland Department of Public Safety and Correctional Services that employs incarcerated individuals in manufacturing and services.
*Example: MCE business plans and meeting minutes account for the majority of false positives in Method 1, because the word* training *appears hundreds of times in the context of vocational job training programs.*

**MSDE -- Maryland State Department of Education**
The Maryland state agency overseeing public education, including K-12 schools and career/technical education programs.
*Example: MSDE Acceptable Use Policy v2.0 (2024) establishes cybersecurity rules for device use and communications across MSDE systems.*

**SCISO -- State Chief Information Security Officer**
The senior cybersecurity official in the Maryland state government, responsible for enterprise security strategy and policy.
*Example: The MD DOIT Cyber Risk Management Policy assigns the SCISO authority to set risk appetite, approve exceptions, and oversee third-party risk assessments.*

**WIOA -- Workforce Innovation and Opportunity Act**
A U.S. federal law enacted in 2014 that funds workforce development programs, including job training, adult education, and employment services.
*Example: The Maryland WIOA Annual Report 2023 is the single most prominent false positive in Method 1, receiving a composite keyword score of 87 due to the word* training *appearing 300+ times in the context of job training programs.*

---

## Statistical and Evaluation Terms

**FN -- False Negative**
A document the classifier labels as non-cybersecurity-relevant that is actually a genuine cybersecurity policy (missed detection).
*Example: Method 1 produces 1 false negative: one genuine cybersecurity policy that scored below the keyword threshold because it used technical vocabulary absent from the keyword list.*

**FP -- False Positive**
A document the classifier labels as cybersecurity-relevant that is not a genuine cybersecurity policy (spurious detection).
*Example: Method 1 produces 21 false positives; 78% of them are caused by the keyword* training *appearing in non-cybersecurity documents.*

**r -- Pearson Correlation Coefficient**
A measure of linear association between two variables, ranging from -1 (perfect negative correlation) to +1 (perfect positive correlation). Values near 0 indicate no linear relationship.
*Example: The Pearson r between keyword and AI Protect scores is 0.151 (p = 0.291), indicating no statistically significant relationship -- keyword Protect counts are noise.*

**p-value**
The probability of observing a test statistic at least as extreme as the one obtained, assuming the null hypothesis (no relationship) is true. A p-value below 0.05 is conventionally considered statistically significant.
*Example: Govern correlation r = 0.789 has p < 0.001 (highly significant); Protect correlation r = 0.151 has p = 0.291 (not significant).*

**TN -- True Negative**
A document the classifier correctly labels as non-cybersecurity-relevant.
*Example: Method 2 produces 39 true negatives -- every non-policy document (meeting agendas, financial statements, business plans) is correctly excluded.*

**TP -- True Positive**
A document the classifier correctly labels as a genuine cybersecurity policy.
*Example: Method 2 produces 7 true positives, identifying all 7 genuine cybersecurity policies in the corpus.*

---

## Other Technical Terms

**ERP -- Enterprise Resource Planning**
Integrated software systems that manage core business processes (finance, HR, procurement, operations) across an organization.
*Example: MCE Council Minutes (Sep 2021) discuss an ERP infrastructure upgrade; the IT context generates keyword hits but no cybersecurity policy content.*

**MOVEit -- Managed Object Transfer**
A file transfer platform by Progress Software. A critical SQL injection vulnerability (CVE-2023-34362) discovered in 2023 was exploited to steal data from thousands of organizations.
*Example: The MOVEit breach affected U.S. federal agencies, state governments, and private organizations, demonstrating the systemic risk of unpatched file transfer software.*

**SolarWinds**
An IT management software company whose Orion platform was compromised in 2020 when attackers inserted a backdoor into a legitimate software update, affecting approximately 18,000 organizations including U.S. government agencies.
*Example: The SolarWinds breach is cited as the canonical supply chain attack motivating CSF 2.0's GV.SC function.*

**ZTA -- Zero Trust Architecture**
A security model that eliminates implicit trust for any user, device, or network location, requiring continuous verification of all access requests.
*Example: The MD DOIT Continuous Monitoring Policy references ZTA as the architectural direction for Maryland state government, requiring monitoring of all access events including from internal network locations.*
