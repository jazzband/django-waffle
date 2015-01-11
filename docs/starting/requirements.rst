.. _starting-requirements:

============
Requirements
============

Waffle depends only on Django (except for :ref:`running Waffle's tests
<about-contributing>`) but does require certain Django features.


User Models
===========

Waffle requires Django's `auth system`_, in particular it requires both
a user model and Django's groups. If you're using a `custom user
model`_, this can be accomplished by including Django's
`PermissionsMixin`_, e.g.::

    from django.contrib.auth import models

    class MyUser(models.AbstractBaseUser, models.PermissionsMixin):

And of ``django.contrib.auth`` must be in ``INSTALLED_APPS``, along with
`its requirements`_.

.. _auth system: https://docs.djangoproject.com/en/dev/topics/auth/
.. _custom user model: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#specifying-a-custom-user-model
.. _PermissionsMixin: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#custom-users-and-permissions
.. _its requirements: https://docs.djangoproject.com/en/dev/topics/auth/#installation


Templates
=========

Waffle provides template tags to check flags directly in templates.
Using these requires the ``request`` object in the template context,
which can be easily added with the ``request`` `template context
processor`_::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.core.context_processors.request',
        # ...

.. _template context processor: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
