"""

Pies API Client

"""


import requests

from trader.pies.constants import PIES_URL
from trader.pies.types import PieDto, CreatePieDto, CreatePieResponseDto
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server


class PiesClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_pies(self) -> list[PieDto]:
        response: requests.Response = self.get(PIES_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return [PieDto(**_) for _ in data]

        print(f"Request failed with status: {status}.")
        return []

    def create_pie(self, pie: CreatePieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self.post(PIES_URL, json=pie.model_dump())
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return CreatePieResponseDto(**data)

        print(f"Request failed with status: {status}.")
        return None

    def delete_pie(self, pie: PieDto) -> None:
        response: requests.Response = self.delete(
            PIES_URL, params=pie.model_dump(exclude_unset=True)
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is not T212ApiResponse.OK:
            print(f"Request failed with status: {status}.")

    def get_pie(self, pie: PieDto) -> PieDto:
        response: requests.Response = self.get(PIES_URL, params=pie.model_dump(exclude_unset=True))
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return PieDto(**data)

        print(f"Request failed with status: {status}.")
        return pie

    def update_pie(self, pie: PieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self.post(
            PIES_URL, json=pie.model_dump(exclude={"id"}),
            params=pie.model_dump(include={"id"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return CreatePieResponseDto(**data)

        print(f"Request failed with status: {status}.")
        return None

    def duplicate_pie(self, pie: PieDto) -> CreatePieResponseDto | None:
        response: requests.Response = self.post(
            PIES_URL+str(pie.id)+"/duplicate",
            json=pie.model_dump(include={"icon", "name"})
        )
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return CreatePieResponseDto(**data)

        print(f"Request failed with status: {status}.")
        return None
