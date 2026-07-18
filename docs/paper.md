# Benchmarking State and Local Cybersecurity Readiness Through Automated Policy Analytics: Evidence from Maryland Local Governments

Devharsh Trivedi, Sage Despeignes, Titorian Huggins
Department of Computer Science, Bowie State University, Bowie, MD 20715

Accepted at CCSC Eastern 2026; to appear in the Journal of Computing Sciences in Colleges 42(3). This markdown version mirrors the camera-ready manuscript.

---

## Abstract

Local governments face increasing cybersecurity risks while operating under significant resource constraints. Ransomware attacks against major U.S. municipalities -- with reported recovery costs exceeding $17-18 million per incident -- underscore the operational consequences of inadequate cybersecurity governance. Yet the extent to which state and local government policies align with modern frameworks such as NIST Cybersecurity Framework (CSF) 2.0 has not been systematically quantified.

This paper presents an automated framework for evaluating state and local cybersecurity policy posture from publicly available documents; because public documents may not reflect internal practice, it measures documented policy alignment rather than operational readiness. We construct a corpus of 51 Maryland government documents and compare two classification approaches against NIST CSF 2.0's six core functions -- Govern, Identify, Protect, Detect, Respond, and Recover: (1) keyword-based analysis using predefined term lists, and (2) AI-assisted classification using a large language model (LLM) prompt.

The keyword-based approach achieves high recall (0.857) but poor precision (0.222, F1 = 0.353), generating 21 false positives by flagging workforce reports, business plans, and meeting agendas as cybersecurity-relevant. The AI-assisted approach achieves recall of 1.00 on this corpus with substantially higher precision (0.583, F1 = 0.737), reducing false positives by 76%; the improvement is statistically significant (McNemar exact p < 0.001). The correlation between keyword and AI scores for the Protect function is statistically non-significant (r = 0.151, p = 0.291), revealing that keyword matching on this dimension is dominated by noise from the term *training* appearing in non-security contexts. Ablations that remove this term or expand the keyword lists narrow the gap (F1 = 0.571 and 0.636) but still trail AI-assisted classification, and AI document-level relevance decisions remain fully stable across three independent classification runs.

Among verified cybersecurity policies, AI classification reveals consistent governance coverage at the state level but measurable gaps in detection and recovery. No standalone municipal cybersecurity policy was publicly discoverable for any of Maryland's 23 counties or Baltimore City: public-facing municipal cybersecurity governance is largely absent or non-discoverable. This work contributes a reproducible Python-based assessment pipeline, an empirical comparison of automated methods, and recommendations for improving state and local cybersecurity policy coverage.

**Keywords:** Cybersecurity Governance, Municipal Cybersecurity, NIST CSF 2.0, Supply Chain Cybersecurity, AI-Assisted Policy Analysis

---

## 1. Introduction

Cybersecurity threats continue to increase in sophistication, frequency, and operational impact. Municipal governments have become attractive targets due to limited budgets, aging infrastructure, and growing reliance on digital services. High-profile ransomware incidents against Baltimore (2019, $18M estimated loss) and Atlanta (2018, $17M recovery cost) have demonstrated the consequences of insufficient cybersecurity governance [11]. Supply-chain compromises such as SolarWinds and MOVEit have shown that vulnerabilities in third-party software can cascade across thousands of organizations simultaneously [2, 3].

Local governments rely increasingly on outside vendors, cloud providers, and managed service providers, expanding the attack surface with supply chain risks many are poorly equipped to manage. Federal guidance, including Executive Order 14028 [6] and the CISA Cybersecurity Performance Goals [4], has emphasized comprehensive governance at all levels of government, but adoption among resource-constrained municipalities remains uneven.

Although cybersecurity frameworks and assessment methods have been extensively studied in enterprise and federal contexts [8, 16], limited empirical work has evaluated local government policy alignment at scale, and manual policy audits are resource-intensive and difficult to replicate across jurisdictions -- motivating automated, reproducible assessment approaches.

This paper addresses that gap through a comparative evaluation of two automated policy analysis methods applied to a corpus of Maryland government documents. We develop a keyword-based baseline and an AI-assisted classification approach, both mapped to NIST CSF 2.0, and provide empirical evidence on their relative accuracy, coverage, and failure modes, including significance testing of the comparison.

### 1.1 Research Questions

This study investigates four research questions; throughout, coverage refers to what publicly available documents state, a proxy for governance transparency rather than for implemented controls or operational maturity.

1. To what extent do publicly available state and local government policy documents address NIST CSF 2.0 functions?
2. How comprehensively do local governments address supply-chain cybersecurity risks?
3. How does AI-assisted classification compare to keyword-based analysis for automated cybersecurity policy assessment?
4. What improvements can resource-constrained municipalities prioritize to improve cybersecurity readiness?

### 1.2 Contributions

1. A reproducible Python-based cybersecurity policy assessment pipeline.
2. Mapping of Maryland government policies to NIST CSF 2.0 using two automated methods.
3. Empirical comparison of keyword-based versus AI-assisted classification with significance testing, false positive analysis, keyword-list ablations, and a classification stability check.
4. Identification of governance and supply-chain cybersecurity gaps in the corpus.
5. Evidence-based recommendations for improving state and local cybersecurity governance.

This work extends our preliminary poster presentation [5] by introducing an AI-assisted assessment methodology, upgrading the evaluation baseline from CSF 1.1 to CSF 2.0, and providing a quantitative comparison of both approaches on an expanded corpus.

---

## 2. Background

### 2.1 Evolution of Cybersecurity Governance Frameworks

The original NIST Cybersecurity Framework (CSF 1.1) [1] organized controls around five functions: Identify, Protect, Detect, Respond, and Recover. NIST CSF 2.0 [9], released in February 2024, introduced a sixth function -- Govern -- representing a major conceptual shift: its introduction explicitly acknowledges that technical controls alone are insufficient without organizational commitment and executive accountability.

Executive Order 14028 [6] directed federal agencies to adopt zero-trust architectures and improve software supply chain security; its principles, operationalized by CISA's Cybersecurity Performance Goals [4], have influenced state and local programs.

### 2.2 Municipal Cybersecurity Threat Landscape

Local governments face a deteriorating threat environment with limited resources to respond. Ransomware dominates: the Baltimore and Atlanta incidents disrupted services for weeks, and smaller municipalities have suffered proportionally greater operational impact [11]. Supply chain attacks compound this exposure: SolarWinds affected an estimated 18,000 organizations, including state and local agencies, and the MOVEit exploitation cascaded to thousands through a single unpatched platform [2, 3].

### 2.3 NIST Cybersecurity Framework 2.0

NIST CSF 2.0 [9] defines six core functions: **Govern** (GV: organizational cybersecurity strategy, risk management policy, roles, and supply chain risk management), **Identify** (ID: asset inventory, risk assessment, and improvement), **Protect** (PR: identity management, access control, awareness training, data security, and platform security), **Detect** (DE: continuous monitoring and adverse event analysis), **Respond** (RS: incident management, analysis, communication, and mitigation), and **Recover** (RC: restoration of operations following incidents).

Cybersecurity governance refers to the organizational structures, policies, and controls that align security objectives with organizational goals [15]. The Govern function formalizes this and integrates supply chain risk management (GV.SC), reflecting that third-party risk -- including procurement requirements for vendor certification and incident notification -- must be addressed at the governance level.

---

## 3. Related Work

### 3.1 Framework-Based Cybersecurity Assessment

Leszczyna [8] reviewed assessment methods and identified NIST CSF, ISO/IEC 27001, and NIST SP 800-53 [14] as dominant models. Toussaint et al. [16] found technical safeguards more consistently implemented than governance-level controls, a pattern replicated here, and Savas and Karatas [15] identified persistent gaps between policy articulation and operational implementation.

### 3.2 Local Government Cybersecurity and Supply Chain Risk

Reporting the first nationwide survey of local government cybersecurity, Norris et al. [10] found that local governments largely fail to practice it effectively, citing chronic underfunding and limited awareness among elected officials. Preis and Susskind [12] likewise concluded from interviews with municipal officials that preparation remains insufficient, and a systematic review by Hossain et al. [7] highlights persistent governance, resourcing, and workforce constraints. Despite the demonstrated impact of supply chain attacks, local procurement policies rarely impose substantive cybersecurity requirements on vendors [11, 2].

### 3.3 Automated Policy Analysis

Rodriguez et al. [13] demonstrated that large language models can annotate and analyze privacy policies at scale with effectiveness comparable to or exceeding earlier specialized classifiers. No prior study has empirically compared keyword and LLM-based methods on a state and local cybersecurity policy corpus -- a gap this paper addresses.

---

## 4. Methodology

### 4.1 Data Collection

The corpus was assembled from two sources: (1) targeted Google dork searches scoped to the md.gov domain with filetype and topic constraints -- *cybersecurity policy* (3 results), *disaster recovery plan* (7), *contractor cybersecurity* (3), *incident response plan* (7), and *procurement policy* (25) -- and (2) six direct downloads from Maryland state agency websites. After removing four exact duplicates (verified by MD5 hash), the final corpus contained 51 unique documents.

Domain-level search operators return highly heterogeneous document types: of 51 documents, only 7 (13.7%) are genuine cybersecurity or IT security policies; the remainder comprises municipal meeting agendas (15), business plans and reports (5), financial statements (4), non-cyber government policies (5), advisory reports (2), procurement and RFP documents (2), and 11 unclassifiable or scanned documents.

### 4.2 Document Processing

All PDFs were processed with PyMuPDF, extracting up to 15,000 characters per document; three scanned documents without embedded text layers returned no text. The pipeline consists of PDF ingestion, text extraction, normalization, keyword or LLM classification, framework mapping, and scoring.

### 4.3 Framework Mapping

Policy content was mapped to NIST CSF 2.0's six functions under both methods. Each document-function pair received one of three ratings:

- **0 -- Absent**: No coverage of the function's requirements.
- **1 -- Partial**: The function is mentioned or partially addressed.
- **2 -- Present**: Substantive, operational coverage of the function.

The partial-versus-present boundary is operational detail: a document that references a function's obligations while delegating specifics elsewhere scores 1 (e.g., the Continuous Monitoring Policy defers response procedures to a separate standard, RS = 1), whereas enumerated operational coverage scores 2 (the same policy's network, personnel, and provider monitoring provisions, DE = 2); stored rationales document each rating. Vendor and supply chain risk provisions were evaluated using additional keyword terms (*vendor*, *third party*, *supplier*, *contractor*, *service provider*, *supply chain*) tracked separately from the six core CSF functions.

---

## 5. Experimental Design

### 5.1 Method 1: Keyword-Based Analysis

Keyword lists of four to five terms were defined for each NIST CSF 2.0 function, e.g., Protect: *access control*, *authentication*, *encryption*, *training*, *firewall*; and Detect: *monitoring*, *intrusion detection*, *logging*, *security event* (complete lists in `keywords.json` in the public repository). Occurrences were counted with case-insensitive regex matching. Raw counts were normalized to 0-2 (0 = no hits; 1 = 1-4; 2 = 5+) for comparison with AI scores, and a document was flagged cybersecurity-relevant if any function reached a raw count of 5 or more.

### 5.2 Method 2: AI-Assisted Classification

Each document's extracted text (first 12,000 characters) was submitted to Claude Sonnet 4.6 using the following structured prompt:

> *You are a cybersecurity auditor. Classify the following policy according to NIST CSF 2.0: Govern / Identify / Protect / Detect / Respond / Recover. For each category provide: 0 = absent, 1 = partial, 2 = present. Explain your reasoning. [document text]*

The model returned a score (0/1/2) and a rationale for each function, stored in `ai_scores.csv` for reproducibility. A document was classified as cybersecurity-relevant if any function scored 1 or higher.

**Reproducibility.** All primary classifications were produced by a single pass of Claude Sonnet 4.6 (model identifier `claude-sonnet-4-6`) using the verbatim prompt above for every document, with no system prompt beyond it, no per-document tuning, and provider-default sampling (no temperature or seed control, which the stability check quantifies); the prompt's requested rationale was stored alongside each score. The corpus, scores, rationales, and analysis code are publicly available at https://github.com/devharsh/municipal-cyber-policy-analytics. To assess run-to-run stability, we re-ran the identical prompt three independent times (Claude Sonnet, default settings) on a stratified 13-document subsample (all seven ground-truth policies plus six non-policy documents spanning the corpus document types); agreement results appear in Section 6.5.

### 5.3 Keyword List Ablation

Because *training* is the only Protect keyword that commonly occurs outside cybersecurity contexts, we evaluated the sensitivity of Method 1 to keyword-list specification using three variants: (V1) removing *training* entirely; (V2) replacing it with security-qualified phrases (e.g., *security awareness training*), which requires co-occurrence with a security term; and (V3) an expanded baseline adding common security terms absent from the original lists (*multi-factor*, *least privilege*, *network segmentation*, *patch management*, *hardening*, *SIEM*, *threat intelligence*, and similar). V3 was constructed after inspecting the corpus failure modes and therefore approximates an upper bound on keyword-list performance. All thresholds and the detection rule were unchanged.

### 5.4 Evaluation Approach

Ground truth labels were assigned based on whether each document's primary purpose is to define cybersecurity requirements, standards, or governance controls (positive class = Cybersecurity Policy). The seven documents meeting this criterion:

| Document | Year |
|---|---|
| MD IT Security Manual v1.2 | 2019 |
| MD DHMH IT Security Policy v4.0 | 2014 |
| MD Judicial Information Security Policy | 2026 |
| MD DOIT Cyber Risk Management Policy | 2026 |
| MD DOIT Continuous Monitoring Policy | 2026 |
| MD DOIT System & Network Security Policy | 2026 |
| MSDE Acceptable Use Policy v2.0 | 2024 |

A second rater independently relabeled all 51 documents using the same written rule: raw agreement was 92.2% (47/51), Cohen's kappa = 0.73, indicating substantial agreement. All seven positives were independently confirmed; the four disagreements were documents the second rater additionally flagged -- two cybersecurity advisory reports, a data management plan, and a workforce disaster-recovery grant policy -- each of which discusses security without defining cybersecurity requirements as its primary purpose, so the original labels were retained. All four are among the five documents the AI method also falsely flags (Section 6.3): residual disagreement concentrates in genuinely ambiguous boundary documents.

Precision, recall, F1 score, and accuracy were computed for each method, along with per-function false positive counts. Method differences were tested with McNemar's exact test on paired document-level decisions, and 95% bootstrap confidence intervals (10,000 resamples over documents) were computed for precision, recall, F1, and the F1 difference.

---

## 6. Results

### 6.1 Method 1: Keyword-Based Results

The Protect function dominates the keyword results with a mean raw score of 18.0 -- more than four times that of any other function (Govern: 4.4, Detect: 4.4, Recover: 2.5, Respond: 1.7, Identify: 1.3). This imbalance does not reflect genuine cybersecurity policy coverage. It results from the keyword *training* appearing hundreds of times in correctional enterprise vocational programs, workforce development reports, and apprenticeship policy documents, none of which have any cybersecurity content.

The keyword maturity ranking places the Maryland WIOA Annual Report, a workforce development outcomes document, fourth overall (composite 87), ahead of three genuine cybersecurity policies. Conversely, the MD DOIT System and Network Security Policy (2026) receives a composite of only 3 because its technical terminology (*configuration management*, *network segmentation*) matches no keyword.

### 6.2 Method 2: AI-Assisted Results

The AI method correctly scores all seven genuine cybersecurity policy documents at >= 1 on at least one function, achieving recall of 1.00 (7/7) with no false negatives on this corpus. Coverage across genuine policies is consistent on Govern (mean 1.71/2) and Protect (1.43/2), but weaker on Detect (0.86/2) and Recover (1.14/2). The MD DOIT System and Network Security Policy is correctly scored PR = 2, RC = 2 despite matching no Protect keyword, while the WIOA Annual Report and all correctional enterprise business plans are correctly scored 0 across all six functions.

### 6.3 Comparative Analysis

Policy detection performance (Method 1 vs. Method 2); the AI advantage is statistically significant (McNemar exact p < 0.001):

| Method | TP | FP | FN | TN | P | R | F1 | Acc. |
|---|---|---|---|---|---|---|---|---|
| Keyword (M1) | 6 | 21 | 1 | 23 | 0.222 | 0.857 | 0.353 | 56.9% |
| AI-Assisted (M2) | 7 | 5 | 0 | 39 | 0.583 | 1.000 | 0.737 | 90.2% |

The AI-assisted approach raises F1 from 0.353 to 0.737 and accuracy from 56.9% to 90.2%. False positives drop from 21 to 5 (76% reduction), and the one false negative in Method 1 is eliminated. The improvement is statistically significant despite the modest corpus size: the AI method corrects 18 keyword errors while introducing one (McNemar exact test, p < 0.001), and bootstrap 95% confidence intervals are [0.133, 0.552] for keyword F1, [0.444, 0.929] for AI F1, and [0.200, 0.588] for the F1 difference.

Per-function agreement between methods (keyword scores normalized to 0-2). Because the ratings are ordinal, Spearman rho and quadratic-weighted Cohen's kappa are reported alongside Pearson's r; all three statistics agree:

| Function | KW Mean | AI Mean | r | rho | kappa_w |
|---|---|---|---|---|---|
| Govern | 0.412 | 0.314 | 0.789 | 0.667 | 0.779 |
| Identify | 0.216 | 0.216 | 0.681 | 0.639 | 0.680 |
| Protect | 1.275 | 0.294 | 0.151 | 0.144 | 0.076 |
| Detect | 0.608 | 0.216 | 0.533 | 0.460 | 0.435 |
| Respond | 0.216 | 0.176 | 0.542 | 0.498 | 0.541 |
| Recover | 0.529 | 0.176 | 0.507 | 0.471 | 0.415 |

All agreements are significant at p < 0.001 except Protect (p > 0.29): keyword matching on Protect is noise-driven, dominated by false occurrences of *training* in non-cybersecurity contexts.

At the function level, Protect accounts for 21 of 27 Method 1 false-positive flags (78%). The AI method produces 12 function-level false-positive cells, distributed across all six functions with no single function dominating, and concentrated in five falsely flagged documents:

| Document (nonzero functions) | Type |
|---|---|
| UMGC Local Gov. Cybersecurity Report, 2021 (all six; GV = 2) | Advisory report |
| MD Cybersecurity Council Report, 2025 (GV = 2) | Advisory report |
| MD Procurement Manual, 2019 (PR = 1) | Procurement |
| MD iMap Data Management Plan, 2015 (GV, ID, PR = 1) | Data management |
| QUEST Disaster Recovery Worker Grant, 2025 (RC = 1) | Workforce policy |

All five are near-boundary cases: the advisory reports analyze and recommend controls without mandating them, the procurement manual and data management plan contain genuine but secondary security provisions, and the workforce grant policy is flagged only because *disaster recovery* in its title refers to economic rather than IT recovery. Under a stricter post hoc rule requiring a score of 2 on at least one function, all seven true policies remain detected while only the two advisory reports stay flagged (precision 0.778, F1 = 0.875): the 0/1/2 rubric separates policy-defining from policy-adjacent documents.

### 6.4 Keyword List Ablation

Detection performance by keyword-list variant:

| Variant | TP | FP | FN | TN | P | R | F1 | Acc. |
|---|---|---|---|---|---|---|---|---|
| Keyword, original (V0) | 6 | 21 | 1 | 23 | 0.222 | 0.857 | 0.353 | 56.9% |
| Keyword, no *training* (V1) | 6 | 8 | 1 | 36 | 0.429 | 0.857 | 0.571 | 82.4% |
| Keyword, qualified (V2) | 6 | 8 | 1 | 36 | 0.429 | 0.857 | 0.571 | 82.4% |
| Keyword, expanded (V3) | 7 | 8 | 0 | 36 | 0.467 | 1.000 | 0.636 | 84.3% |
| AI-Assisted (M2) | 7 | 5 | 0 | 39 | 0.583 | 1.000 | 0.737 | 90.2% |

Removing (V1) or security-qualifying (V2) the ambiguous *training* keyword substantially improves the baseline: document-level false positives fall from 21 to 8, F1 rises from 0.353 to 0.571, and the number of non-policy documents with a Protect raw count >= 5 falls from 21 to 1 (V1) and 2 (V2). The keyword-AI Pearson correlation for Protect becomes significant (V1: r = 0.736; V2: r = 0.666; V3: r = 0.708; all p < 0.001), confirming that the non-significant correlation above was attributable to a single underspecified term.

The remaining eight false positives (V1-V3) arise from generic terms in non-security contexts (*monitoring* in business plans, *governance* in annual reports, *restoration* in workforce documents) and from the two cybersecurity advisory reports that both methods flag. The false negative (the MD DOIT System and Network Security Policy, whose technical vocabulary matches no original keyword) persists under V1 and V2; only V3's added technical terms (*network segmentation*, *patch management*, *hardening*) recover it, lifting keyword recall to 1.00 and F1 to 0.636. Even against this post hoc upper bound, AI-assisted classification retains higher precision (0.583 vs. 0.467) and F1 (0.737 vs. 0.636), although the document-level difference is no longer statistically significant at this corpus size (McNemar exact p = 0.45). The practical distinction: V3 required domain expertise and failure-mode inspection to engineer, whereas the AI-assisted method performed better from a generic prompt with no list engineering.

### 6.5 Classification Stability

Across the three independent AI classification runs on the 13-document subsample, document-level relevance decisions were identical in all runs for all documents (13/13), and no non-cybersecurity document received a nonzero score on any function in any run. At the document-function level (78 cells), 70.5% of cells were scored identically across all three runs and 97.4% varied by at most one point (mean pairwise agreement 79.5%). Disagreements concentrated on the partial-versus-present (1 vs. 2) boundary for long manuals evaluated from truncated excerpts. Run-to-run variance thus affects fine-grained maturity ratings more than the binary detection results; function means carry a one-point tolerance.

### 6.6 Supply Chain Coverage

Supply chain keywords appeared in 34 of 51 documents, but high-frequency occurrences were concentrated in procurement manuals, correctional enterprise contracts, and workforce policy documents. Of the seven genuine cybersecurity policies -- a small absolute sample -- substantive supply chain risk management provisions appeared in four. Within the collected public corpus, no municipal-level document contained dedicated supply chain cybersecurity requirements.

---

## 7. Discussion

### 7.1 Governance Deficit

AI classification reveals a consistent pattern within the collected corpus: governance controls (mean 1.71/2) are broadly covered in state-level policies, but no municipal-level cybersecurity policy documents were recovered. Targeted searches surfaced no standalone cybersecurity policy from any of the 23 Maryland counties or the independent city of Baltimore. While some jurisdictions may maintain non-public internal policies, the absence of public-facing governance documents suggests that formal accountability structures and executive cybersecurity ownership remain underdeveloped -- or at least publicly invisible -- at the municipal level. CSF 2.0's Govern function explicitly requires organizational context definition, risk appetite statements, and board-level oversight; none of these provide a public accountability signal in the current corpus.

### 7.2 Supply Chain Risk Management Gap

Supply chain keywords appeared frequently, but AI classification confirmed that most occurrences reflect vendor-of-record relationships in procurement documents rather than cybersecurity obligations: Maryland eMMA procurement policies showed high supply chain keyword counts but near-zero AI scores on NIST CSF functions, indicating that procurement language routinely references contractors without imposing cybersecurity requirements. Given the demonstrated impact of SolarWinds and MOVEit [2, 3], this is a structural vulnerability: municipalities that contract for cloud services, managed IT, or software platforms without cybersecurity contract language have no contractual mechanism to mitigate supply chain risk.

### 7.3 Automated Assessment: Method Selection Implications

Keyword-based approaches are computationally simple, transparent, and reproducible, but the non-significant Protect correlation (r = 0.151, p = 0.291) demonstrates a fundamental limitation when applied to heterogeneous document corpora. When documents are collected via broad web searches, the proportion of non-policy documents is high (86.3% in this corpus), and keyword false positives systematically distort aggregate coverage statistics.

The ablation shows that much of this limitation is addressable through careful list design: removing *training* raises F1 to 0.571, the expanded V3 list reaches 0.636 with full recall, and both restore a significant Protect correlation. The comparison should therefore not be read as "AI versus keyword matching in general" but as evidence of how sensitive keyword methods are to list specification: a carefully engineered list can approach AI performance at the document-detection level, but engineering it required domain expertise and post hoc inspection of failure modes, and even V3 trails AI-assisted classification on precision and F1.

AI-assisted classification avoids that engineering burden. The LLM's use of document-level context allows it to correctly classify a workforce development report despite multiple occurrences of security-adjacent terms, and to correctly score a technical cybersecurity policy whose vocabulary matches no predefined keyword. The trade-off is computational cost, reduced transparency, and residual run-to-run variance in fine-grained ratings; however, the improvement in precision (0.222 to 0.583) and F1 (0.353 to 0.737, versus 0.636 for the strongest keyword variant) suggests that AI-assisted methods are more appropriate when policy corpora include diverse document types.

---

## 8. Recommendations

Based on the analysis, counties and municipalities should: (1) formally adopt NIST CSF 2.0 Govern provisions, documenting risk appetite and executive cybersecurity roles with minimal technical investment; (2) embed cybersecurity requirements -- vendor certification, incident notification, and right-to-audit clauses -- in standard procurement templates; (3) establish regional incident response partnerships to share detection and response capabilities; and (4) publish cybersecurity governance policies to create external accountability, using Maryland's DOIT policy suite as a template. For researchers, AI-assisted classification should be preferred over keyword matching on heterogeneous corpora.

---

## 9. Threats to Validity

Several limitations should be considered. First, this study measures publicly documented policy alignment, not operational readiness: jurisdictions with non-public internal policies would appear to have gaps that do not exist operationally, so findings describe public-facing governance transparency. Second, the corpus is weighted toward state-level Maryland documents; genuine municipal-level policy representation is limited. Third, ground truth labels rest on a primary-purpose decision rule; second-rater validation shows substantial agreement (kappa = 0.73) with disagreements confined to boundary documents, though adjudication by an additional independent rater would further strengthen the labels (the labeling instrument is in the public repository). Fourth, the keyword threshold (raw count >= 5) is arbitrary, though the ablation shows the Protect false-positive problem stems from a single ambiguous term rather than the threshold. Fifth, AI classifications used a fixed model and prompt; the stability check shows stable document-level decisions with residual one-point variance in function scores, and different models or prompts may yield different results. Finally, the study covers a single state and one collection cycle.

---

## 10. Conclusion and Future Work

This paper introduced an automated pipeline for evaluating publicly documented state and local cybersecurity policy alignment and provided an empirical comparison of keyword-based versus AI-assisted NIST CSF 2.0 classification.

Applied to a 51-document Maryland government corpus, AI-assisted classification (F1 = 0.737, accuracy 90.2%) substantially and significantly outperformed keyword-based analysis (F1 = 0.353, accuracy 56.9%; McNemar exact p < 0.001), reducing false positives by 76% and eliminating false negatives. The non-significant keyword-AI Protect correlation (r = 0.151) exposes a fundamental limitation of keyword approaches on heterogeneous corpora; ablations that remove the ambiguous term *training* or expand the term lists narrow but do not close the gap (F1 = 0.571 and 0.636), and a three-run stability check finds fully stable document-level decisions with residual one-point variance in function scores.

Within the collected public corpus, the analysis reveals consistent governance coverage at the state level, measurable detection and recovery gaps, an absence of supply chain cybersecurity requirements outside state-level policies, and no publicly discoverable standalone municipal cybersecurity policies. The Python-based assessment pipeline developed in this work is designed for replication across jurisdictions and time periods, supporting scalable cybersecurity governance benchmarking for researchers, auditors, and policymakers.

Future work includes cross-state validation toward all 50 states, benchmarking open-source and fine-tuned LLM classifiers against the commercial model used here, retrieval-augmented processing of full documents, longitudinal re-collection to track governance improvement, and releasing the dual-rater labeled dataset for method benchmarking.

---

## References

[1] Matthew P. Barrett et al. Framework for Improving Critical Infrastructure Cybersecurity, Version 1.1. NIST, 2018. https://doi.org/10.6028/NIST.CSWP.04162018

[2] CISA. SolarWinds Orion Supply Chain Compromise: Guidance for Affected Organizations, 2021. https://www.cisa.gov/uscert/ncas/alerts/aa20-352a

[3] CISA. MOVEit Transfer and MOVEit Cloud Vulnerabilities, 2023. https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a

[4] Cybersecurity and Infrastructure Security Agency. Cybersecurity Performance Goals, 2024. https://www.cisa.gov/cross-sector-cybersecurity-performance-goals

[5] Sage Despeignes, Titorian Huggins, and Devharsh Trivedi. Local Government Supply Chain Cybersecurity: Addressing the Implementation Gap in Resource-Limited Municipalities. Journal of Computing Sciences in Colleges, 41(3):36-37, 2025.

[6] Executive Office of the President. Executive Order 14028: Improving the Nation's Cybersecurity, 2021. Federal Register, 86 FR 26633.

[7] S. T. Hossain, T. Yigitcanlar, K. Nguyen, and Y. Xu. Local Government Cybersecurity Landscape: A Systematic Review and Conceptual Framework. Applied Sciences, 14(13):5501, 2024.

[8] Rafal Leszczyna. Review of Cybersecurity Assessment Methods: Applicability Perspective. Computers and Security, 108:102376, 2021.

[9] National Institute of Standards and Technology. Cybersecurity Framework 2.0, 2024. https://doi.org/10.6028/NIST.CSWP.29

[10] Donald F. Norris, Laura Mateczun, Anupam Joshi, and Tim Finin. Managing Cybersecurity at the Grassroots: Evidence from the First Nationwide Survey of Local Government Cybersecurity. Journal of Urban Affairs, 43(8):1173-1195, 2021.

[11] Donald F. Norris, Laura K. Mateczun, and Richard F. Forno. Cybersecurity and Local Government. John Wiley & Sons, Hoboken, NJ, 2022.

[12] Benjamin Preis and Lawrence Susskind. Municipal Cybersecurity: More Work Needs to be Done. Urban Affairs Review, 58(2):614-629, 2022.

[13] David Rodriguez, Ian Yang, Jose M. Del Alamo, and Norman Sadeh. Large Language Models: A New Approach for Privacy Policy Analysis at Scale. Computing, 106(12):3879-3903, 2024.

[14] Ron Ross et al. NIST Special Publication 800-53 Revision 5: Security and Privacy Controls for Information Systems and Organizations. NIST, 2020. https://doi.org/10.6028/NIST.SP.800-53r5

[15] S. Savas and S. Karatas. Cyber Governance Studies in Ensuring Cybersecurity: An Overview of Cybersecurity Governance. International Cybersecurity Law Review, 3(1):7-34, 2022.

[16] M. Toussaint, S. Krima, and H. Panetto. Industry 4.0 Data Security: A Cybersecurity Frameworks Review. Journal of Industrial Information Integration, 39:100604, 2024.
