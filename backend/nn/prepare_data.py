"""
Prepare normalised train/test CSVs from the raw TSV source files.

Output layout (last column = target):
  author_hindex, author_citation_count, author_papers,
  author_age, author_mean_citations_per_paper, hindex_in_5

Run once before training:
    python prepare_data.py
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

FEATURES = [
    "author_hindex",
    "author_citation_count",
    "author_papers",
    "author_age",
    "author_mean_citations_per_paper",
]
TARGET = "hindex_in_5"

ROOT_DIR   = Path(__file__).parent.parent
FEATURES_FILE = str(ROOT_DIR / "data" / "authorFeatures-1975-2005-2015-2.tsv")
RESPONSES_FILE = str(ROOT_DIR / "data" / "authorResponses-1975-2005-2015-2.tsv")
OUTPUT_DIR = str(ROOT_DIR / "data")


def main():
    print("Loading source files...")
    features_df = pd.read_csv(FEATURES_FILE, sep="\t")
    responses_df = pd.read_csv(RESPONSES_FILE, sep="\t")

    df = pd.concat([features_df[FEATURES], responses_df[[TARGET]]], axis=1).dropna()
    df = df[(df["author_papers"] >= 3) & (df["author_hindex"] >= 1)]
    print(f"Clean samples: {len(df)}")

    X = df[FEATURES].values.astype(np.float32)
    y = df[TARGET].values.astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save CSVs: features + target as last column (expected by BESSER-generated code)
    np.savetxt(
        os.path.join(OUTPUT_DIR, "train.csv"),
        np.column_stack([X_train, y_train]),
        delimiter=",",
    )
    np.savetxt(
        os.path.join(OUTPUT_DIR, "test.csv"),
        np.column_stack([X_test, y_test]),
        delimiter=",",
    )

    # Persist the scaler so the FastAPI inference endpoint can reuse it
    with open(os.path.join(OUTPUT_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    print(f"Saved train.csv ({len(X_train)} rows), test.csv ({len(X_test)} rows)")
    print(f"Scaler saved to {OUTPUT_DIR}/scaler.pkl")


if __name__ == "__main__":
    main()