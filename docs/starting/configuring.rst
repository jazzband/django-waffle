.. _starting-configuring:

==================
Configuring Waffle
==================

There are a few global settings you can define to adjust Waffle's
behavior. As of version 0.13 the settings are set in a ``WAFFLE``
dictionary e.g.::

    WAFFLE = {
        'FLAG_DEFAULT' : False,
        'SWITCH_DEFAULT' : False,
        'SAMPLE_DEFAULT' : False,
        ...
    }

The settings are:

``WAFFLE['COOKIE']``
    The format for the cookies Waffle sets. Must contain ``%s``.
    Defaults to ``dwf_%s``.

``WAFFLE['FLAG_DEFAULT']``
    When a Flag is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    flags ``True``.  Defaults to ``False``.

``WAFFLE['SWITCH_DEFAULT']``
    When a Switch is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    switches ``True``.  Defaults to ``False``.

``WAFFLE['SAMPLE_DEFAULT']``
    When a Sample is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    samples ``True``.  Defaults to ``False``.

``WAFFLE['MAX_AGE']``
    How long should Waffle cookies last? (Integer, in seconds.) Defaults
    to ``2529000`` (one month).

``WAFFLE['OVERRIDE']``
    Allow *all* Flags to be controlled via the querystring (to allow
    e.g. Selenium to control their behavior). Defaults to ``False``.

``WAFFLE['SECURE']``
    Whether to set the ``secure`` flag on cookies. Defaults to ``True``.

``WAFFLE['CACHE_PREFIX']``
    Waffle tries to store objects in cache pretty aggressively. If you
    ever upgrade and change the shape of the objects (for example
    upgrading from <0.7.5 to >0.7.5) you'll want to set this to
    something other than ``'waffle:'``.

``WAFFLE['CACHE_NAME']``
    Which cache to use. Defaults to ``'default'``.
