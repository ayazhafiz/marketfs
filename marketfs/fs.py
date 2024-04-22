import errno
import fuse
import stat
from time import time
import typing as t

from marketfs.operation import (
    OperationDirectory,
    OperationFile,
    parse_operation_entry,
)
from marketfs.operation.entry import OperationEntry


class MarketFs(fuse.Operations):
    fds: t.List[OperationEntry] = []

    def access(self, path, amode):
        self._path_entry(path)

    def getattr(self, path, fh=None):
        entry = self._path_entry(path)

        data = dict(
            st_nlink=1,
            st_size=0,
        )

        if isinstance(entry, OperationDirectory):
            st_mode = stat.S_IFDIR
        elif isinstance(entry, OperationFile):
            st_mode = stat.S_IFREG
            st_mode |= entry.can_read and 0o444
            st_mode |= entry.can_write and 0o222
            st_mode |= entry.can_execute and 0o111

            if entry.can_read:
                data["st_size"] = len(entry.read())
        else:
            raise fuse.FuseOSError(errno.EACCES)

        return dict(
            **data,
            st_mode=st_mode,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
        )

    def listxattr(self, path):
        return []

    def open(self, path, flags):
        file = self._path_file(path)

        if not file.can_read:
            raise fuse.FuseOSError(errno.EACCES)
        if not file.can_write and flags & (fuse.os.O_WRONLY | fuse.os.O_RDWR) != 0:
            raise fuse.FuseOSError(errno.EACCES)

        self.fds.append(file)
        return len(self.fds) - 1

    def read(self, path, size, offset, fh):
        file = self._path_file(path)
        return file.read()[offset : offset + size].encode()

    def readdir(self, path, fh):
        dir = self._path_dir(path)
        return list(dir.ls().keys())

    def _path_entry(self, path):
        op = parse_operation_entry(path)
        if op is None:
            raise fuse.FuseOSError(errno.ENOENT)
        return op

    def _path_file(self, path):
        entry = self._path_entry(path)
        if not isinstance(entry, OperationFile):
            raise fuse.FuseOSError(errno.EACCES)
        return entry

    def _path_dir(self, path):
        entry = self._path_entry(path)
        if not isinstance(entry, OperationDirectory):
            raise fuse.FuseOSError(errno.EACCES)
        return entry
