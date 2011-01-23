import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

JINJA_CONFIG = {}

TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'
