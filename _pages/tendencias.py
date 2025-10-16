import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import requests

url = "https://82ddf5320a83.ngrok-free.app/query"


payload = {
    "query": "SELECT * FROM Districts_mean"
}


response = requests.post(url, json=payload)


response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)



import streamlit as st

# Datos de ejemplo
num_operations_last_month = 123
num_operations_last_month_2 = 456


# Crear dos columnas lado a lado
col1, col2 = st.columns(2)

# Estilo CSS para los "cards"
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

# KPI 1
with col1:
    st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-title">
                Operaciones en el último mes del barrio seleccionado 
            </div>
            <div class="metric-value">{num_operations_last_month}</div>
        </div>
    """, unsafe_allow_html=True)
    # with st.popover("ℹ️ Info"):
    #     st.markdown("""
    #     **Operaciones en el último mes:**  
    #     Número total de operaciones registradas durante los últimos 30 días.
    #     """)

# KPI 2
with col2:
    st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-title">
                Operaciones del mes anterior del barrio con más movimiento
            </div>
            <div class="metric-value">{num_operations_last_month_2}</div>
        </div>
    """, unsafe_allow_html=True)
    # with st.popover("ℹ️ Info"):
    #     st.markdown("""
    #     **Operaciones del mes anterior:**  
    #     Total de operaciones contabilizadas en el mes anterior al actual.
    #     """)



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