.. _starting-configuring:

==================
Configuring Waffle
==================

There are a few global settings you can define to adjust Waffle's
behavior.

``WAFFLE_COOKIE``
    The format for the cookies Waffle sets. Must contain ``%s``.
    Defaults to ``dwf_%s``.

``WAFFLE_FLAG_DEFAULT``
    When a Flag is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    flags ``True``.  Defaults to ``False``.

``WAFFLE_FLAG_MODEL``
    The model that will be use to keep track of flags. Defaults to ``waffle.Flag``
    which allows user- and group-based flags. Can be swapped for a different Flag model
    that allows flagging based on other things, such as an organization or a company
    that a user belongs to. Analogous functionality to Django's extendable User models.
    Needs to be set at the start of a project, as the Django migrations framework does not
    support changing swappable models after the initial migration.

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

``WAFFLE_READ_FROM_WRITE_DB``
    When calling ``*_is_active`` methods, Waffle attempts to retrieve a cached
    version of the object, falling back to the database if necessary. In high-
    traffic scenarios with multiple databases (e.g. a primary being replicated
    to a readonly pool) this introduces the risk that a stale version of the
    object might be cached if one of these methods is called immediately after
    an update. Set this to ``True`` to ensure Waffle always reads Flags,
    Switches, and Samples from the DB configured for writes on cache misses.

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
