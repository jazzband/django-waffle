.. _types-flag:

=====
Flags
=====

Flags are the most robust, flexible method of rolling out a feature with
Waffle. Flags can be used to enable a feature for specific users,
groups, users meeting certain criteria (such as being authenticated, or
superusers) or a certain percentage of visitors.


How Flags Work
==============

Flags compare the current request_ to their criteria to decide whether
they are active. Consider this simple example::

    if flag_is_active(request, 'foo'):
        pass

The :ref:`flag_is_active <usage-views>` function takes two arguments, the
request, and the name of a flag. Assuming this flag (``foo``) is defined
in the database, Waffle will make roughly the following decisions:

- Is ``WAFFLE_OVERRIDE`` active and if so does this request specify a
  value for this flag? If so, use that value.
- If not, is the flag set to globally on or off (the *Everyone*
  setting)? If so, use that value.
- If not, is the flag in *Testing* mode, and does the request specify a
  value for this flag? If so, use that value and set a testing cookie.
- If not, does the current user meet any of our criteria? If so, the
  flag is active.
- If not, does the user have an existing cookie set for this flag? If
  so, use that value.
- If not, randomly assign a value for this user based on the
  *Percentage* and set a cookie.


Flag Attributes
===============

Flags can be administered through the Django `admin site`_ or the
:ref:`command line <usage-cli>`. They have the following attributes:

:Name:
    The name of the flag. Will be used to identify the flag everywhere.
:Everyone:
    Globally set the Flag, **overriding all other criteria**. Leave as
    *Unknown* to use other critera.
:Testing:
    Can the flag be specified via a querystring parameter? :ref:`See
    below <types-flag-testing`.
:Percent:
    A percentage of users for whom the flag will be active, if no other
    criteria applies to them.
:Session:
    The flag will only have the percentage chance to be active if
    these Key/Value pairs match in the request's session.
:Superusers:
    Is this flag always active for superusers?
:Staff:
    Is this flag always active for staff?
:Authenticated:
    Is this flag always active for authenticated users?
:Languages:
    Is the ``LANGUAGE_CODE`` of the request in this list?
    (Comma-separated values.)
:Groups:
    A list of group IDs for which this flag will always be active.
:Users:
    A list of user IDs for which this flag will always be active.
:Rollout:
    Activate Rollout mode? :ref:`See below <types-flag-rollout>`.
:Note:
    Describe where the flag is used.

A Flag will be active if *any* of the criteria are true for the current
user or request (i.e. they are combined with ``or``). For example, if a
Flag is active for superusers, a specific group, and 12% of visitors,
then it will be active if the current user is a superuser *or* if they
are in the group *or* if they are in the 12%.

If using the session key/value pairs critiera then they must be present
*in addition* to the percentage criteria triggering for the flag to be active.

.. note::

    Users are assigned randomly when using Percentages, so in practice
    the actual proportion of users for whom the Flag is active will
    probably differ slightly from the Percentage value.


.. _types-flag-testing:

Testing Mode
============

See :ref:`User testing with Waffle <testing-user>`.


.. _types-flag-rollout:

Rollout Mode
============

When a Flag is activated by chance, Waffle sets a cookie so the flag
will not flip back and forth on subsequent visits. This can present a
problem for gradually deploying new features: users can get "stuck" with
the Flag turned off, even as the percentage increases.

*Rollout mode* addresses this by changing the TTL of "off" cookies. When
Rollout mode is active, cookies setting the Flag to "off" are session
cookies, while those setting the Flag to "on" are still controlled by
:ref:`WAFFLE_MAX_AGE <starting-configuring>`.

Effectively, Rollout mode changes the *Percentage* from "percentage of
visitors" to "percent chance that the Flag will be activated per visit."


.. _request: https://docs.djangoproject.com/en/dev/topics/http/urls/#how-django-processes-a-request
.. _admin site: https://docs.djangoproject.com/en/dev/ref/contrib/admin/
