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

.. _types-switch-auto-create-missing:

Auto Create Missing
===================

When a switch is evaluated in code that is missing in the database the
switch returns the :ref:`WAFFLE_SWITCH_DEFAULT <starting-configuring>`
value but does not create a switch in the database. If you'd like waffle
to create missing switches in the database whenever it encounters a
missing switch you can set :ref:`WAFFLE_CREATE_MISSING_SWITCHES
<starting-configuring>` to ``True``. Missing switches will be created in
the database and the value of the ``Active`` switch attribute will be
set to :ref:`WAFFLE_SWITCH_DEFAULT <starting-configuring>` in the
auto-created database record.


.. _types-switch-log-missing:

Log Missing
===================

Whether or not you enabled :ref:`Auto Create Missing Switch <types-switch-auto-create-missing>`,
it can be practical to be informed that a switch was or is missing.
If you'd like waffle to log a warning, error, ... you can set :ref:`WAFFLE_LOG_MISSING_FLAGS
<starting-configuring>` to any level known by Python default logger.
