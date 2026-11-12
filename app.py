import streamlit as st
import plotly.express as px

st.title("My First Dashboard")
st.write("A practice dashboard using Streamlit and Plotly.")

# Temporary practice data
data = {
    "Player": ["Alex", "Jordan", "Taylor"],
    "Points": [18, 25, 14],
    "Assists": [7, 4, 9],
}

# A dropdown that controls the chart
metric = st.selectbox(
    "Choose a statistic:",
    ["Points", "Assists"]
)

# Create the Plotly chart
fig = px.bar(
    data,
    x="Player",
    y=metric,
    title=f"{metric} by Player"
)

# Display it in Streamlit
st.plotly_chart(fig, width="stretch")
