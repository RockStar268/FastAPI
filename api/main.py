from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel
from enums.Messages import Messages
from typing import Annotated
from enums.Tags import Tags

fast_app = FastAPI()

items = []
users = []

class ProductList(BaseModel):
    name: Annotated[str, Query(min_length=3, max_length=50)]
    price: Annotated[float, Query()] = 0.00
    product_category: Annotated[str, Query(min_length=1, max_length=20)]
    stock: Annotated[int, Query()] = 0
    availability: Annotated[bool, Query()] = False


class BaseUser(BaseModel):
    first_name: Annotated[str, Query(max_length=50)] = None
    last_name: Annotated[str, Query(min_length=3, max_length=50)]
    email: Annotated[str, Query(max_length=50, pattern=r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$')]


class CreateUser(BaseUser):
    password: Annotated[str, Query(min_length=8 ,max_length=50)]



class Products:
    @fast_app.get("/product/", tags=[Tags.PRODUCTS])
    async def get_all_items() -> list[ProductList]:
        if not items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.NO_ITEMS_FOUND)
        else:
            return items

    @fast_app.get("/product/{product_id}", tags=[Tags.PRODUCTS])
    async def get_item(product_id: int):
        try:
            if items[product_id]:
                return items[product_id]
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ITEM_NOT_FOUND)


    @fast_app.post("/product/", tags=[Tags.PRODUCTS])
    async def add_items(item: ProductList):
        items.append(item)
        return item
    
    
    @fast_app.put("/product/{product_id}/update/", tags=[Tags.PRODUCTS])
    async def update_item(product_id: int, updated_item: ProductList):
        try:
            if items[product_id]:
                items[product_id]= dict(updated_item)
                return items[product_id]
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ITEM_NOT_FOUND)
        

    @fast_app.delete("/product/{product_id}/delete/", tags=[Tags.PRODUCTS])
    async def update_item(product_id: int):
        try:
            if items[product_id]:
                items.pop(product_id)
                return {'message': Messages.ITEM_DELETED}
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.ITEM_NOT_FOUND)
    
    
class Users:
    @fast_app.post("/users/", tags=[Tags.USERS])
    async def add_user(user: CreateUser) -> BaseUser:
        users.append(user)
        return user
        

    @fast_app.get("/users/", tags=[Tags.USERS])
    async def get_all_users() -> list[BaseUser]:
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.NO_USERS_FOUND)
        else:
            return users

    @fast_app.get("/users/{user_id}", tags=[Tags.USERS])
    async def get_user(user_id: int ) -> BaseUser:
        try:
            if users[user_id]:
                return users[user_id]
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.USER_NOT_FOUND)

    
    @fast_app.put("/users/{user_id}/update", tags=[Tags.USERS])
    async def update_user(user_id: int, updated_user: CreateUser) -> BaseUser:
        try:
            if users[user_id]:
                users[user_id] = dict(updated_user)
                return updated_user
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.USER_NOT_FOUND)



    @fast_app.delete("/users/{user_id}/delete", tags=[Tags.USERS])
    async def delete_user(user_id: int):
        try:
            if users[user_id]:
                users.pop(user_id)
                return {'message': Messages.USER_DELETED}
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Messages.USER_NOT_FOUND)

        