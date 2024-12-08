from pydantic import BaseModel, Field
from typing import Literal


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class User(BaseModel):
    username: str
    fullname: str | None
