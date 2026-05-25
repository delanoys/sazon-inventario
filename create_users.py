from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    # Usuario Admin
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password='123456',
            nombre='Administrador Principal',
            rol='admin'
        )
        db.session.add(admin)
        print("✅ Usuario admin creado")
    else:
        print("ℹ️  admin ya existía")

    # Usuario Bodega1
    if not Usuario.query.filter_by(username='bodega1').first():
        bodega1 = Usuario(
            username='bodega1',
            password='123456',
            nombre='Bodeguero 1',
            rol='bodeguero'
        )
        db.session.add(bodega1)
        print("✅ Usuario bodega1 creado")
    else:
        print("ℹ️  bodega1 ya existía")

    # Usuario Bodega2
    if not Usuario.query.filter_by(username='bodega2').first():
        bodega2 = Usuario(
            username='bodega2',
            password='123456',
            nombre='Bodeguero 2',
            rol='bodeguero'
        )
        db.session.add(bodega2)
        print("✅ Usuario bodega2 creado")
    else:
        print("ℹ️  bodega2 ya existía")

    db.session.commit()
    print("\n🎉 Usuarios creados correctamente!")
