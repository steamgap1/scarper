import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time

class BaseScraper:
    def __init__(self, store, base_url):
        self.store = store
        self.base_url = base_url

    def _get_soup(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'lxml')

    def _get_soup_with_selenium(self, url):
        options = uc.ChromeOptions()
        # options.add_argument('--headless') # Desactivamos el modo headless por ahora
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

        driver = uc.Chrome(options=options)
        
        print("Accediendo a la URL con opciones avanzadas...")
        driver.get(url)
        print("Página cargada. Esperando 5 segundos...")
        time.sleep(5)
        
        print("Obteniendo código fuente...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()
        return soup

    def scrape(self):
        raise NotImplementedError
