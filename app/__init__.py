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

def _seed_users():
    """Crea usuarios iniciales solo si no existen"""
    from .models import Usuario
    
    # Admin
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('123456'),
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)
        print("✅ Usuario 'admin' creado")

    # Bodega1
    if not Usuario.query.filter_by(username='bodega1').first():
        bodega1 = Usuario(
            username='bodega1',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 1',
            rol='bodeguero'
        )
        db.session.add(bodega1)
        print("✅ Usuario 'bodega1' creado")

    # Bodega2
    if not Usuario.query.filter_by(username='bodega2').first():
        bodega2 = Usuario(
            username='bodega2',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 2',
            rol='bodeguero'
        )
        db.session.add(bodega2)
        print("✅ Usuario 'bodega2' creado")

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sazon_del_boulevard_2026')

    # Base de datos
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

    # Inicialización
    with app.app_context():
        db.create_all()
        _seed_users()          # ← Crea usuarios solo si no existen

    return app
