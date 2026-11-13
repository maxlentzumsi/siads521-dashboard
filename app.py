import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Water Contaminant Dashboard")

df = pd.read_csv("data/state_summary.csv")

lithium = (
    df[df["Contaminant"] == "lithium"]
    .sort_values("AboveRefPct", ascending=False)
    .head(10)
)

fig = px.bar(
    lithium,
    x="State",
    y="AboveRefPct",
    hover_data=["TotalPWS", "AboveRefPWS"],
    labels={
        "State": "State",
        "AboveRefPct": "Tested systems above reference lithium (%)",
        "TotalPWS": "Systems",
        "AboveRefPWS": "Systems above reference"
    },
    title="Top 10 states: percentage of systems with at least one above-reference lithium result"
)

fig.update_yaxes(range=[0, 100])

st.plotly_chart(fig, width="stretch")

st.caption(
    "UCMR 5 samples collected during 2023–2025. "
    "Percentages describe tested public water systems with at least one "
    "above-reference result, using EPA's Table 3 comparison method. "
    "The reference is a non-regulatory screening benchmark."
)


####################################################################################################################3


lithium_mrl = (
    df[df["Contaminant"] == "lithium"]
    .sort_values("AtOrAboveMRLPct", ascending=False)
    .head(10)
)

fig_mrl = px.bar(
    lithium_mrl,
    x="State",
    y="AtOrAboveMRLPct",
    hover_data=["TotalPWS", "AtOrAboveMRLPWS"],
    labels={
        "State": "State",
        "AtOrAboveMRLPct": "Tested systems at or above lithium MRL (%)",
        "TotalPWS": "Systems",
        "AtOrAboveMRLPWS": "Systems with lithium results ≥ MRL"
    },
    title="Top 10 states: percentage of systems with at least one above-MRL lithium result"
)

fig_mrl.update_yaxes(range=[0, 100])

st.plotly_chart(fig_mrl, width="stretch")

st.caption(
    "Percentage of tested public water systems with at least one "
    "lithium result ≥ the minimum reporting level of 9 µg/L. "
    "The MRL is a reporting threshold, not a health benchmark."
)
