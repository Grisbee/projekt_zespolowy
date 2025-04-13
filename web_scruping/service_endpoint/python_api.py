from fastapi import FastAPI

app = FastAPI()


#odpalamy jako uvicorn python_api:app --host 0.0.0.0 --port 8082

@app.post("/python-price-chart")
async def generate_price_chart():
    chart = "price chart"
    return {
        "chart": chart
    }

@app.post("/python-rating-chart")
async def generate_rating_chart():
    chart = "rating chart"
    return {
        "chart": chart
    }

@app.post("/python-review-chart")
async def generate_review_chart():
    chart = "review chart"
    return {
        "chart": chart
    }
