from flask import Blueprint, render_template, request
from flask_login import login_required
from . import db
from .models import Producto, Transaccion
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reportes')
@login_required
def reportes():
    # Consumo total por producto
    consumo_por_producto = db.session.query(
        Transaccion.producto_id,
        func.sum(Transaccion.cantidad).label('total_consumido')
    ).filter(Transaccion.tipo == 'SALIDA').group_by(Transaccion.producto_id).all()
    
    consumo_dict = {item[0]: item[1] for item in consumo_por_producto}
    
    productos = Producto.query.all()
    productos_bajos = Producto.query.filter(Producto.stock_actual < Producto.stock_minimo).all()
    ultimos_consumos = Transaccion.query.order_by(Transaccion.fecha_hora.desc()).limit(20).all()
    
    return render_template('reportes.html', 
                         productos=productos,
                         productos_bajos=productos_bajos,
                         ultimos_consumos=ultimos_consumos,
                         consumo_dict=consumo_dict)

@reports_bp.route('/reporte_avanzado')
@login_required
def reporte_avanzado():
    productos = Producto.query.all()
    productos_bajos = Producto.query.filter(Producto.stock_actual < Producto.stock_minimo).all()
    ultimos_consumos = Transaccion.query.order_by(Transaccion.fecha_hora.desc()).limit(30).all()
    
    return render_template('reporte_avanzado.html', 
                         productos=productos,
                         productos_bajos=productos_bajos,
                         ultimos_consumos=ultimos_consumos)
