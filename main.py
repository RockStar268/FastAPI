from fastapi import FastAPI
from pydantic import BaseModel
from enums.Messages import Messages

app = FastAPI()


class ProductList(BaseModel):
    name: str
    price: float = 0
    product_category: str
    stock: int = 0
    availability: bool = False


items = []


@app.get("/item")
async def get_all_items():
    return items


@app.get("/item/{id}")
async def get_item(id: int):
    try:
        if items[id]:
            return items[id]
    except IndexError:
        return {'message': Messages.NOT_FOUND}



@app.post("/item")
async def add_items(item: ProductList):
    items.append(item)
    return items