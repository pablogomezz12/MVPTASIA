import streamlit as st
st.set_page_config(page_title="Tasación IA", layout="wide")
# --------- Página principal (Home) ---------
# Esta será la primera entrada del menú. Las demás páginas deben ir en la carpeta "pages".
st.header("Tasación de inmuebles mediante IA")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Datos básicos", "Ubicación", "Anuncio", "Parking y alquiler", "Otros"])

with tab1:
    col1_db, col2_db = st.columns(2)

    with col1_db:
        tamaño_m2 = st.number_input("Tamaño en (m^2)", min_value=1, value=1, step=1)
        n_hab = st.number_input("Número de habitaciones", min_value=0, value=0, step=1)
        n_bath = st.number_input("Número de baños", min_value=0, value=0, step=1)
        ascensor = st.selectbox("Ascensor", options=["Verdadero", "Falso", "Desconocido"])
    with col2_db:
        propiedad = st.selectbox("Tipo de propiedad", options=["Edificio", "Penthouse", "Chalet", "Duplex", "Estudio", "Casa de campo"])
        estado_propiedad = st.selectbox("Estado de la propiedad", options=["Bueno", "Reformado", "Desconocido", "Nueva promoción"])
        exterior = st.selectbox("Exterior", options=["Verdadero", "Falso", "Desconocido"])

        # Añadir número de plantas y planta, deshabilitando uno si el otro tiene valor
        num_plantas = st.number_input(
            "Número de plantas",
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
    latitude = st.number_input("Latitud", format="%.6f")
    longitude = st.number_input("Longitud", format="%.6f")
with tab3:
    col1_anuncio, col2_anuncio = st.columns(2)
    with col1_anuncio:
        n_fotos = st.number_input("Número de fotos en anuncio", min_value=0, value=0, step=1)
        plano = st.selectbox("Tiene plano", options=["Verdadero", "Falso", "Desconocido"])
        video = st.selectbox("Tiene video", options=["Verdadero", "Falso", "Desconocido"])
    with col2_anuncio:
        tour_3d = st.selectbox("Tiene tour 3D", options=["Verdadero", "Falso", "Desconocido"])
        vista_360 = st.selectbox("Tiene vista 360º", options=["Verdadero", "Falso", "Desconocido"])
        staging = st.selectbox("Tiene staging", options=["Verdadero", "Falso", "Desconocido"])
with tab4:
    col1_parking, col2_parking = st.columns(2)
    with col1_parking:
        parking = st.selectbox("Tiene parking", options=["Verdadero", "Falso", "Desconocido"])
        parking_precio = st.selectbox("Parking incluido", options=["Verdadero", "Falso", "Desconocido"])
        precio_parking = st.number_input("Precio plaza de parking", format="%.2f")
    with col2_parking:
        piso_turistico = st.selectbox("Piso turístico", options=["Verdadero", "Falso", "Desconocido"])
        tiene_contrato = st.selectbox("Tiene contrato de alquiler", options=["Verdadero", "Falso", "Desconocido"])
        ocupa = st.selectbox("Está ocupado", options=["Verdadero", "Falso", "Desconocido"])
with tab5:
    col1_otros, col2_otros = st.columns(2)
    with col1_otros:
        promocion_nueva = st.selectbox("Nueva promoción", options=["Verdadero", "Falso", "Desconocido"])
        promocion_termianda = st.selectbox("Promoción terminada", options=["Verdadero", "Falso", "Desconocido"])
        trastero = st.selectbox("Tiene trastero", options=["Verdadero", "Falso", "Desconocido"])
    with col2_otros:
        piscina = st.selectbox("Tiene piscina", options=["Verdadero", "Falso", "Desconocido"])
        zonas_coumnes = st.selectbox("Tiene zonas comunes", options=["Verdadero", "Falso", "Desconocido"])
        accesible = st.selectbox("Es accesible", options=["Verdadero", "Falso", "Desconocido"])
        amueblado = st.selectbox("Está amueblado", options=["Verdadero", "Falso", "Desconocido"])


if st.button("Predecir precio"):
    st.success("¡Funcionalidad en desarrollo!")
