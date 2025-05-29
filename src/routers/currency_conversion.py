from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.schemas.currency_conversion import CurrencyConversionCreate, CurrencyConversionResponse
from src.services.currency_conversion import CurrencyConversionService

router = APIRouter(prefix="/api/v1/currency", tags=["currency"])


@router.post("/conversions", response_model=CurrencyConversionResponse)
def create_conversion(
    data: CurrencyConversionCreate,
    service: CurrencyConversionService = Depends(lambda: CurrencyConversionService()),
):
    try:
        conversion = service.create_conversion(
            user_id=data.user_id,
            source_currency=data.source_currency,
            target_currency=data.target_currency,
            source_amount=data.source_amount,
        )
        return conversion
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except ConnectionError as ce:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(ce))


@router.get("/conversions/{user_id}", response_model=List[CurrencyConversionResponse])
def list_conversions(user_id: str, service: CurrencyConversionService = Depends(lambda: CurrencyConversionService())):
    conversions = service.list_by_user(user_id)
    return conversions
