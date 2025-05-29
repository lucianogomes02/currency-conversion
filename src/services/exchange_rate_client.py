import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv

from src.schemas.currency_conversion import Currency

load_dotenv()


class ExchangeRateService:
    BASE_URL = os.getenv("EXCHANGE_API_BASE_URL")

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_rates(self, base_currency: "Currency") -> Optional[Dict[str, float]]:
        params = {"base": base_currency}

        if self.api_key:
            params["access_key"] = self.api_key

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("rates")
        except requests.RequestException as e:
            print(f"[ERROR] Erro ao buscar taxas de câmbio: {e}")
            return None
