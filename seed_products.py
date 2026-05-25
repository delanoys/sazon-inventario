from app import create_app, db
from app.models import Producto

app = create_app()

with app.app_context():
    if Producto.query.count() == 0:
        productos = [
            Producto(nombre="Arroz", unidad="kg", stock_actual=50, stock_minimo=10),
            Producto(nombre="Pollo", unidad="kg", stock_actual=30, stock_minimo=8),
            Producto(nombre="Papa", unidad="kg", stock_actual=40, stock_minimo=10),
            Producto(nombre="Aceite", unidad="litros", stock_actual=20, stock_minimo=5),
            Producto(nombre="Tomate", unidad="kg", stock_actual=25, stock_minimo=5),
            Producto(nombre="Cebolla", unidad="kg", stock_actual=35, stock_minimo=8),
        ]
        db.session.bulk_save_objects(productos)
        db.session.commit()
        print("✅ 6 productos creados exitosamente en PostgreSQL")
    else:
        print(f"ℹ️ Ya existen {Producto.query.count()} productos")
