from .scrapers.jamar_scraper_bs import JamarScraperBS
# from .scrapers.mercadolibre_scraper import MercadoLibreScraper # Comentado para desactivar
# from .scrapers.jamar_scraper import JamarScraper # Comentado para desactivar
from .product_service import save_product

SCRAPERS = [
    JamarScraperBS(),
    # MercadoLibreScraper(),
    # JamarScraper(),
]

def run_scrapers():
    for scraper in SCRAPERS:
        try:
            product_data_list = scraper.scrape()
            for product_data in product_data_list:
                save_product(product_data)
        except Exception as e:
            print(f"Error scraping {scraper.store}: {e}")
