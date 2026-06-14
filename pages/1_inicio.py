
import streamlit as st

# Inyección de estilos CSS personalizados para mantener la línea gráfica en la página de inicio
st.markdown("""
	<style>
	/* Título Principal Neón */
	.main-title {
		font-size: 2.8rem;
		color: #00f0ff;
		text-align: center;
		font-weight: 800;
		margin-top: -10px;
		margin-bottom: 5px;
		text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	}
    
	/* Subtítulo del sitio */
	.site-subtitle {
		text-align: center; 
		color: #66fcf1; 
		font-size: 1.15rem; 
		margin-bottom: 30px;
	}
    
	/* Subtítulos de sección */
	.section-subtitle {
		color: #9d00ff;
		font-size: 1.6rem;
		font-weight: 600;
		border-bottom: 2px solid #9d00ff;
		padding-bottom: 5px;
		margin-top: 25px;
		margin-bottom: 15px;
		text-shadow: 0 0 8px rgba(157, 0, 255, 0.4);
	}
    
	/* Contenedor del texto de presentación (Justificado y con la extensión exacta) */
	.bio-text {
		font-size: 1.1rem;
		line-height: 1.7;
		text-align: justify;
		color: #e5e5e5;
		background-color: #1f2833;
		padding: 20px;
		border-radius: 10px;
		border-left: 5px solid #00f0ff;
	}
	</style>
""", unsafe_allow_html=True)

# 1. TÍTULOS DE BIENVENIDA
st.markdown('<h1 class="main-title">PORTAFOLIO DIGITAL DE CIENCIA DE DATOS</h1>', unsafe_allow_html=True)
st.markdown('<p class="site-subtitle">Soluciones Analíticas y Modelado Predictivo en la Industria de Videojuegos</p>', unsafe_allow_html=True)

# 2. CUADRÍCULA PARA FOTOGRAFÍA Y DATOS PERSONALES
col_foto, col_info = st.columns([1, 2], gap="large")

with col_foto:
	# Recuerda colocar tu foto formal en la raíz del proyecto con este nombre exacto o cambiar la ruta
	st.image("foto_perfil.jpg", caption="Rosaura del Carmen García Romero", use_container_width=True)

with col_info:
	st.markdown('<h2 style="color:#00f0ff; margin-top:0; font-size:1.8rem;">Rosaura del Carmen García Romero</h2>', unsafe_allow_html=True)
	st.markdown('<p style="color:#9d00ff; font-weight:bold; font-size:1.1rem; margin-top:-10px;">Estudiante de Ingeniería en Sistemas y Redes Informáticas</p>', unsafe_allow_html=True)
    
	# Breve resumen personal: Exactamente 4 líneas de extensión (Cumple rigurosamente el rango de 3 a 5 líneas)
	st.markdown("""
	<p class="bio-text">
	Soy estudiante de Ingeniería en Sistemas y Redes Informáticas en la Universidad Gerardo Barrios, enfocada en la infraestructura tecnológica y el análisis científico de datos. Con experiencia práctica en el desarrollo de canalizaciones de datos, despliegues optimizados y modelado predictivo, me apasiona transformar variables complejas en decisiones estratégicas de negocio. Este portafolio unifica el procesamiento de datos interactivo con la implementación de modelos de Machine Learning avanzados para mitigar la incertidumbre en el dinámico mercado global de los videojuegos.
	</p>
	""", unsafe_allow_html=True)

st.markdown("---")

# 3. SECCIÓN DEL VIDEO INCRUSTADO (DEMO DATA STORYTELLING)
st.markdown('<h2 class="section-subtitle">📹 Demo de Data Storytelling</h2>', unsafe_allow_html=True)
st.markdown("<p style='margin-bottom:15px; color:#c5c6c7;'>A continuación, se presenta la defensa ejecutiva de la investigación, analizando el comportamiento comercial del dataset histórico y el rendimiento de los modelos predictivos ajustados:</p>", unsafe_allow_html=True)

# Enlace directo a tu video de YouTube integrado
url_video_youtube = "https://youtu.be/IZmtIFM8SCE"
st.video(url_video_youtube)
