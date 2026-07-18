# municipal-cyber-policy-analytics

A reproducible Python pipeline for benchmarking state and local cybersecurity readiness by classifying government policy documents against the NIST Cybersecurity Framework (CSF) 2.0.

> Accepted at CCSC Eastern 2026 (Bowie State University); to appear in the Journal of Computing Sciences in Colleges 42(3) as "Benchmarking State and Local Cybersecurity Readiness Through Automated Policy Analytics: Evidence from Maryland Local Governments"

---

## Documentation

| File | Contents |
|---|---|
| [docs/paper.md](docs/paper.md) | Full CCSC-Eastern 2026 paper |
| [docs/case-study-maryland.md](docs/case-study-maryland.md) | Maryland 51-document corpus: end-to-end example |
| [docs/methodology.md](docs/methodology.md) | Data collection, processing pipeline, and scoring |
| [docs/results.md](docs/results.md) | All figures and statistical findings |
| [docs/acronyms.md](docs/acronyms.md) | Expanded acronyms with definitions and examples |
| [docs/references.md](docs/references.md) | Full bibliography |
| [docs/threat-assessment.md](docs/threat-assessment.md) | Related work: threat impact assessment methodologies |
| [docs/compliance.md](docs/compliance.md) | Related work: cybersecurity compliance landscape |

---

## Repository Layout

```
├── code/
│   ├── ai/           ai_classify.py  compare_methods.py
│   └── manual/       policy_analysis.py  results.py  keywords.json
├── docs/             detailed documentation
├── output/           policy_scores.csv  ai_scores.csv
├── policies/         51 Maryland government PDFs (public domain)
└── results/          10 figures  6 CSVs
```

---

## Quick Start

```bash
pip install pandas matplotlib seaborn scipy pymupdf anthropic
python code/manual/policy_analysis.py   # keyword scores  -> output/policy_scores.csv
python code/manual/results.py           # keyword charts  -> results/
python code/ai/ai_classify.py           # AI scores       -> output/ai_scores.csv
python code/ai/compare_methods.py       # comparison      -> results/
```

---

## Cite This Tool

```bibtex
@software{trivedi2025municyber,
  author    = {Trivedi, Devharsh and Despeignes, Sage and Huggins, Titorian},
  title     = {municipal-cyber-policy-analytics: Automated NIST CSF 2.0
               Benchmarking for Municipal Cybersecurity Policy},
  year      = {2025},
  publisher = {GitHub},
  url       = {https://github.com/devharsh/municipal-cyber-policy-analytics}
}
```

See [CITATION.cff](CITATION.cff) for the machine-readable citation.

---

## Related Publications

- **CCSC-E 2025 Poster** -- Despeignes, S., Huggins, T., and Trivedi, D. (2025). *Local Government Supply Chain Cybersecurity: Addressing the Implementation Gap in Resource-Limited Municipalities*. Journal of Computing Sciences in Colleges, 41(3), 36-37. https://dl.acm.org/doi/abs/10.5555/3801163.3801176 (author-archived copy: https://www.researchgate.net/publication/396960966)

---

## Contact

Questions and collaborations are welcome:

- Devharsh Trivedi -- dtrivedi@bowiestate.edu
- LinkedIn: https://www.linkedin.com/in/devharsh/
- ResearchGate: https://www.researchgate.net/profile/Devharsh-Trivedi/research

---

MIT License. Policy PDFs are public domain government records.
