from app import db
from app.models import Product, Supplier

def save_product(product_data):
    # Extraer datos del proveedor
    supplier_name = product_data.pop('supplier_name', 'Desconocido')
    supplier_url = product_data.pop('supplier_url', None)

    # Buscar o crear el proveedor
    supplier = Supplier.query.filter_by(name=supplier_name).first()
    if not supplier:
        supplier = Supplier(name=supplier_name, url=supplier_url)
        db.session.add(supplier)
        # Hacemos un pre-commit para obtener el ID del proveedor si es nuevo
        db.session.flush()

    # Buscar producto existente por URL
    product = Product.query.filter_by(url=product_data['url']).first()
    
    product_data['supplier_id'] = supplier.id

    if product:
        # Actualizar producto existente
        for key, value in product_data.items():
            setattr(product, key, value)
    else:
        # Crear producto nuevo
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
