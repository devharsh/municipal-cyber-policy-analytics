"""
Keyword Ablation Study: Sensitivity of Method 1 to the Protect keyword list.

Motivated by CCSC-E reviewer feedback: most of the F1 gap between keyword and
AI classification is driven by the ambiguous Protect keyword "training".
This script re-runs the keyword pipeline under three variants:

  V0  Original keyword lists (paper baseline).
  V1  Protect list without "training".
  V2  Protect list with "training" replaced by security-qualified phrases
      ("security training", "security awareness training",
       "cybersecurity training", "awareness training"),
      i.e. requiring co-occurrence with a security term.

Outputs: results/keyword_ablation.csv (detection metrics per variant)
         results/keyword_ablation_protect.csv (Protect correlation with AI)

Run from repository root: python3 code/manual/keyword_ablation.py
"""

import json
import os
import re

import fitz  # PyMuPDF
import pandas as pd
from scipy.stats import pearsonr

POLICY_DIR = "policies"
AI_CSV = "output/ai_scores.csv"
OUT_DIR = "results"
os.makedirs(OUT_DIR, exist_ok=True)

CATS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]

with open("keywords.json") as f:
    BASE = json.load(f)

VARIANTS = {
    "V0_original": dict(BASE),
    "V1_drop_training": {
        **BASE,
        "Protect": [t for t in BASE["Protect"] if t != "training"],
    },
    "V2_qualified_training": {
        **BASE,
        "Protect": [t for t in BASE["Protect"] if t != "training"]
        + [
            "security training",
            "security awareness training",
            "cybersecurity training",
            "awareness training",
        ],
    },
}


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()


def count_hits(text, terms):
    return sum(len(re.findall(re.escape(t.lower()), text)) for t in terms)


def norm_kw(v):
    if v == 0:
        return 0
    return 1 if v <= 4 else 2


# ── Extract text once per document ───────────────────────────────────────────
texts = {}
for fn in sorted(os.listdir(POLICY_DIR)):
    if fn.endswith(".pdf"):
        texts[fn] = extract_text(os.path.join(POLICY_DIR, fn))
print(f"Extracted {len(texts)} documents")

ai = pd.read_csv(AI_CSV)
positives = set(ai.loc[ai.DocumentType == "Cybersecurity Policy", "Policy"])
print(f"Ground-truth positives: {len(positives)}")

metric_rows, protect_rows = [], []
for vname, kw in VARIANTS.items():
    rows = []
    for fn, text in texts.items():
        row = {"Policy": fn}
        for cat in CATS:
            row[cat] = count_hits(text, kw[cat])
        rows.append(row)
    df = pd.DataFrame(rows)

    # Detection rule (unchanged): flag if any function has raw count >= 5
    df["Flagged"] = (df[CATS] >= 5).any(axis=1).astype(int)
    df["IsPolicy"] = df["Policy"].isin(positives).astype(int)

    tp = int(((df.Flagged == 1) & (df.IsPolicy == 1)).sum())
    fp = int(((df.Flagged == 1) & (df.IsPolicy == 0)).sum())
    fn_ = int(((df.Flagged == 0) & (df.IsPolicy == 1)).sum())
    tn = int(((df.Flagged == 0) & (df.IsPolicy == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn_) if tp + fn_ else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = (tp + tn) / len(df)

    # Protect-function false positives (non-policy docs with Protect >= 5)
    pr_fp = int(((df.Protect >= 5) & (df.IsPolicy == 0)).sum())

    # Protect correlation with AI scores (normalized 0-2 vs AI 0-2)
    m = pd.merge(df[["Policy", "Protect"]], ai[["Policy", "Protect"]],
                 on="Policy", suffixes=("_KW", "_AI"))
    m["Protect_KW_norm"] = m["Protect_KW"].apply(norm_kw)
    r, p = pearsonr(m["Protect_KW_norm"], m["Protect_AI"])
    protect_mean = df["Protect"].mean()

    metric_rows.append({
        "Variant": vname, "TP": tp, "FP": fp, "FN": fn_, "TN": tn,
        "Precision": round(prec, 3), "Recall": round(rec, 3),
        "F1": round(f1, 3), "Accuracy": round(acc, 3),
        "Protect_FP_docs": pr_fp,
        "Protect_mean_raw": round(protect_mean, 2),
        "Protect_r_vs_AI": round(r, 3), "Protect_p": round(p, 4),
    })
    df.to_csv(os.path.join(OUT_DIR, f"keyword_scores_{vname}.csv"), index=False)

res = pd.DataFrame(metric_rows)
res.to_csv(os.path.join(OUT_DIR, "keyword_ablation.csv"), index=False)
print(res.to_string(index=False))
