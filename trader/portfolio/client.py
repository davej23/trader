"""

Portfolio API Client

"""


import requests

from trader.portfolio.constants import PORTFOLIO_URL, TICKER_URL
from trader.portfolio.types import PositionDto
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server


class PortfolioClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_positions(self) -> list[PositionDto]:
        response: requests.Response = self.get(PORTFOLIO_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [PositionDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []

    def search_position(self, position: PositionDto) -> PositionDto:
        response: requests.Response = self.post(
            TICKER_URL, json=position.model_dump(include={"ticker"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return PositionDto(**data)

        print(f"Request failed with status: {status}.")
        return position

    def get_position(self, position: PositionDto) -> PositionDto:
        response: requests.Response = self.get(
            PORTFOLIO_URL, params=position.model_dump(include={"ticker"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return PositionDto(**data)

        print(f"Request failed with status: {status}.")
        return position
