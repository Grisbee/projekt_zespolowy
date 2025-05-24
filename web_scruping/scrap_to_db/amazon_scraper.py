from bs4 import BeautifulSoup
import requests
import re
import logging

logger = logging.getLogger(__name__)

# Headers z source_definer.py - sprawdzone i działające
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
           'Accept-Language': 'en-US, en;q=0.5'}


def get_title(soup, title_selector):
    """Pobiera tytuł produktu z Amazon - z demo2_scrap.py"""
    try:
        title = soup.find("span", attrs=title_selector).get_text().strip()
    except AttributeError:
        title = ""
    return title


def get_price(soup, price_selector):
    """Pobiera cenę produktu z Amazon - z demo2_scrap.py"""
    try:
        price = soup.find('span', attrs=price_selector).text.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(soup, rating_selector):
    """Pobiera ocenę produktu z Amazon - z demo2_scrap.py"""
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs=rating_selector).string.strip()
        except:
            rating = ""
    return rating


def get_review_count(soup, review_selector):
    """Pobiera liczbę recenzji z Amazon - z demo2_scrap.py"""
    try:
        review_count = soup.find("span", attrs=review_selector).string.strip()
    except AttributeError:
        review_count = ""
    return review_count


def get_amazon_data(amazon_url):
    """
    Pobiera dodatkowe dane z Amazon.com używając sprawdzonych selektorów
    """
    logger.info(f"Pobieram dane z Amazon: {amazon_url}")

    try:
        webpage = requests.get(amazon_url, headers=HEADERS)
        logger.info(f"Status code: {webpage.status_code}")

        soup = BeautifulSoup(webpage.content, 'html.parser')

        # Selektory dla Amazon.com
        title_selector = {"id": "productTitle"}
        price_selector = {"class": "aok-offscreen"}
        ratings_selector = {"class": "a-icon-alt"}
        reviews_selector = {"id": "acrCustomerReviewText"}

        # Pobieranie danych używając oryginalnych funkcji z demo2_scrap.py
        title = get_title(soup, title_selector)
        price_str = get_price(soup, price_selector)
        rating_str = get_rating(soup, ratings_selector)
        reviews_str = get_review_count(soup, reviews_selector)

        logger.info(
            f"Raw data - title: '{title[:50]}...', price: '{price_str}', rating: '{rating_str}', reviews: '{reviews_str}'")

        # Inicjalizacja domyślnych wartości
        amazon_data = {
            "amazon_title": title,
            "rating": None,
            "review_count": None,
            "currency": "USD",
            "product_src": "Amazon"
        }

        # Przetwarzanie ceny i waluty (z demo2_scrap.py)
        if price_str:
            price_match = re.match(r'([\d\s,]+)\s?(\D+)', price_str.replace('\xa0', ' ').replace('&nbsp;', ' ').strip())
            if price_match:
                currency = price_match.group(2).split()[0][:3]  # tylko pierwsze słowo do 3 znaków
                amazon_data["currency"] = currency
                logger.info(f"Znaleziona waluta: {currency}")

        # Przetwarzanie ratingu - tylko nowy selektor dla span.a-size-base.a-color-base
        try:
            rating_spans = soup.find_all("span", class_="a-size-base a-color-base")
            for span in rating_spans:
                text = span.get_text().strip()
                rating_match = re.match(r'^(\d\.\d)$', text)
                if rating_match:
                    rating_value = float(rating_match.group(1))
                    if 1.0 <= rating_value <= 5.0:
                        amazon_data["rating"] = rating_value
                        logger.info(f"✓ Rating znaleziony: {rating_value}")
                        break
        except Exception as e:
            logger.warning(f"Błąd przy pobieraniu ratingu: {e}")
            amazon_data["rating"] = None

        # Przetwarzanie liczby recenzji (z demo2_scrap.py)
        if reviews_str:
            reviews_match = re.search(r'\d+', reviews_str)
            if reviews_match:
                number_of_reviews = int(reviews_match.group())
                amazon_data["review_count"] = number_of_reviews
                logger.info(f"Znalezione recenzje: {number_of_reviews}")

        logger.info(
            f"WYNIK: title='{amazon_data['amazon_title'][:50] if amazon_data['amazon_title'] else 'BRAK'}...', rating={amazon_data['rating']}, reviews={amazon_data['review_count']}, currency={amazon_data['currency']}")
        return amazon_data

    except Exception as e:
        logger.error(f"Błąd podczas scrapowania Amazon: {e}")
        return {
            "amazon_title": "",
            "rating": None,
            "review_count": None,
            "currency": "USD",
            "product_src": "Amazon"
        }