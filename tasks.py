"""
Creating standalone Django apps is a PITA because you're not in a project, so
you don't have a settings.py file.  I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.
"""
import os
from invoke import run, task


NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = '%s-project.settings' % NAME
os.environ['PYTHONPATH'] = os.pathsep.join([ROOT,
                                            os.path.join(ROOT, 'examples')])


@task
def shell():
    """Start a Django shell with the test settings."""
    run('django-admin.py shell')


@task
def test():
    """Run the Waffle test suite."""
    run('django-admin.py test')


@task
def serve():
    """Start the Django dev server."""
    run('django-admin.py runserver')


@task
def syncdb():
    """Create a database for testing in the shell or server."""
    run('django-admin.py syncdb')


@task
def schema():
    """Create a schema migration for any changes."""
    run('django-admin.py schemamigration waffle --auto')


@task
def migrate():
    """Update a testing database with south."""
    run('django-admin.py migrate')
