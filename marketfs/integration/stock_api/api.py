import abc
import typing as t


class Dollars:
    def __init__(self, dollars: float) -> None:
        self.dollars = dollars

    def __str__(self):
        return f"${self.dollars:.2f}"


class Percent:
    def __init__(self, percent: float) -> None:
        self.percent = percent

    def __str__(self):
        return f"{self.percent:.2f}%"


class Quote(t.NamedTuple):
    current_price: Dollars
    percent_change: Percent
    daily_high: Dollars
    daily_low: Dollars
    daily_open: Dollars
    previous_close: Dollars


class Capitalization(t.NamedTuple):
    market_capitalization: Dollars


class Profile(t.NamedTuple):
    name: str
    exchange: str
    website_url: str


class SearchResult(t.NamedTuple):
    symbol: str
    description: str
    type: str


class StockApi(abc.ABC):
    @abc.abstractmethod
    def list_symbols(self) -> t.Set[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def quote(self, symbol: str) -> Quote:
        raise NotImplementedError()

    @abc.abstractmethod
    def capitalization(self, symbol: str) -> Capitalization:
        raise NotImplementedError()

    @abc.abstractmethod
    def profile(self, symbol: str) -> Profile:
        raise NotImplementedError()

    @abc.abstractmethod
    def search(self, query: str) -> t.List[SearchResult]:
        raise NotImplementedError()
