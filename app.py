import streamlit as st

# 1. CONFIGURACIÓN GLOBAL DE LA APLICACIÓN (Obligatorio en el archivo raíz)
st.set_page_config(
    page_title="Portafolio Profesional de Ciencia de Datos | Rosaura del Carmen García Romero",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. REDIRECCIÓN INMEDIATA A LA PÁGINA DE INICIO
# Reemplaza el texto entre comillas con el nombre EXACTO de tu archivo físico en la carpeta pages/
try:
    st.switch_page("pages/1_Inicio.py")
except Exception:
    # Si tu archivo se llama diferente (por ejemplo, sin emoji o con otro número),
    # Streamlit intentará este plan de respaldo automáticamente.
    st.switch_page("pages/1_inicio.py")
