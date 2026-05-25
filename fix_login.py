from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = create_app()

with app.app_context():
    print("🔄 Corrigiendo usuarios...")

    # Eliminar usuarios existentes para recrearlos limpios
    Usuario.query.delete()
    db.session.commit()

    # Crear usuarios con hash correcto
    admin = Usuario(
        username='admin',
        password=generate_password_hash('123456'),
        nombre='Administrador',
        rol='admin'
    )
    bodega1 = Usuario(
        username='bodega1',
        password=generate_password_hash('123456'),
        nombre='Bodeguero 1',
        rol='bodeguero'
    )
    bodega2 = Usuario(
        username='bodega2',
        password=generate_password_hash('123456'),
        nombre='Bodeguero 2',
        rol='bodeguero'
    )

    db.session.add_all([admin, bodega1, bodega2])
    db.session.commit()

    print("✅ Usuarios recreados correctamente con hash seguro")
    print("   admin     → 123456")
    print("   bodega1   → 123456")
    print("   bodega2   → 123456")
