import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
import requests
st.set_page_config(page_title="AproxIA", page_icon="Aproxia.png", layout="wide")
col1, col2 = st.columns([10, 2])  # proporción: mucho espacio a la izquierda
with col2:
    st.image("Aproxia.png", width=80)
# --------- Página principal (Home) ---------
# Esta será la primera entrada del menú. Las demás páginas deben ir en la carpeta "pages".
st.header("Estima el valor de tus inmuebles mediante IA")


columnas_entrenamiento = [
"numPhotos",
"floor",
"size",
"exterior",
"rooms",
"bathrooms",
"latitude",
"longitude",
"hasVideo",
"newDevelopment",
"hasLift",
"hasPlan",
"has3DTour",
"has360",
"hasStaging",
"newDevelopmentFinished",
"HasParking",
"ParkingIncluded",
"parkingSpacePrice",
"contrato_alquiler",
"ocupado",
"piscina",
"piso_turistico",
"trastero",
"zonas_comunes",
"accesible",
"amueblado",
"is_floor_DP",
"district_Alboraya Centro",
"district_Algirós",
"district_Barrio de la Luz",
"district_Benicalap",
"district_Benimaclet",
"district_Camins al Grau",
"district_Campanar",
"district_Cardenal Benlloch",
"district_Ciutat Vella",
"district_DP",
"district_El Pla del Real",
"district_Extramurs",
"district_Jesús",
"district_L'Eixample",
"district_L'Olivereta",
"district_La Constitución - Canaleta",
"district_La Saïdia",
"district_Los Juzgados",
"district_Patraix",
"district_Poblats Marítims",
"district_Quatre Carreres",
"district_Rascanya",
"district_Zona Ausias March",
"district_Zona Metro",
"status_DP",
"status_good",
"status_newdevelopment",
"status_renew",
"propertyType_chalet",
"propertyType_countryHouse",
"propertyType_duplex",
"propertyType_flat",
"propertyType_penthouse",
"propertyType_studio",
]

mean_prices = {
    "Alboraya Centro": 233800.0, "Algirós": 344917.780822, "Barrio de la Luz": 152333.333333,
    "Benicalap": 267405.30303, "Benimaclet": 357065.625, "Camins al Grau": 355594.771144,
    "Campanar": 421721.0, "Cardenal Benlloch": 186450.0, "Ciutat Vella": 471826.338843,
    "DP": 154875.0, "El Pla del Real": 501607.843137, "Extramurs": 440052.671296,
    "Jesús": 253030.786164, "L'Eixample": 534020.52, "L'Olivereta": 188714.89404,
    "La Constitución - Canaleta": 215605.555556, "La Saïdia": 281952.537037,
    "Los Juzgados": 255125.0, "Patraix": 275937.655844, "Poblats Marítims": 299262.189873,
    "Quatre Carreres": 373587.863454, "Rascanya": 183224.910615,
    "Zona Ausias March": 289666.666667, "Zona Metro": 164966.666667
}

property_types = ["Edificio", "Penthouse", "Duplex", "Chalet", "Estudio", "Casa de campo"]
statuses = ["Bueno", "Reformado", "Desconocido", "Nueva promoción"]
boolean_opts = ["Verdadero", "Falso", "Desconocido"]
districts = list(mean_prices.keys()) + ["Desconocido"]

# ------------------ Función de preprocesamiento ------------------
ONEHOT_CATEGORIES = {
    'propertyType': ['flat', 'penthouse', 'duplex', 'chalet', 'studio', 'countryHouse'],
    'status': ['good', 'renew', 'DP', 'newdevelopment'],
    'district': districts
}

def preprocesar_inputs(input_dict):
    df = pd.DataFrame([input_dict])
    df = df.replace({True: 1, False: 0, 'Verdadero': 1, 'Falso': 0, 'Desconocido': 3})

    # Piso
    df['is_floor_DP'] = df['floor'].apply(lambda x: 1 if x == 'Desconocido' else 0)
    df['floor'] = df['floor'].replace({'Bajo': 0, 'Entresuelo': 0.5, 'Subsuelo': -0.5})
    df['floor'] = pd.to_numeric(df['floor'], errors='coerce').fillna(3.3379)

    # One-hot encoding
    for col in ['district', 'status', 'propertyType']:
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=False)
        df = pd.concat([df, dummies], axis=1)
        df.drop(columns=col, inplace=True)

    for col, categorias in ONEHOT_CATEGORIES.items():
        for categoria in categorias:
            col_name = f"{col}_{categoria}"
            if col_name not in df.columns:
                df[col_name] = 0

    return df


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Datos básicos", "Ubicación", "Anuncio", "Parking y alquiler", "Otros"])

with tab1:
    col1_db, col2_db = st.columns(2)

    with col1_db:
        tamaño_m2 = st.number_input("Tamaño en (m^2)", min_value=10, value=100, step=1)
        n_hab = st.number_input("Número de habitaciones", min_value=0, value=1, step=1)
        n_bath = st.number_input("Número de baños", min_value=1, value=1, step=1)
        ascensor = st.selectbox("Ascensor", options= boolean_opts)
    with col2_db:
        propiedad = st.selectbox("Tipo de propiedad", options= property_types)
        estado_propiedad = st.selectbox("Estado de la propiedad", options= statuses)
        exterior = st.selectbox("Exterior", options= boolean_opts)

        # Añadir número de plantas y planta, deshabilitando uno si el otro tiene valor
        num_plantas = st.number_input(
            "Número de planta",
            min_value=0,
            value=0,
            step=1,
            disabled=False if st.session_state.get("planta", "") == "" else True,
            key="num_plantas"
        )
        planta_cat = st.selectbox(
            "Planta",
            options=["", "Bajo", "Entresuelo", "Subsuelo", "Desconocido"],
            disabled=False if st.session_state.get("num_plantas", 0) == 0 else True,
            key="planta"
        )
with tab2:
    districts = ['Ciutat Vella', 'Extramurs', 'El Pla del Real', "L'Eixample", 'Camins al Grau', 'Benicalap',
             'Patraix', 'Quatre Carreres', 'Rascanya', 'Poblats Marítims', 'Campanar', 'Benimaclet',
             "L'Olivereta", 'Jesús', 'Algirós', 'Barrio de la Luz', 'La Saïdia', 'Los Juzgados',
             'La Constitución - Canaleta', 'Zona Ausias March', 'Alboraya Centro', 'Cardenal Benlloch',
             'Zona Metro', 'Desconocido']
    distrito = st.selectbox("Distrito", options=districts)

    st.title("Marque la ubicación aproximada en el mapa")

    # Create base map
    m = folium.Map(location=[39.4699, -0.3763], zoom_start=15)  # Madrid as default center

    # Add click listener
    m.add_child(folium.LatLngPopup())

    # Render map
    map_data = st_folium(m,use_container_width=True,  height=500)

    # Get last clicked coordinates
    if map_data and map_data["last_clicked"]:
        latitude = map_data["last_clicked"]["lat"]
        longitude = map_data["last_clicked"]["lng"]
        st.success(f"Has hecho click en: Latitud={latitude}, Longitud={longitude}")
with tab3:
    col1_anuncio, col2_anuncio = st.columns(2)
    with col1_anuncio:
        n_fotos = st.number_input("Número de fotos en anuncio", min_value=0, value=1, step=1)
        plano = st.selectbox("Tiene plano", options= boolean_opts)
        video = st.selectbox("Tiene video", options= boolean_opts)
    with col2_anuncio:
        tour_3d = st.selectbox("Tiene tour 3D", options= boolean_opts)
        vista_360 = st.selectbox("Tiene vista 360º", options= boolean_opts)
        staging = st.selectbox("Tiene staging", options= boolean_opts)
with tab4:
    col1_parking, col2_parking = st.columns(2)
    with col1_parking:
        parking = st.selectbox("Tiene parking", options= boolean_opts)
        parking_precio = st.selectbox("Parking incluido", options= boolean_opts, key= "parking_incluido")
        precio_parking = st.number_input("Precio plaza de parking", format="%.2f", 
                                         value=3.0 if parking_precio == "Verdadero" else 0.0, 
                                         disabled= False if st.session_state.get("parking_incluido", 0) in ["Falso", "Desconocido"] else True, key="precio_parking")
    with col2_parking:
        piso_turistico = st.selectbox("Piso turístico", options= boolean_opts)
        tiene_contrato = st.selectbox("Tiene contrato de alquiler", options= boolean_opts)
        ocupa = st.selectbox("Está ocupado", options= boolean_opts)
with tab5:
    col1_otros, col2_otros = st.columns(2)
    with col1_otros:
        promocion_nueva = st.selectbox("Nueva promoción", options= boolean_opts)
        promocion_termianda = st.selectbox("Promoción terminada", options= boolean_opts)
        amueblado = st.selectbox("Está amueblado", options= boolean_opts)
        trastero = st.selectbox("Tiene trastero", options= boolean_opts)
    with col2_otros:
        accesible = st.selectbox("Es accesible", options= boolean_opts)
        zonas_coumnes = st.selectbox("Tiene zonas comunes", options= boolean_opts)
        piscina = st.selectbox("Tiene piscina", options= boolean_opts)


if st.button("Predecir precio"):
    #st.success("¡Funcionalidad en desarrollo!")
    
    
    # Construcción del diccionario con tus variables
    input_dict = {
        "size": tamaño_m2,"rooms": n_hab,"bathrooms": n_bath,"latitude": latitude,"longitude": longitude,
        "parkingSpacePrice": precio_parking,"propertyType": propiedad,"status": estado_propiedad,"district": distrito,
        "floor": planta_cat if planta_cat else num_plantas,"exterior": exterior,"hasVideo": video,"newDevelopment": promocion_nueva,
        "hasLift": ascensor,"hasPlan": plano,"has3DTour": tour_3d,"has360": vista_360,"hasStaging": staging,"newDevelopmentFinished": promocion_termianda,
        "HasParking": parking,"ParkingIncluded": parking_precio,"contrato_alquiler": tiene_contrato,"ocupado": ocupa,"piscina": piscina,
        "piso_turistico": piso_turistico,"trastero": trastero,"zonas_comunes": zonas_coumnes,"accesible": accesible,
        "amueblado": amueblado,"numPhotos": n_fotos
    }
    
    # Preprocesamiento
    df_modelo = preprocesar_inputs(input_dict)

    # Asegurarse de que estén todas las columnas esperadas
    for col in columnas_entrenamiento:
        if col not in df_modelo.columns:
            df_modelo[col] = 0
    df_modelo = df_modelo[columnas_entrenamiento]
    df_dict = df_modelo.to_dict(orient="records")[0]
    response = requests.post("https://41bf5f53024d.ngrok-free.app/modelpredict", json=df_dict)
    
    # Predicción
    # pred = modelo.predict(df_modelo)[0]
    pred = response.json().get("precio", 0)
    # Comparación con el precio medio de la zona
    mean_price = mean_prices.get(distrito, 0)
    diff = pred - mean_price
    diff_sign = "▲" if diff > 0 else "▼"
    diff_color = "red" if diff > 0 else "green"

    # Mostrar resultados
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6;
                        border-radius:12px;
                        padding:20px;
                        text-align:center;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                <h4 style="color:#333;">Precio estimado</h4>
                <h2 style="color:#0d6efd; font-size:32px;">{pred:,.2f} €</h2>
                <div style="font-size:18px; font-weight:bold; color:{diff_color};">
                    diferencia: {diff_sign} {abs(diff):,.2f} €
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color:#f0f2f6;
                        border-radius:12px;
                        padding:20px;
                        text-align:center;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                <h4 style="color:#333;">Precio medio en {distrito}</h4>
                <h2 style="color:#198754; font-size:32px;">{mean_price:,.2f} €</h2>
            </div>
            """,
            unsafe_allow_html=True
        )