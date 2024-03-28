from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from enums.Messages import Messages
from typing import Annotated
import re

fast_app = FastAPI()

items = []
users = []

class ProductList(BaseModel):
    name: Annotated[str, Query(min_length=3, max_length=50)]
    price: Annotated[float, Query()] = 0.00
    product_category: Annotated[str, Query(min_length=1, max_length=20)]
    stock: Annotated[int, Query()] = 0
    availability: Annotated[bool, Query()] = False


class User(BaseModel):
    first_name: Annotated[str, Query(max_length=50)] = None
    last_name: Annotated[str, Query(min_length=3, max_length=50)]
    email: Annotated[str, Query(max_length=50, pattern=r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$')]
    password: Annotated[str, Query(min_length=8 ,max_length=50)]



class Products:
    @fast_app.get("/product/", tags=["Products"])
    async def get_all_items():
        return {'message': Messages.NO_ITEMS_FOUND} if items == [] else items


    @fast_app.get("/product/{product_id}", tags=["Products"])
    async def get_item(product_id: int):
        try:
            if items[product_id]:
                return items[product_id]
        except IndexError:
            return {'message': Messages.ITEM_NOT_FOUND}


    @fast_app.post("/product/", tags=["Products"])
    async def add_items(item: ProductList):
        items.append(item)
        return item
    
    
    @fast_app.put("/product/{product_id}/update/", tags=["Products"])
    async def update_item(product_id: int, updated_item: ProductList):
        try:
            if items[product_id]:
                items[product_id]= dict(updated_item)
                return items[product_id]
        except IndexError:
            return {'message': Messages.ITEM_NOT_FOUND}
        

    @fast_app.delete("/product/{product_id}/delete/", tags=["Products"])
    async def update_item(product_id: int):
        try:
            if items[product_id]:
                items.pop(product_id)
                return {'message': Messages.ITEM_DELETED}
        except IndexError:
            return {'message': Messages.ITEM_NOT_FOUND}
    
    
class Users:
    @fast_app.post("/users/", tags=["Users"])
    async def add_user(user: User):
        users.append(user)
        return user
        

    @fast_app.get("/users/", tags=["Users"])
    async def get_all_users():
        return {'message': Messages.NO_USERS_FOUND} if users == [] else users
        

    @fast_app.get("/users/{user_id}", tags=["Users"])
    async def get_user(user_id: int):
        try:
            if users[user_id]:
                return users[user_id]
        except IndexError:
            return {'message': Messages.USER_NOT_FOUND}

    
    @fast_app.put("/users/{user_id}/update", tags=["Users"])
    async def update_user(user_id: int, updated_user: User):
        try:
            if users[user_id]:
                users[user_id] = dict(updated_user)
                return users[user_id]
        except IndexError:
            return {'message': Messages.USER_NOT_FOUND}



    @fast_app.delete("/users/{user_id}/delete", tags=["Users"])
    async def delete_user(user_id: int):
        try:
            if users[user_id]:
                users.pop(user_id)
                return {'message': Messages.USER_DELETED}
        except IndexError:
            return {'message': Messages.USER_NOT_FOUND}
        