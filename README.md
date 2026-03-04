# Estimación de Costos – Proyecto de Construcción (36 Meses)

Este proyecto estima el costo futuro de dos equipos esenciales para un proyecto de construcción con horizonte de 36 meses.

La estimación se basa en:

- Modelamiento histórico de precios de materias primas (X, Y y Z)
- Modelos ARIMA en niveles
- Simulación estructural Monte Carlo para análisis de riesgo
- Agregación de costos según composición de cada equipo
- Visualización interactiva con Streamlit

---

## 📌 Contexto del Negocio

Una empresa del sector constructor se encuentra en fase de planificación de un proyecto con duración de 36 meses.

El costo de dos equipos depende directamente del comportamiento histórico de tres materias primas.

Composición de los equipos:

- **Equipo 1:** 20% Materia Prima X + 80% Materia Prima Y  
- **Equipo 2:** 33.3% X + 33.3% Y + 33.3% Z  

El objetivo del análisis es:

- Estimar el precio esperado de los equipos al final del horizonte
- Cuantificar la incertidumbre asociada
- Apoyar la planificación financiera
- Facilitar decisiones de negociación y compra

---

## 🧠 Metodología

### 1️⃣ Preparación de Datos

- Conversión a frecuencia diaria hábil
- Alineación temporal entre materias primas
- Forward fill en días sin registro
- Validación de estacionariedad mediante prueba ADF

Se evaluaron dos enfoques:

- Modelado con log-retornos
- Modelado en niveles (I(1))

Se seleccionó ARIMA en niveles por mejor interpretación económica y coherencia en proyección de precios.

---

### 2️⃣ Selección de Modelos

Para cada materia prima:

- Búsqueda de hiperparámetros mediante AIC
- Validación con rolling cross-validation
- Evaluación con métricas:
  - MAE
  - RMSE
  - MAPE

Se seleccionaron los modelos con mejor desempeño predictivo.

---

### 3️⃣ Horizonte de Proyección

- Inicio del proyecto: 4 de abril de 2024
- Duración: 36 meses
- Frecuencia: días hábiles

Cada materia prima se proyecta individualmente y luego se combinan según la estructura de cada equipo.

---

### 4️⃣ Simulación Monte Carlo

Para estimar el riesgo:

- Se generaron múltiples trayectorias futuras
- Se construyó la distribución de precios finales
- Se extrajeron percentiles:
  - P5
  - P50 (mediana)
  - P95

Esto permite estimar el costo esperado y el rango probable de variación.

---

## 📊 Resultados Entregados

Para cada equipo se presenta:

- Precio actual
- Precio esperado en el mes 36
- Variación porcentual proyectada
- Intervalo de confianza del 90%
- Análisis comparativo de riesgo

El análisis evidencia que:

- La incertidumbre aumenta conforme se extiende el horizonte.
- El Equipo 2 presenta menor riesgo relativo debido a diversificación.
- El riesgo acumulado en 36 meses es significativo y debe ser gestionado.

---

## 📈 Dashboard Interactivo

Se desarrolló una aplicación en Streamlit que permite:

- Visualizar histórico vs pronóstico
- Analizar evolución esperada
- Observar bandas de incertidumbre
- Comparar escenarios entre equipos

Ejecutar localmente:

```bash
streamlit run app.py