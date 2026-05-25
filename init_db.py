from app import create_app, db
from app.models import Usuario, Producto

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear usuario administrador de prueba
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password='123456',
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario 'admin' creado exitosamente!")
        print("   Usuario: admin")
        print("   Contraseña: 123456")
    else:
        print("ℹ️  El usuario admin ya existe")
    
    # Crear algunos productos de ejemplo
    if Producto.query.count() == 0:
        productos_ejemplo = [
            {"nombre": "Arroz", "unidad": "kg", "stock_minimo": 10},
            {"nombre": "Pollo", "unidad": "kg", "stock_minimo": 5},
            {"nombre": "Aceite", "unidad": "litros", "stock_minimo": 2},
            {"nombre": "Papa", "unidad": "kg", "stock_minimo": 8},
            {"nombre": "Tomate", "unidad": "kg", "stock_minimo": 3},
        ]
        
        for p in productos_ejemplo:
            prod = Producto(**p)
            db.session.add(prod)
        
        db.session.commit()
        print("✅ Productos de ejemplo creados!")
