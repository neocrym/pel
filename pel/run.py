"""
Defines the Pel runner.

This module is used by the :py:mod:`pel.console` module,
which makes sure to set :py:attr:`pel.core.DEFAULT_GRAPH` first.

"""
import typing

import pel.core
import pel.tasks


def run(
    *,
    graph: typing.Optional[pel.core.Graph] = None,
    filename: str = "build.py",
    encoding: str = "utf-8",
) -> None:
    """Runs a Pel build file."""
    with open(filename, encoding=encoding) as handle:
        build_py = handle.read()
    exec(
        build_py,
        # Put our Pel Task constructor classes in our build script's
        # GLOBAL namespace.
        {
            key: val
            for key, val in pel.tasks.__dict__.items()
            if key in pel.tasks.__all__
        },
        # Do not pass anything to the LOCAL namespace.
        {},
    )
    parser = pel.core.ArgParser(graph=graph)
    parser.interpret_args()
