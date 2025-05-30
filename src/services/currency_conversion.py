from datetime import datetime, timezone
from typing import List

from src.models import CurrencyConversion
from src.repository.currency_conversion import CurrencyConversionRepository
from src.schemas.currency_conversion import Currency, CurrencyConversionResponse
from src.services.exchange_rate_client import ExchangeRateService


class CurrencyConversionService:
    def __init__(self):
        self.exchange_rate_service = ExchangeRateService()
        self.repo = CurrencyConversionRepository()

    def list_by_user(self, user_id: str) -> List[CurrencyConversionResponse]:
        records = self.repo.list_by_user(user_id=user_id)
        return [CurrencyConversionResponse.model_validate(record) for record in records]

    def create_conversion(
        self, user_id: str, source_currency: Currency, target_currency: Currency, source_amount: float
    ) -> CurrencyConversionResponse:
        if not Currency.is_a_supported_currency(source_currency) or not Currency.is_a_supported_currency(
            target_currency
        ):
            raise ValueError(f"Supported currencies are: {Currency.supported_currencies()}")

        if source_currency == target_currency:
            rate = 1.0
            target_amount = source_amount
        else:
            rates = self.exchange_rate_service.get_rates(base_currency=Currency.EUR)
            if rates is None:
                raise ConnectionError("Failed to fetch exchange rates")

            if source_currency == Currency.EUR:
                amount_in_eur = source_amount
            else:
                rate_source_to_eur = 1 / rates.get(source_currency)
                amount_in_eur = source_amount * rate_source_to_eur

            if target_currency == Currency.EUR:
                target_amount = amount_in_eur
            else:
                rate_eur_to_target = rates.get(target_currency)
                target_amount = amount_in_eur * rate_eur_to_target

            rate = target_amount / source_amount if source_amount != 0 else 0.0

        transaction = CurrencyConversion(
            user_id=user_id,
            source_currency=source_currency,
            source_amount=source_amount,
            target_currency=target_currency,
            target_amount=target_amount,
            rate=rate,
            timestamp=datetime.now(timezone.utc),
        )

        created = self.repo.create(transaction)
        return CurrencyConversionResponse.model_validate(created)
