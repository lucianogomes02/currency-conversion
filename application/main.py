from fastapi import FastAPI

from src.routers import currency_conversion

api = FastAPI()

api.include_router(currency_conversion.router)
