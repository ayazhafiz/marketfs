import typing as t

from fuse import os

from marketfs.operation.entry import OperationEntry, OperationDirectory, OperationFile
from marketfs.operation.toplevel_directory import ToplevelDirectory


def parse_operation_entry(path: str) -> t.Optional[OperationEntry]:
    parts = os.path.normpath(path).split(os.path.sep)[1:]
    if parts[-1] == "":
        parts.pop()

    entry: t.Optional[OperationEntry] = ToplevelDirectory()
    for part in parts:
        if isinstance(entry, OperationFile):
            return None
        entry = entry.index(part)
        if entry is None:
            return None
    return entry
