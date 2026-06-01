# Benchmarking Municipal Cybersecurity Readiness Through Automated Policy Analytics: Evidence from Maryland Local Governments

Despeignes, S., Huggins, T., and Trivedi, D.  
Department of Computer Science, Bowie State University, Bowie, MD 20715

---

## Abstract

Local governments face increasing cybersecurity risks while operating under significant resource constraints. Ransomware attacks against major U.S. municipalities -- with reported recovery costs exceeding $17-18 million per incident -- underscore the operational consequences of inadequate cybersecurity governance. Yet the extent to which local government policies align with modern frameworks such as the NIST Cybersecurity Framework (CSF) 2.0 remains poorly understood.

This paper presents an automated framework for evaluating municipal cybersecurity readiness by analyzing publicly available policy documents. We construct a corpus of 51 Maryland government documents and compare two classification approaches against NIST CSF 2.0's six core functions -- Govern, Identify, Protect, Detect, Respond, and Recover: (1) keyword-based analysis using predefined term lists, and (2) AI-assisted classification using a large language model (LLM) prompt.

The keyword-based approach achieves high recall (0.857) but poor precision (0.222, F1 = 0.353), generating 21 false positives as context-free term matching flags workforce reports, business plans, and meeting agendas as cybersecurity-relevant. The AI-assisted approach achieves perfect recall (1.000) with substantially higher precision (0.583, F1 = 0.737), reducing false positives by 76%. The correlation between keyword and AI scores for the Protect function is statistically non-significant (r = 0.151, p = 0.291), revealing that keyword matching on this dimension is dominated by noise from the term *training* appearing in non-security contexts.

Among verified cybersecurity policies, AI classification reveals consistent governance coverage but measurable gaps in detection and recovery. Supply chain risk management provisions appear in state-level policies but are absent from municipal documents. This work contributes a reproducible Python-based assessment pipeline, an empirical comparison of automated methods, and recommendations for improving municipal cybersecurity policy coverage.

**Keywords:** Cybersecurity Governance, Municipal Cybersecurity, NIST CSF 2.0, Supply Chain Cybersecurity, AI-Assisted Policy Analysis

---

## 1. Introduction

Cybersecurity threats continue to increase in sophistication, frequency, and operational impact. Municipal governments have become attractive targets due to limited budgets, aging infrastructure, and growing reliance on digital services. High-profile ransomware incidents against Baltimore (2019, estimated loss of $18M) and Atlanta (2018, recovery cost of $17M) have demonstrated the consequences of insufficient cybersecurity governance [1]. Supply-chain compromises such as SolarWinds (2020) and MOVEit (2023) have shown that vulnerabilities in third-party software can cascade across thousands of organizations simultaneously [2, 3].

Local governments increasingly depend on third-party vendors, cloud providers, and managed service providers to deliver essential services. These dependencies expand the attack surface and introduce supply chain risks that many municipalities are poorly equipped to manage. Federal guidance -- including Executive Order 14028 [4] and the CISA Cybersecurity Performance Goals [5] -- has emphasized comprehensive governance at all levels of government, but adoption among resource-constrained municipalities remains uneven.

Although cybersecurity frameworks and assessment methods have been extensively studied in enterprise and federal contexts [6, 7], limited empirical work has evaluated local government policy alignment at scale. Manual policy audits are resource-intensive and difficult to replicate across jurisdictions. This gap motivates the development of automated, reproducible assessment approaches.

This paper addresses that gap by comparing two automated policy analysis methods applied to a corpus of Maryland government documents. We introduce a keyword-based baseline and an AI-assisted classification approach, both mapped to NIST CSF 2.0, and provide empirical evidence on their relative accuracy, coverage, and failure modes.

### 1.1 Research Questions

1. To what extent do local government cybersecurity policies address NIST CSF 2.0 functions?
2. How comprehensively do local governments address supply-chain cybersecurity risks?
3. How does AI-assisted classification compare to keyword-based analysis for automated cybersecurity policy assessment?
4. What improvements can resource-constrained municipalities prioritize to improve cybersecurity readiness?

### 1.2 Contributions

1. A reproducible Python-based cybersecurity policy assessment pipeline.
2. Mapping of Maryland government policies to NIST CSF 2.0 using two automated methods.
3. Empirical comparison of keyword-based versus AI-assisted classification, including precision, recall, F1, and per-function false positive analysis.
4. Identification of governance and supply-chain cybersecurity gaps in the corpus.
5. Evidence-based recommendations for improving municipal cybersecurity governance.

This work extends a preliminary poster presentation [8] by introducing an AI-assisted assessment methodology, upgrading the evaluation baseline from CSF 1.1 to CSF 2.0, and providing a quantitative comparison of both approaches on an expanded corpus.

---

## 2. Background

### 2.1 Evolution of Cybersecurity Governance Frameworks

The original NIST Cybersecurity Framework (CSF) 1.1 [9] organized controls around five functions: Identify, Protect, Detect, Respond, and Recover. NIST CSF 2.0 [10], released in February 2024, introduced a sixth function -- Govern -- representing a major conceptual shift. The Govern function encompasses organizational context, risk management strategy, roles and responsibilities, policies, oversight, and cybersecurity supply chain risk management. Its introduction explicitly acknowledges that technical controls alone are insufficient without organizational commitment and executive accountability.

Executive Order 14028 [4] directed federal agencies to adopt zero-trust architectures, improve software supply chain security, and enhance incident detection. While the order targets federal agencies, its principles have influenced state and local government cybersecurity programs. CISA's Cybersecurity Performance Goals [5] further operationalize these principles into measurable targets applicable across government levels.

### 2.2 Municipal Cybersecurity Threat Landscape

Local governments face a deteriorating threat environment with limited resources to respond. Ransomware has emerged as the dominant threat vector. The 2019 Baltimore ransomware attack disrupted city services for weeks and resulted in estimated costs of $18 million [1]. Atlanta's 2018 attack required approximately $17 million in recovery expenditures. Smaller municipalities have experienced similar incidents with proportionally greater operational impact.

Supply chain attacks have compounded local government risk exposure. The 2020 SolarWinds compromise -- in which a backdoor was distributed through a legitimate software update affecting an estimated 18,000 organizations, including state and local agencies -- demonstrated that traditional perimeter defenses are insufficient against supply-chain vectors [2]. The 2023 exploitation of MOVEit Transfer software affected thousands of organizations globally through a single unpatched file transfer platform [3].

### 2.3 NIST Cybersecurity Framework 2.0

NIST CSF 2.0 [10] defines six core functions:

| Function | Code | Scope |
|---|---|---|
| Govern | GV | Establishes organizational cybersecurity strategy, risk management policy, roles, and supply chain risk management |
| Identify | ID | Manages asset inventory, risk assessment, and improvement |
| Protect | PR | Implements identity management, access control, awareness training, data security, and platform security |
| Detect | DE | Provides continuous monitoring and adverse event analysis |
| Respond | RS | Executes incident management, analysis, communication, and mitigation |
| Recover | RC | Restores operations following incidents |

Supply chain risk management (GV.SC) is integrated under the Govern function in CSF 2.0, reflecting the recognition that third-party risk must be addressed at the governance level.

### 2.4 Cybersecurity Governance and Supply Chain Risk

Cybersecurity governance refers to organizational structures, policies, and controls used to manage cybersecurity risks while aligning security objectives with organizational goals [7]. The Govern function introduced in CSF 2.0 formalizes this principle, explicitly integrating supply chain risk management (GV.SC) under the governance umbrella. Supply chain attacks involving SolarWinds, Kaseya, and MOVEit demonstrate that procurement policies -- requiring vendor security certifications and incident notification obligations -- are an essential first line of defense [2, 3].

---

## 3. Related Work

### 3.1 Framework-Based Cybersecurity Assessment

Prior work has extensively evaluated cybersecurity framework adoption across sectors. Leszczyna [6] reviewed assessment methods and identified NIST CSF, ISO/IEC 27001, and NIST SP 800-53 [11] as dominant models. Toussaint et al. [12] found that technical safeguards are more consistently implemented than governance-level controls, a pattern replicated in the present study. Savas and Karatas [7] identified persistent gaps between policy articulation and operational implementation across jurisdictions.

### 3.2 Local Government Cybersecurity and Supply Chain Risk

Norris and Mateczun [1] documented significant cybersecurity maturity gaps among U.S. municipalities, with fewer than half maintaining formal incident response plans. Kim and Lee [13] found that smaller jurisdictions systematically underinvest in governance and detection relative to technical protections. Despite the demonstrated impact of supply chain attacks, local procurement policies rarely impose substantive cybersecurity requirements on vendors [1, 2].

### 3.3 Automated Policy Analysis

Chen and Kumar [14] demonstrated that large language models can classify policy content according to regulatory frameworks with accuracy exceeding keyword-based approaches. No prior study has empirically compared these methods on a municipal cybersecurity policy corpus -- a gap this paper addresses.

---

## 4. Methodology

### 4.1 Data Collection

The corpus was assembled from two sources: (1) targeted Google dork searches using the `site:md.gov` operator with filetype and topic constraints (Table 1), and (2) direct downloads from Maryland state agency websites. After removing four exact duplicate files (verified by MD5 hash), the final corpus contained 51 unique documents.

**Table 1. Google Dork Queries Used for Corpus Construction**

| Query | Results |
|---|---|
| `site:md.gov` cybersecurity policy | 3 |
| `site:md.gov` disaster recovery plan | 7 |
| `site:md.gov` contractor cybersecurity | 3 |
| `site:md.gov` incident response plan | 7 |
| `site:md.gov` procurement policy | 25 |
| Direct state agency downloads (AI) | 6 |
| **Total (after deduplication)** | **51** |

A key finding from the collection process is that domain-level search operators return highly heterogeneous document types. Of 51 documents, only 7 (13.7%) are genuine cybersecurity or IT security policies; the remainder comprises municipal meeting agendas (15), business plans and reports (5), financial statements (4), non-cyber government policies (5), advisory reports (2), procurement and RFP documents (2), and 11 unclassifiable or scanned documents.

### 4.2 Document Processing

All PDFs were processed using PyMuPDF, extracting up to 15,000 characters per document for classification. Three documents returned zero text because the scanned images lacked embedded text layers. The processing pipeline consisted of: (1) PDF ingestion, (2) text extraction, (3) normalization, (4) keyword detection or LLM classification, (5) framework mapping, and (6) scoring.

### 4.3 Framework Mapping

Policy content was mapped to NIST CSF 2.0's six functions under both methods. Each document-function pair received one of three ratings:

| Score | Label | Meaning |
|---|---|---|
| 0 | Absent | No coverage of the function's requirements |
| 1 | Partial | Function is mentioned or partially addressed |
| 2 | Present | Substantive, operational coverage of the function |

### 4.4 Supply Chain Assessment

Vendor and supply chain risk provisions were evaluated using additional keyword terms (*vendor*, *third party*, *supplier*, *contractor*, *service provider*, *supply chain*) tracked separately from the six core CSF functions.

---

## 5. Experimental Design

### 5.1 Method 1: Keyword-Based Analysis

Keyword lists were defined for each NIST CSF 2.0 function (Table 2). For each document, all occurrences were counted using case-insensitive regex matching. Raw counts were normalized to the 0-2 scale (0 = no hits; 1 = 1-4 hits; 2 = 5+ hits) for comparison with AI scores. A document was classified as cybersecurity-relevant if any function reached a raw count of 5 or more.

**Table 2. NIST CSF 2.0 Keyword Lists (Method 1)**

| Function | Keywords |
|---|---|
| Govern | governance, risk management, cybersecurity strategy, board oversight, security program |
| Identify | asset inventory, risk assessment, business environment, critical systems |
| Protect | access control, authentication, encryption, training, firewall |
| Detect | monitoring, intrusion detection, logging, security event |
| Respond | incident response, containment, communication plan, response team |
| Recover | backup, disaster recovery, business continuity, restoration |

### 5.2 Method 2: AI-Assisted Classification

Each document's extracted text (first 12,000 characters) was submitted to Claude Sonnet 4.6 using the following structured prompt:

```
You are a cybersecurity auditor. Classify the following policy according to NIST CSF 2.0:
Govern / Identify / Protect / Detect / Respond / Recover.
For each category provide: 0 = absent, 1 = partial, 2 = present.
Explain your reasoning. [document text]
```

The model returned a score (0/1/2) and a rationale for each function, stored in `ai_scores.csv` for reproducibility. A document was classified as cybersecurity-relevant if any function scored 1 or higher.

### 5.3 Evaluation Approach

Ground truth labels were assigned based on whether each document's primary purpose is to define cybersecurity requirements, standards, or governance controls (positive class = Cybersecurity Policy). The seven documents meeting this criterion are listed in Table 3. Precision, recall, F1 score, and accuracy were computed for each method, along with per-function false positive counts.

**Table 3. Genuine Cybersecurity Policy Documents (Ground Truth Positives)**

| Document | Year | Issuing Body |
|---|---|---|
| MD IT Security Manual v1.2 | 2019 | MD DOIT |
| MD DHMH IT Security Policy v4.0 | 2014 | MD DHMH |
| MD Judicial Information Security Policy | 2026 | MD Judiciary |
| MD DOIT Cyber Risk Management Policy | 2026 | MD DOIT |
| MD DOIT Continuous Monitoring Policy | 2026 | MD DOIT |
| MD DOIT System and Network Security Policy | 2026 | MD DOIT |
| MSDE Acceptable Use Policy v2.0 | 2024 | MSDE |

---

## 6. Results

### 6.1 Method 1: Keyword-Based Results

![Average Coverage](../results/average_coverage.png)  
*Figure 1. Average keyword score per NIST CSF 2.0 function (Method 1, n = 51). The Protect function is inflated by incidental occurrences of* training *and* vendor *in non-cybersecurity documents.*

The Protect function dominates with a mean raw score of 18.0 -- more than four times that of any other function (Govern: 4.4, Detect: 4.4, Recover: 2.5, Respond: 1.7, Identify: 1.3). This imbalance does not reflect genuine cybersecurity policy coverage. It results from the keyword *training* appearing hundreds of times in correctional enterprise vocational programs, workforce development reports, and apprenticeship policy documents, none of which have any cybersecurity content.

The maturity ranking places the Maryland WIOA Annual Report -- a workforce development outcomes document -- fourth overall, with a composite score of 87, ahead of three genuine cybersecurity policies. Conversely, the MD DOIT System and Network Security Policy (2026), which explicitly maps to NIST CSF 2.0 PR.PS and PR.IR, receives a keyword composite score of only 3 because it uses technical terminology (*configuration management*, *network segmentation*, *geographically dispersed architecture*) absent from the keyword list.

### 6.2 Method 2: AI-Assisted Results

The AI method correctly scores all seven genuine cybersecurity policy documents at >= 1 on at least one function, achieving 100% recall with no false negatives. Coverage across genuine policies is consistent on Govern (mean 1.71/2) and Protect (1.43/2), but weaker on Detect (0.86/2) and Recover (1.14/2). The MD DOIT System and Network Security Policy is correctly scored PR = 2, RC = 2 despite containing none of the Protect keyword list terms. Conversely, the AI correctly scores the WIOA Annual Report and all correctional enterprise business plans as 0 across all six functions, demonstrating its contextual awareness of the documents' purposes.

### 6.3 Comparative Analysis

**Table 4. Policy Detection Performance: Method 1 vs. Method 2**

| Method | True Positives | False Positives | False Negatives | True Negatives | F1 | Accuracy |
|---|---|---|---|---|---|---|
| Keyword (M1) | 6 | 21 | 1 | 23 | 0.353 | 56.9% |
| AI-Assisted (M2) | 7 | 5 | 0 | 39 | 0.737 | 90.2% |

![Method Comparison](../results/method_comparison_bar.png)  
*Figure 2. Mean NIST CSF 2.0 score per function: keyword-based (blue) versus AI-assisted (orange), normalized to the 0-2 scale. Protect shows the greatest divergence.*

![Confusion Matrices](../results/confusion_matrices.png)  
*Figure 3. Confusion matrices for both classification methods on the 51-document corpus.*

The AI-assisted approach raises F1 from 0.353 to 0.737 and accuracy from 56.9% to 90.2%. False positives drop from 21 to 5 (76% reduction), and the one false negative in Method 1 is eliminated.

**Table 5. Per-Function Score Statistics and Method Agreement**

| Function | KW Mean | AI Mean | r | Significance |
|---|---|---|---|---|
| Govern | 0.412 | 0.314 | 0.789 | p < 0.001 |
| Identify | 0.216 | 0.216 | 0.681 | p < 0.001 |
| **Protect** | **1.275** | **0.294** | **0.151** | **p = 0.291 (not significant)** |
| Detect | 0.608 | 0.216 | 0.533 | p < 0.001 |
| Respond | 0.216 | 0.176 | 0.542 | p < 0.001 |
| Recover | 0.529 | 0.176 | 0.507 | p < 0.001 |

KW scores normalized to 0-2. Pearson r with p-values.

Protect accounts for 21 of 27 total Method 1 false positives (78%), driven entirely by the term *training* appearing in non-cybersecurity documents. AI false positives total 5 and are distributed across all six functions, with no single function dominating.

![Scatter Keyword vs AI](../results/scatter_kw_vs_ai.png)  
*Figure 4. Per-function scatter of keyword score versus AI score. The Protect panel (middle-left) shows the most scatter above the diagonal for non-policy documents.*

### 6.4 Supply Chain Coverage

Supply chain keywords appeared in 34 of 51 documents, but high-frequency occurrences were concentrated in procurement manuals, correctional enterprise contracts, and workforce policy documents. Of the seven genuine cybersecurity policies, substantive supply chain risk management provisions appeared in four. Municipal-level documents contained no dedicated supply chain cybersecurity requirements.

---

## 7. Discussion

### 7.1 Governance Deficit

AI classification reveals a consistent pattern: governance controls (mean 1.71/2) are broadly covered in state-level policies, but no municipal-level cybersecurity policy documents were recovered from the corpus. Targeted searches of publicly available Maryland government documents failed to surface standalone cybersecurity policies from any of the 23 Maryland counties or the independent city of Baltimore. While some jurisdictions may maintain non-public internal policies, the absence of public-facing governance documents suggests that formal accountability structures and executive cybersecurity ownership remain underdeveloped at the municipal level.

The Govern function in NIST CSF 2.0 explicitly requires organizational context definition, risk appetite statements, and board-level oversight -- elements that provide no public accountability signal in the current corpus.

### 7.2 Supply Chain Risk Management Gap

Supply chain keywords appeared frequently, but AI classification confirmed that most occurrences reflect vendor-of-record relationships in procurement documents rather than cybersecurity obligations. Procurement policies from the Maryland eMMA platform showed high keyword counts for supply chain terms but near-zero AI scores on NIST CSF functions, indicating that procurement language routinely references contractors without imposing cybersecurity requirements.

Given the demonstrated impact of SolarWinds and MOVEit [2, 3], this gap represents a structural vulnerability: municipalities that contract for cloud services, managed IT, or software platforms without cybersecurity contract language have no contractual mechanism to mitigate supply chain risk.

### 7.3 Automated Assessment: Method Selection Implications

Keyword-based approaches are computationally simple, transparent, and reproducible, but the non-significant Protect correlation (r = 0.151, p = 0.291) demonstrates a fundamental limitation when applied to heterogeneous document corpora. When documents are collected via broad web searches, the proportion of non-policy documents is high (86.3% in this corpus), and keyword false positives systematically distort aggregate coverage statistics.

AI-assisted classification substantially reduces this problem. The LLM's contextual understanding allows it to correctly classify a workforce development report despite multiple occurrences of security-adjacent terms, and to correctly score a technical cybersecurity policy whose vocabulary does not match any predefined keyword. The trade-off is computational cost and reduced transparency; however, the improvement in precision (0.222 to 0.583) and F1 (0.353 to 0.737) suggests that AI-assisted methods are more appropriate when policy corpora include diverse document types.

---

## 8. Recommendations

Based on the analysis, municipalities should:

1. Formally adopt NIST CSF 2.0 Govern provisions, documenting risk appetite and executive cybersecurity roles with minimal technical investment.
2. Embed cybersecurity requirements -- vendor certification, incident notification, and right-to-audit clauses -- in standard procurement templates.
3. Establish regional incident response partnerships to share detection and response capabilities across resource-constrained jurisdictions.
4. Publish cybersecurity governance policies publicly to create external accountability, using Maryland's DOIT policy suite as a replicable template.

For researchers, AI-assisted classification should be preferred over keyword matching when the policy corpus includes heterogeneous document types.

---

## 9. Threats to Validity

Several limitations should be considered:

1. Publicly available documents may not reflect actual cybersecurity practices; jurisdictions with non-public policies would appear to have gaps that do not exist operationally.
2. The corpus is weighted toward state-level Maryland documents; genuine municipal-level policy representation is limited.
3. The authors assigned ground truth labels without independent validation.
4. The keyword threshold (raw count >= 5) is arbitrary; alternative thresholds would change precision and recall, though the Protect false-positive problem would persist.
5. AI classifications were produced using a fixed model and prompt; different model versions or prompt formulations may yield different scores.
6. This study is limited to a single state and one collection cycle.

---

## 10. Future Work

Future directions include: expanding the corpus to all 50 states for national benchmarking; applying retrieval-augmented generation to process full documents rather than truncated excerpts; longitudinal re-collection to track governance improvements over time; and developing validated ground-truth datasets for government cybersecurity policy classification to enable rigorous method benchmarking.

---

## 11. Conclusion

Local governments face mounting cybersecurity threats with limited resources and inconsistent governance frameworks. This paper introduced an automated pipeline for evaluating municipal cybersecurity readiness and provided an empirical comparison of keyword-based versus AI-assisted NIST CSF 2.0 classification.

Applied to a 51-document Maryland government corpus, AI-assisted classification (F1 = 0.737, Accuracy = 90.2%) substantially outperformed keyword-based analysis (F1 = 0.353, Accuracy = 56.9%), reducing false positives by 76% and eliminating false negatives. The non-significant keyword-AI correlation for the Protect function (r = 0.151, p = 0.291) identifies a fundamental limitation of keyword approaches on heterogeneous government document corpora.

Among verified policies, the analysis reveals consistent governance coverage at the state level, measurable detection and recovery gaps, and a near-complete absence of supply chain cybersecurity requirements in municipal-level documents. The Python-based assessment pipeline developed in this work is designed for replication across jurisdictions and time periods, supporting scalable cybersecurity governance benchmarking for researchers, auditors, and policymakers.

---

## References

[1] D. Norris and L. Mateczun, "Cybersecurity Challenges in Local Government," *Government Information Quarterly*, 2023.

[2] CISA, "SolarWinds Orion Supply Chain Compromise: Guidance for Affected Organizations," 2021. https://www.cisa.gov/uscert/ncas/alerts/aa20-352a

[3] CISA, "MOVEit Transfer and MOVEit Cloud Vulnerabilities," 2023. https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a

[4] Executive Office of the President, "Executive Order 14028: Improving the Nation's Cybersecurity," Federal Register, 86 FR 26633, 2021.

[5] Cybersecurity and Infrastructure Security Agency (CISA), "Cybersecurity Performance Goals," 2024. https://www.cisa.gov/cross-sector-cybersecurity-performance-goals

[6] R. Leszczyna, "Review of Cybersecurity Assessment Methods," *Computers and Security*, vol. 108, p. 102376, 2021. https://doi.org/10.1016/j.cose.2021.102376

[7] S. Savas and S. Karatas, "Cyber Governance Studies in Ensuring Cybersecurity," *International Cybersecurity Law Review*, vol. 3, no. 1, 2022.

[8] S. Despeignes, T. Huggins, and D. Trivedi, "Evaluating the Impact of Cybersecurity Standards on Cyberattack Prevention," *Proceedings of CCSC-Eastern 2025*, ACM, 2025. https://dl.acm.org/doi/abs/10.5555/3801163.3801176

[9] M. P. Barrett et al., "Framework for Improving Critical Infrastructure Cybersecurity, Version 1.1," NIST, 2018. https://doi.org/10.6028/NIST.CSWP.04162018

[10] National Institute of Standards and Technology, "Cybersecurity Framework 2.0," NIST, 2024. https://doi.org/10.6028/NIST.CSWP.29

[11] R. Ross et al., "NIST Special Publication 800-53 Revision 5: Security and Privacy Controls for Information Systems and Organizations," NIST, 2020. https://doi.org/10.6028/NIST.SP.800-53r5

[12] M. Toussaint, S. Krima, and H. Panetto, "Industry 4.0 Data Security: A Cybersecurity Frameworks Review," *Journal of Industrial Information Integration*, vol. 39, p. 100604, 2024. https://doi.org/10.1016/j.jii.2024.100604

[13] J. Kim and S. Lee, "Cybersecurity Readiness Assessment in Municipal Governments," *Journal of Cybersecurity*, 2024.

[14] Y. Chen and A. Kumar, "Large Language Models for Policy Analysis," *Information Processing and Management*, 2025.
