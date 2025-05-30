from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.schemas.currency_conversion import CurrencyConversionCreate, CurrencyConversionResponse
from src.services.currency_conversion import CurrencyConversionService

router = APIRouter(prefix="/api/v1/currency", tags=["currency"])


@router.post(
    "/conversions",
    response_model=CurrencyConversionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new currency conversion",
    description="Creates a currency conversion by converting a given amount from the source currency to the target currency.",
    responses={
        201: {"description": "Conversion created successfully."},
        400: {"description": "Invalid input data or business validation error."},
        503: {"description": "External service (e.g., currency API) unavailable."},
    },
)
def create_conversion(
    data: CurrencyConversionCreate,
    service: CurrencyConversionService = Depends(lambda: CurrencyConversionService()),
):
    """
    Converts a specified amount from the source currency to the target currency
    and stores the conversion in the system.

    - **user_id**: ID of the user requesting the conversion
    - **source_currency**: Currency code to convert from (e.g. USD)
    - **target_currency**: Currency code to convert to (e.g. EUR)
    - **source_amount**: The amount to be converted
    """
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


@router.get(
    "/conversions/{user_id}",
    response_model=List[CurrencyConversionResponse],
    summary="List currency conversions by user",
    description="Retrieves a list of all currency conversions associated with a given user ID.",
    responses={
        200: {"description": "List of conversions successfully retrieved."},
        404: {"description": "User not found or has no conversions."},
    },
)
def list_conversions(
    user_id: str,
    service: CurrencyConversionService = Depends(lambda: CurrencyConversionService()),
):
    """
    Returns all currency conversion records for the specified user.

    - **user_id**: The unique identifier of the user
    """
    conversions = service.list_by_user(user_id)
    if not conversions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No conversions found for this user.")
    return conversions
