.. _usage-cli:
.. highlight:: shell

==========================================
Managing Waffle data from the command line
==========================================

Aside the Django admin interface, you can use the command line tools to
manage all your waffle objects.


Flags
=====

Use ``manage.py`` to change the values of your flags::

    $ ./manage.py waffle_flag name-of-my-flag --everyone --percent=47

Use ``--everyone`` to turn on and ``--deactive`` to turn off the flag.
Set a percentage with ``--percent`` or ``-p``. Set the flag on for
superusers (``--superusers``), staff (``--staff``) or authenticated
(``--authenticated``) users. Set the rollout mode on with ``--rollout``
or ``-r``.

If the flag doesn't exist, add ``--create`` to create it before setting
its values::

    $ ./manage.py waffle_flag name-of-my-flag --deactivate --create

To list all the existing flags, use ``-l``::

    $ ./manage.py waffle_flag -l
    Flags:
    name-of-my-flag


Switches
========

Use ``manage.py`` to change the values of your switches::

    $ ./manage.py waffle_switch name-of-my-switch off

You can set a switch to ``on`` or ``off``. If that switch doesn't exist,
add ``--create`` to create it before setting its value::

    $ ./manage.py waffle_switch name-of-my-switch on --create

To list all the existing switches, use ``-l``::

    $ ./manage.py waffle_switch -l
    Switches:
    name-of-my-switch on


Samples
=======

Use ``manage.py`` to change the values of your samples::

    $ ./manage.py waffle_sample name-of-my-sample 100

You can set a sample to any floating value between ``0.0`` and
``100.0``. If that sample doesn't exist, add ``--create`` to create it
before setting its value::

    $ ./manage.py waffle_sample name-of-my-sample 50.0 --create

To list all the existing samples, use ``-l``::

    $ ./manage.py waffle_sample -l
    Samples:
    name-of-my-sample: 50%
