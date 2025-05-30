import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from src.models import CurrencyConversion
from src.schemas.currency_conversion import Currency, CurrencyConversionResponse
from src.services.currency_conversion import CurrencyConversionService


def test_list_by_user_returns_response_models():
    service = CurrencyConversionService()
    user_id = str(uuid.uuid4())
    mock_record = CurrencyConversion(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source_currency=Currency.USD,
        source_amount=100.0,
        target_currency=Currency.EUR,
        target_amount=90.0,
        rate=0.9,
        timestamp=datetime.now(timezone.utc),
    )
    service.repo.list_by_user = MagicMock(return_value=[mock_record])

    result = service.list_by_user(user_id)

    assert len(result) == 1
    assert isinstance(result[0], CurrencyConversionResponse)
    assert result[0].user_id == user_id


def test_create_conversion_with_unsupported_currency():
    service = CurrencyConversionService()
    user_id = str(uuid.uuid4())

    try:
        service.create_conversion(
            user_id=user_id,
            source_currency="XXX",
            target_currency=Currency.EUR,
            source_amount=100.0,
        )
    except ValueError as e:
        assert "Supported currencies are:" in str(e)


@patch("src.services.currency_conversion.ExchangeRateService.get_rates", return_value=None)
def test_create_conversion_fails_when_api_down(mock_rates):
    service = CurrencyConversionService()

    try:
        service.create_conversion(
            user_id="abc123",
            source_currency=Currency.USD,
            target_currency=Currency.BRL,
            source_amount=100.0,
        )
    except ConnectionError as e:
        assert str(e) == "Failed to fetch exchange rates"
