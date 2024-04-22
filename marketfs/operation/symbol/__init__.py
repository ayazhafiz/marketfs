from marketfs.operation.entry import OperationDirectory
from marketfs.operation.symbol.price import Price
from marketfs.operation.symbol.summary import Summary


class SymbolDirectory(OperationDirectory):
    def __init__(self, symbol: str):
        super().__init__()
        self._entries = {"_summary": Summary(symbol), "price": Price(symbol)}
