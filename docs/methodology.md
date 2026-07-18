# Methodology

This document describes the full data collection and classification pipeline for the `municipal-cyber-policy-analytics` tool, as applied to the Maryland corpus. See [case-study-maryland.md](case-study-maryland.md) for a step-by-step worked example.

---

## Data Collection

The corpus was assembled using two mechanisms. First, targeted Google dork searches using the `site:md.gov` operator with filetype and topic constraints. Second, direct downloads from Maryland state agency websites after reviewing DOIT, MSDE, DHMH, and Judiciary cybersecurity policy pages.

| Query | Results |
|---|---|
| `site:md.gov filetype:pdf cybersecurity policy` | 3 |
| `site:md.gov filetype:pdf disaster recovery plan` | 7 |
| `site:md.gov filetype:pdf contractor cybersecurity` | 3 |
| `site:md.gov filetype:pdf incident response plan` | 7 |
| `site:md.gov filetype:pdf procurement policy` | 25 |
| Direct state agency downloads | 6 |
| **Total collected** | **51** (after removing 4 MD5 duplicates) |

**Key corpus finding:** Only 7 of 51 documents (13.7%) are genuine cybersecurity policies. The remainder are meeting agendas, financial statements, business plans, workforce reports, and administrative documents — a direct consequence of the broad `site:md.gov` operator returning any government PDF.

### Document Type Distribution

| Category | Count |
|---|---|
| Cybersecurity / IT Security Policy | 7 |
| Advisory or Analysis Report | 2 |
| Meeting Agenda or Minutes | 15 |
| Business Plan or Report | 5 |
| Financial Statement | 4 |
| Procurement / RFP Document | 2 |
| Government Policy (Non-Cyber) | 5 |
| Other / Unclassifiable | 11 |
| **Total** | **51** |

### Deduplication

Four exact duplicate files were identified by MD5 hash comparison and removed:

| Duplicate | Original |
|---|---|
| 393fa16f... | 1ef3c6b9... (Apprenticeship Council Minutes) |
| 6d869b64... | 56a4821c... (MCE Management Council Minutes) |
| 1947edb6... | f5ca30b5... (MCE Customer Council Minutes) |
| 141a5778... | 2cdfbc5a... (MCE Management Council Special Session) |

---

## Document Processing Pipeline

All PDFs were processed using **PyMuPDF** (`fitz`), extracting up to 15,000 characters per document.

```
PDF ingestion → text extraction → normalization
→ keyword detection OR LLM classification
→ NIST CSF 2.0 function mapping → scoring
```

Three documents returned zero text because they were scanned images without embedded text layers:
- `af348882...pdf` (garbled OCR)
- `b0c0eb31...pdf` (scanned, no text)
- `c68baa0c...pdf` (scanned, no text)

---

## NIST CSF 2.0 Framework Mapping

Each document-function pair received one of three ratings under both methods:

| Score | Label | Meaning |
|---|---|---|
| 0 | Absent | No coverage of the function's requirements |
| 1 | Partial | Function mentioned or partially addressed |
| 2 | Present | Substantive, operational coverage of the function |

### NIST CSF 2.0 Functions

| Function | Code | Scope |
|---|---|---|
| Govern | GV | Risk management strategy, roles, supply chain risk management, organizational context |
| Identify | ID | Asset inventory, risk assessment, improvement |
| Protect | PR | Access control, identity management, training, data security, platform security |
| Detect | DE | Continuous monitoring, adverse event analysis |
| Respond | RS | Incident management, communication, mitigation |
| Recover | RC | Recovery planning, restoration, improvement |

Supply chain risk management (GV.SC) falls under the Govern function in CSF 2.0 — introduced in this version to formalize third-party risk at the governance level.

---

## Method 1 — Keyword-Based Analysis

### Keyword Lists (`code/manual/keywords.json`)

| Function | Keywords |
|---|---|
| Govern | governance, risk management, cybersecurity strategy, board oversight, security program |
| Identify | asset inventory, risk assessment, business environment, critical systems |
| Protect | access control, authentication, encryption, training, firewall |
| Detect | monitoring, intrusion detection, logging, security event |
| Respond | incident response, containment, communication plan, response team |
| Recover | backup, disaster recovery, business continuity, restoration |
| SupplyChain | vendor, third party, supplier, contractor, service provider, supply chain |

### Scoring

- All keywords matched using case-insensitive regex
- Raw hit counts saved to `output/policy_scores.csv`
- Normalized to 0–2 scale for comparison: 0 = zero hits, 1 = 1–4 hits, 2 = 5+ hits
- Classification threshold: raw count ≥ 5 on any function → document flagged as cybersecurity-relevant

### Scripts

- `code/manual/policy_analysis.py` — produces `output/policy_scores.csv`
- `code/manual/results.py` — produces all Method 1 charts in `results/`

---

## Method 2 — AI-Assisted Classification

### Prompt

```
You are a cybersecurity auditor.
Classify the following policy according to NIST CSF 2.0:
  Govern / Identify / Protect / Detect / Respond / Recover

For each category provide:
  0 = absent
  1 = partial
  2 = present

Explain your reasoning.

[first 12,000 characters of document text]
```

### Model

Claude Sonnet 4.6 (Anthropic). The model returns a score and rationale per function. All rationales are stored in `output/ai_scores.csv` for reproducibility.

### Classification threshold

A document is classified as cybersecurity-relevant if any function scores ≥ 1.

### Scripts

- `code/ai/ai_classify.py` — produces `output/ai_scores.csv`
- `code/ai/compare_methods.py` — produces all comparison charts and CSVs in `results/`

---

## Evaluation

Ground truth labels were assigned based on primary document purpose: a document is a **Cybersecurity Policy** if its explicit purpose is to define cybersecurity requirements, standards, or governance controls. The 7 positive-class documents are:

| Document | Year | Issuing Body |
|---|---|---|
| MD IT Security Manual v1.2 | 2019 | MD DOIT |
| MD DHMH IT Security Policy v4.0 | 2014 | MD DHMH |
| MD Judicial Information Security Policy | 2026 | MD Judiciary |
| MD DOIT Cyber Risk Management Policy | 2026 | MD DOIT |
| MD DOIT Continuous Monitoring Policy | 2026 | MD DOIT |
| MD DOIT System & Network Security Policy | 2026 | MD DOIT |
| MSDE Acceptable Use Policy v2.0 | 2024 | MSDE |

### Limitations

- Ground truth assigned by authors; no independent inter-rater validation.
- Keyword threshold (>=5) is arbitrary; sensitivity analysis not performed.
- AI classification used one fixed model version and prompt; different prompt formulations may yield different scores.
- Corpus covers Maryland only; results may not generalize to other states.
- Three scanned documents were unclassifiable and counted as true negatives.
- Publicly available documents may not reflect actual cybersecurity practices; jurisdictions with non-public policies would appear to have gaps that do not exist operationally.

---

## Reproducing Results

```bash
# From repository root:
pip install pandas matplotlib seaborn scipy pymupdf anthropic

# Method 1: keyword scoring and charts
python code/manual/policy_analysis.py   # -> output/policy_scores.csv
python code/manual/results.py           # -> results/*.png and results/*.csv

# Method 2: AI classification and comparison
export ANTHROPIC_API_KEY=your_key_here
python code/ai/ai_classify.py           # -> output/ai_scores.csv
python code/ai/compare_methods.py       # -> results/*.png and results/*.csv
```

All output files are deterministic given the same model and prompt. The AI scores in `output/ai_scores.csv` were produced using Claude Sonnet 4.6 and are checked into the repository for reproducibility without requiring an API key.

---

## Extending to Other Jurisdictions

To apply this pipeline to a different state or jurisdiction:

1. Replace `policies/` with PDFs from the target jurisdiction.
2. Update the Google dork queries in `dorks.csv` to target the new domain (e.g., `site:virginia.gov`, `site:chicago.gov`).
3. Run `python code/manual/policy_analysis.py` to generate keyword scores.
4. Update ground truth labels in `code/ai/ai_classify.py` based on manual document review.
5. Run `python code/ai/ai_classify.py` and `python code/ai/compare_methods.py`.

The pipeline is jurisdiction-agnostic. No Maryland-specific logic exists in the code; all Maryland-specific content is in `policies/` and the AI score annotations in `ai_classify.py`.

---

## Camera-Ready Additions (2026)

The following methodology components were added for the final CCSC Eastern 2026 version of the paper.

### Input Truncation Rationale

AI classification uses the first 12,000 characters of each document (roughly 3,000 tokens, or 4-6 pages). Policy documents front-load purpose, scope, authority, and requirement statements, so the prefix captures a document's primary intent; a fixed cut also gives every document the same evidence budget and bounds inference cost. The stability check shows the truncation cost appears only as one-point score variance on long manuals; retrieval-augmented full-document processing is listed as future work.

### Keyword-List Ablation (V1-V3)

Three variants of the Method 1 keyword lists isolate the effect of list specification (`code/manual/keyword_ablation.py`, `code/manual/statistical_tests.py`):

| Variant | Definition |
|---|---|
| V0 | Original 4-5 term lists per function (bare *training* included) |
| V1 | V0 minus the single ambiguous term *training* |
| V2 | *training* kept only with a security qualifier (e.g., *security awareness training*) |
| V3 | V1 plus *multi-factor*, *least privilege*, *network segmentation*, *patch management*, *hardening*, *SIEM*, *threat intelligence*, and similar (engineered post hoc; approximates an upper bound) |

Detection rule and thresholds are unchanged across variants. Outputs: `results/keyword_ablation.csv`, `results/keyword_scores_V*.csv`.

### Statistical Evaluation

Method differences are tested with McNemar's exact (binomial) test on paired document-level decisions, and percentile bootstrap 95% confidence intervals (10,000 resamples over documents) are computed for precision, recall, F1, and the F1 difference. Because the 0-2 ratings are ordinal, per-function agreement is reported as Pearson r, Spearman rho, and quadratic-weighted Cohen's kappa. Outputs: `results/statistical_tests.txt`.

### Reproducibility and Model Configuration

All primary classifications: model identifier `claude-sonnet-4-6`, single pass per document, the verbatim auditor prompt (no system prompt beyond it), no per-document tuning, provider-default sampling (no temperature or seed control). Run-to-run stability was measured by re-running the identical prompt three independent times on a stratified 13-document subsample (all 7 ground-truth policies plus 6 non-policy documents). Outputs: `results/llm_stability_run[ABC].csv`, `results/llm_stability_summary.csv`.

### Ground-Truth Label Validation

A second rater independently relabeled all 51 documents using the written primary-purpose rule (`ground_truth_labeling_sheet.xlsx`): raw agreement 92.2% (47/51), Cohen's kappa = 0.73 (substantial). All 7 positives were confirmed; the 4 disagreements are boundary documents (two advisory reports, a data management plan, a workforce disaster-recovery policy), and original labels were retained under the rule. Output: `results/interrater_agreement.txt`.
