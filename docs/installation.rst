============
Installation
============

To start using Waffle, you need to add it to your ``INSTALLED_APPS`` and
``MIDDLEWARE_CLASSES``, and make sure to add the ``request`` context
processor::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.core.context_processors.request',
        # ...
    )

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

Since Waffle will be setting cookies on response objects, you probably
want it *below* any middleware that tweaks cookies before sending them
out.

If you're using South_, you can run ``manage.py migrate`` to create the
necessary tables, you'll need to customize the ``SOUTH_MIGRATION_MODULES``
setting: ::

    SOUTH_MIGRATION_MODULES = {
        'waffle': 'waffle.south_migrations',
    }

If you are not using south, you'll need to create and run the schema
migrations however you handle that.

.. _South: http://south.aeracode.org/
