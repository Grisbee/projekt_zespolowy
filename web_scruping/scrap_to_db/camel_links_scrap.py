import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def scrape_keepa_links(search_term, max_links=5):
    logger.info(f"Rozpoczynam scrapowanie linków dla hasła: {search_term}")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        logger.info("Webdriver został zainicjalizowany pomyślnie")
    except Exception as e:
        logger.error(f"Błąd przy inicjalizacji WebDrivera: {e}")
        return []

    try:
        url = f"https://keepa.com/#!search/1-{search_term}"
        logger.info(f"Otwieranie URL: {url}")
        driver.get(url)

        logger.info("Czekam na załadowanie strony (15 sekund)")
        time.sleep(15)

        driver.save_screenshot("keepa_loaded.png")
        logger.info("Zapisano zrzut ekranu")

        logger.info("Szukam linków produktów...")

        selectors = [
            "a[href^='#!product']",
            ".ag-cell a",
            ".ag-cell-value a",
            "div[comp-id] a",
            "div[col-id='title'] a",
        ]

        raw_product_links = []

        for selector in selectors:
            try:
                logger.info(f"Próbuję selektor: {selector}")
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )

                if elements:
                    logger.info(f"Znaleziono {len(elements)} elementów z selektorem {selector}")

                    for element in elements:
                        href = element.get_attribute("href")
                        text = element.text

                        internal_path = element.get_attribute("href")

                        raw_product_links.append({
                            "internal_path": internal_path,
                            "text": text
                        })

                    if raw_product_links:
                        break
            except Exception as e:
                logger.warning(f"Nie udało się znaleźć elementów z selektorem {selector}: {e}")

        if not raw_product_links:
            logger.info("Nie znaleziono linków z typowymi selektorami. Próbuję znaleźć wszystkie linki na stronie...")

            try:
                all_links = driver.find_elements(By.TAG_NAME, "a")
                logger.info(f"Znaleziono {len(all_links)} linków ogółem")

                product_links_elements = [link for link in all_links if
                                          "#!product" in (link.get_attribute("href") or "")]
                logger.info(f"Z tego {len(product_links_elements)} to linki produktów")

                for element in product_links_elements:
                    href = element.get_attribute("href")
                    text = element.text

                    raw_product_links.append({
                        "internal_path": href,
                        "text": text
                    })
            except Exception as e:
                logger.error(f"Błąd przy wyszukiwaniu wszystkich linków: {e}")

        with open("keepa_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("Zapisano źródło strony do analizy")

        driver.quit()
        logger.info("Przeglądarka zamknięta")

        result_links = []

        start_idx = 1
        end_idx = min(6, len(raw_product_links))

        if len(raw_product_links) > 1:
            for i in range(start_idx, end_idx):
                link = raw_product_links[i]

                product_code = None
                if link["internal_path"]:
                    match = re.search(r'/1-([A-Z0-9]+)(?:$|[^A-Z0-9])', link["internal_path"])
                    if match:
                        product_code = match.group(1)

                if product_code:
                    result_links.append({
                        "product_name": link["text"][:50],
                        "link_keepa": f"https://keepa.com/#!product/1-{product_code}",
                        "link_amazon": f"https://www.amazon.com/dp/{product_code}?psc=1",
                        "link_chart": f"https://graph.keepa.com/pricehistory.png?asin={product_code}&domain=com"
                    })

                    logger.info(f"Dodano produkt {product_code}: {link['text'][:30]}...")

        return result_links

    except Exception as e:
        logger.error(f"Wystąpił nieoczekiwany błąd: {e}")
        try:
            driver.quit()
        except:
            pass
        return []


if __name__ == "__main__":
    try:
        links = scrape_keepa_links("iphone x", max_links=10)

        if links:
            df = pd.DataFrame(links)
            df.to_csv("iphone_x_keepa_links.csv", index=False)
            print(f"Zapisano {len(links)} linków do pliku CSV")

            print("\nZnalezione linki:")
            import json

            print(json.dumps(links, indent=2))
        else:
            print("Nie udało się pobrać żadnych linków")
    except Exception as e:
        print(f"Błąd w głównej funkcji: {e}")