from fastapi import FastAPI, Path, Query
from typing import Annotated
from models import Item, FilterParams

app = FastAPI()

ITEMS = [{"item_id": 1, "value": "something"}, {"item_id": 2, "value": "nothing"}]

FAKE_ITEMS_DB = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[
        int, Path(title="this defines how the `item_id` in path will work", gt=0, le=3)
    ],
):
    for item in ITEMS:
        if item["item_id"] == item_id:
            return item
    return None


@app.get("/fakeItems/{item_id}")
async def get_fake_item(item_id: str, q: str | None = None, short: bool = False):
    item = {}
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


@app.post("/items/create")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price with tax": price_with_tax})
    return item_dict


@app.put("/items/update/{item_id}")
async def update_item(item_id: str, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.get("/items")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Some title",
            min_length=3,
            max_length=50,
            pattern="^startswithsendswithh$",
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/queryParamsArePydantic")
async def read_items_pydantic_query(filter_query: Annotated[FilterParams, Query()]):
    """
    Info

    Extended info

    Args:
        filter_query (Annotated[FilterParams, Query): Uses FilterParams Class

    Returns:
        Pydantic Model: 😬
    """
    return filter_query
