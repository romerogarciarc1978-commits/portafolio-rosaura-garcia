import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Analizador de Archivos", layout="wide")

st.title("📊 Analizador Dinámico de Datos")
st.write("Carga tu archivo de datos (CSV o Excel) para explorar su estructura y generar gráficos instantáneos.")

# 1. Componente para cargar archivos desde la computadora
archivo_cargado = st.file_uploader(
    "Selecciona un archivo desde tu equipo:", 
    type=["csv", "xlsx", "xls"]
)

if archivo_cargado is not None:
    # Determinar el tipo de archivo y leerlo correctamente
    nombre_archivo = archivo_cargado.name
    extension = os.path.splitext(nombre_archivo)[1].lower()
    
    try:
        if extension == '.csv':
            df = pd.read_csv(archivo_cargado)
        else:
            df = pd.read_excel(archivo_cargado)
            
        st.success(f"¡Archivo '{nombre_archivo}' cargado exitosamente!")
        
        # 2. Visualización previa de los datos
        st.subheader("📋 Vista Previa de los Datos")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Resumen básico en métricas de Streamlit
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total de Filas (Registros)", f"{df.shape[0]:,}")
        with col_m2:
            st.metric("Total de Columnas (Variables)", df.shape[1])
            
        st.write("---")
        
        # 3. Sección de Graficación Dinámica
        st.subheader("📈 Generador de Gráficos")
        
        # Separar columnas según su tipo de dato para facilitar la selección del usuario
        todas_columnas = df.columns.tolist()
        columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        columnas_categoricas = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        if len(todas_columnas) < 1:
            st.warning("El archivo no contiene columnas válidas para graficar.")
        else:
            # Layout de control para el gráfico
            col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
            
            with col_ctrl1:
                tipo_grafico = st.selectbox(
                    "Tipo de Gráfico:",
                    ["Líneas", "Barras", "Dispersión (Scatter)", "Histograma"]
                )
                
            with col_ctrl2:
                # Eje X suele ser cualquier variable
                eje_x = st.selectbox("Eje X (Horizontal):", todas_columnas, index=0)
                
            with col_ctrl3:
                # Eje Y suele requerir datos numéricos en la mayoría de gráficos
                opciones_y = columnas_numericas if len(columnas_numericas) > 0 else todas_columnas
                eje_y = st.selectbox("Eje Y (Vertical):", opciones_y, index=min(1, len(opciones_y)-1))

            # Selector opcional para colorear o agrupar datos (Variables categóricas)
            opciones_color = ["Ninguno"] + columnas_categoricas
            color_by = st.selectbox("Agrupar/Colorear por (Opcional):", opciones_color, index=0)
            color_param = None if color_by == "Ninguno" else color_by

            # Control de rendimiento para evitar congelamientos si el archivo tiene millones de filas
            df_render = df
            if len(df) > 5000:
                st.info("💡 El archivo es grande. Optimizando el gráfico mostrando una muestra aleatoria de 5,000 registros para mantener la fluidez.")
                df_render = df.sample(n=5000, random_state=42)

            # 4. Construcción del gráfico basado en la selección con AGRUPACIÓN AUTOMÁTICA
            fig = None
            
            # Verificación de categorías únicas en el Eje X para evitar colapsos visuales
            valores_unicos_x = df_render[eje_x].nunique()

            if tipo_grafico == "Barras":
                # Si el eje X tiene demasiados valores únicos (como Order_ID), agrupamos para proteger el navegador
                if valores_unicos_x > 30:
                    st.warning(f"⚠️ '{eje_x}' tiene demasiados valores únicos ({valores_unicos_x}). Agrupando automáticamente los datos para mostrar los 20 valores más altos y evitar que la página se congele.")
                    
                    # Agrupamos por el Eje X, sumamos la variable Y y nos quedamos con el Top 20
                    df_agrupado = df_render.groupby(eje_x)[eje_y].sum().reset_index()
                    df_agrupado = df_agrupado.sort_values(by=eje_y, ascending=False).head(20)
                    
                    fig = px.bar(
                        df_agrupado, 
                        x=eje_x, 
                        y=eje_y, 
                        title=f"Top 20 de {eje_y} por {eje_x} (Datos Agrupados)"
                    )
                else:
                    fig = px.bar(df_render, x=eje_x, y=eje_y, color=color_param, title=f"Gráfico de Barras: {eje_y} por {eje_x}")

            elif tipo_grafico == "Líneas":
                # Para gráficos de líneas con IDs, es mejor ordenar por el eje X para que la línea sea fluida y no un laberinto
                df_ordenado = df_render.sort_values(by=eje_x)
                fig = px.line(df_ordenado, x=eje_x, y=eje_y, color=color_param, title=f"Gráfico de Líneas: {eje_y} vs {eje_x}")

            elif tipo_grafico == "Dispersión (Scatter)":
                # El Scatter es ideal para manejar miles de puntos individuales sin congelarse porque no dibuja rectángulos pesados
                fig = px.scatter(df_render, x=eje_x, y=eje_y, color=color_param, title=f"Análisis de Dispersión: {eje_y} vs {eje_x}")

            elif tipo_grafico == "Histograma":
                fig = px.histogram(df_render, x=eje_x, color=color_param, title=f"Distribución (Histograma) de: {eje_x}")

            # Desplegar el gráfico de forma segura si se generó correctamente
            if fig:
                fig.update_layout(
                    template="plotly_white",
                    margin=dict(l=40, r=40, t=50, b=40),
                    hovermode="closest"
                )
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
