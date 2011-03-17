"""
Creating standalone Django apps is a PITA because you're not in a project, so
you don't have a settings.py file.  I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.
"""
import functools
import os

from fabric.api import local


NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = '%s-project.settings' % NAME
os.environ['PYTHONPATH'] = os.pathsep.join([ROOT,
                                            os.path.join(ROOT, 'examples')])

local = functools.partial(local, capture=False)


def shell():
    """Start a Django shell with the test settings."""
    local('django-admin.py shell')


def test():
    """Run the Waffle test suite."""
    local('django-admin.py test -s')


def serve():
    """Start the Django dev server."""
    local('django-admin.py runserver')


def syncdb():
    """Create a database for testing in the shell or server."""
    local('django-admin.py syncdb')
