import os
import re
import json
import fitz
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

POLICY_DIR = "policies"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("keywords.json") as f:
    keywords = json.load(f)

results = []

def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text.lower()


for file in os.listdir(POLICY_DIR):

    if not file.endswith(".pdf"):
        continue

    path = os.path.join(POLICY_DIR, file)

    text = extract_text(path)

    row = {"Policy": file}

    for category, terms in keywords.items():

        hits = 0

        for term in terms:
            hits += len(re.findall(re.escape(term.lower()), text))

        row[category] = hits

    results.append(row)

df = pd.DataFrame(results)

df.to_csv(
    os.path.join(OUTPUT_DIR,
    "policy_scores.csv"),
    index=False
)

print(df)

