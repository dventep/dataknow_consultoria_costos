import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from io import BytesIO
from PIL import Image

# ---------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------

st.set_page_config(
    page_title="Estimación de Costos - Proyecto 36 Meses",
    layout="wide"
)

# ---------------------------------------------------
# LOGO DESDE URL (CORREGIDO)
# ---------------------------------------------------

try:
    url = "https://dataknow.io/wp-content/uploads/2021/12/juan-david-pulgarin-dataknow.png"
    response = requests.get(url)
    logo = Image.open(BytesIO(response.content))
    st.sidebar.image(logo, use_container_width=True)
except:
    st.sidebar.write("DataKnow")

st.sidebar.markdown("### Proyecto de Estimación de Costos")
st.sidebar.markdown("Horizonte: 36 meses")

# ---------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------

X_full = pd.read_csv("../data/X_full.csv", parse_dates=["Date"])
Y_full = pd.read_csv("../data/Y_full.csv", parse_dates=["Date"])
Z_full = pd.read_csv("../data/Z_full.csv", parse_dates=["Date"])

teams_expected = pd.read_csv("../data/Teams_expected.csv", parse_dates=["Date"])
team_1_percentiles = pd.read_csv("../data/Team_1_percentiles.csv", parse_dates=["Date"])
team_2_percentiles = pd.read_csv("../data/Team_2_percentiles.csv", parse_dates=["Date"])
summary_df = pd.read_csv("../data/Teams_summary_36m.csv")

# ---------------------------------------------------
# PRECIO ACTUAL (último histórico antes del forecast)
# ---------------------------------------------------

precio_actual_equipo1 = teams_expected["Team_1_expected"].iloc[0]
precio_actual_equipo2 = teams_expected["Team_2_expected"].iloc[0]

# Precio esperado al mes 36
equipo1_row = summary_df[summary_df["Equipo"] == "Equipo 1"].iloc[0]
equipo2_row = summary_df[summary_df["Equipo"] == "Equipo 2"].iloc[0]

precio_36_equipo1 = equipo1_row["Media"]
precio_36_equipo2 = equipo2_row["Media"]

variacion_1 = ((precio_36_equipo1 - precio_actual_equipo1) / precio_actual_equipo1) * 100
variacion_2 = ((precio_36_equipo2 - precio_actual_equipo2) / precio_actual_equipo2) * 100

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("Estimación de Costos – Proyecto 36 Meses")

st.markdown("""
Modelo basado en ARIMA en niveles y simulación Monte Carlo estructural.
Se presentan precios esperados y bandas de incertidumbre.
""")

# ---------------------------------------------------
# RESUMEN EJECUTIVO CORREGIDO
# ---------------------------------------------------

st.subheader("Resumen Ejecutivo")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Equipo 1")
    st.metric("Precio Actual", f"{precio_actual_equipo1:,.2f}")
    st.metric("Precio Esperado Mes 36", f"{precio_36_equipo1:,.2f}")
    st.metric("Variación Proyectada (%)", f"{variacion_1:.2f}%")
    st.metric("Intervalo 90% (P5 - P95)",
              f"{equipo1_row['P5']:,.2f}  –  {equipo1_row['P95']:,.2f}")

with col2:
    st.markdown("### Equipo 2")
    st.metric("Precio Actual", f"{precio_actual_equipo2:,.2f}")
    st.metric("Precio Esperado Mes 36", f"{precio_36_equipo2:,.2f}")
    st.metric("Variación Proyectada (%)", f"{variacion_2:.2f}%")
    st.metric("Intervalo 90% (P5 - P95)",
              f"{equipo2_row['P5']:,.2f}  –  {equipo2_row['P95']:,.2f}")

# ---------------------------------------------------
# HISTÓRICO VS PRONÓSTICO
# ---------------------------------------------------

st.subheader("Histórico y Pronóstico")

materia = st.selectbox("Seleccionar Materia Prima", ["X", "Y", "Z"])

if materia == "X":
    df_plot = X_full
elif materia == "Y":
    df_plot = Y_full
else:
    df_plot = Z_full

fig_hist = px.line(
    df_plot,
    x="Date",
    y="Price",
    color="Type",
    color_discrete_map={
        "Historical": "#0B3C5D",
        "Forecast": "#00A878",
        "Aligned": "#F4A261"
    }
)

fig_hist.update_layout(
    yaxis=dict(rangemode="tozero"),
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------------------------
# PROYECCIÓN ESPERADA EQUIPOS
# ---------------------------------------------------

st.subheader("Proyección esperada equipos")

fig_teams = px.line(
    teams_expected,
    x="Date",
    y=["Team_1_expected", "Team_2_expected"],
    color_discrete_sequence=["#0B3C5D", "#00A878"]
)

fig_teams.update_layout(
    yaxis=dict(rangemode="tozero"),
    template="plotly_white"
)

st.plotly_chart(fig_teams, use_container_width=True)

# ---------------------------------------------------
# BANDAS DE INCERTIDUMBRE
# ---------------------------------------------------

st.subheader("Bandas de Incertidumbre (90%)")

equipo_band = st.selectbox("Seleccionar Equipo", ["Equipo 1", "Equipo 2"])

if equipo_band == "Equipo 1":
    band_df = team_1_percentiles
else:
    band_df = team_2_percentiles

fig_band = go.Figure()

fig_band.add_trace(go.Scatter(
    x=band_df["Date"],
    y=band_df["P95"],
    line=dict(width=0),
    showlegend=False
))

fig_band.add_trace(go.Scatter(
    x=band_df["Date"],
    y=band_df["P5"],
    fill='tonexty',
    fillcolor="rgba(0,168,120,0.2)",
    line=dict(width=0),
    name="Intervalo 90%"
))

fig_band.add_trace(go.Scatter(
    x=band_df["Date"],
    y=band_df["P50"],
    line=dict(color="#0B3C5D"),
    name="Mediana"
))

fig_band.update_layout(
    yaxis=dict(rangemode="tozero"),
    template="plotly_white"
)

st.plotly_chart(fig_band, use_container_width=True)

st.markdown("---")
st.markdown("Actualización recomendada: trimestral.")