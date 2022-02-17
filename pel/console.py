"""
The Pel command line entrypoint.

When we run Pel from the command line, we always initialize
the :py:attr:`pel.core.DEFAULT_GRAPH` .
"""
import pel.core

pel.core.DEFAULT_GRAPH = pel.core.Graph()

import pel.run  # pylint: disable=wrong-import-position

run = pel.run.run
