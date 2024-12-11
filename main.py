from fastapi import FastAPI, Path, Query, Body, Cookie, Header
from typing import Annotated, Any
from models import (
    Item,
    FilterParams,
    Media,
    RandomItems,
    User,
    Offer,
    Cookies,
    CommonHeaders,
    UserIn,
    UserOut,
)
from datetime import datetime, time, timedelta
from uuid import UUID

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


@app.get(
    "/items/queryParamsArePydantic",
    summary="Using pydantic model to define query",
    response_description="This is a description of the response",
)
async def read_items_pydantic_query(filter_query: Annotated[FilterParams, Query()]):
    """
    Uses a Pydantic Model to filter items.

    - **FilterParams**
    - *This is italic*
        - This ~~is~~ a **subpoint** --> does not strikethrough
            - Clearly not all `md` features work?
    """
    return filter_query


@app.put(
    "/items/update2/{item_id}",
    summary="New Update",
    description="Cleaner way to do it is using `docstrings` under functions + `markdown`. **This here takes precedence.**",
    response_description="Returns `item_id`, the `item` itself, and `user` information",
)
async def update_items2(
    item_id: Annotated[
        int,
        Path(
            title="Updating an item with a given `item_id`",
            description="This describes what `item_id` is",
            ge=0,
            le=1000,
        ),
    ],
    user: Annotated[
        User,
        Body(
            description="This is to show that multiple body params can be included in an API call"
        ),
    ],
    importance: Annotated[int, Body()],
    item: Item | None = None,
    q: Annotated[str | None, Query(description="This is a random query")] = None,
):
    """
    Does this work? This gets overshadowed by the `summary` kwarg in the decorator
    """

    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}

    if q:
        results.update({"q": q})

    return results


@app.put(
    "/items/update3/{item_id}", summary="Updating items using embedded Body params"
)
async def update_items3(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            embed=True,
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/media/{item_id}")
async def get_media(item_id: int, item: Media):
    result = {"item_id": item_id, "item": item}
    return result


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


@app.put("/items/update4/{item_id}")
async def update_item4(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/items/read1/{item_id}")
async def read_items1(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
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


@app.get("/itemCookiesAndHeaders")
def get_item_using_cookies(
    ads: Annotated[str | None, Cookie()] = None,
    trackers: Annotated[Cookies, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    header_without_conversion: Annotated[
        CommonHeaders, Header(convert_underscores=False)
    ] = None,
):
    return {
        "ads": ads,
        "trackers": trackers,
        "user-agent": user_agent,
        "header_without_conversion": header_without_conversion,
    }


@app.get("/itemsDuplicateHeaders")
async def get_items_dup_headers(x_token: Annotated[list[str] | None, Header()] = None):
    """
    example:

    X-Token:foo
    X-Token: bar


    response:
    {
        X-TokenValues: [
            "bar",
            "foo"
        ]
    }

    """
    return {"X-TokenValues": x_token}


@app.post("/create/randomItems")
async def create_random_items(item: RandomItems) -> RandomItems:
    return item


@app.post(
    "/create/randomItemsResponseModel",
    description="Here we are using a `response model` to validate the *response* against a *Pydantic Model*",
    summary="Validating response against Pydantic Model",
    response_model=RandomItems,
)
async def create_and_validate_response_against_models(item: RandomItems) -> Any:
    return item


@app.get("/get/randomItems")
async def get_random_items() -> list[RandomItems]:
    return [
        RandomItems(
            name="Item 1",
            description="Non-descript",
            price=100.0,
            tax=12.2,
            tags=["No tags", "Definitely not a tag"],
        ),
        RandomItems(name="name", price=10, tax=1),
    ]


@app.get("/get/randomItemsResponseModel", response_model=list[RandomItems])
async def get_and_validate_response_against_models() -> Any:
    return [
        RandomItems(
            name="Item 1",
            description="Non-descript",
            price=100.0,
            tax=12.2,
            tags=["No tags", "Definitely not a tag"],
        ),
        RandomItems(name="name", price=10, tax=1),
    ]


@app.post("/user/create", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
