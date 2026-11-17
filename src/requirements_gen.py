"""Turn classified feedback into ranked, traceable user stories.

Usage: python3 -m src.requirements_gen [prompt_version] [classified_version]
Example: python3 -m src.requirements_gen v2 v2
"""
import json
import sys
from pathlib import Path

import pandas as pd

from src.classify import load_prompt
from src.llm import call_llm, parse_json

ROOT = Path(__file__).resolve().parent.parent
URGENCY_WEIGHT = {"high": 3, "medium": 2, "low": 1}
REQUIRED_KEYS = {"title", "user_story", "acceptance_criteria"}


def rank_themes(df, top_n=4):
    """Rank themes by evidence: mentions weighted by urgency."""
    d = df[df["valid"].astype(bool)]
    d = d[(d["sentiment"] != "positive") | (d["theme"] == "feature_request")]
    d = d[d["theme"] != "other"].copy()
    d["weight"] = d["urgency"].map(URGENCY_WEIGHT)

    ranked = d.groupby("theme").agg(
        mentions=("id", "count"),
        score=("weight", "sum"),
        high_urgency=("urgency", lambda s: int((s == "high").sum())),
        avg_rating=("rating", "mean"),
    )
    ranked = ranked.sort_values(
        ["score", "high_urgency", "avg_rating"], ascending=[False, False, True]
    )
    return ranked.head(top_n), d

def priority_from_data(row):
    """Priority comes from evidence, not from the LLM."""
    if row["high_urgency"] >= 2:
        return "high"
    if row["high_urgency"] == 1 or row["mentions"] >= 3:
        return "medium"
    return "low"


def is_valid(p):
    return (
        isinstance(p, dict)
        and REQUIRED_KEYS <= p.keys()
        and isinstance(p["user_story"], str)
        and isinstance(p["acceptance_criteria"], list)
        and len(p["acceptance_criteria"]) > 0
    )


def build_story(theme, rows, version):
    texts = rows["text"].head(8).tolist()  # cap prompt size for small models
    prompt = (
        load_prompt(version, "requirements")
        .replace("{theme}", theme)
        .replace("{feedback_list}", "\n".join(f"- {t}" for t in texts))
    )
    for attempt in range(2):
        temp = 0.0 if attempt == 0 else 0.4  # vary on retry, same input would give same output
        parsed = parse_json(call_llm(prompt, json_mode=True, temperature=temp))
        if is_valid(parsed):
            parsed.setdefault("assumptions", [])
            parsed.setdefault("open_questions", [])
            return parsed
    return None


def write_markdown(path, ranked, stories, version):
    lines = [
        "# Requirements from Customer Feedback",
        "",
        f"_Generated with prompt version `{version}`. Priorities are computed from feedback evidence; "
        "story text is drafted by an LLM and should be reviewed by a BA._",
        "",
        "## Theme ranking",
        "",
        "| Rank | Theme | Mentions | High-urgency | Avg rating | Score | Priority |",
        "|---|---|---|---|---|---|---|",
    ]
    for rank, (theme, r) in enumerate(ranked.iterrows(), start=1):
        lines.append(
            f"| {rank} | {theme} | {r['mentions']} | {r['high_urgency']} | "
            f"{r['avg_rating']:.1f} | {r['score']} | {priority_from_data(r)} |"
        )

    lines += ["", "## User stories", ""]
    for i, s in enumerate(stories, start=1):
        lines += [
            f"### REQ-{i:02d}: {s['title']}",
            f"- **Theme:** {s['theme']}",
            f"- **Priority:** {s['priority']}",
            f"- **Source feedback IDs:** {', '.join(str(x) for x in s['source_ids'])}",
            "",
            f"**User story:** {s['user_story']}",
            "",
            "**Acceptance criteria:**",
        ]
        lines += [f"{n}. {c}" for n, c in enumerate(s["acceptance_criteria"], start=1)]
        lines += ["", "**Assumptions:**"]
        lines += [f"- {a}" for a in s["assumptions"]] or ["- None"]
        lines += ["", "**Open questions:**"]
        lines += [f"- {q}" for q in s["open_questions"]] or ["- None"]
        lines.append("")

    Path(path).write_text("\n".join(lines))


if __name__ == "__main__":
    prompt_version = sys.argv[1] if len(sys.argv) > 1 else "v2"
    classified_version = sys.argv[2] if len(sys.argv) > 2 else "v2"

    df = pd.read_csv(ROOT / "data" / f"classified_{classified_version}.csv")
    ranked, filtered = rank_themes(df)
    print("Top themes:\n", ranked, "\n")

    stories = []
    for theme, r in ranked.iterrows():
        rows = filtered[filtered["theme"] == theme]
        print(f"Drafting story for {theme}...")
        story = build_story(theme, rows, prompt_version)
        if story is None:
            print(f"  ! failed to get valid output for {theme}, skipping")
            continue
        story["theme"] = theme
        story["priority"] = priority_from_data(r)
        story["source_ids"] = rows["id"].tolist()
        stories.append(story)

    out_json = ROOT / "data" / f"requirements_{prompt_version}.json"
    out_md = ROOT / "docs" / f"requirements_{prompt_version}.md"
    out_json.write_text(json.dumps(stories, indent=2))
    write_markdown(out_md, ranked, stories, prompt_version)
    print(f"\nSaved {out_json.name} and docs/{out_md.name} ({len(stories)} stories)")