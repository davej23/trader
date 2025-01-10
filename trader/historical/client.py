"""

Historical Data API Client

"""


import requests

from trader.historical.constants import (
    ORDERS_URL,
    DIVIDENDS_URL,
    EXPORTS_URL,
    TRANSACTIONS_URL
)
from trader.historical.types import (
    HistoricalOrderDto,
    HistoricalOrderRequestDto,
    HistoricalDividendItemDto,
    HistoricalTransactionItemDto,
    TransactionsRequestDto,
    ExportCsvDto,
    ExportDataDto
)
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server, PaginatedResponse, create_paginated_response


class HistoricalClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_orders(self, settings: HistoricalOrderRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self.get(
            ORDERS_URL, params=settings.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return create_paginated_response(HistoricalOrderDto)(**data)

        print(f"Request failed with status: {status}.")
        return None

    def get_dividends(self, settings: HistoricalOrderRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self.get(
            DIVIDENDS_URL, params=settings.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return create_paginated_response(HistoricalDividendItemDto)(**data)

        print(f"Request failed with status: {status}.")
        return None

    def get_exports(self) -> list[ExportDataDto]:
        response: requests.Response = self.get(DIVIDENDS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [ExportDataDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []

    def export_data(self, settings: ExportCsvDto) -> ExportDataDto | None:
        response: requests.Response = self.post(EXPORTS_URL, json=settings.model_dump())
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return ExportDataDto(**data)

        print(f"Request failed with status: {status}.")
        return None

    def get_transactions(self, settings: TransactionsRequestDto) -> PaginatedResponse | None:
        response: requests.Response = self.get(
            TRANSACTIONS_URL, params=settings.model_dump()
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return create_paginated_response(HistoricalTransactionItemDto)(**data)

        print(f"Request failed with status: {status}.")
        return None
