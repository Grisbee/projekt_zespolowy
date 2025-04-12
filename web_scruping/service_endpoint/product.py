from pydantic import BaseModel


class Product(BaseModel):
    productSource = str
    title: str
    price: float