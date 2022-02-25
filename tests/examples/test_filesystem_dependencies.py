"""Tests for examples/filesystem-dependencies."""
import os
import unittest
from pathlib import Path

import pel.core
import pel.run
from tests.util import delete_file, set_path_times

NEWEST = 1000
NEW = 100
OLD = 1


class TestFilesystemDependencies(unittest.TestCase):
    """Tests for examples/filesystem-dependencies."""

    def setUp(self) -> None:
        self.example_path: Path = (
            Path(__file__).parent.parent.parent / "examples" / "filesystem-dependencies"
        )
        self.old_path: str = os.getcwd()
        os.chdir(str(self.example_path))

        self.src1_path = Path(self.example_path / "src1")
        self.src1_file_1_path = Path(self.example_path / "src1" / "file1.txt")
        self.src2_path = Path(self.example_path / "src2")
        self.src2_file_2_path = Path(self.example_path / "src2" / "file2.txt")
        self.src3_path = Path(self.example_path / "src3")
        self.src3_file_3_path = Path(self.example_path / "src3" / "file3.txt")
        self.outputs_file_1_path = Path(
            self.example_path / "outputs" / "output-file-1.txt"
        )
        self.outputs_file_2_path = Path(
            self.example_path / "outputs" / "output-file-2.txt"
        )

    def tearDown(self) -> None:
        delete_file(self.outputs_file_2_path)
        os.chdir(self.old_path)

    def test_third_runs(self) -> None:
        """Check that the task runs when inputs are newer than outputs."""
        set_path_times(self.src2_path, access=OLD, mod=NEW)
        set_path_times(self.src2_file_2_path, access=OLD, mod=NEW)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)
        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("third")._executed == pel.core.TaskExecuted.EXECUTED

    def test_third_does_not_run(self) -> None:
        """Check that the task does not run when outputs are newer than inputs."""
        set_path_times(self.src2_path, access=NEW, mod=OLD)
        set_path_times(self.src2_file_2_path, access=NEW, mod=OLD)
        set_path_times(self.outputs_file_1_path, access=OLD, mod=NEW)
        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("third")._executed == pel.core.TaskExecuted.NOT_EXPIRED

    def test_output_file_does_not_exist(self) -> None:
        """Check that the task runs because outputs_file_2_path is missing."""
        set_path_times(self.src1_path, access=OLD, mod=NEW)
        set_path_times(self.src1_file_1_path, access=OLD, mod=NEW)
        set_path_times(self.src2_path, access=OLD, mod=NEW)
        set_path_times(self.src2_file_2_path, access=OLD, mod=NEW)
        set_path_times(self.src3_file_3_path, access=OLD, mod=NEW)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)

        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("fourth")._executed == pel.core.TaskExecuted.EXECUTED

    def test_run_outputs_older_than_inputs(self) -> None:
        """Check that the task runs because both output files are older than input files."""
        set_path_times(self.src1_path, access=OLD, mod=NEW)
        set_path_times(self.src1_file_1_path, access=OLD, mod=NEW)
        set_path_times(self.src2_path, access=OLD, mod=NEW)
        set_path_times(self.src2_file_2_path, access=OLD, mod=NEW)
        set_path_times(self.src3_file_3_path, access=OLD, mod=NEW)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)
        self.outputs_file_2_path.touch()
        set_path_times(self.outputs_file_2_path, access=NEW, mod=OLD)

        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("fourth")._executed == pel.core.TaskExecuted.EXECUTED

    def test_run_outputs_file_1_older(self) -> None:
        """Check that the task runs because output_file_1_path is older than inputs."""
        set_path_times(self.src1_path, access=OLD, mod=NEW)
        set_path_times(self.src1_file_1_path, access=OLD, mod=NEW)
        set_path_times(self.src2_path, access=OLD, mod=NEW)
        set_path_times(self.src2_file_2_path, access=OLD, mod=NEW)
        set_path_times(self.src3_file_3_path, access=OLD, mod=NEW)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)
        self.outputs_file_2_path.touch()
        set_path_times(self.outputs_file_2_path, access=OLD, mod=NEW)

        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("fourth")._executed == pel.core.TaskExecuted.EXECUTED

    def test_run_outputs_file_1_older_2(self) -> None:
        """
        Check that the task does not run because outputs_file_1_path is older than inputs."""
        set_path_times(self.src1_path, access=NEW, mod=OLD)
        set_path_times(self.src1_file_1_path, access=NEW, mod=OLD)
        set_path_times(self.src2_path, access=NEW, mod=OLD)
        set_path_times(self.src2_file_2_path, access=NEW, mod=OLD)
        set_path_times(self.src3_file_3_path, access=NEW, mod=OLD)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)
        self.outputs_file_2_path.touch()
        set_path_times(self.outputs_file_2_path, access=OLD, mod=NEW)

        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("fourth")._executed == pel.core.TaskExecuted.EXECUTED

    def test_does_not_run_all_files_same_modification_time(self) -> None:
        """
        Check that the task does not run because all inputs and outputs
        have the same modification time.
        """
        set_path_times(self.src1_path, access=NEW, mod=OLD)
        set_path_times(self.src1_file_1_path, access=NEW, mod=OLD)
        set_path_times(self.src2_path, access=NEW, mod=OLD)
        set_path_times(self.src2_file_2_path, access=NEW, mod=OLD)
        set_path_times(self.src3_file_3_path, access=NEW, mod=OLD)
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)
        self.outputs_file_2_path.touch()
        set_path_times(self.outputs_file_1_path, access=NEW, mod=OLD)

        graph = pel.core.Graph()
        exit_code = pel.run.run(graph=graph, args=["--all"])
        assert exit_code == 0
        assert graph.get_task("fourth")._executed == pel.core.TaskExecuted.NOT_EXPIRED
