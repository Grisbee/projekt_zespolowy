from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.post("/python-price-chart")
async def generate_price_chart():
    chart = "implementacja dashboarda"
    return {
        "chart": chart
    }