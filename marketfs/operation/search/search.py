from tabulate import tabulate

from marketfs.integration.stock_api import get_stock_api
from marketfs.operation.entry import OperationFile


class Search(OperationFile):
    can_read = True

    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query

    def _read(self) -> str:
        results = get_stock_api().search(self.query)
        return tabulate(
            map(lambda r: [r.symbol, r.description, r.type], results),
            headers=["Symbol", "Description", "Type"],
        )
