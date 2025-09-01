from .base_scraper import BaseScraper

class JamarScraper(BaseScraper):
    def __init__(self):
        super().__init__('Jamar', 'https://www.jamar.com.co')

    def scrape(self):
        # Lógica de scraping para Jamar
        print(f"Scraping {self.store}...")
        # Ejemplo: Devolver datos dummy
        return [
            {
                'name': 'Producto Jamar 1',
                'price': 250.00,
                'url': f'{self.base_url}/producto1',
                'store': self.store
            }
        ]
