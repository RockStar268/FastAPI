from fastapi import FastAPI
from pydantic import BaseModel
from enums.Messages import Messages

fast_app = FastAPI()


class ProductList(BaseModel):
    name: str
    price: float = 0.00
    product_category: str
    stock: int = 0
    availability: bool = False


items = []


@fast_app.get("/product/")
async def get_all_items():
    return items


@fast_app.get("/product/{product_id}")
async def get_item(product_id: int):
    try:
        if items[product_id]:
            return items[product_id]
    except IndexError:
        return {'message': Messages.NOT_FOUND}


@fast_app.post("/product/")
async def add_items(item: ProductList):
    items.append(item)
    return items