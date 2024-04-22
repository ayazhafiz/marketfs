from contextlib import contextmanager
from requests_cache import CachedSession
import typing as t
from urllib.parse import urlencode

from marketfs.integration.stock_api.api import (
    Capitalization,
    Dollars,
    Percent,
    Profile,
    Quote,
    SearchResult,
    StockApi,
)

API_URL = "https://api.finnhub.io/api/v1"
DEFAULT_CACHE_EXPIRY_SECONDS = 600


class FinnhubApi(StockApi):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = CachedSession(
            cache_control=True,
            expire_after=DEFAULT_CACHE_EXPIRY_SECONDS,
        )

    def _get(self, path, *, params, cached: bool):
        with self._cache(cached):
            response = self.session.get(
                f"{API_URL}{path}",
                params={**params, "token": self.api_key},
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    @contextmanager
    def _cache(self, cached: bool):
        if not cached:
            with self.session.cache_disabled():
                yield
        else:
            yield

    def list_symbols(self):
        symbols = self._get("/stock/symbol", params=dict(exchange="US"), cached=True)
        return set(map(lambda s: s["symbol"], symbols))

    def quote(self, symbol: str) -> Quote:
        r = self._get("/quote", params=dict(symbol=symbol), cached=False)
        return Quote(
            current_price=Dollars(r["c"]),
            percent_change=Percent(r["dp"]),
            daily_high=Dollars(r["h"]),
            daily_low=Dollars(r["l"]),
            daily_open=Dollars(r["o"]),
            previous_close=Dollars(r["pc"]),
        )

    def capitalization(self, symbol: str) -> Capitalization:
        r = self._get("/stock/profile2", params=dict(symbol=symbol), cached=True)
        return Capitalization(market_capitalization=Dollars(r["marketCapitalization"]))

    def profile(self, symbol: str) -> Profile:
        r = self._get("/stock/profile2", params=dict(symbol=symbol), cached=True)
        return Profile(name=r["name"], exchange=r["exchange"], website_url=r["weburl"])

    def search(self, query: str) -> t.List[SearchResult]:
        def _to_search_result(r):
            return SearchResult(
                symbol=r["symbol"],
                description=r["description"],
                type=r["type"],
            )

        r = self._get("/search", params=dict(q=query), cached=True)
        return list(map(_to_search_result, r.get("result", [])))
