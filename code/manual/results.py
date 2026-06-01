import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "output/policy_scores.csv"
OUTPUT_DIR = "results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# Load Data
# =====================================================

df = pd.read_csv(INPUT_FILE)

categories = [
    "Govern",
    "Identify",
    "Protect",
    "Detect",
    "Respond",
    "Recover"
]

# =====================================================
# Figure 1: NIST CSF Heatmap
# =====================================================

plt.figure(figsize=(10, 6))

heat = df.set_index("Policy")[categories]

sns.heatmap(
    heat,
    annot=True,
    cmap="YlGnBu",
    linewidths=0.5
)

plt.title("NIST CSF Coverage by Municipality")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "nist_heatmap.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# Figure 2: Radar Chart
# =====================================================

avg = df[categories].mean()

angles = np.linspace(
    0,
    2 * np.pi,
    len(categories),
    endpoint=False
).tolist()

values = avg.tolist()

angles += angles[:1]
values += values[:1]

fig = plt.figure(figsize=(7, 7))

ax = plt.subplot(polar=True)

ax.plot(
    angles,
    values,
    linewidth=2
)

ax.fill(
    angles,
    values,
    alpha=0.25
)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

ax.set_title(
    "Average Municipal Cybersecurity Coverage",
    pad=20
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "radar_chart.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# Maturity Score Calculation
# =====================================================

df["MaturityScore"] = df[categories].sum(axis=1)

ranking = df.sort_values(
    "MaturityScore",
    ascending=False
)

ranking.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "maturity_ranking.csv"
    ),
    index=False
)

# =====================================================
# Figure 3: Maturity Ranking Bar Chart
# =====================================================

plt.figure(figsize=(12, 6))

sns.barplot(
    data=ranking,
    x="Policy",
    y="MaturityScore"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.title(
    "Municipal Cybersecurity Policy Maturity Ranking"
)

plt.ylabel("Maturity Score")
plt.xlabel("Municipality Policy")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "maturity_ranking.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# Summary Statistics
# =====================================================

summary = pd.DataFrame({
    "Category": categories,
    "AverageScore": avg.values
})

summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "summary_statistics.csv"
    ),
    index=False
)

print("\nAnalysis Complete")
print(f"Policies analyzed: {len(df)}")
print(f"Results saved to: {OUTPUT_DIR}")
print("\nGenerated files:")
print("- nist_heatmap.png")
print("- radar_chart.png")
print("- maturity_ranking.png")
print("- maturity_ranking.csv")
print("- summary_statistics.csv")

# =====================================================
# Figure 4: NIST Function Distribution Boxplot
# =====================================================

plt.figure(figsize=(10, 6))

box_data = df[categories]

sns.boxplot(data=box_data)

plt.title(
    "Distribution of NIST CSF Function Coverage"
)

plt.ylabel("Coverage Score")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "coverage_boxplot.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# Figure 5: Correlation Heatmap
# =====================================================

corr = df[categories].corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    square=True
)

plt.title(
    "Correlation Between NIST CSF Functions"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================================================
# Figure 6: Average Coverage by Function
# =====================================================

coverage_avg = df[categories].mean()

plt.figure(figsize=(8, 5))

coverage_avg.sort_values(
    ascending=False
).plot(
    kind="bar"
)

plt.title(
    "Average Coverage Across NIST CSF Functions"
)

plt.ylabel("Average Score")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "average_coverage.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

