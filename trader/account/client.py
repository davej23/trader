"""

Account API Client

"""


import requests

from trader.account.constants import ACCOUNT_CASH_URL, ACCOUNT_METADATA_URL
from trader.account.types import AccountCashDto, AccountMetadataDto
from trader._client import _T212Client
from trader.types import T212ApiResponse, T212Server


class AccountClient(_T212Client):
    def __init__(self, server: T212Server) -> None:
        super().__init__(server=server)

    def get_account_cash(self) -> AccountCashDto | None:
        response: requests.Response = self.get(ACCOUNT_CASH_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return AccountCashDto(**data)

        print(f"Request failed with status: {status}.")
        return None

    def get_account_metadata(self) -> AccountMetadataDto | None:
        response: requests.Response = self.get(ACCOUNT_METADATA_URL)
        status: T212ApiResponse = T212ApiResponse(response.status_code)

        if status is T212ApiResponse.OK:
            data = response.json()
            return AccountMetadataDto(**data)

        print(f"Request failed with status: {status}.")
        return None
