from typing import List, Optional

from libs.repository import Repository
from src.models import CurrencyConversion


class CurrencyConversionRepository(Repository):
    def create(self, currency_conversion: CurrencyConversion) -> CurrencyConversion:
        self.db.add(currency_conversion)
        self.db.commit()
        self.db.refresh(currency_conversion)
        return currency_conversion

    def get_by_id(self, currency_conversion_id: str) -> Optional[CurrencyConversion]:
        return self.db.query(CurrencyConversion).filter(CurrencyConversion.id == currency_conversion_id).first()

    def list_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[CurrencyConversion]:
        return (
            self.db.query(CurrencyConversion)
            .filter(CurrencyConversion.user_id == user_id)
            .order_by(CurrencyConversion.timestamp.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def update(self, currency_conversion_id: str, **kwargs) -> Optional[CurrencyConversion]:
        currency_conversion = self.get_by_id(currency_conversion_id)
        if not currency_conversion:
            return None

        for key, value in kwargs.items():
            if hasattr(currency_conversion, key):
                setattr(currency_conversion, key, value)

        self.db.commit()
        self.db.refresh(currency_conversion)
        return currency_conversion

    def delete(self, currency_conversion_id: str) -> bool:
        currency_conversion = self.get_by_id(currency_conversion_id)
        if not currency_conversion:
            return False
        self.db.delete(currency_conversion)
        self.db.commit()
        return True
