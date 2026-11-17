"""Single entry point for all LLM calls.

LLM_MODE=ollama (default) -> real local Llama via Ollama
LLM_MODE=mock             -> fast keyword-based fake, no model needed
"""
import json
import os
import re

MODE = os.getenv("LLM_MODE", "ollama")
MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")


def call_llm(prompt, system=None, json_mode=False, temperature=0.0):
    """Send a prompt to the LLM and return the raw text response."""
    if MODE == "mock":
        return _mock_response(prompt, json_mode)

    import ollama  # imported here so mock mode works without Ollama running

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": MODEL,
        "messages": messages,
        "options": {"temperature": temperature},
    }
    if json_mode:
        kwargs["format"] = "json"

    response = ollama.chat(**kwargs)
    return response["message"]["content"]


def parse_json(text):
    """Parse JSON from model output. Small models sometimes add extra text,
    so fall back to extracting the first {...} block."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


# ---------- Mock mode ----------
# Convention: every classification prompt ends with "FEEDBACK: <text>".
# The mock only looks at the text after that marker.
# Order matters: the first theme with a matching keyword wins.

_THEMES = {
    "safety_concern": ["safety", "allergen"],
    "delivery_delay": ["late", "arrived", "estimate", "weekend", "took an hour", "never arrived", "wrong building", "driver"],
    "app_bug": ["crash", "froze", "login", "failing", "lags", "update"],
    "pricing": ["fee", "price", "expensive", "portions", "charged", "cost"],
    "payment_issue": ["payment", "deducted", "refund", "charged twice"],
    "customer_support": ["support", "service", "chat", "reply"],
    "food_quality": ["cold", "taste", "fresh", "quality", "food"],
    "feature_request": ["wish", "please add", "would like", "dark mode", "schedule", "pause"],
}
_NEG = ["late", "cold", "crash", "never", "frustrat", "useless", "wrong", "failed", "froze", "spammy", "missing", "cannot", "twice"]
_POS = ["love", "great", "best", "fast", "impressive", "nice", "good", "improved", "helpful"]
_URGENT = ["safety", "allergen", "deducted", "charged twice", "cannot place", "never arrived"]


def _mock_response(prompt, json_mode):
    # Requirements prompts get a canned placeholder story
    if "TASK: REQUIREMENTS" in prompt:
        m = re.search(r"THEME: (\w+)", prompt)
        label = (m.group(1) if m else "unknown").replace("_", " ")
        return json.dumps({
            "title": f"Improve {label}",
            "user_story": f"As a customer, I want {label} issues resolved so that I can rely on the service.",
            "acceptance_criteria": [
                "Given a typical order, when the issue occurs, then the customer sees a clear resolution.",
                "Given a resolved issue, when the customer reorders, then the problem does not recur.",
            ],
            "assumptions": ["Mock mode: placeholder content."],
            "open_questions": ["Mock mode: placeholder content."],
        })

    # Classification prompts
    text = prompt.split("FEEDBACK:")[-1].lower()

    theme = "other"
    for name, words in _THEMES.items():
        if any(w in text for w in words):
            theme = name
            break

    neg = sum(w in text for w in _NEG)
    pos = sum(w in text for w in _POS)
    sentiment = "negative" if neg > pos else "positive" if pos > neg else "neutral"

    urgency = "high" if any(w in text for w in _URGENT) else "medium" if sentiment == "negative" else "low"

    return json.dumps({"sentiment": sentiment, "theme": theme, "urgency": urgency})