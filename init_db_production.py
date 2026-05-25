from app import create_app, db
from app.models import Usuario, Producto

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear usuario admin
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
        print("✅ Usuario admin ya existía")
    
    # Crear algunos productos de ejemplo
    if Producto.query.count() == 0:
        productos = [
            Producto(nombre="Arroz", unidad="kg", stock_actual=50, stock_minimo=10),
            Producto(nombre="Pollo", unidad="kg", stock_actual=30, stock_minimo=8),
            Producto(nombre="Papa", unidad="kg", stock_actual=40, stock_minimo=10),
            Producto(nombre="Aceite", unidad="litros", stock_actual=20, stock_minimo=5),
        ]
        db.session.bulk_save_objects(productos)
        print("✅ Productos de ejemplo creados")
    
    db.session.commit()
    print("✅ Base de datos inicializada correctamente")
