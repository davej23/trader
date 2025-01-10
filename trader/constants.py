from enum import Enum


T212ApiToken = str
Ticker = str


class T212Server(Enum):
    DEMO: str = "https://demo.trading212.com"
    LIVE: str = "https://live.trading212.com"


class T212ApiResponse(Enum):
    OK: int = 200
    INVALID: int = 400
    BAD_KEY: int = 401
    MISSING_SCOPE: int = 403
    NOT_FOUND: int = 404
    TIMED_OUT: int = 408
    LIMITED: int = 429


class RequestType(str, Enum):
    GET = "get"
    POST = "post"


INSTRUMENTS_BASE_URL: str = "/api/v0/equity/metadata/"
EXCHANGES_URL: str = INSTRUMENTS_BASE_URL + "exchanges"
INSTRUMENTS_URL: str = INSTRUMENTS_BASE_URL + "instruments"
PIES_URL: str = "/api/v0/equity/pies/"
EQUITY_ORDERS_URL: str = "/api/v0/equity/orders/"
LIMIT_ORDER_URL: str = EQUITY_ORDERS_URL + "limit"
MARKET_ORDER_URL: str = EQUITY_ORDERS_URL + "market"
STOP_ORDER_URL: str = EQUITY_ORDERS_URL + "stop"
STOP_LIMIT_ORDER_URL: str = EQUITY_ORDERS_URL + "stop_limit"
ACCOUNT_URL: str = "/api/v0/equity/account/"
ACCOUNT_CASH_URL: str = ACCOUNT_URL + "cash"
ACCOUNT_METADATA_URL: str = ACCOUNT_URL + "info"
PORTFOLIO_URL: str = "/api/v0/equity/portfolio/"
TICKER_URL: str = PORTFOLIO_URL + "ticker"
HISTORY_URL: str = "/api/v0/history"
ORDERS_URL: str = HISTORY_URL + "orders"
DIVIDENDS_URL: str = HISTORY_URL + "dividends"
EXPORTS_URL: str = HISTORY_URL + "exports"
TRANSACTIONS_URL: str = HISTORY_URL + "transactions"
