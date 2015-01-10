.. _starting-installation:

============
Installation
============

After ensuring that the :ref:`requirements <starting-requirements>` are
met, installing Waffle is a simple process.


Getting Waffle
==============

Waffle is `hosted on PyPI`_ and can be installed with ``pip`` or
``easy_install``:

.. code-block:: shell

    $ pip install django-waffle
    $ easy_install django-waffle

Waffle is also available `on GitHub`_. In general, ``master`` should be
stable, but use caution depending on unreleased versions.

.. _hosted on PyPI: http://pypi.python.org/pypi/django-waffle
.. _on GitHub: https://github.com/jsocol/django-waffle


Settings
========

Add ``waffle`` to the ``INSTALLED_APPS`` setting, and
``waffle.middleware.WaffleMiddleware`` to ``MIDDLEWARE_CLASSES``, e.g.::

    INSTALLED_APPS = (
        # ...
        'waffle',
        # ...
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'waffle.middleware.WaffleMiddleware',
        # ...
    )

If you're using South_ for database migrations, you'll need to add
Waffle to the ``SOUTH_MIGRATION_MODULES`` setting, as well::

    SOUTH_MIGRATION_MODULES = {
        # ...
        'waffle': 'waffle.south_migrations',
        # ...
    }


Database Schema
===============

Waffle includes both South_ migrations and `Django migrations`_ for
creating the correct database schema. If using South or Django >= 1.7,
simply run the ``migrate`` management command after adding Waffle to
``INSTALLED_APPS``:

.. code-block:: shell

    $ django-admin.py migrate

If you're using a version of Django without migrations, you can run
``syncdb`` to create the Waffle tables.

.. _South: http://south.aeracode.org/
.. _Django migrations: https://docs.djangoproject.com/en/dev/topics/migrations/
