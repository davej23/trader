"""

Account-related dataclasses

"""


from pydantic import BaseModel
from pydantic_extra_types.currency_code import Currency


class AccountCashDto(BaseModel):
    blocked: float
    free: float
    invested: float
    pieCash: float
    ppl: float
    result: float
    total: float


class AccountMetadataDto(BaseModel):
    currencyCode: Currency
    id: int
