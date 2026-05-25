from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario
    return Usuario.query.get(int(user_id))

def _seed_data():
    """Crea usuarios y productos iniciales solo si no existen"""
    from .models import Usuario, Producto
    
    # === USUARIOS ===
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('123456'),
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)
        print("✅ Admin creado")

    if not Usuario.query.filter_by(username='bodega1').first():
        db.session.add(Usuario(
            username='bodega1',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 1',
            rol='bodeguero'
        ))
        print("✅ Bodega1 creado")

    if not Usuario.query.filter_by(username='bodega2').first():
        db.session.add(Usuario(
            username='bodega2',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 2',
            rol='bodeguero'
        ))
        print("✅ Bodega2 creado")

    # === PRODUCTOS ===
    if Producto.query.count() == 0:
        productos = [
            Producto(nombre="Arroz", unidad="kg", stock_actual=50, stock_minimo=10),
            Producto(nombre="Pollo", unidad="kg", stock_actual=30, stock_minimo=8),
            Producto(nombre="Papa", unidad="kg", stock_actual=40, stock_minimo=10),
            Producto(nombre="Aceite", unidad="litros", stock_actual=20, stock_minimo=5),
            Producto(nombre="Tomate", unidad="kg", stock_actual=25, stock_minimo=5),
            Producto(nombre="Cebolla", unidad="kg", stock_actual=35, stock_minimo=8),
            Producto(nombre="Carne de Res", unidad="kg", stock_actual=25, stock_minimo=5),
            Producto(nombre="Huevos", unidad="unidades", stock_actual=300, stock_minimo=100),
        ]
        db.session.bulk_save_objects(productos)
        print("✅ 8 productos creados exitosamente")
    else:
        print(f"ℹ️ Ya existen {Producto.query.count()} productos")

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sazon_del_boulevard_2026')

    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        print("🟢 Usando PostgreSQL en Render")
    else:
        instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance')
        os.makedirs(instance_path, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "inventario.db")}' 
        print("🟡 Usando SQLite local")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .main import main_bp
    from .reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(reports_bp)

    # Inicialización automática
    with app.app_context():
        db.create_all()
        _seed_data()   # ← Crea usuarios y productos

    return app
