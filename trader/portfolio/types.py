"""

Portfolio-related dataclasses

"""


from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from trader.types import Ticker


class Frontend(str, Enum):
    API = "API"
    IOS = "IOS"
    ANDROID = "ANDROID"
    WEB = "WEB"
    SYSTEM = "SYSTEM"
    AUTOINVEST = "AUTOINVEST"


class PositionDto(BaseModel):
    averagePrice: float
    currentPrice: float
    frontend: Frontend
    fxPpl: float
    initialFillDate: datetime
    maxBuy: float
    maxSell: float
    pieQuantity: float
    ppl: float
    ticker: Ticker
