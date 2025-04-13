from pydantic import BaseModel


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