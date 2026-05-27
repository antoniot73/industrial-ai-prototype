# Industrial AI Prototype

Prototipo Industria 4.0 usando:

- FastAPI
- SQLite
- Streamlit
- Machine Learning
- Simulación de variables industriales

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

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar API

```bash
uvicorn app.main:app --reload
```

## Abrir Swagger

http://127.0.0.1:8000/docs
