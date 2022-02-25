"""Tests for examples/simple."""
import os
import unittest
from pathlib import Path

import pel.core
import pel.run


class TestSimple(unittest.TestCase):
    """Tests for examples/simple."""

    def setUp(self) -> None:
        self.example_path: Path = (
            Path(__file__).parent.parent.parent / "examples" / "simple"
        )
        self.old_path: str = os.getcwd()
        os.chdir(str(self.example_path))

    def tearDown(self) -> None:
        os.chdir(self.old_path)

    def test_all(self) -> None:
        """Check that all tasks in the graph are run."""
        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("second")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("third")._executed == pel.core.TaskExecuted.EXECUTED

    def test_only_third(self) -> None:
        """Check that we can run only the third task.."""
        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["third"])
        assert exit_code == 0
        assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.NOT_RUN
        assert graph.get_task("second")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("third")._executed == pel.core.TaskExecuted.EXECUTED

    def test_only_first(self) -> None:
        """Check that we can run only the first task.."""
        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["first"])
        assert exit_code == 0
        assert graph.get_task("first")._executed == pel.core.TaskExecuted.EXECUTED
        assert graph.get_task("other_first")._executed == pel.core.TaskExecuted.NOT_RUN
        assert graph.get_task("second")._executed == pel.core.TaskExecuted.NOT_RUN
        assert graph.get_task("third")._executed == pel.core.TaskExecuted.NOT_RUN
