import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy import Enum as SQLEnum

from application.database import Base
from src.schemas.currency_conversion import Currency


class CurrencyConversion(Base):
    __tablename__ = "currency_conversions"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True)
    source_currency = Column(SQLEnum(Currency, name="currency_enum"))
    source_amount = Column(Float)
    target_currency = Column(SQLEnum(Currency, name="currency_enum"))
    target_amount = Column(Float)
    rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
