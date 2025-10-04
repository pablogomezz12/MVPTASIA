import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# --- DATABASE CONFIG ---
DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/mydatabase"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="District Statistics",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ District Price Statistics Dashboard")

# --- CONNECT TO DATABASE ---
@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    query = "SELECT * FROM Districts_mean;"
    df = pd.read_sql(query, con=engine)
    return df

# --- LOAD DATA ---
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

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