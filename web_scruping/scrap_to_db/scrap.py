import logging
import json
from keepa_scraper import scrape_keepa_products
from amazon_scraper import get_amazon_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def scrape_enhanced_products(search_term, max_links=5):
    """
    Główna funkcja łącząca dane z Keepa i Amazon
    """
    logger.info(f"Rozpoczynam rozszerzone scrapowanie dla: {search_term}")

    # 1. Pobierz dane z Keepa
    keepa_products = scrape_keepa_products(search_term, max_links)

    if not keepa_products:
        logger.error("Nie udało się pobrać danych z Keepa")
        return []

    # 2. Wzbogać każdy produkt o dane z Amazon
    enhanced_products = []

    for product in keepa_products:
        logger.info(f"Wzbogacam dane dla produktu: {product['product_name'][:30]}...")

        # Pobierz dodatkowe dane z Amazon
        amazon_data = get_amazon_data(product["link_amazon"])

        # Połącz dane
        enhanced_product = {**product, **amazon_data}
        enhanced_products.append(enhanced_product)

    logger.info(f"Zakończono scrapowanie. Pobrano {len(enhanced_products)} produktów")
    return enhanced_products


def scrap_five_products(name):
    try:
        products = scrape_enhanced_products(name, max_links=5)

        if products:
            print(f"\n=== Znaleziono {len(products)} produktów ===\n")

            for i, product in enumerate(products, 1):
                print(f"--- PRODUKT {i} ---")
                print(json.dumps(product, indent=2, ensure_ascii=False))
                print()
            return products
        else:
            print("Nie udało się pobrać żadnych danych")

    except Exception as e:
        print(f"Błąd w głównej funkcji: {e}")