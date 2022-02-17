"""Pel errors."""


class PelError(Exception):
    """Parent class for all Pel exceptions."""


class MissingGraph(PelError, ValueError):
    """
    Raised when DEFAULT_GRAPH is disabled and the user
    did not provide their own Graph.
    """
