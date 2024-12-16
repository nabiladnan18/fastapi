from pydantic import BaseModel, Field, HttpUrl, EmailStr
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


class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    friendface_tracker: str | None = None
    talktalk_tracker: str | None = None


class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


class RandomItems(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Lightsabre",
                    "description": "Cuts stuff with light",
                    "price": 123.5,
                    "tax": 67.8,
                    "tags": ["jedi", "star wars"],
                }
            ]
        }
    }

    name: str
    description: str | None = None
    price: float
    tax: float
    tags: list = []


class UserIn(BaseModel):
    username: str
    password: str  #! Never store PW in plain text!
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn2(BaseUser):
    password: str
