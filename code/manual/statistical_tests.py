"""
Statistical comparison of Method 1 (keyword) and Method 2 (AI-assisted) and an
expanded keyword baseline (V3), motivated by reviewer feedback.

Computes, on the real 51-document corpus:
  1. McNemar's exact test on paired document-level detection decisions.
  2. Bootstrap 95% confidence intervals (10,000 resamples) for precision,
     recall, and F1 of each method, and for the F1 difference.
  3. Spearman rank correlation and quadratic-weighted Cohen's kappa per
     function between normalized keyword scores and AI scores.
  4. V3 expanded keyword baseline: base lists plus common security terms
     (bare "training" replaced by security-qualified phrases).

Outputs: results/statistical_tests.txt, results/keyword_scores_V3_expanded.csv,
         updates results/keyword_ablation.csv is left untouched (V3 reported
         separately in statistical_tests.txt).

Run from repository root: python3 code/manual/statistical_tests.py
"""

import json
import math
import os
import re

import fitz  # PyMuPDF
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

POLICY_DIR = "policies"
AI_CSV = "output/ai_scores.csv"
KW_CSV = "results/keyword_scores_V0_original.csv"
OUT = "results"
CATS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]
rng = np.random.default_rng(42)

ai = pd.read_csv(AI_CSV)
kw = pd.read_csv(KW_CSV)
ai["AI_flag"] = (ai[CATS] >= 1).any(axis=1).astype(int)
ai["IsPolicy"] = (ai.DocumentType == "Cybersecurity Policy").astype(int)
df = kw[["Policy", "Flagged", "IsPolicy"]].merge(
    ai[["Policy", "AI_flag"] + CATS], on="Policy"
)
assert len(df) == 51

lines = []


def metrics(flags, truth):
    tp = int(((flags == 1) & (truth == 1)).sum())
    fp = int(((flags == 1) & (truth == 0)).sum())
    fn = int(((flags == 0) & (truth == 1)).sum())
    tn = int(((flags == 0) & (truth == 0)).sum())
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return tp, fp, fn, tn, p, r, f1


# ── 1. McNemar exact test ────────────────────────────────────────────────────
kw_correct = (df.Flagged == df.IsPolicy).astype(int)
ai_correct = (df.AI_flag == df.IsPolicy).astype(int)
b = int(((kw_correct == 1) & (ai_correct == 0)).sum())  # KW right, AI wrong
c = int(((kw_correct == 0) & (ai_correct == 1)).sum())  # AI right, KW wrong
n = b + c
# exact two-sided binomial test
p_mcnemar = sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2**n * 2
p_mcnemar = min(1.0, p_mcnemar)
lines.append(f"McNemar discordant pairs: KW-only-correct b={b}, AI-only-correct c={c}, "
             f"exact two-sided p={p_mcnemar:.6f}")

# ── 2. Bootstrap CIs ─────────────────────────────────────────────────────────
B = 10000
idx = np.arange(51)
stats = {"kw": [], "ai": [], "diff": []}
for _ in range(B):
    s = rng.choice(idx, size=51, replace=True)
    sub = df.iloc[s]
    _, _, _, _, pk, rk, fk = metrics(sub.Flagged.values, sub.IsPolicy.values)
    _, _, _, _, pa, ra, fa = metrics(sub.AI_flag.values, sub.IsPolicy.values)
    stats["kw"].append((pk, rk, fk))
    stats["ai"].append((pa, ra, fa))
    stats["diff"].append(fa - fk)


def ci(vals, lo=2.5, hi=97.5):
    return np.percentile(vals, lo), np.percentile(vals, hi)


for name in ["kw", "ai"]:
    arr = np.array(stats[name])
    for j, m in enumerate(["precision", "recall", "F1"]):
        l, h = ci(arr[:, j])
        lines.append(f"{name} {m}: 95% CI [{l:.3f}, {h:.3f}]")
dl, dh = ci(stats["diff"])
frac_pos = float((np.array(stats["diff"]) > 0).mean())
lines.append(f"F1 difference (AI - KW): 95% CI [{dl:.3f}, {dh:.3f}]; "
             f"share of resamples with AI > KW: {frac_pos:.4f}")

# ── 3. Ordinal agreement per function ────────────────────────────────────────
def norm_kw(v):
    return 0 if v == 0 else (1 if v <= 4 else 2)


def quadratic_kappa(a, bvals):
    cats = [0, 1, 2]
    O = np.zeros((3, 3))
    for x, y in zip(a, bvals):
        O[x, y] += 1
    N = O.sum()
    w = np.array([[(i - j) ** 2 / 4 for j in range(3)] for i in range(3)])
    row = O.sum(1)
    col = O.sum(0)
    E = np.outer(row, col) / N
    denom = (w * E).sum()
    if denom == 0:
        return float("nan")
    return 1 - (w * O).sum() / denom


kw_raw = pd.read_csv(KW_CSV)
m = kw_raw[["Policy"] + CATS].merge(ai[["Policy"] + CATS], on="Policy",
                                    suffixes=("_KW", "_AI"))
lines.append("Function, Pearson r, Spearman rho, quadratic weighted kappa:")
for ccat in CATS:
    a_ = m[f"{ccat}_KW"].apply(norm_kw).astype(int).values
    b_ = m[f"{ccat}_AI"].astype(int).values
    r, pr_ = pearsonr(a_, b_)
    rho, ps_ = spearmanr(a_, b_)
    kap = quadratic_kappa(a_, b_)
    lines.append(f"  {ccat}: r={r:.3f} (p={pr_:.4f}), rho={rho:.3f} (p={ps_:.4f}), "
                 f"kappa_w={kap:.3f}")

# ── 4. V3 expanded keyword baseline ──────────────────────────────────────────
with open("keywords.json") as f:
    BASE = json.load(f)

EXPANDED = {
    "Govern": BASE["Govern"] + ["risk appetite", "security policy",
                                "chief information security officer", "ciso"],
    "Identify": BASE["Identify"] + ["asset management", "vulnerability assessment",
                                    "threat intelligence", "data classification"],
    "Protect": [t for t in BASE["Protect"] if t != "training"] + [
        "multi-factor", "mfa", "least privilege", "identity management",
        "network segmentation", "endpoint protection", "patch management",
        "vulnerability management", "hardening", "security awareness training",
        "security training"],
    "Detect": BASE["Detect"] + ["siem", "security monitoring", "audit log",
                                "anomaly detection", "intrusion prevention"],
    "Respond": BASE["Respond"] + ["incident handling", "escalation", "forensic"],
    "Recover": BASE["Recover"] + ["recovery plan", "resilience",
                                  "recovery time objective"],
}


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()


rows = []
for fn in sorted(os.listdir(POLICY_DIR)):
    if not fn.endswith(".pdf"):
        continue
    text = extract_text(os.path.join(POLICY_DIR, fn))
    row = {"Policy": fn}
    for ccat in CATS:
        row[ccat] = sum(len(re.findall(re.escape(t.lower()), text))
                        for t in EXPANDED[ccat])
    rows.append(row)
v3 = pd.DataFrame(rows)
v3["Flagged"] = (v3[CATS] >= 5).any(axis=1).astype(int)
v3 = v3.merge(ai[["Policy", "IsPolicy"]], on="Policy")
tp, fp, fn_, tn, p, r, f1 = metrics(v3.Flagged.values, v3.IsPolicy.values)
acc = (tp + tn) / 51
lines.append(f"V3 expanded keyword baseline: TP={tp} FP={fp} FN={fn_} TN={tn} "
             f"P={p:.3f} R={r:.3f} F1={f1:.3f} Acc={acc:.3f}")
# Protect correlation for V3
mm = v3[["Policy", "Protect"]].merge(ai[["Policy", "Protect"]], on="Policy",
                                     suffixes=("_KW", "_AI"))
rv3, pv3 = pearsonr(mm.Protect_KW.apply(norm_kw), mm.Protect_AI)
lines.append(f"V3 Protect r vs AI = {rv3:.3f} (p={pv3:.4f})")
v3.to_csv(os.path.join(OUT, "keyword_scores_V3_expanded.csv"), index=False)

# V3 McNemar vs AI
v3m = v3[["Policy", "Flagged"]].merge(df[["Policy", "AI_flag", "IsPolicy"]], on="Policy")
v3_correct = (v3m.Flagged == v3m.IsPolicy).astype(int)
ai_c2 = (v3m.AI_flag == v3m.IsPolicy).astype(int)
b2 = int(((v3_correct == 1) & (ai_c2 == 0)).sum())
c2 = int(((v3_correct == 0) & (ai_c2 == 1)).sum())
n2 = b2 + c2
p2 = min(1.0, sum(math.comb(n2, k) for k in range(0, min(b2, c2) + 1)) / 2**n2 * 2)
lines.append(f"McNemar AI vs V3: b={b2}, c={c2}, exact p={p2:.6f}")

out = "\n".join(lines)
open(os.path.join(OUT, "statistical_tests.txt"), "w").write(out + "\n")
print(out)
