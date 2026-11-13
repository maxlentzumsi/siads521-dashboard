import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Water Contaminant Dashboard")

df = pd.read_csv("data/state_summary.csv")

lithium = df[df["Contaminant"] == "lithium"].sort_values(
    "AboveRefPct",
    ascending=False
)

fig = px.bar(
    lithium,
    x="State",
    y="AboveRefPct",
    hover_data=["TotalPWS", "AboveRefPWS"],
    labels={
        "State": "State",
        "AboveRefPct": "Tested systems above reference (%)",
        "TotalPWS": "Systems tested",
        "AboveRefPWS": "Systems above reference"
    },
    title="Lithium: systems with at least one above-reference result"
)

fig.update_yaxes(range=[0, 100])

st.plotly_chart(fig, width="stretch")

st.caption(
    "UCMR 5 samples collected during 2023–2025. "
    "Percentages describe tested public water systems with at least one "
    "above-reference result, using EPA's Table 3 comparison method. "
    "The reference is a non-regulatory screening benchmark."
)
