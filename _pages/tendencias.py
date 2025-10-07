import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import requests

url = "https://4594e0bb4895.ngrok-free.app/query"


payload = {
    "query": "SELECT * FROM PropertiesClean"
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)


print(df.head())


st.title("🏙️ District Price Statistics Dashboard")


# --- SIDEBAR FILTERS ---
districts = df['district'].sort_values().unique()
selected_districts = st.sidebar.multiselect("Select districts", districts, default=districts)

filtered_df = df[df['district'].isin(selected_districts)]

# --- BAR CHART ---
st.subheader("Average Price by District")

fig = px.bar(
    filtered_df,
    x='district',
    y='avg(price)',
    title="Average Property Price by District",
    labels={'district': 'District', 'avg(price)': 'Average Price (€)'},
    color='AVG(priceByArea)',
    color_continuous_scale='Viridis'
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# --- ADDITIONAL STATS TABLE ---
st.subheader("Summary Statistics")
st.dataframe(filtered_df)