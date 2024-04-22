import typing as t

from marketfs.integration.stock_api import get_stock_api
from marketfs.operation.entry import OperationFile


class Price(OperationFile):
    can_read = True

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def _read(self) -> str:
        quote = get_stock_api().quote(self.symbol)
        return str(quote.current_price)
