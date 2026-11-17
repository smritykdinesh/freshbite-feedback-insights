"""Compare prompt versions against the hand-labeled test set.

Usage: python3 -m src.evaluate v1 v2
"""
import sys
from pathlib import Path

import pandas as pd

from src.classify import classify_df

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["sentiment", "theme", "urgency"]


def load_eval():
    feedback = pd.read_csv(ROOT / "data" / "feedback.csv")
    labels = pd.read_csv(ROOT / "eval" / "labeled.csv")
    labels = labels.rename(columns={f: f"true_{f}" for f in FIELDS})
    return feedback.merge(labels, on="id")


def score(df):
    metrics = {"valid_rate": df["valid"].mean()}
    for f in FIELDS:
        metrics[f"{f}_acc"] = (df[f] == df[f"true_{f}"]).mean()
    all_match = pd.Series(True, index=df.index)
    for f in FIELDS:
        all_match &= df[f] == df[f"true_{f}"]
    metrics["exact_match"] = all_match.mean()
    return metrics


if __name__ == "__main__":
    versions = sys.argv[1:] or ["v1", "v2"]
    eval_df = load_eval()
    print(f"Evaluating on {len(eval_df)} labeled rows\n")

    results = {}
    for version in versions:
        out = classify_df(eval_df, version)
        results[version] = score(out)

        # Save every row where the model disagreed with the labels
        wrong = pd.Series(False, index=out.index)
        for f in FIELDS:
            wrong |= out[f] != out[f"true_{f}"]
        cols = ["id", "text"] + [c for f in FIELDS for c in (f"true_{f}", f)]
        out.loc[wrong, cols].to_csv(ROOT / "eval" / f"mismatches_{version}.csv", index=False)

    table = pd.DataFrame(results).T
    table.to_csv(ROOT / "eval" / "results.csv")
    print("\n=== RESULTS ===")
    print((table * 100).round(1).astype(str) + "%")