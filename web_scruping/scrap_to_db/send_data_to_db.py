import demo2_scrap
import psycopg2
import scrap

conn = None
cursor = None

try:
    # Bezpośrednie dane połączenia z bazą danych
    conn = psycopg2.connect(
        host="localhost",
        database="projekt_zespolowy",
        user="postgres",
        password="kanapa123",
        port=5432
    )
    cursor = conn.cursor()

    data = scrap.scrap_five_products("iphone x")
    print(data)

    # Lista ID produktów które zostały dodane/już istnieją
    product_ids = []
    new_product_ids = []  # Lista tylko nowo dodanych produktów

    # Dodawanie produktów do tabeli Product
    for product in data:
        # Sprawdzenie czy produkt już istnieje (po amazon_title)
        cursor.execute("SELECT id FROM Product WHERE amazon_title = %s", (product['amazon_title'],))
        existing_product = cursor.fetchone()

        if existing_product:
            # Produkt już istnieje, zapisujemy jego ID ale NIE dodajemy do new_product_ids
            product_ids.append(existing_product[0])
            print(f"Produkt już istnieje: {product['amazon_title']}, ID: {existing_product[0]}")
        else:
            # Wstawianie nowego produktu
            insert_product_script = '''
                INSERT INTO Product (keepa_name, amazon_title, link_keepa, link_amazon, 
                                   chart_url, price_box, price_new, price_used, 
                                   rating, review_count, currency, product_src) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING id
            '''

            cursor.execute(insert_product_script, (
                product['product_name'],  # keepa_name
                product['amazon_title'],  # amazon_title
                product['link_keepa'],  # link_keepa
                product['link_amazon'],  # link_amazon
                product['link_chart'],  # chart_url
                int(float(product['box_price'])) if product['box_price'] else None,  # price_box
                int(float(product['new_price'])) if product['new_price'] else None,  # price_new
                int(float(product['used_price'])) if product['used_price'] else None,  # price_used
                product['rating'],  # rating
                product['review_count'],  # review_count
                product['currency'],  # currency
                product['product_src']  # product_src
            ))

            # Pobieranie ID nowo dodanego produktu
            new_product_id = cursor.fetchone()[0]
            product_ids.append(new_product_id)
            new_product_ids.append(new_product_id)  # Dodajemy tylko nowo dodane
            print(f"Dodano nowy produkt: {product['amazon_title']}, ID: {new_product_id}")

    # Dodawanie podobnych produktów TYLKO dla nowo dodanych produktów
    for main_product_id in new_product_ids:
        # Pobieramy pozostałe produkty (bez aktualnego)
        other_product_ids = [pid for pid in product_ids if pid != main_product_id]

        # Jeśli mamy mniej niż 4 innych produktów, dopełniamy NULL-ami
        while len(other_product_ids) < 4:
            other_product_ids.append(None)

        print(f"Dodawanie podobnych produktów dla nowego produktu ID: {main_product_id}")
        print(f"Podobne produkty (ID): {other_product_ids[:4]}")

        # Dodanie wpisu z głównym produktem i 4 podobnymi
        cursor.execute("""
            INSERT INTO SimilarProducts (product_id, similar_product_1, similar_product_2, 
                                        similar_product_3, similar_product_4) 
            VALUES (%s, %s, %s, %s, %s)
        """, (main_product_id, other_product_ids[0], other_product_ids[1],
              other_product_ids[2], other_product_ids[3]))
        print(f"Dodano podobne produkty dla produktu ID: {main_product_id}")

    conn.commit()
    print("Wszystkie dane zostały pomyślnie dodane do bazy!")

except Exception as e:
    print(e)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()