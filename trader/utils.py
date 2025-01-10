from typing import TypeVar, Any

from pydantic import BaseModel, create_model


T = TypeVar('T')


class PaginatedResponse(BaseModel):
    items: list[T]
    nextPagePath: str


def create_paginated_response(field_type: Any) -> PaginatedResponse:
    return create_model("PaginatedResponse", dynamic_field=(field_type,))
