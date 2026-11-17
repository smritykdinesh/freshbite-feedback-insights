"""FreshBite Feedback Insights: dashboard for the BA + prompt-engineering project.

Run: streamlit run app.py
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.classify import classify_text
from src.requirements_gen import priority_from_data, rank_themes

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="FreshBite Feedback Insights", layout="wide")


@st.cache_data
def load_classified(version):
    path = ROOT / "data" / f"classified_{version}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


@st.cache_data
def load_requirements(version):
    path = ROOT / "data" / f"requirements_{version}.json"
    return json.loads(path.read_text()) if path.exists() else None


@st.cache_data
def load_results():
    path = ROOT / "eval" / "results.csv"
    return pd.read_csv(path, index_col=0) if path.exists() else None


df = load_classified("v2")
if df is None:
    st.error("Run `python3 -m src.classify v2` first to generate data/classified_v2.csv.")
    st.stop()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
sources = st.sidebar.multiselect(
    "Source", sorted(df["source"].unique()), default=sorted(df["source"].unique())
)
fdf = df[df["source"].isin(sources)]

st.title("FreshBite Feedback Insights")
st.caption("Customer feedback analysed with a local Llama model via Ollama, using versioned prompts.")

tab_overview, tab_priorities, tab_reqs, tab_eval, tab_live = st.tabs(
    ["Overview", "Priorities", "Requirements", "Prompt evaluation", "Try it live"]
)

# ---------- Overview ----------
with tab_overview:
    if fdf.empty:
        st.warning("No feedback matches the selected filters.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Feedback items", len(fdf))
        c2.metric("Average rating", f"{fdf['rating'].mean():.1f} / 5")
        c3.metric("Negative share", f"{(fdf['sentiment'] == 'negative').mean():.0%}")
        c4.metric("High-urgency items", int((fdf["urgency"] == "high").sum()))

        left, right = st.columns(2)
        with left:
            trend = fdf.groupby(["month", "sentiment"]).size().reset_index(name="count")
            fig = px.bar(
                trend, x="month", y="count", color="sentiment", title="Sentiment by month",
                color_discrete_map={"positive": "#2e9e5b", "neutral": "#9aa0a6", "negative": "#d64545"},
            )
            st.plotly_chart(fig, use_container_width=True)
        with right:
            themes = fdf.groupby(["theme", "sentiment"]).size().reset_index(name="count")
            fig = px.bar(
                themes, x="count", y="theme", color="sentiment", orientation="h",
                title="Feedback by theme",
                color_discrete_map={"positive": "#2e9e5b", "neutral": "#9aa0a6", "negative": "#d64545"},
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

        src = fdf.groupby("source")["rating"].mean().reset_index()
        st.plotly_chart(
            px.bar(src, x="source", y="rating", title="Average rating by source", range_y=[0, 5]),
            use_container_width=True,
        )

# ---------- Priorities ----------
with tab_priorities:
    st.subheader("Which problems should we fix first?")
    st.write(
        "Score = mentions weighted by urgency (high=3, medium=2, low=1). Positive feedback is excluded, "
        "except feature requests. Ties are broken by high-urgency count, then lower average rating."
    )
    if fdf.empty:
        st.warning("No feedback matches the selected filters.")
    else:
        ranked, _ = rank_themes(fdf, top_n=8)
        if ranked.empty:
            st.info("Not enough negative feedback in this selection to rank.")
        else:
            ranked["priority"] = ranked.apply(priority_from_data, axis=1)
            ranked["avg_rating"] = ranked["avg_rating"].round(1)
            st.dataframe(ranked.reset_index(), use_container_width=True, hide_index=True)
            fig = px.bar(
                ranked.reset_index(), x="theme", y="score", color="priority",
                title="Priority score by theme",
                color_discrete_map={"high": "#d64545", "medium": "#e8a33d", "low": "#9aa0a6"},
            )
            st.plotly_chart(fig, use_container_width=True)

# ---------- Requirements ----------
with tab_reqs:
    st.subheader("Generated requirements")
    version = st.radio("Prompt version", ["v2", "v1"], horizontal=True)
    stories = load_requirements(version)
    if not stories:
        st.info(f"Run `python3 -m src.requirements_gen {version} v2` to generate these.")
    else:
        st.caption("Priorities are computed from the feedback data. Story text is LLM-drafted and needs BA review.")
        for i, s in enumerate(stories, start=1):
            with st.expander(f"REQ-{i:02d}: {s['title']}  |  priority: {s['priority']}"):
                st.markdown(f"**Theme:** {s['theme']}")
                st.markdown(f"**Source feedback IDs:** {', '.join(str(x) for x in s['source_ids'])}")
                st.markdown(f"**User story:** {s['user_story']}")
                st.markdown("**Acceptance criteria:**")
                for n, c in enumerate(s["acceptance_criteria"], start=1):
                    st.markdown(f"{n}. {c}")
                st.markdown("**Assumptions:**")
                for a in s["assumptions"] or ["None"]:
                    st.markdown(f"- {a}")
                st.markdown("**Open questions:**")
                for q in s["open_questions"] or ["None"]:
                    st.markdown(f"- {q}")

# ---------- Prompt evaluation ----------
with tab_eval:
    st.subheader("Prompt v1 vs v2 on 30 hand-labeled items")
    res = load_results()
    if res is None:
        st.info("Run `python3 -m src.evaluate v1 v2` first.")
    else:
        pct = (res * 100).round(1)
        st.dataframe(pct.astype(str) + "%", use_container_width=True)
        long = pct.reset_index().rename(columns={"index": "prompt"}).melt(
            id_vars="prompt", var_name="metric", value_name="percent"
        )
        st.plotly_chart(
            px.bar(long, x="metric", y="percent", color="prompt", barmode="group",
                   title="Accuracy by metric"),
            use_container_width=True,
        )
        st.caption(
            "Caveats: v1 was never given the allowed theme list, so theme accuracy and valid rate mostly show "
            "the effect of constrained output. The theme list was designed after seeing the same 30 items, "
            "so v2 theme accuracy is likely optimistic. Sentiment and urgency are the fairer comparison."
        )

# ---------- Live classifier ----------
with tab_live:
    st.subheader("Classify new feedback")
    st.caption("Needs Ollama running locally.")
    text = st.text_area("Customer feedback", "My order arrived cold and the driver would not answer my calls.")
    version = st.selectbox("Prompt version", ["v2", "v1"])
    if st.button("Classify") and text.strip():
        with st.spinner("Asking Llama..."):
            result = classify_text(text, version)
        st.json(result)
        if not result["valid"]:
            st.warning("Output failed validation (unparseable or values outside the allowed lists).")