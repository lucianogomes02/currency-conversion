from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Currency(StrEnum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"

    @classmethod
    def supported_currencies(cls):
        return [currency.value for currency in cls]

    @classmethod
    def is_a_supported_currency(cls, value: str) -> bool:
        return value in cls.choices()

class CurrencyConversionCreate(BaseModel):
    user_id: str
    source_currency: Currency
    target_currency: Currency
    source_amount: float


class CurrencyConversionResponse(BaseModel):
    id: str
    user_id: str
    source_currency: Currency
    source_amount: float
    target_currency: Currency
    target_amount: float
    rate: float
    timestamp: datetime

    class Config:
        orm_mode = True
