import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

st.title("🤖 Laboratorio de Aprendizaje Automático")
st.write("Configura, entrena y evalúa modelos predictivos en tiempo real utilizando los datos de **datos.csv**.")

# Carga directa y simple sin caché para evitar el bloqueo 'RESULT_CODE_HUNG'
ruta_archivo = "datos.csv"

if not os.path.exists(ruta_archivo):
	st.error("No se pudo encontrar el archivo 'datos.csv' en la raíz del proyecto. Verifica su ubicación.")
else:
	df = pd.read_csv(ruta_archivo)
    
	# Seleccionar solo columnas numéricas
	columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

	if len(columnas_numericas) < 2:
		st.warning("El archivo CSV necesita tener al menos 2 columnas numéricas para realizar la regresión.")
	else:
		# Interfaz de dos columnas
		col_izq, col_der = st.columns([1, 2], gap="large")

		with col_izq:
			st.markdown("### ⚙️ Configuración")
            
			algoritmo = st.selectbox(
				"1. Algoritmo:", 
				["Regresión Lineal", "Árbol de Decisión"]
			)
            
			variable_y = st.selectbox(
				"2. Variable Dependiente (Y):", 
				columnas_numericas,
				index=len(columnas_numericas)-1
			)
            
			opciones_x = [col for col in columnas_numericas if col != variable_y]
            
			variable_x = st.selectbox(
				"3. Variable Independiente (X):", 
				opciones_x,
				index=0
			)
            
			porcentaje_test = st.slider(
				"Porcentaje para Prueba (Test %):", 
				min_value=10, 
				max_value=50, 
				value=20, 
				step=5
			)
            
			test_size_proporcion = porcentaje_test / 100.0
			entrenamiento_size_pct = 100 - porcentaje_test

		# Limpieza rápida de datos para el modelo
		df_limpio = df[[variable_x, variable_y]].dropna()
        
		# Limitamos el procesamiento máximo para asegurar fluidez instantánea en el navegador
		if len(df_limpio) > 1000:
			df_limpio = df_limpio.sample(n=1000, random_state=42)

		X = df_limpio[[variable_x]]
		y = df_limpio[variable_y]

		# Separación de conjuntos
		X_train, X_test, y_train, y_test = train_test_split(
			X, y, 
			test_size=test_size_proporcion, 
			random_state=42
		)

		# Entrenamiento del modelo seleccionado
		if algoritmo == "Regresión Lineal":
			modelo = LinearRegression()
			modelo.fit(X_train, y_train)
			param_nombre = "Coeficiente Slope"
			param_valor = f"{modelo.coef_[0]:.4f}"
		else:
			modelo = DecisionTreeRegressor(max_depth=3, random_state=42)
			modelo.fit(X_train, y_train)
			param_nombre = "Profundidad Nodo"
			param_valor = f"{modelo.get_depth()}"

		# Predicciones y métricas
		y_test_pred = modelo.predict(X_test)
		r2_prueba = r2_score(y_test, y_test_pred)
		mse_prueba = mean_squared_error(y_test, y_test_pred)

		# Mostrar métricas en la columna derecha
		with col_der:
			st.markdown("### 📈 Evaluación y Parámetros")
            
			metric_col1, metric_col2, metric_col3 = st.columns(3)
			with metric_col1:
				st.metric(label="Precisión R²", value=f"{r2_prueba:.4f}")
			with metric_col2:
				st.metric(label="Error (MSE)", value=f"{mse_prueba:.2f}")
			with metric_col3:
				st.metric(label=param_nombre, value=param_valor)

			st.write("---")
            
			# Gráfica optimizada con Plotly (Generando pocos puntos de línea para evitar colapsos)
			fig = go.Figure()

			# Puntos de entrenamiento (Azul)
			fig.add_trace(go.Scatter(
				x=X_train[variable_x], y=y_train, 
				mode='markers', name='Entrenamiento',
				marker=dict(color='#3B82F6', size=5, opacity=0.6)
			))

			# Puntos de prueba (Verde)
			fig.add_trace(go.Scatter(
				x=X_test[variable_x], y=y_test, 
				mode='markers', name='Prueba (Predicciones)',
				marker=dict(color='#10B981', size=7)
			))

			# Línea de tendencia estimada (Rojo - Simplificada a 50 puntos máx para rendimiento)
			x_min, x_max = X[variable_x].min(), X[variable_x].max()
			x_linea = np.linspace(x_min, x_max, 50).reshape(-1, 1)
			y_linea_pred = modelo.predict(pd.DataFrame(x_linea, columns=[variable_x]))

			fig.add_trace(go.Scatter(
				x=x_linea.flatten(), y=y_linea_pred, 
				mode='lines', name='Línea de Ajuste',
				line=dict(color='#EF4444', width=3)
			))

			fig.update_layout(
				xaxis_title=variable_x,
				yaxis_title=variable_y,
				margin=dict(l=10, r=10, t=10, b=10),
				legend=dict(orientation="h", y=1.1),
				plot_bgcolor='rgba(0,0,0,0)',
				paper_bgcolor='rgba(0,0,0,0)'
			)
            
			st.plotly_chart(fig, use_container_width=True)

