from . import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100))
    rol = db.Column(db.String(20), default='bodeguero')  # admin o bodeguero

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)  # kg, litros, unidades, etc.
    stock_minimo = db.Column(db.Float, default=5.0)
    stock_actual = db.Column(db.Float, default=0.0)

class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)        # 'SALIDA' o 'ENTRADA'
    cantidad = db.Column(db.Float, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    observacion = db.Column(db.Text)

    producto = db.relationship('Producto')
