"""The Pel Graph, Task, and ArgParser models."""
import argparse
import collections
import threading
from enum import Enum, auto
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    OrderedDict,
    Sequence,
    Set,
    Type,
    Union,
    cast,
)

from pel._vendor.graphlib import TopologicalSorter  # type: ignore


def _get_recursive_need_names_from_tasks(end_tasks: Sequence[Type["Task"]]) -> Set[str]:
    def _recursive(tasks: Set[Type["Task"]]) -> Iterator[str]:
        for task in tasks:
            yield task.__name__
            yield from _recursive(set(task._get_needs()))

    return set(_recursive(set(end_tasks)))


class TaskExecuted(Enum):
    """Describes whether a Task has been executed."""

    NOT_RUN = auto()
    NOT_EXPIRED = auto()
    EXECUTED = auto()
    RAISED_EXCEPTION = auto()
    SKIPPED = auto()


class Task:
    """Subclass this to create your own Task types."""

    needs: Union[List[Type["Task"]], Type["Task"], None] = None

    _result: Any = NotImplemented
    _exception: Optional[BaseException] = None
    _executed: TaskExecuted = TaskExecuted.NOT_RUN

    @classmethod
    def _get_needs(cls) -> List[Type["Task"]]:
        """
        Getter method for this Task's dependencies.
        """
        if not cls.needs:
            return []
        if isinstance(cls.needs, Task.__class__):  # type: ignore
            return [cls.needs]  # type: ignore
        if not isinstance(cls.needs, list):
            cast(List[Type["Task"]], cls.needs)
            raise TypeError(f"bad needs type {cls.needs}")
        for task in cls.needs:
            if not isinstance(task, Task.__class__):  # type: ignore
                raise TypeError(f"bad needs task type {task}")
        return cls.needs

    @classmethod
    def is_expired(cls) -> bool:
        """
        Override this to return False when this Task does not need to run.

        By default, this classmethod always returns True, which is handy
        for when you always want a Task to run.
        """
        return True

    @classmethod
    def run(cls) -> None:
        """
        Override this with the actual business logic that you want this Task to run.
        """
        raise NotImplementedError("HI")


class Graph:
    """Keeps track of :py:class:`Task` classes and executes them."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.clear()

    def clear(self) -> None:
        """Clear all references in the graph."""
        self._registry: Dict[str, Type[Task]] = {}

    def get_task(self, name: str) -> Type[Task]:
        """Get a Task class by its name."""
        return self._registry[name]

    def add_task(self, cls: Type[Task]) -> None:
        """
        Add a Task class to the graph.

        Args:
            cls: The Task class. Do not pass an instance of the class.
        """
        with self._lock:
            for base in cls.__bases__:
                self._registry.pop(base.__name__, None)
            self._registry[cls.__name__] = cls

    def add_tasks_from_scope(self, scope: Mapping[str, Any]) -> None:
        """Search a variable scope dictionary for any Task subclass objects."""
        for obj in scope.values():
            if isinstance(obj, Task.__class__):  # type: ignore
                self.add_task(obj)

    def remove_task(self, name: str) -> None:
        """Remove a Task by name."""
        with self._lock:
            self._registry.pop(name, None)

    def get_all_tasks(self) -> Dict[str, Type[Task]]:
        """Return a dictionary mapping Task names to Task classes."""
        return self._registry

    def _get_recursive_need_names(
        self, end_task_names: Union[Sequence[str], str]
    ) -> Set["str"]:
        """List the names of all of the tasks needed to execute these task names."""
        if isinstance(end_task_names, str):
            end_task_names = [end_task_names]
        return _get_recursive_need_names_from_tasks(
            [self._registry[name] for name in end_task_names]
        )

    def _get_needs_map(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> OrderedDict[str, Set[str]]:
        """Return a dict mapping task names to their dependencies' names."""
        needs_map: OrderedDict[str, Set[str]] = collections.OrderedDict()
        if end_task_names:
            tasks = self._get_recursive_need_names(end_task_names)
        else:
            tasks = set(self._registry.keys())
        for name in sorted(tasks):
            task = self._registry[name]
            needs_map[name] = {dep.__name__ for dep in task._get_needs()}
        return needs_map

    def get_needs_map(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> Dict[str, Set[str]]:
        """
        Return a dict mapping task names to their dependencies' names.

        Acquires the lock.
        """
        with self._lock:
            return self._get_needs_map(end_task_names)

    def _get_sorted_task_names(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> List[str]:
        """Returns all task names, topologically sorted by dependencies."""
        return list(
            TopologicalSorter(self._get_needs_map(end_task_names)).static_order()
        )

    def get_sorted_task_names(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> List[str]:
        """
        Returns all task names, topologically sorted by dependencies.

        Acquires the lock.
        """
        with self._lock:
            return self._get_sorted_task_names(end_task_names)

    def _get_sorted_tasks(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> List[Type[Task]]:
        """
        Returns all task class instances, topologically sorted by dependencies.
        """
        return [
            self._registry[name] for name in self._get_sorted_task_names(end_task_names)
        ]

    def get_sorted_tasks(
        self, end_task_names: Union[Sequence[str], str] = ""
    ) -> List[Type[Task]]:
        """
        Returns all task class instances, topologically sorted by dependencies.

        Acquires the lock.
        """
        with self._lock:
            return self._get_sorted_tasks(end_task_names)

    def _execute(self, end_task_names: Union[Sequence[str], str] = "") -> None:
        """
        Executes the task names provided, including dependencies.

        If no names are provided, we execute all of the tasks.
        """
        for task in self._get_sorted_tasks(end_task_names):
            if task.is_expired():
                print(task.__name__, "[running]")
                try:
                    task._result = task.run()
                except BaseException as exc:
                    task._executed = TaskExecuted.RAISED_EXCEPTION
                    task._exception = exc
                    raise
                task._executed = TaskExecuted.EXECUTED
            else:
                print(task.__name__, "[not expired]")
                task._executed = TaskExecuted.NOT_EXPIRED

    def execute(self, end_task_names: Union[Sequence[str], str] = "") -> None:
        """
        Executes the task names provided, including dependencies.

        If no names are provided, we execute all of the tasks.

        Acquires the lock.
        """
        with self._lock:
            self._execute(end_task_names)


class ArgParser:
    """Parses shell arguments to run Tasks."""

    def __init__(self, *, graph: Graph) -> None:
        """
        Initialize the argument parser.

        Args:
            graph: The Graph to parse.
        """
        self._graph: Graph = graph
        self._parser = argparse.ArgumentParser()
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--list", "-l", action="store_true")
        group.add_argument("--all", "-a", action="store_true")
        group.add_argument("tasks", metavar="task", type=str, nargs="*", default=())

    def parse_args(self, *, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse the args."""
        return self._parser.parse_args(args=args)

    def interpret_args(self, *, args: Optional[List[str]] = None) -> None:
        """Parse the args and do what they say."""
        parsed_args = self.parse_args(args=args)
        if parsed_args.list:
            self.list_tasks()
            return
        if parsed_args.all:
            self.execute_tasks()
            return
        if not parsed_args.tasks:
            self.print_help()
            return
        self.execute_tasks(parsed_args.tasks)
        return

    def list_tasks(self) -> None:
        """Print the Tasks in our Graph to standard output."""
        print("Detected tasks:\n")
        for name, task in sorted(self._graph.get_all_tasks().items()):
            dash_name = name.replace("_", "-")
            task_help = (task.__doc__ or "").strip().split("\n")[0].strip()
            if task_help:
                print(f"{dash_name}:\n    {task_help}\n")
            else:
                print(f"{dash_name}:\n")

    def print_help(self) -> None:
        """Print this argparser's Help message to standard output."""
        return self._parser.print_help()

    def execute_tasks(self, dash_names: Union[Sequence[str], str] = "") -> None:
        """Execute the tasks."""
        end_task_names = [name.replace("-", "_") for name in dash_names]
        self._graph.execute(end_task_names=end_task_names)
