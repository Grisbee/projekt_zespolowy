from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


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

if __name__ == "__main__":
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = "https://www.amazon.pl/s?k=hulajnoga+elektryczna&crid=100KGTELDEQ4M&sprefix=hulajnoga%2Caps%2C105&ref=nb_sb_ss_ts-doa-p_1_9"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    links = soup.find_all('a', attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})

    link_list = []
    for link in links:
        link_list.append(link.get('href'))

    d = { 'title':[], 'price':[], 'rating': [], 'reviews':[] }
    for link in link_list:
        new_webpage = requests.get("https://www.amazon.pl" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))

amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'] = amazon_df['title'].replace('', np.nan)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)