from typing import Union
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world!"}


@app.post("/")
async def post():
    return {"message": "hello from post route!"}


@app.put("/{id}")
async def put():
    return {"message": "hello from put route!"}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetable = "vege"
    dairy = "dairy"


@app.get(("/food/{food_name}"))
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetable:
        return {"food_name": food_name, "message": "you are healthy"}
    if food_name == FoodEnum.fruits:
        return {"food_name": food_name, "message": "you are still healthy, but like sweet things"}
    return {"food_name": food_name, "message": "you are healthy"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "bar"}, {"item_name": "Baz"}, {"item_name": "TGIF"}, ]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def list_items(item_id: str, q: str):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: str, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "lorem ipsum dolor sit amt."
            }
        )
        return item


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result



