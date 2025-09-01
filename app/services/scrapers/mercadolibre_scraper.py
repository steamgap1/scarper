from .base_scraper import BaseScraper
import time
from urllib.parse import urlparse, urlunparse

class MercadoLibreScraper(BaseScraper):
    def __init__(self):
        super().__init__('MercadoLibre', 'https://www.mercadolibre.com.co')

    def scrape(self):
        print(f"Iniciando scraping en {self.store}...")
        url = f"{self.base_url}/ofertas#nav-header"
        
        soup = self._get_soup_with_selenium(url)

        if soup.title and "Acceso Denegado" in soup.title.text:
            print("¡BLOQUEO DETECTADO! Mercado Libre nos ha denegado el acceso.")
            with open("mercadolibre_bloqueado.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))
            print("HTML de la página de bloqueo guardado en 'mercadolibre_bloqueado.html' para análisis.")
            return []

        with open("mercadolibre_ofertas.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        print("HTML de la página de ofertas guardado en 'mercadolibre_ofertas.html' para análisis.")

        products = []
        # Selectores actualizados basados en el HTML proporcionado
        items = soup.select('div.andes-card.poly-card.poly-card--grid-card')
        print(f"Se encontraron {len(items)} items con el selector 'div.andes-card.poly-card.poly-card--grid-card'.")

        if not items:
            print("No se encontraron productos con el selector principal. La estructura de la página puede haber cambiado de nuevo.")
            return []

        for item in items[:10]: # Limitamos a 10 productos
            try:
                # URL y Nombre
                link_element = item.select_one('a.poly-component__title')
                raw_product_url = link_element['href'] if link_element else None
                
                # Limpiar la URL: eliminar parámetros de consulta y fragmentos
                if raw_product_url:
                    parsed_url = urlparse(raw_product_url)
                    product_url = urlunparse(parsed_url._replace(query='', fragment=''))
                else:
                    product_url = None

                name = link_element.text.strip() if link_element else "Nombre no disponible"

                # Precio
                price_element = item.select_one('div.poly-price__current span.andes-money-amount__fraction')
                price = float(price_element.text.strip().replace('.', '')) if price_element and price_element.text.strip() else 0.0

                # Imagen
                img_element = item.select_one('img.poly-component__picture')
                image_url = img_element['src'] if img_element and img_element.has_attr('src') else None

                # Proveedor
                supplier_element = item.select_one('span.poly-component__seller')
                supplier_name = supplier_element.text.strip().replace('Por ', '').strip() if supplier_element else "Vendedor Desconocido"

                products.append({
                    'name': name,
                    'price': price,
                    'url': product_url,
                    'image_url': image_url,
                    'store': self.store,
                    'supplier_name': supplier_name
                })
            except Exception as e:
                print(f"Error procesando un item: {e}. Saltando al siguiente.")
        
        print(f"Scraping finalizado. Se extrajeron {len(products)} productos.")
        return products
