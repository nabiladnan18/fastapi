from fastapi import FastAPI

app = FastAPI()

ITEMS = [{"item_id": 1, "value": "something"}, {"item_id": 2, "value": "nothing"}]

FAKE_ITEMS_DB = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return FAKE_ITEMS_DB[skip : skip + limit]


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in ITEMS:
        if item["item_id"] == item_id:
            return item
    return None


@app.get("/fakeItems/{item_id}")
async def get_fake_item(item_id: str, q: str | None = None, short: bool = False):
    item = None
    for fake_item in FAKE_ITEMS_DB:
        if fake_item["item_name"] == item_id:
            item = fake_item
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
