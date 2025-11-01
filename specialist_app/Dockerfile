FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install flask flask_sqlalchemy flask_migrate flask_jwt_extended flasgger psycopg2-binary

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
ENV PYTHONPATH=/app

EXPOSE 5001
CMD ["flask", "run"]