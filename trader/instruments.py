from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from trader.constants import T212Server, T212ApiToken


class TimeEventType(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    BREAK_START = "BREAK_START"
    BREAK_END = "BREAK_END"
    PRE_MARKET_OPEN = "PRE_MARKET_OPEN"
    AFTER_HOURS_OPEN = "AFTER_HOURS_OPEN"
    AFTER_HOURS_CLOSE = "AFTER_HOURS_CLOSE"
    OVERNIGHT_OPEN = "OVERNIGHT_OPEN"


class InstrumentType(str, Enum):
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    ETF = "ETF"
    FOREX = "FOREX"
    FUTURES = "FUTURES"
    INDEX = "INDEX"
    STOCK = "STOCK"
    WARRANT = "WARRANT"
    CRYPTO = "CRYPTO"
    CVR = "CVR"
    CORPACT = "CORPACT"


class TimeEvent(BaseModel):
    date: datetime
    type: TimeEventType


class WorkingSchedules(BaseModel):
    id: int
    timeEvents: list[TimeEvent]


class ExchangeDto(BaseModel):
    id: int
    name: str
    workingSchedules: WorkingSchedules


class InstrumentDto(BaseModel):
    addedOn: datetime
    currencyCode: str
    isin: str
    maxOpenQuantity: int
    minTradeQuantity: int
    name: str
    shortName: str
    ticker: str
    type: InstrumentType
    workingScheduleId: int
