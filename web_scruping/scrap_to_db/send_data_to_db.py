import demo2_scrap
import db_properties
import psycopg2

conn = None
cursor = None

try:
    username, pwd, port_id, hostname, database = db_properties.return_properties()
    conn = psycopg2.connect(user=username, password=pwd, port=port_id, dbname=database, host=hostname)
    cursor = conn.cursor()

    data = demo2_scrap.get_all_data()

    insert_script = ''' INSERT INTO products (title, price, url, product_source, currency, rating, review_count) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    insert_value = [(data['title'][i],
        data['price'][i],
        data['url'][i],
        data['product_src'][i],
        data['currency'][i],
        data['rating'][i],
        data['reviews'][i]
    ) for i in range(len(data['title']))]

    cursor.executemany(insert_script, insert_value)
    conn.commit()

except Exception as e:
    print(e)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()



