import os
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------
# API URL
# ---------------------------------------------------

API_URL = os.getenv(
    "API_URL",
    "https://industrial-ai-api-5ypf.onrender.com"
)

# ---------------------------------------------------
# STREAMLIT CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Industrial AI Prototype",
    layout="wide"
)

st.title("Industrial AI Prototype Dashboard")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Configuración")

refresh_rate = st.sidebar.slider(
    "Frecuencia actualización (segundos)",
    min_value=5,
    max_value=60,
    value=10
)

# ---------------------------------------------------
# FASTAPI CONNECTION
# ---------------------------------------------------

try:

    # -----------------------------------------------
    # CURRENT ENDPOINT WITH RETRIES
    # -----------------------------------------------

    MAX_RETRIES = 5

    current_response = None

    for attempt in range(MAX_RETRIES):

        try:

            current_response = requests.get(
                f"{API_URL}/current",
                timeout=20
            )

            if current_response.status_code == 200:
                break

        except Exception:
            pass

        st.warning(
            f"Esperando activación API Render... intento {attempt + 1}"
        )

        time.sleep(5)

    if current_response is None:

        st.error(
            "No fue posible conectar con FastAPI."
        )

        st.stop()

    st.sidebar.write(
        f"API STATUS CURRENT: {current_response.status_code}"
    )

    current_response.raise_for_status()

    try:

        current = current_response.json()

    except Exception as exc:

        st.error(
            f"Error parseando JSON API: {exc}"
        )

        st.write(current_response.text)

        st.stop()

    # -----------------------------------------------
    # HISTORY ENDPOINT
    # -----------------------------------------------

    history_response = requests.get(
        f"{API_URL}/history?limit=100",
        timeout=20
    )

    st.sidebar.write(
        f"API STATUS HISTORY: {history_response.status_code}"
    )

    history_response.raise_for_status()

    history = history_response.json()

    # -----------------------------------------------
    # DATAFRAME
    # -----------------------------------------------

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

# ---------------------------------------------------
# REAL-TIME KPIs
# ---------------------------------------------------

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

# ---------------------------------------------------
# HISTORICAL TRENDS
# ---------------------------------------------------

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

# ---------------------------------------------------
# INDUSTRIAL GAUGES
# ---------------------------------------------------

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

# ---------------------------------------------------
# HISTORICAL TABLE
# ---------------------------------------------------

st.header("Últimos Registros")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

st.caption(
    f"Frecuencia recomendada: {refresh_rate} segundos"
)

# ---------------------------------------------------
# MACHINE LEARNING
# ---------------------------------------------------

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
        timeout=20
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
