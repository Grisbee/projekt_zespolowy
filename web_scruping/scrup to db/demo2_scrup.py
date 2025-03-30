from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re


def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})

        title_value = title.text

        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_price(soup):
    try:
        price = soup.find('span', attrs={'class': 'aok-offscreen'}).text.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

def get_all_data():
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = "https://www.amazon.pl/s?k=hulajnoga+elektryczna&crid=100KGTELDEQ4M&sprefix=hulajnoga%2Caps%2C105&ref=nb_sb_ss_ts-doa-p_1_9"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})

    link_list = []
    for link in links:
        link_list.append(link.get('href'))

    d = { 'title':[], 'price':[], 'rating': [], 'reviews':[], 'currency':[], 'url':[], 'product_src': [] }
    for link in link_list:
        request_link = "https://www.amazon.pl" + link
        new_webpage = requests.get(request_link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        title = get_title(new_soup)
        price = get_price(new_soup)
        rating_str = get_rating(new_soup)
        reviews_str = get_review_count(new_soup)

        price_match = re.match(r'([\d\s,]+)\s?(\D+)', price.replace('\xa0', ' ').replace('&nbsp;', ' ').strip())
        if price_match:
            amount_str = price_match.group(1).replace(" ", "").replace(",", ".")
            currency = price_match.group(2).split()[0][:3]  # tylko pierwsze słowo do 3 znaków

            try:
                amount = float(amount_str)
            except ValueError:
                continue
        else:
            continue

        rating_match = re.match(r'(\d,\d)', rating_str)
        rating = rating_match.group(1).replace(",", ".") if rating_match else None

        reviews_match = re.search(r'\d+', reviews_str)
        number_of_reviews = int(reviews_match.group()) if reviews_match else None

        d['title'].append(title)
        d['price'].append(float(amount) if amount else None)
        d['currency'].append(currency)
        d['rating'].append(float(rating) if rating else None)
        d['reviews'].append(number_of_reviews)
        d['url'].append(request_link)
        d['product_src'].append('amazon')
    return d;



# amazon_df = pd.DataFrame.from_dict(d)
# amazon_df['title'] = amazon_df['title'].replace('', np.nan)
# amazon_df = amazon_df.dropna(subset=['title'])
# amazon_df.to_csv("amazon_data.csv", header=True, index=False)