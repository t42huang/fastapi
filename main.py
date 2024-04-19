from typing import Union, Annotated
from enum import Enum

from fastapi import FastAPI, Query, Path
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


# Enum
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# q 是可选参数，默认值位None
@app.get("/items/2/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"Item_id": item_id, "q": q}
    return {"item_id": id}


# item_id 是路径参数， q是查询参数
@app.get("/items/{item_id}")
async def list_items(item_id: str, q: Union[str, None] = Query(default=None, max_length=50)):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# 多个路径和查询参数
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: Union[str, None], short: bool = False):
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


@app.get("/items/3/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# request body
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: Union[float, None] = None  # optional param


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


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


@app.put("/items/{item_id}")
async def update_item(
        item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: Union[str, None] = None,
        item: Union[Item, None] = None,
        user: Union[User, None] = None
):
    results = {"item_id": item_id, "user": User}
    if q:
        results.update({"q": q})
    if item:
        results = {"item": item, "user": User}
    return results
