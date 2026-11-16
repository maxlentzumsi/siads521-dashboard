import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

st.title("Water Contaminant Dashboard")

contaminant_summary = pd.read_csv("data/contaminant_summary.csv")
state_summary = pd.read_csv("data/state_summary.csv")
value_data = pd.read_csv("data/value_data.csv")


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

########################################################################################################################
left, right = st.columns(2)

with left:
    state = "CO"
    contaminant = "lithium"

    row = state_summary[
        (state_summary["State"] == state) &
        (state_summary["Contaminant"] == contaminant)
    ].iloc[0]

    total = int(row["TotalPWS"])
    at_or_above = int(row["AtOrAboveMRLPWS"])
    below = total - at_or_above

    labels = [
        f"All tested systems: {total:,}",
        f"Below MRL only: {below:,} ({below / total:.1%})",
        f"At or above MRL: {at_or_above:,} ({at_or_above / total:.1%})"
    ]

    source = [0, 0]
    target = [1, 2]
    values = [below, at_or_above]
    colors = ["gray", "lightgray", "goldenrod"]

    # Add the reference breakdown when a cutoff is available
    if pd.notna(row["AboveRefPWS"]):
        above_ref = int(row["AboveRefPWS"])
        mrl_only = at_or_above - above_ref

        labels += [
            f"None above reference: {mrl_only:,} ({mrl_only / total:.1%})",
            f"Above reference: {above_ref:,} ({above_ref / total:.1%})"
        ]

        source += [2, 2]
        target += [3, 4]
        values += [mrl_only, above_ref]
        colors += ["#E8BE50", "#8C6500"]

    fig = go.Figure(go.Sankey(
        node=dict(
            label=[
                f"Tested systems: {total}",
                f"Below MRL only: {below}",
                f"At or above MRL, none above reference: {mrl_only}",
                f"Above reference: {above_ref}"
            ],
            color=["gray", "lightgray", "#E8BE50", "#8C6500"],
            pad=30,
            thickness=20
        ),
        link=dict(
            source=[0, 0, 0],
            target=[1, 2, 3],
            value=[below, mrl_only, above_ref],
            color=[
                "rgba(180,180,180,0.4)",
                "rgba(232,190,80,0.4)",
                "rgba(140,101,0,0.5)"
            ]
        )
    ))

    fig.update_layout(
        title=f"{state}: {contaminant} — tested water systems",
        height=400,
        width=700,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#171717",
        font_color="white"
    )

    fig.show()

    st.plotly_chart(fig, width="stretch")
    
    st.caption(
        "Chart shows the breakdown counts of public water systems within a state into three categories. "
        "Below MRL - the system had no measurements of the specified contaminant above minimul reporting level. "
        "At or above MRL but not above reference concentration - one or more measurements between 2023-2025 at or above "
        "minimum reporting level but not above the health-based reference. "
        "Above ref - one or more measurements between 2023-2025 for the specified contaminant above the health-based reference concentration."
    )

####################################################################################################################3
with right:

    selected_state = "CO"
    containment = "lithium"

    state_values = value_data[
        (value_data["State"] == selected_state) &
        (value_data["Contaminant"] == containment)
    ].copy()

    fig = px.scatter(
        state_values,
        x="CollectionDate",
        y="AnalyticalResultValue",
        color="AboveRef",
        color_discrete_map={False: "darkgray", True: "goldenrod"},
        hover_data=["PWSID"],
        title=f"Lithium measurements in {selected_state} at or above MRL",
        labels={
            "CollectionDate": "Collection date",
            "AnalyticalResultValue": "Lithium concentration (µg/L)",
            "AboveRef": "Above reference flag"
        },
        opacity=0.7
    )

    fig.show()

    st.plotly_chart(fig, width="stretch")

    st.caption(
        "UCMR 5 samples collected during 2023–2025. "
        "Concentration of collection (µg/L) at time of collection date "
        "MRL / Reference concentration are non-regulatory screening benchmarks."
    )


###################################################################################################################################################################


containment = "lithium"

lithium_states = state_summary[
    state_summary["Contaminant"] == containment
]

fig = px.choropleth(
    lithium_states,
    locations="State",
    locationmode="USA-states",
    scope="usa",
    color="AboveRefPct",
    color_continuous_scale=["#FFFDE7", "#F9D65C", "#DAA520", "#8C6500"],
    range_color=[0, 100],
    hover_data=["TotalPWS", "AboveRefPWS"],
    labels={
        "AboveRefPct": "Above reference (%)",
        "TotalPWS": "Total Systems",
        "AboveRefPWS": "Systems above reference"
    },
    title="Lithium: tested water systems above reference cutoff, 2023-2025",
    height=550
)

fig.show()

fig.update_layout(
    paper_bgcolor="#171717",
    font_color="white"
)

fig.update_geos(
    bgcolor="#171717",
    landcolor="#333333",
    lakecolor="#171717"
)

st.plotly_chart(fig, width="stretch")

st.caption(
    "UCMR 5 samples collected during 2023–2025. "
    "Map of US states by percentage of PWS (Public Water System) having > 0 measurements above reference concentration "
    "MRL / Reference concentration are non-regulatory screening benchmarks."
)


###################################################################################################################################################################################3


