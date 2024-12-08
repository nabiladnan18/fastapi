from pydantic import BaseModel, Field, HttpUrl
from typing import Literal


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="Price must be greater than 0")
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            ]
        }
    }


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class User(BaseModel):
    username: str
    fullname: str | None


class Image(BaseModel):
    url: HttpUrl = Field(example="https://www.url.tld")
    name: str


class Media(BaseModel):
    title: str
    description: str | None = None
    price: float
    tax: float | None
    tags: set[str] = set()
    image: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    media: list[Media]
