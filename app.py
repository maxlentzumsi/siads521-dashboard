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

########################################################################################################################
left, right = st.columns(2)

with left:
    pws_summary = pd.read_csv("data/pws_summary.csv")

    state = "CO"
    contaminant = "lithium"

    systems = pws_summary[
        (pws_summary["State"] == state) &
        (pws_summary["Contaminant"] == contaminant)
    ].copy()

    #set everything to below MRL to start
    systems["Category"] = "Below MRL only"

    #overwrite the ones at or above MRL
    systems.loc[
        systems["AtOrAboveMRL"], "Category"
    ] = "At or above MRL, none above reference"

    #overwrite the ones above ref
    systems.loc[
        systems["AboveRef"].fillna(False), "Category"
    ] = "Above reference"

    #system is one of the three categories
    categories = [
        "Below MRL only",
        "At or above MRL, none above reference",
        "Above reference"
    ]

    systems["Category"] = pd.Categorical(
        systems["Category"],
        categories=categories,
        ordered=True
    )

    systems = systems.sort_values("Category").reset_index(drop=True)

    systems["x"] = systems.index % 15
    systems["y"] = systems.index // 15

    fig = px.scatter(
        systems,
        x="x",
        y="y",
        color="Category",
        hover_name="PWSID",
        color_discrete_map={
            categories[0]: "lightgray", #below MRL
            categories[1]: "#E8BE50", #MRL
            categories[2]: "#8C6500"  #above ref
        },
        title="Colorado lithium findings — each square is one tested PWS"
    )

    fig.update_traces(
        marker=dict(
            symbol="square",
            size=32,
            line=dict(color="white", width=2)
    ),
    hovertemplate="PWS: %{hovertext}<extra>%{fullData.name}</extra>"
    )

    fig.update_xaxes(
        visible=False,
        range=[-0.5, 14.5],
        constrain="domain"
    )

    fig.update_yaxes(
        visible=False,
        range=[systems["y"].max() + 0.5, -0.5],
        scaleanchor=None
    )

    fig.update_layout(
        autosize=True,
        width=None,
        height=450,
        margin=dict(l=10, r=10, t=50, b=70),
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.08, title_text="")
    )

    st.plotly_chart(fig, width="stretch")
    
    st.caption(
        "UCMR 5 samples collected during 2023–2025. "
        "Public Water Systems (PWS) categorized by having at least one measurement of the above labeled categories from 2023 - 2025 "
        "MRL / Reference concentration are non-regulatory screening benchmarks."
    )

####################################################################################################################3
with right:
    value_data = pd.read_csv("data/value_data.csv")

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

state_summary = pd.read_csv("data/state_summary.csv")

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

st.plotly_chart(fig, width="stretch")

st.caption(
    "UCMR 5 samples collected during 2023–2025. "
    "Map of US states by percentage of PWS (Public Water System) having > 0 measurements above reference concentration "
    "MRL / Reference concentration are non-regulatory screening benchmarks."
)


###################################################################################################################################################################################3


