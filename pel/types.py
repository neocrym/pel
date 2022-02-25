"""Utilities for typing Python code."""
from typing import List, Union


def enforce_list_of_str(inp: Union[str, List[str]]) -> List[str]:
    """Always convert strings into lists of strings."""
    if isinstance(inp, str):
        return [inp]
    return inp
