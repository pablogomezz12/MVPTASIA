import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import requests

url = "https://4594e0bb4895.ngrok-free.app/query"


payload = {
    "query": "SELECT * FROM Districts_mean"
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)


st.title("🏙️ District Price Statistics Dashboard")

# Datos de ejemplo
num_operations_last_month = 123
num_operations_last_month_2 = 456

# Estilo CSS para los cuadros
st.markdown("""
    <style>
        .container {
            display: flex;
            justify-content: space-between;  /* Espacio entre los cuadros */
            margin-bottom: 30px;
        }
        .card {
            width: 48%;  /* Los cuadros ocupan el 48% de ancho de la pantalla */
            padding: 40px;
            border-radius: 15px;
            color: white;
            text-align: center;
            font-size: 28px;
        }
        .card1 {
            background-color: #4CAF50;  /* Verde para el primer cuadro */
        }
        .card2 {
            background-color: #FF5722;  /* Naranja para el segundo cuadro */
        }
        .title {
            font-size: 36px;
            font-weight: bold;
        }
        .value {
            font-size: 60px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Contenedor para alinear los cuadros en la misma fila
st.markdown("""
    <div class="container">
""", unsafe_allow_html=True)

# Cuadro 1: Operaciones último mes
st.markdown(f"""
    <div class="card card1">
        <div class="title">Operaciones en el último mes</div>
        <div class="value">{num_operations_last_month}</div>
    </div>
""", unsafe_allow_html=True)

# Cuadro 2: Operaciones del mes anterior
st.markdown(f"""
    <div class="card card2">
        <div class="title">Operaciones del mes anterior</div>
        <div class="value">{num_operations_last_month_2}</div>
    </div>
""", unsafe_allow_html=True)

# Cerrar el contenedor
st.markdown("</div>", unsafe_allow_html=True)




# --- SIDEBAR FILTERS ---
districts = df['district'].sort_values().unique()
selected_districts = st.sidebar.selectbox("Select a district", districts, index=0)


filtered_df = df[df['district']== districts]

# --- BAR CHART ---
st.subheader("Average Price by District")

fig = px.bar(
    df,
    x='district',
    y='avg(price)',
    title="Average Property Price by District",
    labels={'district': 'District', 'avg(price)': 'Average Price (€)'},
    color='AVG(priceByArea)',
    color_continuous_scale='Blues'
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# --- ADDITIONAL STATS TABLE ---
st.subheader(f"Parámetros medios de {selected_districts}")
st.dataframe(filtered_df)

# --- ADDITIONAL STATS TABLE ---

st.subheader(f"Top 3 inmuebles más caros de {selected_districts}")

payload = {
    "query": f"""SELECT * FROM APROXIA_DB.PropertiesClean 
    WHERE district = '{selected_districts}' and propertyType = 'flat' 
    ORDER BY price Desc 
    LIMIT 3;"""
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

st.dataframe(df)

# --- ADDITIONAL STATS TABLE ---

st.subheader(f"Top 3 inmuebles más baratos de {selected_districts}")

payload = {
    "query": f"""SELECT * FROM APROXIA_DB.PropertiesClean 
    WHERE district = '{selected_districts}' and propertyType = 'flat' 
    ORDER BY price Asc 
    LIMIT 3;"""
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

st.dataframe(df)
