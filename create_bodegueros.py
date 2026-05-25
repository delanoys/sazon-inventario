from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crear bodega1
    if not Usuario.query.filter_by(username='bodega1').first():
        bodega1 = Usuario(
            username='bodega1',
            password='123456',
            nombre='Bodeguero 1',
            rol='bodeguero'
        )
        db.session.add(bodega1)
        print("✅ Usuario 'bodega1' creado")
    else:
        print("ℹ️  bodega1 ya existe")

    # Crear bodega2
    if not Usuario.query.filter_by(username='bodega2').first():
        bodega2 = Usuario(
            username='bodega2',
            password='123456',
            nombre='Bodeguero 2',
            rol='bodeguero'
        )
        db.session.add(bodega2)
        print("✅ Usuario 'bodega2' creado")
    else:
        print("ℹ️  bodega2 ya existe")

    db.session.commit()
    print("\n🎉 Usuarios creados exitosamente!")
    print("   bodega1 → usuario: bodega1 | pass: 123456")
    print("   bodega2 → usuario: bodega2 | pass: 123456")
