from fastapi import FastAPI, Query
from pydantic import BaseModel, validator
from enums.Messages import Messages
from typing import Annotated
import re

fast_app = FastAPI()


class ProductList(BaseModel):
    name: str
    price: float = 0.00
    product_category: str
    stock: int = 0
    availability: bool = False

class User(BaseModel):
    first_name: Annotated[str, Query(max_length=50)] = None
    last_name: Annotated[str, Query(min_length=3, max_length=50)]
    email: Annotated[str, Query(max_length=50, pattern=r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$')]
    password: Annotated[str, Query(min_length=8 ,max_length=50)]

items = []

class Products:
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
    
    class Users:
        @fast_app.post("/users/")
        async def add_user(user: User):
            return user