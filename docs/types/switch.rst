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

:name:
    The name of the Switch.
:active:
    Is the Switch active or inactive.
:note:
    Describes where the Switch is used.


.. _admin site: https://docs.djangoproject.com/en/dev/ref/contrib/admin/


Switch Methods
==============

The Switch class has the following public methods:

:is_active:
    Determines if the switch is active. Returns a boolean value.


.. _types-custom-switch-models:

Custom Switch Models
======================

For many cases, the default Switch model provides all the necessary functionality.
If you would like additional fields not supported by the default Switch model,
you can use a custom Switch model.

An application needs to define a ``WAFFLE_SWITCH_MODEL`` settings. The default is ``waffle.Switch``
but can be pointed to an arbitrary object.

.. note::

    It is not possible to change the Switch model and generate working migrations. Ideally, the Switch
    model should be defined at the start of a new project. This is a limitation of the `swappable`
    Django magic. Please use magic responsibly.

The custom Switch model must inherit from `waffle.models.AbstractBaseSwitch`.

When using a custom Switch model, you must run Django's
``makemigrations`` before running migrations as outlined in the :ref:`installation docs
<installation-settings-migrations>`.

If you need to reference the class that is being used as the `Switch` model in your project, use the
``get_waffle_model('SWITCH_MODEL')`` method. If you reference the Switch a lot, it may be convenient
to add ``Switch = get_waffle_model('SWITCH_MODEL')`` right below your imports and reference the Switch
model as if it had been imported directly.

Example:

.. code-block:: python

    # settings.py
    WAFFLE_SWITCH_MODEL = 'myapp.Switch'

    # models.py
    from waffle.models import AbstractBaseSwitch, CACHE_EMPTY

    class Switch(AbstractBaseSwitch):

        owner = models.CharField(
            max_length=100,
            blank=True,
            help_text=_('The individual/team who owns this switch.'),
        )

    # admin.py
    from waffle.admin import SwitchAdmin as WaffleSwitchAdmin

    class SwitchAdmin(WaffleSwitchAdmin):
        raw_id_fields = tuple(list(WaffleSwitchAdmin.raw_id_fields) + ['owner'])
    admin.site.register(Switch, SwitchAdmin)


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
