import typing as t

from marketfs.operation.entry import OperationDirectory, OperationEntry
from marketfs.operation.search.search import Search
from marketfs.operation.symbol.price import Price
from marketfs.operation.symbol.summary import Summary


class SearchDirectory(OperationDirectory):
    def index(self, query: str) -> t.Optional[OperationEntry]:
        return Search(query)
