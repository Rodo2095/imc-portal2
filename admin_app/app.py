from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta-admin'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/imc_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Credenciales de administrador (puedes mover esto a variables de entorno)
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('dashboard'))
        return "Credenciales inválidas", 401
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))

    resultado = []
    columnas = []
    error = None

    if request.method == 'POST':
        query = request.form['query'].strip()

        # Seguridad básica: solo permitir SELECT
        if not query.lower().startswith('select'):
            error = "Solo se permiten consultas SELECT"
        else:
            try:
                conn = psycopg2.connect(
                    dbname="imc_db",
                    user="admin",
                    password="admin",
                    host="db",
                    port="5432"
                )
                cur = conn.cursor()
                cur.execute(query)
                columnas = [desc[0] for desc in cur.description]
                resultado = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                error = str(e)

    return render_template('dashboard.html', columnas=columnas, resultado=resultado, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)