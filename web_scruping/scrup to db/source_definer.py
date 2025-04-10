from dataclasses import dataclass
from enum import Enum
from dataclasses import replace

class ScrapingPlatform(Enum):
    AMAZON = "amazon"
    EBAY = "ebay"

class ScrapingBaseUrl(Enum):
    AMAZON = "https://www.amazon.pl"
    EBAY = "https://www.ebay.pl"
    def __str__(self):
        return self.value

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0', 'Accept-Language': 'en-US, en;q=0.5'})

@dataclass
class ScrapingConfig:
    base_url: ScrapingBaseUrl
    search_url: str
    link_selector: str
    headers: dict
    title_selector: dict
    price_selector: dict
    ratings_selector: dict
    reviews_selector: dict
    scruping_platform: ScrapingPlatform

BASIC_AMAZON_CFG = ScrapingConfig(
    base_url=ScrapingBaseUrl.AMAZON,
    search_url="",
    link_selector="a-link-normal s-line-clamp-4 s-link-style a-text-normal",
    headers=HEADERS,
    title_selector={"id": "productTitle"},
    price_selector={"class": "aok-offscreen"},
    ratings_selector={"class": "a-icon-alt"},
    reviews_selector={"id": "acrCustomerReviewText"},
    scruping_platform=ScrapingPlatform.AMAZON
)

MOBILE_PHONE_AMAZON_CFG = replace(
    BASIC_AMAZON_CFG,
    search_url="https://www.amazon.pl/s?k=telefon+kom%C3%B3rkowy&crid=1NTVWV8AXYQ7R&sprefix=telefon+komurkowy%2Caps%2C156&ref=nb_sb_ss_ts-doa-p_1_17"
)

TELEWIZOR_SAMSUNG_AMAZON_CFG = replace(
    BASIC_AMAZON_CFG,
    search_url="https://www.amazon.pl/s?k=telewozor+samsung&__mk_pl_PL=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=MTNW7KUO0XL6&sprefix=telewozor+samsung%2Caps%2C114&ref=nb_sb_noss"
)
