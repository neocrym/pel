#!/usr/bin/env python3
"""
The Pel command line entrypoint.

When we run Pel from the command line, we always initialize
the :py:attr:`pel.core.DEFAULT_GRAPH` .
"""
import sys

import pel.core

pel.core.DEFAULT_GRAPH = pel.core.Graph()

import pel.run  # pylint: disable=wrong-import-position

def run():
    sys.exit(pel.run.run())


if __name__ == "__main__":
    run()
