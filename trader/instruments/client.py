"""

Instruments API Client

"""


import requests

from trader.instruments.constants import EXCHANGES_URL, INSTRUMENTS_URL
from trader.instruments.types import ExchangeDto, InstrumentDto
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server


class InstrumentsClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_exchanges(self) -> list[ExchangeDto]:
        response: requests.Response = self.get(EXCHANGES_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [ExchangeDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []

    def get_instruments(self) -> list[InstrumentDto]:
        response: requests.Response = self.get(INSTRUMENTS_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [InstrumentDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []
