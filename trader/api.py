import os
import requests

from typing import Any

from trader.account import AccountCashDto, AccountMetadataDto
from trader.constants import (
    T212Server, T212ApiResponse, EXCHANGES_URL,
    INSTRUMENTS_URL, PIES_URL, EQUITY_ORDERS_URL,
    LIMIT_ORDER_URL, MARKET_ORDER_URL, STOP_ORDER_URL,
    STOP_LIMIT_ORDER_URL, ACCOUNT_CASH_URL, ACCOUNT_METADATA_URL,
    PORTFOLIO_URL, TICKER_URL, ORDERS_URL, DIVIDENDS_URL,
    EXPORTS_URL, TRANSACTIONS_URL
)
from trader.equity_orders import EquityOrderDto
from trader.historical import (
    HistoricalOrderRequestDto, ExportDataDto, ExportCsvDto,
    TransactionsRequestDto, HistoryTransactionItem, HistoryDividendItem
)
from trader.instruments import ExchangeDto, InstrumentDto
from trader.pies import PieDto, CreatePieDto, CreatePieResponseDto
from trader.portfolio import PositionDto
from trader.utils import PaginatedResponse, create_paginated_response


class T212Client:
    _REQUESTOR: requests.Session = requests.Session()

    def __init__(self, server: T212Server = T212Server.DEMO):
        self.server = server

        if token := os.getenv("T212_API_TOKEN", None) is None:
            raise ValueError("Could not retrieve T212 API token.")
        else:
            self._REQUESTOR.headers = {"Authorization": token}

    def _get(self, url: str, params: dict[str, Any] = None) -> requests.Response:
        return self._REQUESTOR.get(self.server.value + url, params=params)

    def _post(self, url: str, json: dict[str, Any], params: dict[str, Any] = None) -> requests.Response:
        return self._REQUESTOR.post(self.server.value + url, json=json, params=params)

    def _delete(self, url: str, params: dict[str, Any]) -> requests.Response:
        return self._REQUESTOR.delete(self.server.value + url, params=params)

    def get_exchanges(self) -> list[ExchangeDto]:
        response: requests.Response = self._get(EXCHANGES_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            exchanges = response.json()
            return [ExchangeDto(**_) for _ in exchanges]
        else:
            print(f"Request failed with status: {status}.")
            return []

    def get_instruments(self) -> list[InstrumentDto]:
        response: requests.Response = self._get(INSTRUMENTS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            instruments = response.json()
            return [InstrumentDto(**_) for _ in instruments]
        else:
            print(f"Request failed with status: {status}.")
            return []

    def get_pies(self) -> list[PieDto]:
        response: requests.Response = self._get(PIES_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            pies = response.json()
            return [PieDto(**_) for _ in pies]
        else:
            print(f"Request failed with status: {status}.")
            return []

    def create_pie(self, pie: CreatePieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self._post(PIES_URL, json=pie.model_dump())
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            pie = response.json()
            return CreatePieResponseDto(**pie)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def delete_pie(self, pie: PieDto) -> None:
        response: requests.Response = self._delete(PIES_URL, params=pie.model_dump(exclude_unset=True))
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is not T212ApiResponse.OK:
            print(f"Request failed with status: {status}.")

    def get_pie(self, pie: PieDto) -> PieDto:
        response: requests.Response = self._get(PIES_URL, params=pie.model_dump(exclude_unset=True))
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            pie = response.json()
            return PieDto(**pie)
        else:
            print(f"Request failed with status: {status}.")
            return pie

    def update_pie(self, pie: PieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self._post(
            PIES_URL, json=pie.model_dump(exclude=["id"]),
            params=pie.model_dump(include=["id"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            pie = response.json()
            return CreatePieResponseDto(**pie)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def duplicate_pie(self, pie: PieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self._post(
            PIES_URL+pie.id+"/duplicate",
            json=pie.model_dump(include=["icon", "name"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            pie = response.json()
            return CreatePieResponseDto(**pie)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def get_orders(self) -> list[EquityOrderDto]:
        response: requests.Response = self._get(EQUITY_ORDERS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            orders = response.json()
            return [EquityOrderDto(**_) for _ in orders]
        else:
            print(f"Request failed with status: {status}.")
            return []

    def place_limit_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self._post(
            LIMIT_ORDER_URL,
            json=order.model_dump(include=["limitPrice", "quantity", "ticker", "timeValidity"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            order = response.json()
            return EquityOrderDto(**order)
        else:
            print(f"Request failed with status: {status}.")
            return order

    def place_market_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self._post(
            MARKET_ORDER_URL,
            json=order.model_dump(include=["quantity", "ticker"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            order = response.json()
            return EquityOrderDto(**order)
        else:
            print(f"Request failed with status: {status}.")
            return order

    def place_stop_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self._post(
            STOP_ORDER_URL,
            json=order.model_dump(include=["quantity", "stopPrice", "ticker", "timeValidity"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            order = response.json()
            return EquityOrderDto(**order)
        else:
            print(f"Request failed with status: {status}.")
            return order

    def place_stop_limit_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self._post(
            STOP_LIMIT_ORDER_URL,
            json=order.model_dump(include=["limitPrice", "quantity", "stopPrice", "ticker", "timeValidity"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            order = response.json()
            return EquityOrderDto(**order)
        else:
            print(f"Request failed with status: {status}.")
            return order

    def cancel_order(self, order: EquityOrderDto) -> None:
        response: requests.Response = self._delete(
            EQUITY_ORDERS_URL, params=order.model_dump(exclude_unset=True)
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is not T212ApiResponse.OK:
            print(f"Request failed with status: {status}.")

    def get_order(self, order: EquityOrderDto) -> EquityOrderDto:
        response: requests.Response = self._get(
            EQUITY_ORDERS_URL, json=order.model_dump(exclude_unset=True)
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            order = response.json()
            return EquityOrderDto(**order)
        else:
            print(f"Request failed with status: {status}.")
            return order

    def get_account_cash(self) -> AccountCashDto | None:
        response: requests.Response = self._get(ACCOUNT_CASH_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            account = response.json()
            return AccountCashDto(**account)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def get_account_metadata(self) -> AccountMetadataDto | None:
        response: requests.Response = self._get(ACCOUNT_METADATA_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            account = response.json()
            return AccountMetadataDto(**account)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def get_positions(self) -> list[PositionDto]:
        response: requests.Response = self._get(PORTFOLIO_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            positions = response.json()
            return [PositionDto(**_) for _ in positions]
        else:
            print(f"Request failed with status: {status}.")
            return []

    def search_position(self, position: PositionDto) -> PositionDto:
        response: requests.Response = self._post(
            TICKER_URL, json=position.model_dump(include=["ticker"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            position = response.json()
            return PositionDto(**position)
        else:
            print(f"Request failed with status: {status}.")
            return position

    def get_position(self, position: PositionDto) -> PositionDto:
        response: requests.Response = self._get(
            PORTFOLIO_URL, params=position.model_dump(include=["ticker"])
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            position = response.json()
            return PositionDto(**position)
        else:
            print(f"Request failed with status: {status}.")
            return position

    def get_orders(self, filter: HistoricalOrderRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self._get(
            ORDERS_URL, params=filter.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            paginated_response = response.json()
            return PaginatedResponse(**paginated_response)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def get_dividends(self, filter: HistoricalOrderRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self._get(
            DIVIDENDS_URL, params=filter.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            paginated_response = response.json()
            return create_paginated_response(HistoryDividendItem)(**paginated_response)
        else:
            print(f"Request failed with status: {status}.")
            return None

    def get_exports(self) -> list[ExportDataDto]:
        response: requests.Response = self._get(DIVIDENDS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            exports = response.json()
            return [ExportDataDto(**_) for _ in exports]
        else:
            print(f"Request failed with status: {status}.")
            return None

    def export_data(self, settings: ExportCsvDto) -> ExportDataDto:
        response: requests.Response = self._post(EXPORTS_URL, json=settings.model_dump())
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is not T212ApiResponse.OK:
            print(f"Request failed with status: {status}.")

    def get_transactions(self, filter: TransactionsRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self._get(
            TRANSACTIONS_URL, params=filter.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            paginated_response = response.json()
            return create_paginated_response(HistoryTransactionItem)(**paginated_response)
        else:
            print(f"Request failed with status: {status}.")
            return None
