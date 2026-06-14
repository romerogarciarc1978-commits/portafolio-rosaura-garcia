import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CONTROL DE ESTILOS Y LÍNEA GRÁFICA
# ==========================================
st.markdown("""
    <style>
    .section-title {
        color: #00f0ff;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
        margin-bottom: 20px;
    }
    .subtitle-text {
        color: #9d00ff;
        font-size: 1.6rem;
        font-weight: 600;
        margin-top: 5px;
        margin-bottom: 15px;
        text-shadow: 0 0 8px rgba(157, 0, 255, 0.4);
        border-bottom: 1px solid #9d00ff;
        padding-bottom: 5px;
    }
    .box-conclusion {
        background-color: #1f2833;
        border-left: 5px solid #66fcf1;
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
        color: #e5e5e5;
    }
    .dataset-box {
        background-color: #1a1a24;
        border: 1px solid #00f0ff;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="section-title">Tarea 1: Análisis Exploratorio de Datos (EDA)</h1>', unsafe_allow_html=True)

# Carga de datos limpia y remoción de espacios en blanco en las columnas
@st.cache_data
def cargar_datos():
    data = pd.read_csv("datos.csv")
    data.columns = data.columns.str.strip() # Elimina espacios fantasmas
    return data

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar 'datos.csv': {e}")
    st.stop()

# ==========================================
# 2. SUBMENÚ CON CÍRCULOS (SIDEBAR RADIO)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #00f0ff; font-size: 1.1rem; font-weight: bold;'>🔍 SECCIONES DEL EDA</h3>", unsafe_allow_html=True)

submenu = st.sidebar.radio(
    "Seleccione haciendo clic en el círculo:",
    [
        "Descripción del dataset",
        "Descripción de los campos",
        "Navegador del dataset completo",
        "Graficador exploratorio",
        "Hipótesis"
    ]
)

st.sidebar.caption("Portafolio Académico")

# ==========================================
# 3. LÓGICA DE RENDERIZADO DE CONTENIDOS
# ==========================================

# --- MÓDULO 1: DESCRIPCIÓN DEL DATASET ---
if submenu == "Descripción del dataset":
    st.markdown('<p class="subtitle-text">📄 Descripción del Dataset</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dataset-box">
        <p style="text-align: justify; line-height: 1.6; margin-bottom: 0;">
        Este conjunto de datos recopila el registro histórico y comercial de los videojuegos a nivel internacional. 
        Consolida variables críticas del sector tecnológico y del entretenimiento digital, incluyendo volumetrías 
        de ventas regionales, calificaciones de la crítica especializada y de los propios usuarios.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Registros Totales", f"{df.shape[0]:,}")
    c2.metric("Variables Evaluadas", f"{df.shape[1]}")
    if 'Platform' in df.columns:
        c3.metric("Consolas Únicas", f"{df['Platform'].nunique()}")

# --- MÓDULO 2: DESCRIPCIÓN DE LOS CAMPOS (ADAPTADO A TU CSV REAL) ---
elif submenu == "Descripción de los campos":
    st.markdown('<p class="subtitle-text">📋 Descripción de los Campos y Variables</p>', unsafe_allow_html=True)
    
    # Mapeo corregido usando los nombres reales que vimos en tu captura de pantalla
    campos_config = {
        "Nombre del Juego (Name)": {"columna": "Name", "tipo": "cat", "desc": "Título comercial oficial del videojuego."},
        "Plataforma (Platform)": {"columna": "Platform", "tipo": "cat", "desc": "Plataforma o consola de hardware para la cual fue lanzado el software."},
        "Año de Lanzamiento (Year_of_Release)": {"columna": "Year_of_Release", "tipo": "num", "desc": "Año cronológico del lanzamiento oficial al mercado."},
        "Género (Genre)": {"columna": "Genre", "tipo": "cat", "desc": "Categoría o género temático del videojuego."},
        "Publicador / Distribuidor (Publisher)": {"columna": "Publisher", "tipo": "cat", "desc": "Compañía editorial encargada de la distribución."},
        "Ventas Norteamérica (NA_Sales)": {"columna": "NA_Sales", "tipo": "num", "desc": "Volumen de ventas en Norteamérica (en millones de unidades)."},
        "Ventas Europa (EU_Sales)": {"columna": "EU_Sales", "tipo": "num", "desc": "Volumen de ventas en la Unión Europea (en millones de unidades)."},
        "Ventas Japón (JP_Sales)": {"columna": "JP_Sales", "tipo": "num", "desc": "Volumen de ventas en Japón (en millones de unidades)."},
        "Otras Ventas (Other_Sales)": {"columna": "Other_Sales", "tipo": "num", "desc": "Volumen de ventas en mercados secundarios o resto del mundo."},
        "Ventas Globales (Global_Sales)": {"columna": "Global_Sales", "tipo": "num", "desc": "Facturación total estimada a nivel mundial (en millones)."},
        "Puntuación de la Crítica (Critic_Score)": {"columna": "Critic_Score", "tipo": "num", "desc": "Calificación promedio otorgada por la prensa especializada."},
        "Puntuación de Usuarios (User_Score)": {"columna": "User_Score", "tipo": "num", "desc": "Calificación promedio otorgada por la comunidad de jugadores."}
    }
    
    opcion_elegida = st.selectbox("Seleccione el campo técnico que desea auditar:", list(campos_config.keys()))
    
    config = campos_config[opcion_elegida]
    columna_real = config["columna"]
    tipo_campo = config["tipo"]
    
    st.info(f"**Definición Operacional:** {config['desc']}")
    
    if columna_real in df.columns:
        if tipo_campo == "num":
            st.write("📈 **Medidas Estadísticas (Campo Cuantitativo):**")
            # Convertimos a numérico en tiempo real ignorando textos extraños (como 'tbd' en User_Score)
            serie_numerica = pd.to_numeric(df[columna_real], errors='coerce')
            st.dataframe(serie_numerica.describe(), use_container_width=True)
        else:
            st.write("🔤 **Valores Posibles (Campo Categórico):**")
            valores_unicos = df[columna_real].dropna().unique()
            st.write(list(valores_unicos[:50]))
    else:
        st.error(f"⚠️ La columna '{columna_real}' no se detectó en el archivo. Verifica si está escrita de otra forma.")

# --- MÓDULO 3: NAVEGADOR DEL DATASET COMPLETO ---
elif submenu == "Navegador del dataset completo":
    st.markdown('<p class="subtitle-text">🗂️ Navegador del Dataset Completo</p>', unsafe_allow_html=True)
    rango_filas = st.slider("Cantidad de registros a desplegar:", min_value=5, max_value=200, value=25)
    st.dataframe(df.head(rango_filas), use_container_width=True)

# --- MÓDULO 4: GRAFICADOR EXPLORATORIO ---
elif submenu == "Graficador exploratorio":
    st.markdown('<p class="subtitle-text">📊 Graficador Exploratorio Automatizado</p>', unsafe_allow_html=True)
    columna_graficar = st.selectbox("Seleccione la variable que desea graficar:", df.columns)
    
    columnas_numericas = ["Year_of_Release", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales", "Critic_Score", "User_Score"]
    
    if columna_graficar in columnas_numericas:
        st.write(f"Detectado campo cuantitativo. Renderizando Histograma para: `{columna_graficar}`")
        df_temp_graf = df.copy()
        df_temp_graf[columna_graficar] = pd.to_numeric(df_temp_graf[columna_graficar], errors='coerce')
        fig = px.histogram(df_temp_graf, x=columna_graficar, title=f"Distribución de {columna_graficar}", color_discrete_sequence=['#00f0ff'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Detectado campo categórico. Renderizando Frecuencias para: `{columna_graficar}`")
        conteo_categorias = df[columna_graficar].value_counts().head(15).reset_index()
        conteo_categorias.columns = [columna_graficar, 'Frecuencia']
        fig = px.bar(conteo_categorias, x=columna_graficar, y='Frecuencia', title=f"Frecuencia de {columna_graficar}", color='Frecuencia', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

# --- MÓDULO 5: HIPÓTESIS ---
elif submenu == "Hipótesis":
    st.markdown('<p class="subtitle-text">💡 Validación y Contraste de Hipótesis</p>', unsafe_allow_html=True)
    
    opcion_hipotesis = st.radio(
        "Seleccione la hipótesis analítica que desea auditar:",
        [
            "Hipótesis A: El mercado de Japón (JP_Sales) muestra una fuerte inclinación hacia las consolas portátiles frente a Norteamérica (NA_Sales).",
            "Hipótesis B: El volumen financiero de ventas globales de software físico experimenta una contracción estructural a partir del año 2015."
        ]
    )
    
    if "Hipótesis A" in opcion_hipotesis:
        st.markdown("### Análisis Gráfico Comparativo Regional")
        consolas_clave = ['NES', 'GB', 'DS', '3DS', 'Wii', 'GBA', 'PS2', 'X360', 'PS3']
        if 'Platform' in df.columns:
            df_filtrado_h1 = df[df['Platform'].isin(consolas_clave)].copy()
            df_filtrado_h1['NA_Sales'] = pd.to_numeric(df_filtrado_h1['NA_Sales'], errors='coerce')
            df_filtrado_h1['JP_Sales'] = pd.to_numeric(df_filtrado_h1['JP_Sales'], errors='coerce')
            agrupado_h1 = df_filtrado_h1.groupby('Platform')[['NA_Sales', 'JP_Sales']].sum().reset_index()
            
            fig = px.bar(agrupado_h1, x='Platform', y=['NA_Sales', 'JP_Sales'], barmode='group', title="Ventas por Plataforma: NA vs JP")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="box-conclusion">
            <strong>📝 Conclusión del Análisis:</strong><br>
            La hipótesis se <strong>VALIDA</strong>. Los datos demuestran una preferencia histórica en la región asiática por plataformas móviles y portátiles de Nintendo en comparación con mercados occidentales.
        </div>
        """, unsafe_allow_html=True)
        
    elif "Hipótesis B" in opcion_hipotesis:
        st.markdown("### Análisis de Tendencia Temporal del Mercado Global")
        df_temp_h2 = df.copy()
        
        # Usamos el nombre real de tu columna de años
        nombre_año = 'Year_of_Release' if 'Year_of_Release' in df.columns else 'Year'
        
        df_temp_h2[nombre_año] = pd.to_numeric(df_temp_h2[nombre_año], errors='coerce')
        df_temp_h2['Global_Sales'] = pd.to_numeric(df_temp_h2['Global_Sales'], errors='coerce')
        
        agrupado_h2 = df_temp_h2.groupby(nombre_año)['Global_Sales'].sum().reset_index()
        agrupado_h2 = agrupado_h2[(agrupado_h2[nombre_año] >= 1980) & (agrupado_h2[nombre_año] <= 2020)]
        
        fig = px.line(agrupado_h2, x=nombre_año, y='Global_Sales', title="Evolución Histórica de Ventas Globales", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="box-conclusion">
            <strong>📝 Conclusión del Análisis:</strong><br>
            La hipótesis se <strong>VALIDA PARCIALMENTE</strong>. El análisis refleja un decrecimiento continuo a partir de la transición hacia los formatos y transacciones 100% digitales en tiendas modernas de distribución.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. PIE DE PÁGINA / BOTONES DE NAVEGACIÓN
# ==========================================
st.markdown("---")
st.markdown("### 🧭 Navegación Rápida")
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("⬅️ Volver al Inicio", use_container_width=True):
        st.switch_page("pages/1_inicio.py")
with col_nav2:
    if st.button("Ir al Aprendizaje Automático (Tarea 2) ➡️", use_container_width=True):
        st.switch_page("pages/3_aprendizaje.py")
