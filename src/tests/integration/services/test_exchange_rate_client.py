import pytest

from src.schemas.currency_conversion import Currency
from src.services.exchange_rate_client import ExchangeRateService


def test_get_rates_returns_data():
    service = ExchangeRateService()
    rates = service.get_rates(base_currency=Currency.EUR)

    assert isinstance(rates, dict)
    assert Currency.USD in rates
    assert rates[Currency.USD] > 0


def test_get_rates_handles_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Exception("Simulated failure")

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(Exception, match="Simulated failure"):
        service = ExchangeRateService()
        result = service.get_rates(base_currency=Currency.EUR)
        assert result is None
