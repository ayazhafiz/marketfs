import typing as t

from marketfs.integration.stock_api import get_stock_api
from marketfs.operation.entry import OperationDirectory, OperationEntry
from marketfs.operation.search import SearchDirectory
from marketfs.operation.symbol import SymbolDirectory


class ToplevelDirectory(OperationDirectory):
    def __init__(self):
        super().__init__()
        self.symbols = get_stock_api().list_symbols()
        self._entries["_search"] = SearchDirectory()

    def index(self, path: str) -> t.Optional[OperationEntry]:
        if super().index(path) is None:
            path = path.upper()
            if path in self.symbols:
                self._entries[path] = SymbolDirectory(path)

        return super().index(path)
