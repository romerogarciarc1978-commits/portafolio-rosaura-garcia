import streamlit as st
import pandas as pd

st.title("🎮 Sistema de Recomendación de Videojuegos")
st.write("Encuentra tu próximo juego favorito basado en tus preferencias de categoría.")

# Datos de catálogo extendido
juegos_repo = pd.DataFrame({
    'Nombre': ['Cyberpunk 2077', 'The Witcher 3', 'Elden Ring', 'FIFA 24', 'NBA 2K24', 'Starcraft II', 'Age of Empires IV', 'Doom Eternal'],
    'Genero': ['RPG', 'RPG', 'RPG', 'Deportes', 'Deportes', 'Estrategia', 'Estrategia', 'Acción'],
    'Popularidad_Score': [9.2, 9.6, 9.5, 7.8, 7.2, 8.9, 8.7, 9.1]
})

genero_favorito = st.selectbox("Selecciona tu género de videojuegos preferido:", juegos_repo['Genero'].unique())

if st.button("Generar Recomendaciones"):
    recomendaciones = juegos_repo[juegos_repo['Genero'] == genero_favorito].sort_values(by='Popularidad_Score', ascending=False)
    
    st.success(f"Hemos encontrado {len(recomendaciones)} títulos recomendados para ti:")
    for idx, row in recomendaciones.iterrows():
        st.markdown(f"**{row['Nombre']}** - Puntaje de Recomendación: `★ {row['Popularidad_Score']}`")
