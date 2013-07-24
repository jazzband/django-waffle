.. _types-chapter:

===========================
Flags, Switches and Samples
===========================

Waffle supports three separate but ultimately similar concepts:
**Flags** and **Switches**, and **Samples**.

Basically, a Flag is **tied to a request**, while Switches and Samples
are **not**. Consequently, Flags are much more complicated, while
Switches are just a named boolean in the database, and Samples are
just a percentage stored in the database.


Flags
-----

Creating and managing flags is done through the Django admin
interface. Each feature flag is represented by a ``Flag`` object,
which has several properties.

Name:
    The name of the flag. Will be used to identify the flag
    everywhere.
Everyone:
    You can flip this flag on (``Yes``) or off (``No``) for everyone,
    overriding all other settings. Leave as ``Unknown`` to use
    normally.
Testing:
    Let's you override the flag value using the url querystring.
    See :ref:`overriding-flags` for details.
Percent:
    A percentage of users for whom the flag will be active. This is
    maintained through cookies, so clever users can get around
    it. Still, it's the most common case.
Superusers:
    Is this flag always active for superusers?
Staff:
    Is this flag always active for staff?
Authenticated:
    Is this flag always active for authenticated users?
Groups:
    A list of group IDs for which this flag will always be active.
Users:
    A list of user IDs for which this flag will always be active.
Rollout:
    Activate Rollout mode? See :ref:`rollout-mode` for details.
Note:
    Describe where the flag is used.

You can combine multiple settings here. For example, you could offer a
feature to 12% of users *and* all superusers. When combining settings,
the flag will be active for the user if *any* of the settings matches
for them.


Switches
--------

Switches are also managed through the Django admin. Each ``Switch``
object has these properties:

Name:
    The name of the switch.
Active:
    Is the switch active or inactive.
Note:
    Describe where the switch is used.

Like Flags, Switches can be used in views, templates, or wrapped
around entire templates. But because they don't rely on a ``request``
objects, Switches can also be used in crons, Celery tasks,
daemons---basically anywhere you can access the database.


Samples
-------

Samples, also managed through the Django admin, has these properties:

Name:
    The name.
Percent:
    A number from 0.0 to 100.0 that determines how often the sample
    will be active.
Note:
    Describe where the sample is used.

Samples are useful for datamining or other "some of the time" tasks
that are not linked to a user or request---that is, unlike Flags, they
do not set cookies and can't be reliably assumed to be a given value
for a given user.

Command line management
-----------------------

Aside the Django admin interface, you can use the command line tools to manage
all your waffle objects.

Flags
=====

Use ``manage.py`` to change the values of your flags::

    $ ./manage.py flag name-of-my-flag --everyone --percent=47

Use ``--everyone`` to turn on and ``--deactive`` to turn off the flag. Set a
percentage with ``--percent`` or ``-p``. Set the flag on for superusers
(``--superusers``), staff (``--staff``) or authenticated (``--authenticated``)
users. Set the rollout mode on with ``--rollout`` or ``-r``.

If the flag doesn't exist, add ``--create`` to create it before setting its
values::

    $ ./manage.py flag name-of-my-flag --deactivate --create

To list all the existing flags, use ``-l``::

    $ ./manage.py flag -l
    Flags:
    name-of-my-flag

Switches
========

Use ``manage.py`` to change the values of your switches::

    $ ./manage.py switch name-of-my-switch off

You can set a switch to ``on`` or ``off``. If that switch doesn't exist,
add ``--create`` to create it before setting its value::

    $ ./manage.py switch name-of-my-switch on --create

To list all the existing switches, use ``-l``::

    $ ./manage.py switch -l
    Switches:
    name-of-my-switch on

Samples
=======

Use ``manage.py`` to change the values of your samples::

    $ ./manage.py sample name-of-my-sample 100

You can set a sample to any floating value between ``0.0`` and ``100.0``. If
that sample doesn't exist, add ``--create`` to create it before setting its
value::

    $ ./manage.py sample name-of-my-sample 50.0 --create

To list all the existing samples, use ``-l``::

    $ ./manage.py sample -l
    Samples:
    name-of-my-sample: 50%
