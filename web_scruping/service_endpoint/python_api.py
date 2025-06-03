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
    product_id: int


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="projekt_zespolowy",
        user="postgres",
        password="kanapa123",
        port=5432
    )


def generate_price_chart(product_id: int, price_type: str):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT amazon_title, {price_type} 
            FROM Product 
            WHERE id = %s
        """, (product_id,))

        main_product = cursor.fetchone()
        if not main_product:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute("""
            SELECT similar_product_1, similar_product_2, similar_product_3, similar_product_4
            FROM SimilarProducts 
            WHERE product_id = %s
        """, (product_id,))

        similar_ids = cursor.fetchone()

        product_names = [main_product[0]]
        prices = [main_product[1] if main_product[1] is not None else 0]

        if similar_ids:
            for similar_id in similar_ids:
                if similar_id is not None:
                    cursor.execute(f"""
                        SELECT amazon_title, {price_type} 
                        FROM Product 
                        WHERE id = %s
                    """, (similar_id,))

                    similar_product = cursor.fetchone()
                    if similar_product:
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
        # plt.savefig(f'chart_{product_id}_{price_type}.png', dpi=300, bbox_inches='tight')

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
    chart = generate_price_chart(request.product_id, "price_new")
    return {
        "chart": chart
    }


@app.post("/python-price-used")
async def generate_price_used(request: ProductRequest):
    chart = generate_price_chart(request.product_id, "price_used")
    return {
        "chart": chart
    }


@app.post("/python-price-box")
async def generate_price_box(request: ProductRequest):
    chart = generate_price_chart(request.product_id, "price_box")
    return {
        "chart": chart
    }