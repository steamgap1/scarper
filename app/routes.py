from flask import render_template, current_app, flash, redirect, url_for, request
from .models import Product, Supplier
from .services.scraper_service import run_scrapers

@current_app.route('/')
def index():
    return render_template('index.html')

@current_app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.order_by(Product.scraped_date.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('products.html', products_pagination=products_pagination)

@current_app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@current_app.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@current_app.route('/supplier/<int:supplier_id>')
def supplier_detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier_detail.html', supplier=supplier)

@current_app.route('/scrape')
def scrape():
    flash('Iniciando proceso de scraping. Esto puede tardar unos minutos...', 'info')
    try:
        run_scrapers()
        flash('¡Scraping completado con éxito!', 'success')
    except Exception as e:
        flash(f'Ocurrió un error durante el scraping: {e}', 'danger')
    return redirect(url_for('products'))
