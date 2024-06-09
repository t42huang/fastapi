from datetime import datetime, timedelta, time
from typing import Union, Annotated, Set
from enum import Enum
from uuid import UUID

from fastapi import FastAPI, Query, Path, Body, Form, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List

from starlette.responses import HTMLResponse
from typing_extensions import Annotated

#创建 fastAPI的实例
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
async def read_item_2(item_id: str, q: Union[str, None] = None):
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
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="the description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None  # optional param
    test: str = "test"
    tags: list[str] = []
    tags_set: Set[str] = set()
    image: Union[List[Image], None] = None


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


@app.put("/items/2/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.put("/items/{item_id}")
async def update_item2(
        item_id: int,
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


@app.put("/items/3/{item_id}")
async def update_item3(
        item_id: int,
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


@app.put("/items/{item_id}")
async def update_item(
        item_id: int,
        q: Union[str, None] = None,
        item: Item = Body(embed=True),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results = {"item": item}
    return results


@app.put("/items/4/{item_id}")
async def update_item_4(
        item_id: int,
        q: Union[str, None] = None,
        item: Union[Item, None] = None
        # item: Item = Body(embed=True),

):
    results = {"item_id": item_id, "item": item}
    if q:
        results.update({"q": q})
    if item:
        results = {"item_id": item_id, "item": item}
    return results


@app.put("/items/5/{item_id}")
async def read_items_5(
        item_id: UUID,
        start_datetime: Annotated[datetime, Body()],
        end_datetime: Annotated[datetime, Body()],
        process_after: Annotated[timedelta, Body()],
        repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


# 响应模型

@app.post("/items/3/", response_model=Item)
async def create_item_3(item: Item):
    return item


@app.get("/items/3/", response_model=List[Item])
async def create_item_3():
    return [
        {"name": "leo", "price": 12},
        {"name": "leo2", "price": 123}
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: Union[str, None] = None


@app.post("/user/4/", response_model=UserOut, tags=["User"])
async def create_user(user: UserIn):
    return user


# 响应模型编码参数
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/6/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item_6(item_id: str):
    return items[item_id]


@app.get("/items/7/{item_id}", response_model=Item, response_model_exclude={"tax"})
async def read_items_7(item_id: str):
    return items[item_id]


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/7/", response_model=UserOut, tags=["User"])
async def create_user_7(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


@app.post("/files/", tags=["upload"])
async def create_files(file: bytes=File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/", tags=["upload"])
async def create_upload_file(file: UploadFile):

    return {"filename": file.filename}





@app.post("/files/2/", tags=["upload"], summary="update multiple files, this is summary", description="this is description")
async def create_files_2(
    files: List[bytes] = File(description="Multiple files as bytes"),
):
    """
    test docstring, markdown doc
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/2/", tags=["upload"], deprecated=True)
async def create_upload_files_2(
    files: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}


# 数据库
@app.get("/items/8/{item_id}", response_model=Item)
async def read_item_8(item_id: str):
    return items[item_id]

@app.put("/items/8/{item_id}", response_model=Item)
async def update_item_8(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.put("/items/9/{item_id}", response_model=Item)
async def update_item_9(item_id: str, item: Item):
    # 拿到数据，json
    stored_item_encoded = items[item_id]
    # 转成item model
    stored_item_model = Item(**stored_item_encoded)
    # 更新数据 添加exclude_unset
    update_data = item.dict(exclude_unset=True)
    # 将更新的数据 放到模型里去
    update_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(update_item)
    return update_item


@app.put("items/10/{item_id}")
async def update(item_id: str, item: Item):
    store_item = item[item_id]
    update_data_model = Item(**store_item)
    update_data = item.dict(exclude_unset=True)
    update_item = update_data_model.copy(update=update_data)
    item[item_id] = jsonable_encoder(update_item)
    return update_item


@app.get("/items/11/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id], "status_code": 404}

@app.get("/items/12/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404,
                            headers={"X-Error": "There goes my error"},
                            detail="Item not found",
                            )
    return {"item": items[item_id], "status_code": 404}
