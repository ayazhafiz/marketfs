import typing as t
from tabulate import tabulate

from marketfs.integration.stock_api import get_stock_api
from marketfs.operation.entry import OperationFile


class Summary(OperationFile):
    can_read = True

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def _read(self) -> str:
        quote = get_stock_api().quote(self.symbol)
        cap = get_stock_api().capitalization(self.symbol)
        profile = get_stock_api().profile(self.symbol)
        rows = [
            ("Current price", quote.current_price),
            ("% change", quote.percent_change),
            ("Daily high", quote.daily_high),
            ("Daily low", quote.daily_low),
            ("Open", quote.daily_open),
            ("Previous close", quote.previous_close),
            ("Market cap", cap.market_capitalization),
            ("Exchange", profile.exchange),
            ("Company name", profile.name),
            ("Company website", profile.website_url),
        ]
        return tabulate(rows, tablefmt="plain")
