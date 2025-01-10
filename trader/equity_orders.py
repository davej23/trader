from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from trader.constants import Ticker


class EquityOrderStatus(str, Enum):
    LOCAL = "LOCAL"
    UNCONFIRMED = "UNCONFIRMED"
    CONFIRMED = "CONFIRMED"
    NEW = "NEW"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    REPLACING = "REPLACING"
    REPLACED = "REPLACED"


class EquityOrderStrategy(str, Enum):
    QUANTITY = "QUANTITY"
    VALUE = "VALUE"


class EquityOrderType(str, Enum):
    LIMIT = "LIMIT"
    STOP = "STOP"
    MARKET = "MARKET"
    STOP_LIMIT = "STOP_LIMIT"


class TimeValidity(str, Enum):
    DAY = "DAY"
    GOOD_TILL_CANCEL = "GOOD_TILL_CANCEL"


class EquityOrderDto(BaseModel):
    creationDate: datetime
    filledQuantity: float
    filledValue: float
    id: int
    limitPrice: float
    quantity: float
    status: EquityOrderStatus
    stopPrice: float
    strategy: EquityOrderStrategy
    ticker: Ticker
    type: EquityOrderType
    value: float
