"""
Useful Pel tasks.
"""
__all__ = [
    "Shell",
]

import subprocess
from typing import Any, List, NamedTuple, Union

from pel.core import Task
from pel.filesystem import filesystem_target_is_older_than_source


class ShellResult(NamedTuple):
    """The result of a single shell command."""

    cmd: str
    proc: "Union[subprocess.CompletedProcess[bytes], subprocess.CompletedProcess[str]]"


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
    def run(cls) -> Any:
        if isinstance(cls.cmd, str):
            cmds = [cls.cmd]
        else:
            cmds = cls.cmd
        return [
            ShellResult(
                cmd=cmd,
                proc=subprocess.run(
                    cmd,
                    shell=True,
                    text=cls.text,
                    capture_output=cls.quiet,
                    check=cls.check,
                ),
            )
            for cmd in cmds
        ]
