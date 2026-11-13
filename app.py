import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

st.title("Water Contaminant Dashboard")

contaminant_summary = pd.read_csv("data/contaminant_summary.csv")

plot_data = (
    contaminant_summary
    .nlargest(10, "AtOrAboveMRLPct")
    .sort_values("AtOrAboveMRLPct")
)

fig = px.bar(
    plot_data,
    x="AtOrAboveMRLPct",
    y="Contaminant",
    orientation="h",
    title="Top 10 contaminants by percentage at or above MRL",
    height=500
)

fig.update_traces(
    marker_color=[
        "#E8BE50" if i % 2 == 0 else "goldenrod"
        for i in range(len(plot_data))
    ]
)

fig.show()

st.plotly_chart(fig, width="stretch")

st.caption(
    "UCMR 5 samples collected during 2023–2025. "
    "Percentages describe precentage of measurements at or above miminum reportable level (MRL) "
    "MRL is a non-regulatory screening benchmark."
)


####################################################################################################################3

