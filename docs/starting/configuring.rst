.. _starting-configuring:

==================
Configuring Waffle
==================

There are a few global settings you can define to adjust Waffle's
behavior.

``WAFFLE_COOKIE``
    The format for the cookies Waffle sets. Must contain ``%s``.
    Defaults to ``dwf_%s``.

``WAFFLE_FLAG_MODEL``
    The model that will be used to keep track of flags. Defaults to ``waffle.Flag``
    which allows user- and group-based flags. Can be swapped for a different Flag model
    that allows flagging based on other relationships or properties, such as an Organization 
    a user belongs to.
    Analogous functionality to Django's extendable User models.
    Needs to be set at the start of a project. Migrations do not support changing after the
    initial migration.

``WAFFLE_FLAG_DEFAULT``
    When a Flag is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    flags ``True``.  Defaults to ``False``.

``WAFFLE_SWITCH_DEFAULT``
    When a Switch is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    switches ``True``.  Defaults to ``False``.

``WAFFLE_SAMPLE_DEFAULT``
    When a Sample is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    samples ``True``.  Defaults to ``False``.

``WAFFLE_MAX_AGE``
    How long should Waffle cookies last? (Integer, in seconds.) Defaults
    to ``2529000`` (one month).

``WAFFLE_OVERRIDE``
    Allow *all* Flags to be controlled via the querystring (to allow
    e.g. Selenium to control their behavior). Defaults to ``False``.

``WAFFLE_SECURE``
    Whether to set the ``secure`` flag on cookies. Defaults to ``True``.

``WAFFLE_CACHE_PREFIX``
    Waffle tries to store objects in cache pretty aggressively. If you
    ever upgrade and change the shape of the objects (for example
    upgrading from <0.7.5 to >0.7.5) you'll want to set this to
    something other than ``'waffle:'``.

``WAFFLE_CACHE_NAME``
    Which cache to use. Defaults to ``'default'``.
