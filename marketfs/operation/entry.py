import abc
import typing as t

OperationEntry = t.Union["OperationFile", "OperationDirectory"]


class OperationFile(abc.ABC):
    can_read: bool = False
    can_write: bool = False
    can_execute: bool = False

    def read(self) -> str:
        data = self._read()
        if not data.endswith("\n"):
            data += "\n"
        return data

    @abc.abstractmethod
    def _read(self) -> str:
        raise NotImplementedError()


class OperationDirectory(abc.ABC):
    _entries: t.Dict[str, OperationEntry] = {}

    def index(self, operation: str) -> t.Optional[OperationEntry]:
        return self._entries.get(operation)

    def ls(self) -> t.Dict[str, OperationEntry]:
        return dict(self._entries)
