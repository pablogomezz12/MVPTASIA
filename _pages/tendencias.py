import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import requests

url = "https://dfcb4fa51fc2.ngrok-free.app/query"


payload = {
    "query": "SELECT * FROM Districts_mean"
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

# # --- SIDEBAR FILTERS ---
# districts = df['district'].sort_values().unique()
# selected_districts = st.sidebar.selectbox("Select a district", districts, index=0)

import streamlit as st

district_data = {
    "Ciutat Vella": {"last_month": 45},
    "L'Eixample": {"last_month": 62},
    "Extramurs": {"last_month": 53},
    "El Pla del Real": {"last_month": 40},
    "Campanar": {"last_month": 38},
    "Benimaclet": {"last_month": 42},
    "Algirós": {"last_month": 55},
    "Camins al Grau": {"last_month": 50},
    "Jesús": {"last_month": 35},
    "La Saïdia": {"last_month": 41},
    "L'Olivereta": {"last_month": 33},
    "Benicalap": {"last_month": 39},
}

# ==============================================
# 🔹 Calcular el barrio con más operaciones
# ==============================================
top_district = max(district_data, key=lambda x: district_data[x]["last_month"])
top_value = district_data[top_district]["last_month"]

# ==============================================
# 🔹 Sidebar - Selector de distrito
# ==============================================
districts = sorted(district_data.keys())
selected_district = st.sidebar.selectbox("🏘️ Selecciona un barrio de Valencia", districts, index=0)

# Valores dinámicos
num_operations_last_month = district_data[selected_district]["last_month"]

# ==============================================
# 🔹 Estilo de las cards
# ==============================================
st.markdown("""
    <style>
        .metric-card {
            background-color: #262730;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25);
            color: white;
        }
        .metric-title {
            font-size: 22px;
            font-weight: 500;
            color: white;
        }
        .metric-value {
            font-size: 48px;
            font-weight: bold;
            margin-top: 10px;
        }
        .green {
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
        }
        .orange {
            background: linear-gradient(135deg, #FF5722, #FF7043);
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================
# 🔹 Crear las dos columnas KPI
# ==============================================
col1, col2 = st.columns(2)

# KPI 1: Operaciones último mes (dinámico)
with col1:
    st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-title">
                Operaciones en el último mes en <b>{selected_district}</b>
            </div>
            <div class="metric-value">{num_operations_last_month}</div>
        </div>
    """, unsafe_allow_html=True)

# KPI 2: Operaciones del barrio con más movimiento
with col2:
    st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-title">
                Barrio con más operaciones el último mes: <b>{top_district}</b>
            </div>
            <div class="metric-value">{top_value}</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================
# 🔹 Contexto explicativo
# ==============================================
st.markdown(f"""
### 📊 Contexto
En **{selected_district}**, se registraron **{num_operations_last_month} operaciones** de compraventa de vivienda en el último mes.  
El barrio con mayor actividad inmobiliaria fue **{top_district}**, con **{top_value} operaciones**, lo que indica una demanda más alta en esa zona.
""")



filtered_df = df[df['district']== selected_district]

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
st.subheader(f"Parámetros medios de {selected_district}")
st.dataframe(filtered_df)

# --- ADDITIONAL STATS TABLE ---
safe_district = selected_district.replace("'", "''")
st.subheader(f"Top 3 inmuebles más caros de {selected_district}")

payload = {
    "query": f"""SELECT price,floor,propertyType,size,rooms,bathrooms,address,hasLift FROM APROXIA_DB.PropertiesClean 
    WHERE district = '{safe_district}' and propertyType = 'flat' 
    ORDER BY price Desc 
    LIMIT 3;"""
}


response = requests.post(url, json=payload)

response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

st.dataframe(df)

# --- ADDITIONAL STATS TABLE ---

st.subheader(f"Top 3 inmuebles más baratos de {selected_district}")

payload = {
    "query": f"""SELECT price,floor,propertyType,size,rooms,bathrooms,address,hasLift FROM APROXIA_DB.PropertiesClean 
    WHERE district = '{safe_district}' and propertyType = 'flat' 
    ORDER BY price Asc 
    LIMIT 3;"""
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

st.dataframe(df)