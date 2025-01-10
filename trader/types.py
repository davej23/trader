"""

General Types

"""


from enum import Enum
from typing import Any

from pydantic import BaseModel, create_model

from trader.constants import T212_DEMO_URL, T212_LIVE_URL


T212ApiToken = str
Ticker = str


class T212Server(str, Enum):
    DEMO = T212_DEMO_URL
    LIVE = T212_LIVE_URL


class T212ApiResponse(int, Enum):
    OK = 200
    INVALID = 400
    BAD_KEY = 401
    MISSING_SCOPE = 403
    NOT_FOUND = 404
    TIMED_OUT = 408
    LIMITED = 429

class RequestType(str, Enum):
    GET = "get"
    POST = "post"
    DELETE = "delete"


class PaginatedResponse(BaseModel):
    items: list[Any]
    nextPagePath: str


def create_paginated_response(field_type: Any) -> Any:
    return create_model(
        "PaginatedResponse",
        dynamic_field=(field_type,)
    )  # type: ignore[return-value]
