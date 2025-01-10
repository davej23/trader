from enum import Enum
from typing import Any

from pydantic import BaseModel


class PieStatus(str, Enum):
    AHEAD = "AHEAD"
    ON_TRACK = "ON_TRACK"
    BEHIND = "BEHIND"


class DividendCashAction(str, Enum):
    REINVEST = "REINVEST"
    TO_ACCOUNT_CASH = "TO_ACCOUNT_CASH"


class InstrumentIssueName(str, Enum):
    DELISTED = "DELISTED"
    SUSPENDED = "SUSPENDED"
    NO_LONGER_TRADABLE = "NO_LONGER_TRADABLE"
    MAX_POSITION_SIZE_REACHED = "MAX_POSITION_SIZE_REACHED"
    APPROACHING_MAX_POSITION_SIZE = "APPROACHING_MAX_POSITION_SIZE"
    COMPLEX_INSTRUMENT_APP_TEST_REQUIRED = "COMPLEX_INSTRUMENT_APP_TEST_REQUIRED"


class InstrumentIssueSeverity(str, Enum):
    IRREVERSIBLE = "IRREVERSIBLE"
    REVERSIBLE = "REVERSIBLE"
    INFORMATIVE = "INFORMATIVE"


class DividendDetails(BaseModel):
    gained: float
    inCash: float
    reinvested: float

    @classmethod
    def new(cls) -> "DividendDetails":
        return cls(
            gained=0.0,
            inCash=0.0,
            reinvested=0.0
        )


class InvestmentResult(BaseModel):
    priceAvgInvestedValue: float
    priceAvgResult: float
    priceAvgResultCoef: float
    priceAvgValue: float

    @classmethod
    def new(cls) -> "InvestmentResult":
        return cls(
            priceAvgInvestedValue=0.0,
            priceAvgResult=0.0,
            priceAvgResultCoef=0.0,
            priceAvgValue=0.0
        )


class InstrumentIssue(BaseModel):
    name: InstrumentIssueName
    severity: InstrumentIssueSeverity


class AccountBucketInstrumentResult(BaseModel):
    currentShare: float
    expectedShare: float
    issues: list[InstrumentIssue]
    ownedQuantity: float
    result: InvestmentResult
    ticker: str


class AccountBucketDetailedResponse(BaseModel):
    creationDate: str
    dividendCashAction: DividendCashAction
    endDate: str
    goal: float
    icon: str
    id: int
    initialInvestment: float
    instrumentShares: dict[str, Any]


class PieDto(BaseModel):
    cash: float
    dividendDetails: DividendDetails
    id: int
    progress: float
    result: InvestmentResult
    status: PieStatus

    @classmethod
    def new(cls) -> "PieDto":
        return cls(
            cash=0.0,
            dividendDetails=DividendDetails.new(),
            id=-1,
            progress=0.0,
            result=InvestmentResult.new(),
            status=PieStatus.ON_TRACK
        )


class CreatePieDto(BaseModel):
    dividendCashAction: DividendCashAction
    endDate: str
    goal: float
    icon: str
    instrumentShares: dict[str, Any]
    name: str


class CreatePieResponseDto(BaseModel):
    instruments: list[AccountBucketInstrumentResult]
    settings: AccountBucketDetailedResponse


class DeletePieDto(BaseModel):
    id: int
