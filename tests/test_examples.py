# pylint: disable=import-outside-toplevel
"""Tests for the examples/ subdirectories."""
import concurrent.futures  # pylint: disable=unused-import
import os
import typing  # pylint: disable=unused-import
from pathlib import Path

import pytest

from tests import EXECUTOR


def get_example_dir(example_name: str) -> str:
    """Return the absolute path of a given example subdirectory."""
    return str(Path(__file__).parent.parent / "examples" / example_name)


def sp_simple_all() -> None:
    """Run all tasks in the `simple` example."""
    import pel.core
    import pel.run

    os.chdir(get_example_dir("simple"))
    graph = pel.core.Graph()
    exit_code = pel.run.run(graph=graph, args=["--all"])
    assert exit_code == 0
    assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("second")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("third")._executed == pel.core.TaskExecuted.EXECUTED


def sp_simple_only_third() -> None:
    """Run `third` task and deps in the `simple` example."""
    import pel.core
    import pel.run

    os.chdir(get_example_dir("simple"))
    graph = pel.core.Graph()
    exit_code = pel.run.run(graph=graph, args=["third"])
    assert exit_code == 0
    assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.NOT_RUN
    assert graph.get_task("second")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("third")._executed == pel.core.TaskExecuted.EXECUTED


def sp_simple_only_first() -> None:
    """Run only the `first` task in the `simple` example."""
    import pel.core
    import pel.run

    os.chdir(get_example_dir("simple"))
    graph = pel.core.Graph()
    exit_code = pel.run.run(graph=graph, args=["first"])
    assert exit_code == 0
    assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
    assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.NOT_RUN
    assert graph.get_task("second")._executed == pel.core.TaskExecuted.NOT_RUN
    assert graph.get_task("third")._executed == pel.core.TaskExecuted.NOT_RUN


FUTURES = {
    key: EXECUTOR.submit(func)
    for key, func in globals().items()
    if key.startswith("sp_")
}


@pytest.mark.parametrize("name,future", FUTURES.items())  # type: ignore
# pylint: disable=unused-argument
def test_future(name: str, future: "concurrent.futures.Future[typing.Any]") -> None:
    """Wait on the futures that we launched."""
    future.result()
