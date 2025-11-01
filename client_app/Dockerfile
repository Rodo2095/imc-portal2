FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instala dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
RUN pip install --upgrade pip && \
    pip install flask flask_sqlalchemy flask_migrate flask_jwt_extended flasgger psycopg2-binary

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONPATH=/app

EXPOSE 5000

# Usa flask run para servir la app (mejor para desarrollo)
CMD ["flask", "run"]