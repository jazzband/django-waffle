.. _types-switch:

========
Switches
========

Switches are simple booleans: they are on or off, for everyone, all the
time. They do not require a request object and can be used in other
contexts, such as management commands and tasks.


Switch Attributes
=================

Switches can be administered through the Django `admin site`_ or the
:ref:`command line <usage-cli>`. They have the following attributes:

:Name:
    The name of the Switch.
:Active:
    Is the Switch active or inactive.
:Note:
    Describe where the Switch is used.


.. _admin site: https://docs.djangoproject.com/en/dev/ref/contrib/admin/
