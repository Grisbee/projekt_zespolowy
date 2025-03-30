from bs4 import BeautifulSoup
import requests
import pandas as pd


# demo scrup hulajnogi z amazon

URL = "https://www.amazon.pl/s?k=hulajnoga+elektryczna&crid=100KGTELDEQ4M&sprefix=hulajnoga%2Caps%2C105&ref=nb_sb_ss_ts-doa-p_1_9"
HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0', 'Accept-Language': 'en-US,en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)


soup = BeautifulSoup(webpage.content, 'html.parser')

links = soup.find_all('a', attrs={'class': 'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})
link = links[0].get('href')
product_list_link = "https://www.amazon.pl" + link

new_webpage = requests.get(product_list_link, headers=HEADERS)
new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
productTitle = new_soup.find('span', attrs={'id': 'productTitle'}).text.strip()
productPrice = new_soup.find('span', attrs={'class': 'aok-offscreen'}).text.strip()
print(productTitle, productPrice)
