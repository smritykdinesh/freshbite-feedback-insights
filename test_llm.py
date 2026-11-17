import pandas as pd
from src.llm import call_llm, parse_json

df = pd.read_csv("data/feedback.csv")
print(f"Loaded {len(df)} rows\n")

text = df.loc[27, "text"]  # the allergen one
prompt = f"""Classify this customer feedback. Respond with JSON only, using keys:
sentiment (positive/neutral/negative), theme (short snake_case label), urgency (low/medium/high).

FEEDBACK: {text}"""

raw = call_llm(prompt, json_mode=True)
print("Raw output:", raw)
print("Parsed:", parse_json(raw))