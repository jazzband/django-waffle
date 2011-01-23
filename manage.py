#!/usr/bin/env python
import os
import site
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

sys.path.insert(0, os.environ['PYTHONPATH'])

# Now we can import from third-party libraries.
from django.core.management import execute_manager, setup_environ

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write(
        "Error: Tried importing 'settings_local.py' and 'settings.py' "
        "but neither could be found (or they're throwing an ImportError)."
        " Please come back and try again later.")
    raise

# The first thing execute_manager does is call `setup_environ`.  Logging config
# needs to access settings, so we'll setup the environ early.
setup_environ(settings)

# Import for side-effect: configures our logging handlers.


if __name__ == "__main__":
    execute_manager(settings)
