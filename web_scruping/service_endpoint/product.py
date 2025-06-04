from pydantic import BaseModel

#odpalamy jako uvicorn python_api:app --host 0.0.0.0 --port 8082
class PriceChart(BaseModel):
    productSource = str
    title: str
    price: float

class ReviewChart(BaseModel):
    productSource = str
    title: str
    review: int

class RatingChart(BaseModel):
    productSource = str
    title: str
    rating: float