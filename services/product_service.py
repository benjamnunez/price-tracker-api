from sqlalchemy.orm import Session
from models.product import Product
from models.price_history import PriceHistory
from services.scraper import scrape_product_data


def create_product(db: Session, user_id: int, url: str):

    scraped_data = scrape_product_data(url)

    if not scraped_data:
        raise Exception("No se pudo scrapear el producto")

    if not scraped_data.get("price"):
        raise Exception("No se pudo obtener el precio")

    if not scraped_data.get("name"):
        raise Exception("No se pudo obtener el nombre")

    product = Product(
        user_id=user_id,
        url=url,
        name=scraped_data["name"],
        image_url=scraped_data.get("image_url"),
        store=scraped_data.get("store"),
        current_price=scraped_data["price"]
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    price_history = PriceHistory(
        product_id=product.id,
        price=scraped_data["price"]
    )

    db.add(price_history)
    db.commit()

    return product