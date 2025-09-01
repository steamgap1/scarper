from .base_scraper import BaseScraper
from urllib.parse import urljoin

class JamarScraperBS(BaseScraper):
    def __init__(self):
        super().__init__('Jamar', 'https://www.jamar.com')

    def scrape(self):
        print(f"Iniciando scraping en {self.store} con BeautifulSoup...")
        url = f"{self.base_url}/collections/sale"
        
        try:
            soup = self._get_soup(url) # Usamos el método _get_soup que usa requests
        except Exception as e:
            print(f"Error al obtener la página de Jamar: {e}")
            return []

        products = []
        # Selectores basados en una suposición de la estructura HTML común de e-commerce
        # Estos selectores pueden necesitar ajuste si la estructura real es diferente
        items = soup.select('div[data-gtm-product-id]')

        if not items:
            print("No se encontraron productos con el selector 'div[data-gtm-product-id]'. La estructura de la página puede ser diferente.")
            return []

        for item in items:
            try:
                name = item.get('data-gtm-product-name', "Nombre no disponible")
                
                price_text = item.get('data-gtm-product-final-price', "0.0")
                try:
                    price = float(price_text)
                except ValueError:
                    price = 0.0 # Default value if conversion fails

                relative_url = item.get('data-gtm-product-url')
                product_url = urljoin(self.base_url, relative_url) if relative_url else None

                image_url = item.get('data-gtm-product-image')

                products.append({
                    'name': name,
                    'price': price,
                    'url': product_url,
                    'image_url': image_url,
                    'store': self.store,
                    'supplier_name': self.store
                })
            except Exception as e:
                print(f"Error procesando un item en JamarScraperBS: {e}. Saltando al siguiente.")
        
        print(f"Scraping de Jamar finalizado. Se extrajeron {len(products)} productos.")
        return products
