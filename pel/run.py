"""
Defines the Pel runner.
"""
import typing
from pathlib import Path

import pel.core
import pel.tasks
from pel.tasks import *


def run(
    *,
    graph: typing.Optional[pel.core.Graph] = None,
    args: typing.Optional[typing.List[str]] = None,
    filename: str = "build.py",
    encoding: str = "utf-8",
) -> int:
    """Runs a Pel build file."""
    if graph is None:
        graph = pel.core.Graph()
    filepath = str((Path.cwd() / filename).absolute())
    try:
        with open(filepath, encoding=encoding) as handle:
            source = handle.read()
    except FileNotFoundError:
        print("Could not find a Pel Build File at:")
        print("\t", filepath, sep="")
        print("\nNeed help writing a Build File?")
        print("You can find instructions at https://github.com/neocrym/pel\n")
        return 1
    exec_globals = {
        key: val for key, val in pel.tasks.__dict__.items() if key in pel.tasks.__all__
    }
    exec(
        compile(source=source, filename=filename, mode="exec"),
        exec_globals,
        exec_globals,
    )
    graph.add_tasks_from_scope(exec_globals)
    parser = pel.core.ArgParser(graph=graph)
    parser.interpret_args(args=args)
    return 0
