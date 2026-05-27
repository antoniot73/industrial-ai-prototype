import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "https://industrial-ai-api-5ypf.onrender.com"
)

st.set_page_config(
    page_title="Industrial AI Prototype",
    layout="wide"
)

st.title("Industrial AI Prototype Dashboard")

st.sidebar.header("Configuración")

refresh_rate = st.sidebar.slider(
    "Frecuencia actualización (segundos)",
    min_value=5,
    max_value=60,
    value=10
)

try:

    current_response = requests.get(
        f"{API_URL}/current",
        timeout=15
    )

    st.sidebar.write(
        f"API STATUS CURRENT: {current_response.status_code}"
    )

    current_response.raise_for_status()

    current = current_response.json()

    history_response = requests.get(
        f"{API_URL}/history?limit=100",
        timeout=15
    )

    st.sidebar.write(
        f"API STATUS HISTORY: {history_response.status_code}"
    )

    history_response.raise_for_status()

    history = history_response.json()

    df = pd.DataFrame(history)

    if not df.empty:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        df = df.sort_values(
            "timestamp"
        )

except requests.exceptions.RequestException as exc:

    st.error(
        f"Error HTTP conectando con FastAPI: {exc}"
    )

    st.stop()

except ValueError as exc:

    st.error(
        f"Error JSON FastAPI: {exc}"
    )

    st.stop()

except Exception as exc:

    st.error(
        f"Error general dashboard: {exc}"
    )

    st.stop()

st.header("Variables Tiempo Real")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperatura",
    f"{current['temperatura']} °C"
)

col2.metric(
    "Presión",
    f"{current['presion']} PSI"
)

col3.metric(
    "Flujo",
    f"{current['flujo']} L/min"
)

col4.metric(
    "Vibración",
    f"{current['vibracion']} mm/s"
)

st.divider()

st.header("Tendencias Históricas")

variables = [
    "temperatura",
    "presion",
    "flujo",
    "vibracion"
]

selected_var = st.selectbox(
    "Seleccionar variable",
    variables
)

fig = px.line(
    df,
    x="timestamp",
    y=selected_var,
    title=f"Tendencia histórica: {selected_var}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.header("Indicadores Industriales")

g1, g2 = st.columns(2)

with g1:

    fig_temp = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current["temperatura"],
        title={"text": "Temperatura"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    ))

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )

with g2:

    fig_pres = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current["presion"],
        title={"text": "Presión"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    ))

    st.plotly_chart(
        fig_pres,
        use_container_width=True
    )

st.divider()

st.header("Últimos Registros")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

st.caption(
    f"Frecuencia recomendada: {refresh_rate} segundos"
)

st.divider()

st.header("Predicción IA Industrial")

try:

    prediction_response = requests.get(
        f"{API_URL}/predict",
        params={
            "presion": current["presion"],
            "flujo": current["flujo"],
            "vibracion": current["vibracion"]
        },
        timeout=15
    )

    prediction_response.raise_for_status()

    prediction = prediction_response.json()

    if "temperatura_predicha" in prediction:

        ml_col1, ml_col2 = st.columns(2)

        ml_col1.metric(
            "Temperatura Real",
            f"{current['temperatura']} °C"
        )

        ml_col2.metric(
            "Temperatura Predicha IA",
            f"{prediction['temperatura_predicha']} °C"
        )

        st.success(
            f"MAE Modelo IA: {prediction['mae_modelo']}"
        )

        diferencia = abs(
            current["temperatura"] -
            prediction["temperatura_predicha"]
        )

        st.info(
            f"Diferencia Real vs IA: {round(diferencia, 2)} °C"
        )

    else:

        st.warning(
            prediction.get(
                "message",
                "No fue posible generar predicción."
            )
        )

except Exception as exc:

    st.error(
        f"Error módulo IA: {exc}"
    )
