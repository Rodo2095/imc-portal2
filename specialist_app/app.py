from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import Swagger
from shared.config import SQLALCHEMY_DATABASE_URI
from shared.models import db, UsuarioCliente, UsuarioEspecialista, IMCHistorial

app = Flask(__name__)
app.secret_key = 'clave-secreta-especialista'

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SWAGGER'] = {
    'title': 'IMC Specialist API',
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

        if UsuarioEspecialista.query.filter_by(username=username).first():
            return "Usuario ya existe", 409

        especialista = UsuarioEspecialista(username=username, email=email, password_hash=password)
        db.session.add(especialista)
        db.session.commit()
        return redirect(url_for('login_web'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_web():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        especialista = UsuarioEspecialista.query.filter_by(username=username).first()

        if not especialista or especialista.password_hash != password:
            return "Credenciales inválidas", 401

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover_web():
    if request.method == 'POST':
        email = request.form['email']
        especialista = UsuarioEspecialista.query.filter_by(email=email).first()

        if not especialista:
            return "Usuario no encontrado", 404

        return f"Tu contraseña es: {especialista.password_hash}"

    return render_template('recover.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_web'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/historial', methods=['GET', 'POST'])
def historial_web():
    if 'username' not in session:
        return redirect(url_for('login_web'))

    resultado = []
    nombre = None

    if request.method == 'POST':
        nombre = request.form['nombre']
        cliente = UsuarioCliente.query.filter_by(username=nombre).first()

        if not cliente:
            return render_template('historial.html', error="Paciente no encontrado")

        historiales = IMCHistorial.query.filter_by(cliente_id=cliente.id).all()

        for h in historiales:
            resultado.append({
                'peso': h.peso,
                'altura': h.altura,
                'imc': h.imc,
                'clasificacion': h.clasificacion,
                'fecha': h.fecha.strftime('%Y-%m-%d %H:%M:%S')
            })

    return render_template('historial.html', nombre=nombre, historial=resultado)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_web'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)