"""

Orders API Client

"""


import requests

from trader.orders.constants import (
    EQUITY_ORDERS_URL,
    LIMIT_ORDER_URL,
    MARKET_ORDER_URL,
    STOP_ORDER_URL,
    STOP_LIMIT_ORDER_URL
)
from trader.orders.types import EquityOrderDto
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server


class OrdersClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_equity_orders(self) -> list[EquityOrderDto]:
        response: requests.Response = self.get(EQUITY_ORDERS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [EquityOrderDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []

    def place_limit_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self.post(
            LIMIT_ORDER_URL,
            json=order.model_dump(include={"limitPrice", "quantity", "ticker", "timeValidity"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return EquityOrderDto(**data)

        print(f"Request failed with status: {status}.")
        return order

    def place_market_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self.post(
            MARKET_ORDER_URL,
            json=order.model_dump(include={"quantity", "ticker"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return EquityOrderDto(**data)

        print(f"Request failed with status: {status}.")
        return order

    def place_stop_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self.post(
            STOP_ORDER_URL,
            json=order.model_dump(include={"quantity", "stopPrice", "ticker", "timeValidity"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return EquityOrderDto(**data)

        print(f"Request failed with status: {status}.")
        return order

    def place_stop_limit_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self.post(
            STOP_LIMIT_ORDER_URL,
            json=order.model_dump(
                include={"limitPrice", "quantity", "stopPrice",
                         "ticker", "timeValidity"}
            )
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return EquityOrderDto(**data)

        print(f"Request failed with status: {status}.")
        return order

    def cancel_order(self, order: EquityOrderDto) -> None:
        response: requests.Response = self.delete(
            EQUITY_ORDERS_URL, params=order.model_dump(exclude_unset=True)
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is not T212ApiResponse.OK:
            print(f"Request failed with status: {status}.")

    def get_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self.get(
            EQUITY_ORDERS_URL, params=order.model_dump(exclude_unset=True)
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return EquityOrderDto(**data)

        print(f"Request failed with status: {status}.")
        return order
