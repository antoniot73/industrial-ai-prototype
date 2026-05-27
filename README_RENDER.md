
# Industrial AI Prototype

Sistema prototipo Industria 4.0 orientado a:

- Simulación SCADA-like
- Historian industrial
- Dashboard web industrial
- Machine Learning supervisado
- Arquitectura cloud con Render.com
- Integración GitHub

---

# Arquitectura General

```text
[ Simulador Industrial ]
            ↓
[ SQLite Historian ]
            ↓
[ FastAPI REST API ]
            ↓
[ Streamlit Dashboard ]
            ↓
[ Machine Learning ]
            ↓
[ Render Cloud Deployment ]
```

---

# Tecnologías utilizadas

- Python
- FastAPI
- Streamlit
- SQLite
- SQLAlchemy
- Plotly
- Pandas
- Scikit-learn
- Render.com
- GitHub

---

# Estructura del proyecto

```text
industrial_ai_prototype/
│
├── app/
├── dashboard/
├── data/
├── .streamlit/
├── requirements.txt
├── Dockerfile
├── render.yaml
├── Procfile
├── start.sh
├── README.md
└── .gitignore
```

---

# Instalación local

## Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecución local

## FastAPI

```bash
uvicorn app.main:app --reload
```

## Streamlit

```bash
streamlit run dashboard/streamlit_app.py
```

---

# URLs locales

## FastAPI

```text
http://127.0.0.1:8000/docs
```

## Streamlit

```text
http://localhost:8501
```

---

# Endpoints FastAPI

- /health
- /current
- /history
- /predict

---

# Deploy en Render.com

El proyecto utiliza DOS servicios independientes:

1. FastAPI API
2. Streamlit Dashboard

---

# Configuración Render — FastAPI

## Tipo de servicio

```text
Web Service
```

## Runtime

```text
Python 3
```

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Swagger

```text
https://industrial-ai-api.onrender.com/docs
```

---

# Configuración Render — Streamlit Dashboard

## Tipo de servicio

```text
Web Service
```

## Runtime

```text
Python 3
```

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
streamlit run dashboard/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

## URL esperada

```text
https://industrial-ai-dashboard.onrender.com
```

---

# Configuración .streamlit/config.toml

```toml
[server]
headless = true
port = 10000
enableCORS = false
```

---

# Machine Learning

Modelo utilizado:

```text
RandomForestRegressor
```

Predicción:

```text
temperatura = f(presion, flujo, vibracion)
```

---

# Problemas comunes

## Render cold start

Render Free duerme servicios tras inactividad.

El primer request puede tardar:

```text
30-60 segundos
```

## SQLite vacío

La base de datos local NO se sube automáticamente.

---

# Arquitectura final

```text
[ Streamlit Dashboard ]
           ↓ requests
[ FastAPI REST API ]
           ↓
[ SQLite Historian ]
           ↓
[ Machine Learning ]
```

---

# Resultado final

```text
Industrial AI Monitoring Platform
```
