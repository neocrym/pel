"""Utilities for testing."""
import os
from pathlib import Path
from typing import Union


def set_path_times(
    path: Path, *, access: Union[int, float], mod: Union[int, float]
) -> None:
    """
    Set the access and modification time for a local file. Not recursive.

    Args:
        path: The file or directory to change.

        access: The access time to set, as a Unix timestamp.

        mod: The file modification time to set, as a Unix timestamp.
    """
    os.utime(str(path), times=(access, mod), follow_symlinks=True)


def delete_file(path: Path) -> None:
    """Delete the file at the path, ignoring if the file not found."""
    try:
        path.unlink()
    except FileNotFoundError:
        pass
