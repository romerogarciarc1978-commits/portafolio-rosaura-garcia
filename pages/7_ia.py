import streamlit as st
import pandas as pd
import re

# =========================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =========================================================================
st.set_page_config(page_title="Asistente IA - Analizador", layout="wide")

# =========================================================================
# 2. CARGA DE DATOS OPTIMIZADA CON CACHÉ
# =========================================================================
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("datos.csv")
        
        # Homologar tipos de datos numéricos para evitar fallos analíticos
        columnas_numericas = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count', 
                             'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Cantidad']
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'datos.csv'.")
        return None
    except Exception as e:
        st.error(f"❌ Error al cargar el dataset: {e}")
        return None

df = cargar_datos()

if df is not None:

    # Diccionario para mapear términos comunes a columnas reales del CSV
    diccionario_columnas = {
        'nombre': 'Name', 'juegos': 'Name', 'juego': 'Name',
        'plataforma': 'Platform', 'platform': 'Platform',
        'año': 'Year_of_Release', 'year_of_release': 'Year_of_Release',
        'genero': 'Genre', 'género': 'Genre', 'genre': 'Genre',
        'editor': 'Publisher', 'publisher': 'Publisher',
        'na_sales': 'NA_Sales', 'eu_sales': 'EU_Sales', 'jp_sales': 'JP_Sales',
        'global_sales': 'Global_Sales', 'critic_score': 'Critic_Score',
        'user_score': 'User_Score', 'desarrollador': 'Desarrollador',
        'calificación': 'Calificación', 'cantidad': 'Cantidad'
    }

    st.title("🧠 Consultas de Datos mediante Prompts de IA")
    st.caption("Interactúa con el archivo **datos.csv** utilizando procesamiento de lenguaje natural.")

    with st.expander("👀 Ver estructura de columnas detectadas"):
        st.write(list(df.columns))

    st.markdown("---")

    # =========================================================================
    # 3. INTERFAZ: ASISTENTE DE CONSULTAS GUIADAS
    # =========================================================================
    st.subheader("💡 Asistente de Consultas Guiadas")
    
    col1, col2 = st.columns(2)
    with col1:
        operacion_guiada = st.selectbox(
            "Métrica / Operación:", 
            ["Recomendar el mejor juego de", "Listar valores únicos de", "Mayor Valor del Campo", "Media del Campo"]
        )
    with col2:
        columna_guiada = st.selectbox("Columna / Categoría objetivo:", df.columns)

    if "Recomendar" in operacion_guiada:
        prompt_sugerido = f"¿Cuál es el mejor juego del género Adventure?"
    elif "Listar" in operacion_guiada:
        prompt_sugerido = f"¿Cuáles son los valores únicos del campo {columna_guiada}?"
    else:
        prompt_sugerido = f"¿Cuál es la {operacion_guiada.lower()} {columna_guiada}?"
    
    if st.button("Ejecutar Consulta Guiada"):
        st.session_state['query_ia'] = prompt_sugerido

    st.markdown("---")

    # =========================================================================
    # 4. INTERFAZ: CONSULTA LIBRE EN LENGUAJE NATURAL
    # =========================================================================
    st.subheader("✍️ Escribe tu consulta libre para la IA:")
    
    query_inicial = st.session_state.get('query_ia', "")
    user_query = st.text_input("Introduce tu pregunta:", value=query_inicial, placeholder="Ej: cual es el mejor juego de aventura")

    if st.button("Consultar a la IA"):
        if user_query:
            query_min = user_query.lower()
            procesado_exitoso = False
            columna_detectada = None

            for termino, col_real in diccionario_columnas.items():
                if termino in query_min and col_real in df.columns:
                    columna_detectada = col_real
                    break

            # -----------------------------------------------------------------
            # NUEVA REGLA: Recomendaciones y mejores juegos (Subjetivas / Top)
            # -----------------------------------------------------------------
            if "mejor" in query_min or "recomienda" in query_min or "recomendacion" in query_min or "recomendar" in query_min:
                st.success("🎯 ¡Entendido! Analizando los mejores videojuegos basados en calificaciones y éxito comercial.")
                
                df_filtrado = df.copy()
                subtitulo = "globales del dataset"

                # Detectar si especifican un género en la pregunta de forma dinámica
                if 'genre' in df.columns or 'Genre' in df.columns:
                    generos_disponibles = df['Genre'].dropna().unique()
                    for gen in generos_disponibles:
                        # Reemplazar tildes o variaciones comunes para la comparación
                        if gen.lower() in query_min or (gen.lower() == 'adventure' and 'aventura' in query_min):
                            df_filtrado = df_filtrado[df_filtrado['Genre'].str.lower() == gen.lower()]
                            subtitulo = f"del género **{gen}**"
                            break

                # Ordenar por las mejores notas (Critic_Score) y luego por Ventas globales
                col_score = 'Critic_Score' if 'Critic_Score' in df.columns else ('User_Score' if 'User_Score' in df.columns else 'Global_Sales')
                
                if col_score in df_filtrado.columns:
                    # Obtenemos de forma segura el Top 5
                    top_juegos = df_filtrado.sort_values(by=[col_score, 'Global_Sales'], ascending=False).head(5)
                    
                    st.write(f"### 🏆 Top 5 mejores videojuegos {subtitulo}:")
                    columnas_mostrar = [c for c in ['Name', 'Platform', 'Genre', col_score, 'Global_Sales'] if c in df.columns]
                    st.dataframe(top_juegos[columnas_mostrar], use_container_width=True)
                    procesado_exitoso = True
                else:
                    st.error("No se encontraron columnas de puntuación o ventas para calcular el mejor juego.")

            # -----------------------------------------------------------------
            # REGLA A: Consulta de Categorías / Valores Únicos (Genre, Platform, Name)
            # -----------------------------------------------------------------
            if not procesado_exitoso and ("valores unicos" in query_min or "lista de" in query_min or "valores únicos" in query_min or "cuales son" in query_min or "cual es" in query_min):
                if columna_detectada:
                    valores_unicos = df[columna_detectada].dropna().unique()
                    st.success(f"📋 Se detectaron **{len(valores_unicos)}** valores únicos en la columna **{columna_detectada}**.")
                    
                    if len(valores_unicos) > 50:
                        st.info("💡 Debido al alto volumen de datos, se muestran en una tabla interactiva organizada:")
                        df_items = pd.DataFrame(valores_unicos, columns=[f"Lista de {columna_detectada}"]).sort_values(by=f"Lista de {columna_detectada}")
                        st.dataframe(df_items, use_container_width=True)
                    else:
                        columnas_lista = st.columns(3)
                        for i, item in enumerate(valores_unicos):
                            with columnas_lista[i % 3]:
                                st.write(f"• {item}")
                    procesado_exitoso = True

            # -----------------------------------------------------------------
            # REGLA B: Condicionales Numéricos (Filtros de "mayor a")
            # -----------------------------------------------------------------
            if not procesado_exitoso and ("superior a" in query_min or "mayor a" in query_min or ">" in query_min):
                numeros = [int(s) for s in re.findall(r'\b\d+\b', query_min)]
                if numeros and columna_detectada:
                    valor_limite = numeros[0]
                    resultado_filtrado = df[df[columna_detectada] > valor_limite]
                    
                    st.success(f"🎯 Filtro aplicado: **{columna_detectada} > {valor_limite}**")
                    st.write(f"Se encontraron **{len(resultado_filtrado)}** registros.")
                    st.dataframe(resultado_filtrado.head(10), use_container_width=True)
                    procesado_exitoso = True

            # -----------------------------------------------------------------
            # REGLA C: Operaciones Estadísticas y Métricas Base
            # -----------------------------------------------------------------
            if not procesado_exitoso and columna_detectada:
                if df[columna_detectada].dtype in ['int64', 'float64']:
                    if "menor valor" in query_min or "mínimo" in query_min:
                        st.metric(label=f"Valor Mínimo de {columna_detectada}", value=df[columna_detectada].min())
                        procesado_exitoso = True
                    elif "mayor valor" in query_min or "máximo" in query_min:
                        st.metric(label=f"Valor Máximo de {columna_detectada}", value=df[columna_detectada].max())
                        procesado_exitoso = True
                    elif "media" in query_min or "promedio" in query_min:
                        st.metric(label=f"Media de {columna_detectada}", value=round(df[columna_detectada].mean(), 2))
                        procesado_exitoso = True
                    elif "suma" in query_min or "total" in query_min:
                        st.metric(label=f"Suma Total de {columna_detectada}", value=round(df[columna_detectada].sum(), 2))
                        procesado_exitoso = True

            # -----------------------------------------------------------------
            # REGLA D: Mensaje de Advertencia Seguro
            # -----------------------------------------------------------------
            if not procesado_exitoso:
                lista_columnas_formateada = ", ".join(df.columns)
                st.warning(
                    f"⚠️ **Estructura de pregunta no reconocida.**\n\n"
                    f"• Para recomendaciones intenta: *'¿cuál es el mejor juego de aventura?'* o *'recomienda un juego'*.\n"
                    f"• Para listas intenta: *'valores unicos del campo Genre'*.\n\n"
                    f"**Campos de datos.csv:**\n`{lista_columnas_formateada}`"
                )
        else:
            st.info("Por favor, introduce una consulta.")