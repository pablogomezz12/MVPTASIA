import streamlit as st

# Initialize logged_in flag if it doesn't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
else:
    st.session_state.logged_in = False
# Simple login function
def login():
    st.title("Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")


# Show login or app depending on login state
if not st.session_state.logged_in:
    login()
else:
    pages = {
        "": [
            st.Page("pages/tasacion.py", title="Tasación IA"),
        ]
    }
    pg = st.navigation(pages)
    pg.run()
