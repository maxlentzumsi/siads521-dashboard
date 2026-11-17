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
    "Percentages describe precentage of public water systems which having a measurement at or above miminum reportable level (MRL) "
    "MRL is a non-regulatory screening benchmark."
    "Samples were collected from 2023-2025."
)

########################################################################################################################

# Shared filters for the Sankey and scatter
st.subheader("Explore a state and contaminant")

filter_left, filter_right = st.columns(2)

states = sorted(state_summary["State"].dropna().unique().tolist())

with filter_left:
    selected_state = st.selectbox(
        "State",
        states,
        index=states.index("CO"),
        key="detail_state"
    )

# Offer contaminants available in the selected state
contaminants = sorted(
    state_summary.loc[
        state_summary["State"] == selected_state,
        "Contaminant"
    ].unique().tolist()
)

with filter_right:
    selected_contaminant = st.selectbox(
        "Contaminant",
        contaminants,
        index=(
            contaminants.index("lithium")
            if "lithium" in contaminants else 0
        ),
        key="detail_contaminant"
    )

left, right = st.columns(2)

# Sankey
with left:
    row = state_summary[
        (state_summary["State"] == selected_state) &
        (state_summary["Contaminant"] == selected_contaminant)
    ].iloc[0]

    total = int(row["TotalPWS"])
    at_or_above = int(row["AtOrAboveMRLPWS"])
    below = total - at_or_above

    if pd.notna(row["AboveRefPWS"]):
        above_ref = int(row["AboveRefPWS"])
        mrl_only = at_or_above - above_ref

        labels = [
            f"Tested systems: {total:,}",
            f"Below MRL only: {below:,}",
            f"At or above MRL, none above reference: {mrl_only:,}",
            f"Above reference: {above_ref:,}"
        ]

        values = [below, mrl_only, above_ref]
        node_colors = ["gray", "lightgray", "#E8BE50", "#8C6500"]
        link_colors = [
            "rgba(180,180,180,0.4)",
            "rgba(232,190,80,0.4)",
            "rgba(140,101,0,0.5)"
        ]

    else:
        labels = [
            f"Tested systems: {total:,}",
            f"Below MRL only: {below:,}",
            f"At or above MRL: {at_or_above:,}"
        ]

        values = [below, at_or_above]
        node_colors = ["gray", "lightgray", "goldenrod"]
        link_colors = [
            "rgba(180,180,180,0.4)",
            "rgba(218,165,32,0.4)"
        ]

    fig = go.Figure(go.Sankey(
        node=dict(
            label=labels,
            color=node_colors,
            pad=30,
            thickness=20
        ),
        link=dict(
            source=[0] * len(values),
            target=list(range(1, len(values) + 1)),
            value=values,
            color=link_colors
        )
    ))

    fig.update_layout(
        title=f"{selected_state}: {selected_contaminant} — tested systems",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#171717",
        font_color="white"
    )

    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Each system is counted once, based on its highest threshold "
        "category reached during 2023–2025. Reference categories are "
        "shown only when a reference cutoff is available."
    )

# Scatter — uses the same two selections
with right:
    state_values = value_data[
        (value_data["State"] == selected_state) &
        (value_data["Contaminant"] == selected_contaminant)
    ].copy()

    if state_values.empty:
        st.info(
            "No measurements at or above MRL are available "
            "for this selection."
        )

    else:
        state_values["CollectionDate"] = pd.to_datetime(
            state_values["CollectionDate"]
        )

        # Use readable categories, including missing reference information
        state_values["Reference status"] = "Reference unavailable"

        state_values.loc[
            state_values["AboveRef"].eq(False),
            "Reference status"
        ] = "Not above reference cutoff"

        state_values.loc[
            state_values["AboveRef"].eq(True),
            "Reference status"
        ] = "Above reference cutoff"

        fig = px.scatter(
            state_values,
            x="CollectionDate",
            y="AnalyticalResultValue",
            color="Reference status",
            color_discrete_map={
                "Not above reference cutoff": "darkgray",
                "Above reference cutoff": "goldenrod",
                "Reference unavailable": "darkgray"
            },
            hover_data=["PWSID"],
            title=(
                f"{selected_contaminant} measurements in "
                f"{selected_state} at or above MRL"
            ),
            labels={
                "CollectionDate": "Collection date",
                "AnalyticalResultValue": "Concentration (µg/L)"
            },
            opacity=0.7,
            height=400
        )

        st.plotly_chart(fig, width="stretch")

    st.caption(
        "Each dot represents a measurement at or above MRL, "
        "collected during 2023–2025. MRL is a reporting threshold. "
        "Reference concentrations are non-regulatory health-based screening "
        "benchmarks."
    )

# Independent filter for the map
st.subheader("Compare states")

# This map needs a reference cutoff, so offer only applicable contaminants
map_contaminants = sorted(
    state_summary.loc[
        state_summary["AboveRefPct"].notna(),
        "Contaminant"
    ].unique().tolist()
)

map_contaminant = st.selectbox(
    "Map contaminant",
    map_contaminants,
    index=(
        map_contaminants.index("lithium")
        if "lithium" in map_contaminants else 0
    ),
    key="map_contaminant"
)

map_data = state_summary[
    state_summary["Contaminant"] == map_contaminant
]

fig = px.choropleth(
    map_data,
    locations="State",
    locationmode="USA-states",
    scope="usa",
    color="AboveRefPct",
    color_continuous_scale=["#FFFDE7", "#F9D65C", "#DAA520", "#8C6500"],
    range_color=[0, 100],
    hover_data=["TotalPWS", "AboveRefPWS"],
    labels={
        "AboveRefPct": "Above reference (%)",
        "TotalPWS": "Systems tested",
        "AboveRefPWS": "Systems above reference"
    },
    title=f"{map_contaminant}: tested systems above reference cutoff",
    height=550
)

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
    "Percentage of tested systems with at least one measurement above "
    "the reference comparison cutoff during 2023–2025. "
    "Only contaminants with an assigned reference cutoff are offered."
)


