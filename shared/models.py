from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsuarioCliente(db.Model):
    __tablename__ = 'usuario_cliente'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class UsuarioEspecialista(db.Model):
    __tablename__ = 'usuario_especialista'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class IMCHistorial(db.Model):
    __tablename__ = 'imc_historial'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario_cliente.id'), nullable=False)
    altura = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
