from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("🔄 Creando usuarios...")

    # Admin
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password=generate_password_hash('123456'),
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)
        print("✅ Admin creado")
    else:
        print("ℹ️ Admin ya existía")

    # Bodega1
    if not Usuario.query.filter_by(username='bodega1').first():
        bodega1 = Usuario(
            username='bodega1',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 1',
            rol='bodeguero'
        )
        db.session.add(bodega1)
        print("✅ Bodega1 creado")
    else:
        print("ℹ️ Bodega1 ya existía")

    # Bodega2
    if not Usuario.query.filter_by(username='bodega2').first():
        bodega2 = Usuario(
            username='bodega2',
            password=generate_password_hash('123456'),
            nombre='Bodeguero 2',
            rol='bodeguero'
        )
        db.session.add(bodega2)
        print("✅ Bodega2 creado")
    else:
        print("ℹ️ Bodega2 ya existía")

    db.session.commit()
    print("\n🎉 ¡Usuarios creados correctamente!")
