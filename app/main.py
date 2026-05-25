from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from . import db
from .models import Producto, Transaccion

main_bp = Blueprint('main', __name__)

# Decorador para solo Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol != 'admin':
            flash('⛔ No tienes permiso. Solo Administrador puede realizar esta acción.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ====================== DASHBOARD ======================
@main_bp.route('/dashboard')
@login_required
def dashboard():
    productos_bajos = Producto.query.filter(Producto.stock_actual < Producto.stock_minimo).count()
    productos_bajos_list = Producto.query.filter(Producto.stock_actual < Producto.stock_minimo).all()
    total_productos = Producto.query.count()
    return render_template('dashboard.html', 
                         productos_bajos=productos_bajos,
                         productos_bajos_list=productos_bajos_list,
                         total_productos=total_productos)

# ====================== GESTIÓN DE PRODUCTOS (SOLO ADMIN) ======================
@main_bp.route('/productos', methods=['GET', 'POST'])
@login_required
@admin_required
def productos():
    if request.method == 'POST':
        nombre = request.form.get('nombre').strip()
        if Producto.query.filter(Producto.nombre.ilike(nombre)).first():
            flash('Producto ya existe', 'danger')
        else:
            nuevo = Producto(
                nombre=nombre,
                unidad=request.form.get('unidad'),
                stock_actual=float(request.form.get('stock_inicial', 0)),
                stock_minimo=float(request.form.get('stock_minimo', 5))
            )
            db.session.add(nuevo)
            db.session.commit()
            flash(f'Producto "{nombre}" agregado correctamente', 'success')
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@main_bp.route('/productos/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    producto.stock_minimo = float(request.form.get('stock_minimo'))
    db.session.commit()
    flash('Stock mínimo actualizado', 'success')
    return redirect(url_for('main.productos'))

@main_bp.route('/productos/eliminar/<int:id>')
@login_required
@admin_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    nombre = producto.nombre
    db.session.delete(producto)
    db.session.commit()
    flash(f'Producto "{nombre}" eliminado correctamente', 'danger')
    return redirect(url_for('main.productos'))

# ====================== ENTRADA Y CONSUMO (TODOS) ======================
@main_bp.route('/registrar_entrada', methods=['GET', 'POST'])
@login_required
def registrar_entrada():
    # ... (mantengo la lógica anterior)
    productos = Producto.query.all()
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        cantidad = float(request.form.get('cantidad', 0))
        stock_minimo = float(request.form.get('stock_minimo', 5))
        
        producto = Producto.query.filter(Producto.nombre.ilike(nombre)).first()
        
        if producto:
            producto.stock_actual += cantidad
            if stock_minimo != producto.stock_minimo:
                producto.stock_minimo = stock_minimo
            flash(f'Se agregaron {cantidad} {producto.unidad} a {producto.nombre}', 'success')
        else:
            unidad = request.form.get('unidad')
            if nombre and unidad and cantidad > 0:
                producto = Producto(nombre=nombre, unidad=unidad, stock_minimo=stock_minimo, stock_actual=cantidad)
                db.session.add(producto)
                flash(f'Nuevo producto "{nombre}" creado', 'success')
            else:
                flash('Datos incompletos', 'danger')
                return redirect(url_for('main.registrar_entrada'))
        
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    
    return render_template('registrar_entrada.html', productos=productos)

@main_bp.route('/registrar_consumo', methods=['GET', 'POST'])
@login_required
def registrar_consumo():
    productos = Producto.query.all()
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        cantidad = float(request.form.get('cantidad'))
        observacion = request.form.get('observacion')
        
        producto = Producto.query.get(producto_id)
        if producto and cantidad > 0:
            if producto.stock_actual < cantidad:
                flash(f'❌ No hay suficiente stock. Disponible: {producto.stock_actual} {producto.unidad}', 'danger')
            else:
                transaccion = Transaccion(
                    producto_id=producto.id,
                    tipo='SALIDA',
                    cantidad=cantidad,
                    observacion=observacion or 'Consumo',
                    usuario_id=current_user.id
                )
                db.session.add(transaccion)
                producto.stock_actual -= cantidad
                db.session.commit()
                flash(f'✅ Consumo registrado: {cantidad} {producto.unidad} de {producto.nombre}', 'success')
                return redirect(url_for('main.dashboard'))
    return render_template('registrar_consumo.html', productos=productos)
