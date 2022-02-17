"""
Useful Pel tasks.
"""
__all__ = [
    "Shell",
]

import subprocess
from typing import List, Union

from pel.core import Task
from pel.filesystem import filesystem_target_is_older_than_source


class Shell(Task):
    """Run a shell command."""

    cmd: Union[str, List[str]]
    src: str = ""
    target: str = ""
    text: bool = False
    quiet: bool = False
    check: bool = False

    @classmethod
    def is_expired(cls) -> bool:
        if cls.src and cls.target:
            return filesystem_target_is_older_than_source(
                source=cls.src, target=cls.target
            )
        return True

    @classmethod
    def run(cls) -> None:
        if isinstance(cls.cmd, str):
            cmds = [cls.cmd]
        else:
            cmds = cls.cmd
        for cmd in cmds:
            subprocess.run(
                cmd,
                shell=True,
                text=cls.text,
                capture_output=cls.quiet,
                check=cls.check,
            )
