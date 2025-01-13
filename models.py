from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Maestro de cuentas contables
class Cuenta(db.Model):
    __tablename__ = 'cuentas'  # Nombre explícito de la tabla
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
    numero_cuenta = db.Column(db.String(50), nullable=False)
    nombre_cuenta = db.Column(db.String(100), nullable=False)
    tipo_cuenta = db.Column(db.String(50), nullable=False)

# Contacto
class Contacto(db.Model):
    __tablename__ = 'contactos'  # Nombre explícito de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    tipo_documento = db.Column(db.String(20), nullable=False)
    numero_documento = db.Column(db.String(50), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    numero_celular = db.Column(db.String(15), nullable=False)
    numero_fijo = db.Column(db.String(15), nullable=True)
    tipo_contacto = db.Column(db.String(50), nullable=False)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)  # Referencia a la tabla `cuentas`
    valor_descuento = db.Column(db.Integer, nullable=False)

    # Relación con la cuenta contable
    cuenta = db.relationship('Cuenta', backref='contactos', lazy=True)
