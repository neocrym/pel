"""Utilities for filesystem tasks."""
import os
import stat
from typing import Iterator, Optional, Tuple


def path_iterator(root: str) -> Iterator[Tuple[str, float]]:
    """
    Iterates over the filesystem in top-down order, yielding
    tuples of ``(filenames, last_modified)`` times.

    The iterator includes the root path.
    """

    # pylint: disable=unused-argument
    def _path_iterator(
        path: str, _last_mod: Optional[float] = None
    ) -> Iterator[Tuple[str, float]]:
        """Internal iterator for yielding subdirectories."""
        with os.scandir(path) as scandir_iter:
            dir_paths = []
            for obj in scandir_iter:
                obj_stat = obj.stat(follow_symlinks=True)
                yield (obj.path, obj_stat.st_mtime)
                if obj.is_dir():
                    dir_paths.append(obj.path)
            for dir_path in dir_paths:
                yield from path_iterator(dir_path)

    root_abspath = os.path.abspath(root)
    root_stat = os.stat(root_abspath, follow_symlinks=True)
    yield (root_abspath, root_stat.st_mtime)
    if stat.S_ISDIR(os.stat(root_abspath).st_mode):
        yield from _path_iterator(root_abspath)


def filesystem_path_is_not_older_than(path: str, last_modified: float) -> bool:
    """
    Returns ``True`` if any file or directory in ``path``
    has a modification time >= ``last_modified``.

    This function also checks the ``path`` directory itself.
    """
    for _, path_last_mod in path_iterator(path):
        if path_last_mod >= last_modified:
            return True
    return False


def filesystem_target_is_older_than_source(*, source: str, target: str) -> bool:
    """
    Return True if ``target`` is newer than ``source``.
    """
    newest_target_lm: Optional[float] = None
    try:
        for _, iter_lm in path_iterator(target):
            if newest_target_lm is None or newest_target_lm < iter_lm:
                newest_target_lm = iter_lm
    except FileNotFoundError:
        return True
    if newest_target_lm is None:
        return True
    return filesystem_path_is_not_older_than(source, newest_target_lm)
