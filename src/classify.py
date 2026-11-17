"""Classify feedback with a versioned prompt and validate the output."""
import sys
from pathlib import Path

import pandas as pd

from src.llm import call_llm, parse_json

ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = ROOT / "prompts"

SENTIMENTS = {"positive", "neutral", "negative"}
URGENCIES = {"low", "medium", "high"}
THEMES = {
    "delivery_delay", "app_bug", "pricing", "payment_issue",
    "customer_support", "food_quality", "feature_request",
    "safety_concern", "other",
}


def load_prompt(version, name="classify"):
    return (PROMPT_DIR / version / f"{name}.txt").read_text()


def _norm(value):
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def classify_text(text, version="v2", retries=1):
    """Return {sentiment, theme, urgency, valid}.

    valid=True only if the model returned parseable JSON AND every value
    is inside the allowed sets. We track this because it is a prompt-quality metric.
    """
    # .replace instead of .format, because the prompt contains JSON braces
    prompt = load_prompt(version).replace("{text}", str(text))

    for _ in range(retries + 1):
        parsed = parse_json(call_llm(prompt, json_mode=True))
        if isinstance(parsed, dict):
            result = {
                "sentiment": _norm(parsed.get("sentiment", "")),
                "theme": _norm(parsed.get("theme", "")),
                "urgency": _norm(parsed.get("urgency", "")),
            }
            result["valid"] = (
                result["sentiment"] in SENTIMENTS
                and result["theme"] in THEMES
                and result["urgency"] in URGENCIES
            )
            return result

    return {"sentiment": None, "theme": None, "urgency": None, "valid": False}


def classify_df(df, version="v2"):
    rows = []
    for i, text in enumerate(df["text"], start=1):
        print(f"[{version}] classifying {i}/{len(df)}", end="\r")
        rows.append(classify_text(text, version))
    print()
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


if __name__ == "__main__":
    version = sys.argv[1] if len(sys.argv) > 1 else "v2"
    df = pd.read_csv(ROOT / "data" / "feedback.csv")
    out = classify_df(df, version)

    out_path = ROOT / "data" / f"classified_{version}.csv"
    out.to_csv(out_path, index=False)

    print(f"\nSaved {out_path.name}")
    print(f"Valid outputs: {out['valid'].sum()}/{len(out)}")
    print("\nThemes:\n", out["theme"].value_counts(dropna=False))
    print("\nSentiment:\n", out["sentiment"].value_counts(dropna=False))
    print("\nUrgency:\n", out["urgency"].value_counts(dropna=False))