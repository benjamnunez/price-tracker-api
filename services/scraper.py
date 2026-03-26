# services/scraper.py

import requests
from bs4 import BeautifulSoup
from services.scrapers.falabella import scrape_falabella

def safe_get_title(soup):
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Producto sin nombre"

def scrape_product_data(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔴 Versión genérica (fallback)
        title = safe_get_title(soup)

        # ⚠️ Precio genérico (no siempre funciona)
        price = extract_price_generic(soup)

        return {
            "name": title.strip(),
            "price": price,
            "image_url": None,
            "store": "hola"
        }

    except Exception as e:
        print("Error scraping:", e)
        return None
    
def detect_store(url: str):
    if "falabella" in url:
        return "Falabella"
    elif "mercadolibre" in url:
        return "MercadoLibre"
    elif "ripley" in url:
        return "Ripley"
    elif "paris" in url:
        return "Paris"
    elif "aliexpress" in url:
        return "AliExpress"
    elif "buscalibre" in url:
        return "BuscaLibre"
    elif "pcfactory" in url:
        return "PcFactory"
    return "Unknown"


def extract_price_generic(soup):
    possible_prices = soup.find_all(text=True)

    for text in possible_prices:
        if "$" in text:
            cleaned = text.replace("$", "").replace(".", "").strip()
            if cleaned.isdigit():
                return float(cleaned)

    return None