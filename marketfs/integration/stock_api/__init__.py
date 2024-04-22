import functools
import os

from marketfs.integration.stock_api.api import StockApi
from marketfs.integration.stock_api.finnhub import FinnhubApi


@functools.cache
def get_stock_api() -> StockApi:
    match os.environ["STOCK_API_STRATEGY"]:
        case "finnhub":
            return FinnhubApi(api_key=os.environ["FINNHUB_API_KEY"])
        case other:
            raise ValueError(f"Unknown STOCK_API_STRATEGY {other}")
