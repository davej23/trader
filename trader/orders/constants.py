"""

Equity order endpoint URLs

"""


EQUITY_ORDERS_URL: str = "/api/v0/equity/orders/"
LIMIT_ORDER_URL: str = EQUITY_ORDERS_URL + "limit"
MARKET_ORDER_URL: str = EQUITY_ORDERS_URL + "market"
STOP_ORDER_URL: str = EQUITY_ORDERS_URL + "stop"
STOP_LIMIT_ORDER_URL: str = EQUITY_ORDERS_URL + "stop_limit"
