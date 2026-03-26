import requests
from bs4 import BeautifulSoup
import json


def scrape_falabella(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept-Language": "es-CL,es;q=0.9",
            "Accept": "text/html,application/xhtml+xml",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("ERROR STATUS:", response.status_code)
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔥 BUSCAR JSON INTERNO (ESTO ES LO IMPORTANTE)
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)

                # A veces viene como lista
                if isinstance(data, list):
                    for item in data:
                        result = extract_product_data(item)
                        if result:
                            return result
                else:
                    result = extract_product_data(data)
                    if result:
                        return result

            except Exception:
                continue

        print("No se encontró JSON válido")
        return None

    except Exception as e:
        print("ERROR SCRAPER:", e)
        return None


def extract_product_data(data: dict):
    """
    Busca estructura tipo schema.org Product
    """

    if data.get("@type") == "Product":

        name = data.get("name")

        # 🔥 PRECIO
        offers = data.get("offers", {})
        price = offers.get("price")

        # 🔥 IMAGEN
        image = data.get("image")

        if price:
            try:
                price = float(price)
            except:
                price = None

        print("NAME:", name)
        print("PRICE:", price)

        return {
            "name": name,
            "price": price,
            "image_url": image,
            "store": "Falabella"
        }

    return None