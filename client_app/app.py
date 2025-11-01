from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import Swagger
from datetime import datetime
from shared.config import SQLALCHEMY_DATABASE_URI
from shared.models import db, UsuarioCliente, IMCHistorial

app = Flask(__name__)
app.secret_key = 'clave-secreta-session'  # para sesiones

# Configuración base
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SWAGGER'] = {
    'title': 'IMC API',
    'uiversion': 3,
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT token con formato: Bearer <token>'
        }
    }
}

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
swagger = Swagger(app)

@app.route('/')
def home():
    return redirect(url_for('login_web'))

@app.route('/register', methods=['GET', 'POST'])
def register_web():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if UsuarioCliente.query.filter_by(username=username).first():
            return "Usuario ya existe", 409

        cliente = UsuarioCliente(username=username, email=email, password_hash=password)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('login_web'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_web():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cliente = UsuarioCliente.query.filter_by(username=username).first()

        if not cliente or cliente.password_hash != password:
            return "Credenciales inválidas", 401

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_web'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/calcular-imc', methods=['GET', 'POST'])
def calcular_imc_web():
    if 'username' not in session:
        return redirect(url_for('login_web'))

    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = round(peso / (altura ** 2), 2)

        if imc < 18.5:
            clasificacion = 'Bajo peso'
        elif imc < 25:
            clasificacion = 'Normal'
        elif imc < 30:
            clasificacion = 'Sobrepeso'
        else:
            clasificacion = 'Obesidad'

        cliente = UsuarioCliente.query.filter_by(username=session['username']).first()
        historial = IMCHistorial(
            cliente_id=cliente.id,
            peso=peso,
            altura=altura,
            imc=imc,
            clasificacion=clasificacion,
            fecha=datetime.utcnow()
        )
        db.session.add(historial)
        db.session.commit()

        return render_template('imc.html', imc=imc, clasificacion=clasificacion)

    return render_template('imc.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover_web():
    if request.method == 'POST':
        email = request.form['email']
        cliente = UsuarioCliente.query.filter_by(email=email).first()

        if not cliente:
            return "Usuario no encontrado", 404

        return f"Tu contraseña es: {cliente.password_hash}"

    return render_template('recover.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_web'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)