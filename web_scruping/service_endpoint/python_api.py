from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

matplotlib.use('Agg')

app = FastAPI()


class ProductRequest(BaseModel):
    keepa_name: str


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="webscruping-db-1",
        user="postgres",
        password="cat2880",
        port=5432
    )


def generate_price_chart(keepa_name: str, price_type: str):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT amazon_title, {price_type} 
            FROM Product 
            WHERE keepa_name = %s
        """, (keepa_name,))

        main_product = cursor.fetchone()
        if not main_product:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute("""
            SELECT similar_product_1, similar_product_2, similar_product_3, similar_product_4
            FROM SimilarProducts 
            WHERE similar_product_1 = %s OR similar_product_2 = %s OR similar_product_3 = %s OR similar_product_4 = %s
        """, (keepa_name, keepa_name, keepa_name, keepa_name))

        similar_products_entry = cursor.fetchone()
        similar_ids = []

        if similar_products_entry:
            cursor.execute("""
                SELECT similar_product_1, similar_product_2, similar_product_3, similar_product_4
                FROM SimilarProducts 
                WHERE similar_product_1 = %s OR similar_product_2 = %s OR similar_product_3 = %s OR similar_product_4 = %s
            """, (keepa_name, keepa_name, keepa_name, keepa_name))

            similar_row = cursor.fetchone()

            if similar_row:
                for sim_name in similar_row:
                    if sim_name is not None and sim_name != keepa_name:
                        similar_ids.append(sim_name)

        product_names = [main_product[0]]
        prices = [main_product[1] if main_product[1] is not None else 0]

        if similar_ids:
            similar_names_placeholder = ', '.join(['%s'] * len(similar_ids))
            cursor.execute(f"""
                SELECT amazon_title, {price_type} 
                FROM Product 
                WHERE keepa_name IN ({similar_names_placeholder})
            """, tuple(similar_ids))

            similar_products_data = cursor.fetchall()

            for similar_product in similar_products_data:
                product_names.append(similar_product[0])
                prices.append(similar_product[1] if similar_product[1] is not None else 0)

        price_labels = {
            'price_new': ('Porównanie cen (stan nowy)', 'Cena (USD)'),
            'price_used': ('Porównanie cen (stan używany)', 'Cena (USD)'),
            'price_box': ('Porównanie cen (nowy w pudełku)', 'Cena (USD)')
        }

        title, ylabel = price_labels.get(price_type, ('Porównanie cen', 'Cena (zł)'))

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(product_names)), prices, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])

        plt.xlabel('Produkty')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(range(len(product_names)), [name[:30] + '...' if len(name) > 30 else name for name in product_names],
                   rotation=45, ha='right')

        max_price = max(prices) if prices else 0
        plt.ylim(0, max_price * 1.1)

        for bar, price in zip(bars, prices):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height + max_price * 0.01,
                     f'{price}', ha='center', va='bottom')

        plt.tight_layout()

        # Zapis na dysk (odkomentuj jak chcesz testować)
        #plt.savefig(f'chart_{price_type}.png', dpi=300, bbox_inches='tight')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.post("/python-price-new")
async def generate_price_new(request: ProductRequest):
    chart = generate_price_chart(request.keepa_name, "price_new")
    return {
        "chart": chart
    }


@app.post("/python-price-used")
async def generate_price_used(request: ProductRequest):
    chart = generate_price_chart(request.keepa_name, "price_used")
    return {
        "chart": chart
    }


@app.post("/python-price-box")
async def generate_price_box(request: ProductRequest):
    chart = generate_price_chart(request.keepa_name, "price_box")
    return {
        "chart": chart
    }


@app.post("/python-product-data")
async def get_product_data(request: ProductRequest):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Select main product data using keepa_name (remove id selection)
        cursor.execute("""
            SELECT keepa_name, amazon_title, link_keepa, link_amazon, 
                   chart_url, price_box, price_new, price_used, 
                   rating, review_count, currency, product_src
            FROM Product 
            WHERE keepa_name = %s
        """, (request.keepa_name,))

        product_data = cursor.fetchone()
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")

        # Query SimilarProducts using the keepa_name of the main product
        cursor.execute("""
            SELECT similar_product_1, similar_product_2, similar_product_3, similar_product_4
            FROM SimilarProducts 
            WHERE similar_product_1 = %s OR similar_product_2 = %s OR similar_product_3 = %s OR similar_product_4 = %s
        """, (request.keepa_name, request.keepa_name, request.keepa_name, request.keepa_name))

        similar_row = cursor.fetchone()
        similar_products = []

        if similar_row:
            similar_names_to_fetch = []
            for sim_name in similar_row:
                if sim_name is not None and sim_name != request.keepa_name:
                    similar_names_to_fetch.append(sim_name)

            if similar_names_to_fetch:
                similar_names_placeholder = ', '.join(['%s'] * len(similar_names_to_fetch))
                # Fetch data for similar products using their keepa_names (remove id selection)
                cursor.execute(f"""
                    SELECT keepa_name, amazon_title, link_keepa, link_amazon, 
                           chart_url, price_box, price_new, price_used, 
                           rating, review_count, currency, product_src
                    FROM Product 
                    WHERE keepa_name IN ({similar_names_placeholder})
                """, tuple(similar_names_to_fetch))

                similar_products_data = cursor.fetchall()

                # Manually map fetched data to dictionary for similar products
                similar_products = []
                for similar_product_tuple in similar_products_data:
                    similar_products.append({
                        "keepa_name": similar_product_tuple[0],
                        "amazon_title": similar_product_tuple[1],
                        "link_keepa": similar_product_tuple[2],
                        "link_amazon": similar_product_tuple[3],
                        "chart_url": similar_product_tuple[4],
                        "price_box": similar_product_tuple[5],
                        "price_new": similar_product_tuple[6],
                        "price_used": similar_product_tuple[7],
                        "rating": similar_product_tuple[8],
                        "review_count": similar_product_tuple[9],
                        "currency": similar_product_tuple[10],
                        "product_src": similar_product_tuple[11]
                    })

        # Manually map fetched data to dictionary for the main product
        main_product_response = {
            "keepa_name": product_data[0],
            "amazon_title": product_data[1],
            "link_keepa": product_data[2],
            "link_amazon": product_data[3],
            "chart_url": product_data[4],
            "price_box": product_data[5],
            "price_new": product_data[6],
            "price_used": product_data[7],
            "rating": product_data[8],
            "review_count": product_data[9],
            "currency": product_data[10],
            "product_src": product_data[11]
        }


        return {
            "product": main_product_response,
            "similar_products": similar_products
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()