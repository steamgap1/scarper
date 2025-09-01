from . import db
from datetime import datetime

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(512), nullable=True)
    products = db.relationship('Product', backref='supplier', lazy=True)

    def __repr__(self):
        return f'<Supplier {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(512), nullable=False, unique=True)
    image_url = db.Column(db.String(512))
    description = db.Column(db.Text)
    store = db.Column(db.String(50)) # 'MercadoLibre', 'Jamar', etc.
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    scraped_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'
