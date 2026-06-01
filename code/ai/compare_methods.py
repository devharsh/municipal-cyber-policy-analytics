"""
Method Comparison: Keyword-Based vs. AI-Assisted NIST CSF 2.0 Classification
Generates all comparison outputs for the CCSC-E 2027 paper.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy.stats import pearsonr

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_DIR  = "results"
KEYWORD_CSV = "output/policy_scores.csv"
AI_CSV      = "output/ai_scores.csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATS = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]

# Ground-truth document types that are genuine cybersecurity/IT security policies
POLICY_TYPES = {"Cybersecurity Policy"}

# ─────────────────────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────────────────────
df_kw = pd.read_csv(KEYWORD_CSV)
df_ai = pd.read_csv(AI_CSV)

# Merge on Policy filename (inner join — only documents present in both)
df = pd.merge(df_kw[["Policy"] + CATS],
              df_ai[["Policy"] + CATS + ["DocumentType", "Reasoning"]],
              on="Policy",
              suffixes=("_KW", "_AI"))

print(f"Matched documents: {len(df)}")

# ─────────────────────────────────────────────────────────────────────────────
# Normalise keyword scores to 0-2 scale for fair comparison
# (keyword counts → 0/1/2 by thresholding: 0=0, 1-4=1, 5+=2)
# ─────────────────────────────────────────────────────────────────────────────
def norm_kw(v):
    if v == 0:
        return 0
    elif v <= 4:
        return 1
    else:
        return 2

for c in CATS:
    df[f"{c}_KW_norm"] = df[f"{c}_KW"].apply(norm_kw)

# Ground truth: is document a genuine cybersecurity policy?
df["IsPolicy"] = df["DocumentType"].isin(POLICY_TYPES).astype(int)

# ─────────────────────────────────────────────────────────────────────────────
# Build binary detection: does the method flag the document as cyber-relevant?
# KW: any category keyword count >= 5  (raw score)
# AI: any category AI score >= 1
# ─────────────────────────────────────────────────────────────────────────────
kw_score_cols = [f"{c}_KW" for c in CATS]
ai_score_cols = [f"{c}_AI" for c in CATS]

df["KW_flagged"] = (df[kw_score_cols].max(axis=1) >= 5).astype(int)
df["AI_flagged"] = (df[ai_score_cols].max(axis=1) >= 1).astype(int)

# ─────────────────────────────────────────────────────────────────────────────
# Confusion metrics
# ─────────────────────────────────────────────────────────────────────────────
def confusion(y_true, y_pred):
    tp = ((y_pred == 1) & (y_true == 1)).sum()
    fp = ((y_pred == 1) & (y_true == 0)).sum()
    fn = ((y_pred == 0) & (y_true == 1)).sum()
    tn = ((y_pred == 0) & (y_true == 0)).sum()
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy  = (tp + tn) / len(y_true)
    return dict(TP=tp, FP=fp, FN=fn, TN=tn,
                Precision=round(precision,3), Recall=round(recall,3),
                F1=round(f1,3), Accuracy=round(accuracy,3))

metrics_kw = confusion(df["IsPolicy"], df["KW_flagged"])
metrics_ai = confusion(df["IsPolicy"], df["AI_flagged"])

# ─────────────────────────────────────────────────────────────────────────────
# Save comparison summary CSV
# ─────────────────────────────────────────────────────────────────────────────
rows = []
for c in CATS:
    kw_vals = df[f"{c}_KW_norm"].values
    ai_vals = df[f"{c}_AI"].values
    if kw_vals.std() > 0 and ai_vals.std() > 0:
        r, p = pearsonr(kw_vals, ai_vals)
    else:
        r, p = float("nan"), float("nan")
    rows.append({
        "Category": c,
        "KW_Mean": round(kw_vals.mean(), 3),
        "AI_Mean": round(ai_vals.mean(), 3),
        "KW_StdDev": round(kw_vals.std(), 3),
        "AI_StdDev": round(ai_vals.std(), 3),
        "Pearson_r": round(r, 3) if not np.isnan(r) else "N/A",
        "p_value":   round(p, 4) if not np.isnan(p) else "N/A",
    })

df_summary = pd.DataFrame(rows)
df_summary.to_csv(os.path.join(OUTPUT_DIR, "method_comparison_by_category.csv"), index=False)

# Overall metrics table
metrics_df = pd.DataFrame({
    "Method": ["Keyword-Based (Method 1)", "AI-Assisted (Method 2)"],
    "True Positives":  [metrics_kw["TP"],  metrics_ai["TP"]],
    "False Positives": [metrics_kw["FP"],  metrics_ai["FP"]],
    "False Negatives": [metrics_kw["FN"],  metrics_ai["FN"]],
    "True Negatives":  [metrics_kw["TN"],  metrics_ai["TN"]],
    "Precision":       [metrics_kw["Precision"], metrics_ai["Precision"]],
    "Recall":          [metrics_kw["Recall"],    metrics_ai["Recall"]],
    "F1 Score":        [metrics_kw["F1"],        metrics_ai["F1"]],
    "Accuracy":        [metrics_kw["Accuracy"],  metrics_ai["Accuracy"]],
})
metrics_df.to_csv(os.path.join(OUTPUT_DIR, "detection_metrics.csv"), index=False)

print("\n=== Detection Metrics ===")
print(metrics_df.to_string(index=False))
print("\n=== Category Comparison ===")
print(df_summary.to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Side-by-side bar — mean score per NIST CSF function
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(CATS))
width = 0.35
bars_kw = ax.bar(x - width/2, df_summary["KW_Mean"], width,
                 label="Method 1: Keyword", color="#2196F3", alpha=0.85, edgecolor="white")
bars_ai = ax.bar(x + width/2, df_summary["AI_Mean"], width,
                 label="Method 2: AI-Assisted", color="#FF5722", alpha=0.85, edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(CATS, fontsize=11)
ax.set_ylabel("Mean Score (0-2 scale)", fontsize=11)
ax.set_title("Average NIST CSF 2.0 Score per Function:\nKeyword vs. AI-Assisted Classification",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.set_ylim(0, 2.4)
for bar in bars_kw:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
            f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)
for bar in bars_ai:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
            f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "method_comparison_bar.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Confusion matrix comparison (2x2 side-by-side)
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, m, title in zip(axes, [metrics_kw, metrics_ai],
                         ["Method 1: Keyword-Based", "Method 2: AI-Assisted"]):
    matrix = np.array([[m["TP"], m["FP"]], [m["FN"], m["TN"]]])
    im = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=max(matrix.max(), 1))
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Flagged Positive", "Flagged Negative"], fontsize=9)
    ax.set_yticklabels(["Actually Positive\n(True Policy)", "Actually Negative\n(Not a Policy)"],
                       fontsize=9)
    ax.set_title(f"{title}\nPrec={m['Precision']}  Rec={m['Recall']}  F1={m['F1']}", fontsize=10)
    labels = [["TP", "FP"], ["FN", "TN"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{labels[i][j]}\n{matrix[i, j]}",
                    ha="center", va="center", fontsize=14, fontweight="bold",
                    color="white" if matrix[i, j] > matrix.max() * 0.5 else "black")
plt.suptitle("Confusion Matrices: Policy Detection Performance", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrices.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Scatter — KW normalised vs AI score for each category
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(13, 8))
colors = {"Cybersecurity Policy": "#E91E63", "Advisory Report": "#9C27B0",
          "Data Management Plan": "#FF9800"}
def doc_color(dtype):
    if dtype in colors:
        return colors[dtype]
    return "#90A4AE"  # grey for non-policy docs

for ax, cat in zip(axes.flat, CATS):
    x_vals = df[f"{cat}_KW_norm"]
    y_vals = df[f"{cat}_AI"]
    c_vals = [doc_color(t) for t in df["DocumentType"]]
    ax.scatter(x_vals + np.random.uniform(-0.06, 0.06, len(x_vals)),
               y_vals + np.random.uniform(-0.06, 0.06, len(y_vals)),
               c=c_vals, alpha=0.75, s=60, edgecolors="white", linewidths=0.5)
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(-0.3, 2.3)
    ax.plot([-0.3, 2.3], [-0.3, 2.3], "--", color="gray", alpha=0.4, linewidth=1)
    ax.set_title(cat, fontsize=11, fontweight="bold")
    ax.set_xlabel("Keyword (normalised)", fontsize=9)
    ax.set_ylabel("AI Score", fontsize=9)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    r_val = df_summary.loc[df_summary["Category"] == cat, "Pearson_r"].values[0]
    ax.text(0.05, 0.92, f"r={r_val}", transform=ax.transAxes, fontsize=9, color="#333")
    # Shade quadrants
    ax.axhspan(0.5, 2.3, xmin=0, xmax=0.35, alpha=0.05, color="blue")  # AI yes, KW no (FN-KW)
    ax.axhspan(-0.3, 0.5, xmin=0.35, xmax=1, alpha=0.05, color="red")  # KW yes, AI no (FP-KW)

legend_patches = [
    mpatches.Patch(color="#E91E63", label="Cybersecurity Policy"),
    mpatches.Patch(color="#9C27B0", label="Advisory Report"),
    mpatches.Patch(color="#FF9800", label="Data Mgmt Plan"),
    mpatches.Patch(color="#90A4AE", label="Other (non-policy)"),
]
fig.legend(handles=legend_patches, loc="upper center", ncol=4,
           bbox_to_anchor=(0.5, 1.01), fontsize=9)
plt.suptitle("Keyword vs. AI Scores by NIST CSF 2.0 Function\n(points above diagonal: AI rates higher; below: Keyword rates higher)",
             fontsize=11, y=1.04)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "scatter_kw_vs_ai.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 4: Heatmap — AI scores for cybersecurity policy documents only
# ─────────────────────────────────────────────────────────────────────────────
df_policy = df[df["DocumentType"].isin(POLICY_TYPES)].copy()
ai_heat = df_policy.set_index("Policy")[[f"{c}_AI" for c in CATS]].rename(
    columns={f"{c}_AI": c for c in CATS})
# Shorten policy names for display
ai_heat.index = [p.replace("MD_", "").replace(".pdf", "").replace("_", " ")[:38]
                 for p in ai_heat.index]
plt.figure(figsize=(10, max(4, len(ai_heat) * 0.55)))
sns.heatmap(ai_heat, annot=True, cmap="YlOrRd", vmin=0, vmax=2,
            linewidths=0.5, fmt="d", cbar_kws={"label": "0=Absent  1=Partial  2=Present"})
plt.title("AI-Assisted NIST CSF 2.0 Classification\n(Genuine Cybersecurity Policy Documents Only)",
          fontsize=12, fontweight="bold")
plt.ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "ai_heatmap_policies.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 5: Radar chart — average scores for genuine policy docs, both methods
# ─────────────────────────────────────────────────────────────────────────────
kw_policy_avg = df_policy[[f"{c}_KW_norm" for c in CATS]].mean().values
ai_policy_avg = df_policy[[f"{c}_AI" for c in CATS]].mean().values

angles = np.linspace(0, 2 * np.pi, len(CATS), endpoint=False).tolist()
kw_vals = kw_policy_avg.tolist() + [kw_policy_avg[0]]
ai_vals = ai_policy_avg.tolist() + [ai_policy_avg[0]]
angles += [angles[0]]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
ax.plot(angles, kw_vals, "o-", linewidth=2, color="#2196F3", label="Method 1: Keyword")
ax.fill(angles, kw_vals, alpha=0.15, color="#2196F3")
ax.plot(angles, ai_vals, "s-", linewidth=2, color="#FF5722", label="Method 2: AI-Assisted")
ax.fill(angles, ai_vals, alpha=0.15, color="#FF5722")
ax.set_xticks(angles[:-1])
ax.set_xticklabels(CATS, fontsize=11)
ax.set_ylim(0, 2)
ax.set_yticks([0.5, 1.0, 1.5, 2.0])
ax.set_yticklabels(["0.5", "1.0", "1.5", "2.0"], fontsize=8)
ax.set_title("Average NIST CSF 2.0 Coverage\n(Genuine Policy Documents, n=7)",
             fontsize=12, fontweight="bold", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15), fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "radar_kw_vs_ai.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 6: False positive analysis — KW scores for non-policy documents
# ─────────────────────────────────────────────────────────────────────────────
df_nonpol = df[~df["DocumentType"].isin(POLICY_TYPES)].copy()
fp_data = []
for c in CATS:
    fp_data.append({
        "Category": c,
        "KW_FalsePositives": (df_nonpol[f"{c}_KW"] >= 5).sum(),
        "AI_FalsePositives": (df_nonpol[f"{c}_AI"] >= 1).sum(),
    })
df_fp = pd.DataFrame(fp_data)
df_fp.to_csv(os.path.join(OUTPUT_DIR, "false_positive_analysis.csv"), index=False)

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(CATS))
width = 0.35
ax.bar(x - width/2, df_fp["KW_FalsePositives"], width,
       label="Method 1: Keyword", color="#2196F3", alpha=0.85)
ax.bar(x + width/2, df_fp["AI_FalsePositives"], width,
       label="Method 2: AI-Assisted", color="#FF5722", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(CATS, fontsize=11)
ax.set_ylabel("Count of False Positives\n(non-policy docs incorrectly flagged)", fontsize=10)
ax.set_title("False Positive Count by NIST CSF 2.0 Function\n(Non-Policy Documents Incorrectly Flagged as Cybersecurity-Relevant)",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "false_positive_comparison.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Figure 7: Stacked bar — document type distribution of flagged docs
# ─────────────────────────────────────────────────────────────────────────────
type_order = df["DocumentType"].value_counts().index.tolist()
kw_counts = df[df["KW_flagged"] == 1]["DocumentType"].value_counts().reindex(type_order, fill_value=0)
ai_counts = df[df["AI_flagged"] == 1]["DocumentType"].value_counts().reindex(type_order, fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
palette = plt.cm.Set2(np.linspace(0, 1, len(type_order)))
for ax, counts, title in zip(axes, [kw_counts, ai_counts],
                              ["Method 1: Keyword-Based", "Method 2: AI-Assisted"]):
    bars = ax.bar(range(len(type_order)), counts.values, color=palette)
    ax.set_xticks(range(len(type_order)))
    ax.set_xticklabels(type_order, rotation=40, ha="right", fontsize=8)
    ax.set_title(f"{title}\n(Documents Flagged as Cybersecurity-Relevant)", fontsize=10, fontweight="bold")
    ax.set_ylabel("Number of Documents")
    for bar, v in zip(bars, counts.values):
        if v > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    str(int(v)), ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "flagged_by_doctype.png"), dpi=300, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Save full merged comparison table
# ─────────────────────────────────────────────────────────────────────────────
out_cols = ["Policy", "DocumentType", "IsPolicy"] + \
           [f"{c}_KW" for c in CATS] + \
           [f"{c}_KW_norm" for c in CATS] + \
           [f"{c}_AI" for c in CATS] + \
           ["KW_flagged", "AI_flagged", "Reasoning"]
df[out_cols].to_csv(os.path.join(OUTPUT_DIR, "full_comparison_table.csv"), index=False)

print("\n=== False Positive Analysis ===")
print(df_fp.to_string(index=False))
print("\nAll output files saved to results/")
print("Files generated:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    print(f"  {f}")
