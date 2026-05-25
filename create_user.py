from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    # Crear usuario bodeguero
    if not Usuario.query.filter_by(username='bodega1').first():
        bodega = Usuario(
            username='bodega1',
            password='123456',      # Temporal (en producción usaríamos hash)
            nombre='Encargado de Bodega',
            rol='bodeguero'
        )
        db.session.add(bodega)
        db.session.commit()
        print("✅ Usuario 'bodega1' creado exitosamente!")
        print("   Usuario: bodega1")
        print("   Contraseña: 123456")
        print("   Rol: bodeguero")
    else:
        print("⚠️ El usuario bodega1 ya existe")
