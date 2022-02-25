"""
Useful Pel tasks.
"""
__all__ = [
    "Shell",
]

import subprocess
from typing import Any, List, NamedTuple, Union

from pel.core import Task
from pel.filesystem import any_source_newer_or_eq_than_target
from pel.types import enforce_list_of_str


class ShellResult(NamedTuple):
    """The result of a single shell command."""

    cmd: str
    proc: "Union[subprocess.CompletedProcess[bytes], subprocess.CompletedProcess[str]]"


class Shell(Task):
    """Run a shell command."""

    cmd: Union[str, List[str]]
    src: Union[str, List[str]] = ""
    target: Union[str, List[str]] = ""
    text: bool = False
    quiet: bool = False
    check: bool = False

    @classmethod
    def is_expired(cls) -> bool:
        if cls.src and cls.target:
            sources = enforce_list_of_str(cls.src)
            targets = enforce_list_of_str(cls.target)
            return any_source_newer_or_eq_than_target(sources=sources, targets=targets)
        return True

    @classmethod
    def run(cls) -> Any:
        cmds = enforce_list_of_str(cls.cmd)
        return [
            ShellResult(
                cmd=cmd,
                proc=subprocess.run(
                    cmds,
                    shell=True,
                    text=cls.text,
                    capture_output=cls.quiet,
                    check=cls.check,
                ),
            )
            for cmd in cmds
        ]
