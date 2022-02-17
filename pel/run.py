"""
Defines the Pel runner.

This module is used by the :py:mod:`pel.console` module,
which makes sure to set :py:attr:`pel.core.DEFAULT_GRAPH` first.

"""
from pathlib import Path
import typing

import pel.core
import pel.tasks


def run(
    *,
    graph: typing.Optional[pel.core.Graph] = None,
    filename: str = "build.py",
    encoding: str = "utf-8",
) -> int:
    """Runs a Pel build file."""
    filepath = str((Path.cwd() / filename).absolute())
    try:
        with open(filepath, encoding=encoding) as handle:
            build_py = handle.read()
    except FileNotFoundError:
        print(f"Could not find a Pel Build File at:")
        print("\t", filepath, sep="")
        print("\nNeed help writing a Build File?")
        print("You can find instructions at https://github.com/neocrym/pel\n")
        return 1
    exec(
        build_py,
        # Put our Pel Task constructor classes in our build script's
        # GLOBAL namespace.
        {
            key: val
            for key, val in pel.tasks.__dict__.items()
            if key in pel.tasks.__all__
        },
    )
    parser = pel.core.ArgParser(graph=graph)
    parser.interpret_args()
    return 0