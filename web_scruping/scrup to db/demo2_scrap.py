from bs4 import BeautifulSoup
import requests
import re
import source_definer


def get_title(s, title_selector):
    try:
        title = s.find("span", attrs=title_selector).get_text().strip()

    except AttributeError:
        title = ""

    return title

def get_price(soup, price_selector):
    try:
        price = soup.find('span', attrs=price_selector).text.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(soup, rating_selector):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs=rating_selector).string.strip()
        except:
            rating = ""

    return rating


def get_review_count(soup, review_selector):
    try:
        review_count = soup.find("span", attrs=review_selector).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

def generate_links(soup, class_selector):
    expected_classes = set(class_selector.split())
    links = []
    for a_tag in soup.find_all('a'):
        actual_classes = set(a_tag.get('class', []))
        if actual_classes == expected_classes:
            href = a_tag.get('href')
            if href:
                links.append(href)
    return links


def get_all_data(src):
    HEADERS = source_definer.HEADERS
    URL = src.search_url
    print(URL)

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    link_list = generate_links(soup, src.link_selector)
    print(link_list)

    d = {'title':[], 'price':[], 'rating': [], 'reviews':[], 'currency':[], 'url':[], 'product_src': [] }

    for link in link_list:
        request_link = str(src.base_url) + link
        print(request_link)

        new_webpage = requests.get(request_link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        title = get_title(new_soup, src.title_selector)
        print(title)
        price = get_price(new_soup, src.price_selector)
        print(price)
        rating_str = get_rating(new_soup, src.ratings_selector)
        reviews_str = get_review_count(new_soup, src.reviews_selector)

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
        d['product_src'].append(src.scruping_platform)
    return d


if __name__ == '__main__':
    data = get_all_data(source_definer.TELEWIZOR_SAMSUNG_AMAZON_CFG)
    print(data)

# amazon_df = pd.DataFrame.from_dict(d)
# amazon_df['title'] = amazon_df['title'].replace('', np.nan)
# amazon_df = amazon_df.dropna(subset=['title'])
# amazon_df.to_csv("amazon_data.csv", header=True, index=False)