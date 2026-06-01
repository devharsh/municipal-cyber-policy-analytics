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
