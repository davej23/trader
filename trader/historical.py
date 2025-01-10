from enum import Enum

from pydantic import BaseModel

from trader.constants import Ticker
from trader.equity_orders import EquityOrderStatus
from trader.portfolio import Frontend


class FillType(str, Enum):
    TOTV = "TOTV"
    OTC = "OTC"


class TaxType(str, Enum):
    COMMISSION_TURNOVER = "COMMISSION_TURNOVER"
    CURRENCY_CONVERSION_FEE = "CURRENCY_CONVERSION_FEE"
    FINRA_FEE = "FINRA_FEE"
    FRENCH_TRANSACTION_TAX = "FRENCH_TRANSACTION_TAX"
    PTM_LEVY = "PTM_LEVY"
    STAMP_DUTY = "STAMP_DUTY"
    STAMP_DUTY_RESERVE_TAX = "STAMP_DUTY_RESERVE_TAX"
    TRANSACTION_FEE = "TRANSACTION_FEE"


class ExportStatus(str, Enum):
    QUEUED = "Queued"
    PROCESSING = "Processing"
    RUNNING = "Running"
    CANCELED = "Canceled"
    FAILED = "Failed"
    FINISHED = "Finished"


class TransactionType(str, Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    FEE = "FEE"
    TRANSFER = "TRANSFER"


class Tax(BaseModel):
    fillId: str
    name: TaxType
    quantity: float
    timeCharged: str


class HistoricalOrderRequestDto(BaseModel):
    cursor: int
    ticker: Ticker
    limit: int


class HistoricalOrderDto(BaseModel):
    dateCreated: str
    dateExecuted: str
    dateModified: str
    executor: Frontend
    fillCost: float
    fillId: int
    fillPrice: float
    fillResult: float
    fillType: FillType
    filledQuantity: float
    id: int
    limitPrice: float
    orderedQuantity: float
    orderedValue: float
    parentOrder: int
    status: EquityOrderStatus
    stopPrice: float
    taxes: list[Tax]
    ticker: Ticker


class HistoricalDividendItemDto(BaseModel):
    amount: float
    amountInEuro: float
    grossAmountPerShare: float
    paidOn: str
    quantity: float
    reference: str
    ticker: Ticker
    type: str


class HistoricalTransactionItemDto(BaseModel):
    amount: float
    dateTime: str
    reference: str
    type: TransactionType


class ReportDataIncluded(BaseModel):
    includeDividends: bool
    includeInterest: bool
    includeOrders: bool
    includeTransactions: bool


class ExportDataDto(BaseModel):
    dataIncluded: ReportDataIncluded
    downloadLink: str
    reportId: int
    status: ExportStatus
    timeFrom: str
    timeTo: str


class ExportCsvDto(BaseModel):
    dataIncluded: ReportDataIncluded
    timeFrom: str
    timeTo: str


class TransactionsRequestDto(BaseModel):
    cursor: int
    time: str
    limit: int
