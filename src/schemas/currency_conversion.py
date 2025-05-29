from enum import StrEnum

class Currency(StrEnum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"

    @classmethod
    def choices(cls):
        return [currency.value for currency in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.choices()