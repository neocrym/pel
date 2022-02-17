#!/usr/bin/env python3
"""
The Pel command line entrypoint.
"""
import sys

import pel.run


def run() -> None:
    """Run the Pel CLI and exit with a status code."""
    sys.exit(pel.run.run())


if __name__ == "__main__":
    run()
