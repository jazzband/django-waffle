=============
Django Waffle
=============

Django Waffle is (yet another) feature flipper for Django. You can define the
conditions for which a flag should be active, and use it in a number of ways.


Installation
============

To start using Waffle, you just need to add it to your
``INSTALLED_APPS`` and ``MIDDLEWARE_CLASSES``, and make sure to add the
``request`` context processor::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.core.context_processors.request',
        # ...
    )

    INSTALLED_APPS = (
        # ...
        'waffle',
        # ...
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'waffle.middleware.WaffleMiddleware',
        # ...
    )

Since Waffle will be setting cookies on response objects, you probably want it
*below* any middleware that tweaks cookies before sending them out.


Flags, Switches and Samples
===========================

Waffle supports three separate but ultimately similar concepts: **Flags** and
**Switches**, and **Samples**.

Basically, a Flag is **tied to a request**, while Switches and Samples are
**not**. Consequently, Flags are much more complicated, while Switches are
just a named boolean in the database, and Samples are just a percentage stored
in the database.


Flags
-----

Creating and managing flags is done through the Django admin interface. Each
feature flag is represented by a ``Flag`` object, which has several properties.

Name:
    The name of the flag. Will be used to identify the flag everywhere.
Everyone:
    You can flip this flag on (``Yes``) or off (``No``) for everyone,
    overriding all other settings. Leave as ``Unknown`` to use normally.
Percent:
    A percentage of users for whom the flag will be active. This is maintained
    through cookies, so clever users can get around it. Still, it's the most
    common case.
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
    Activate Rollout mode? (See **Rollout Mode** below.)
Note:
    Describe where the flag is used.

You can combine multiple settings here. For example, you could offer a feature
to 12% of users *and* all superusers. When combining settings, the flag will be
active for the user if *any* of the settings matches for them.


Switches
--------

Switches are also managed through the Django admin. Each ``Switch`` object has
only two properties:

Name:
    The name of the switch.
Active:
    Is the switch active or inactive.
Note:
    Describe where the switch is used.

Like Flags, Switches can be used in views, templates, or wrapped around entire
templates. But because they don't rely on a ``request`` objects, Switches can
also be used in crons, Celery tasks, daemons--basically anywhere you can
access the database.


Samples
-------

Samples, also managed through the Django admin, have two properties:

Name:
    The name.
Percent:
    A number from 0.0 to 100.0 that determines how often the sample will be
    active.
Note:
    Describe where the sample is used.

Samples are useful for datamining or other "some of the time" tasks that are
not linked to a user or request--that is, unlike Flags, they do not set cookies
and can't be reliably assumed to be a given value for a given user.


Using Waffle
============

Flags and Switches can be used in templates, in views, or wrapped around
entire views. Samples can be used in templates or views but not to wrap an
entire view.

If you try to use a flag or switch that is not defined, it will *always*
be **inactive**.


Using Waffle in Templates
-------------------------


Jingo/Jinja2
^^^^^^^^^^^^

To use a Flag in a Jinja2 template via `Jingo
<http://github.com/jbalogh/jingo>`_, you can simply do::

    {% if waffle.flag('flag_name') %}
      Content if flag is active
    {% endif %}

You can also add an ``{% else %}`` section, of course::

    {% if waffle.flag('flag_name') %}
      Flag is active!
    {% else %}
      Flag is inactive!
    {% endif %}

To use a Switch in a Jinja2 template via `Jingo
<http://github.com/jbalogh/jingo>`_, you can do::

    {% if waffle.switch('switch_name') %}
      Content if switch is active
    {% endif %}

You can also add an ``{% else %}`` section, of course::

    {% if waffle.switch('switch_name') %}
      Switch is active!
    {% else %}
      Switch is inactive!
    {% endif %}

For Samples::

    {% if waffle.sample('sample_name') %}
      Sample is active!
    {% else %}
      Sample is inactive!
    {% endif %}


Django Templates
^^^^^^^^^^^^^^^^

To use a *flag* in vanilla Django templates, you can use the ``flag`` tag::

    {% load waffle_tags %}
    {% flag flag_name %}
      Content if flag is active
    {% endflag %}

The ``{% flag %}`` tag also supports an ``{% else %}`` section::

    {% flag flag_name %}
      Flag is active!
    {% else %}
      Flag is inactive!
    {% endflag %}

To use a *switch* in vanilla Django templates, you can use the ``switch``
tag::

    {% load waffle_tags %}
    {% switch switch_name %}
      Content if switch is active
    {% endswitch %}

The ``{% switch %}`` tag also supports an ``{% else %}`` section::

    {% switch switch_name %}
      Switch is active!
    {% else %}
      Switch is inactive!
    {% endswitch %}


To use a *sample*, just use the ``sample`` tag::

    {% sample sample_name %}
      Sample is active!
    {% else %} {# Optional `else` section #}
      Sample is inactive!
    {% endsample %}

Using Waffle in Views
---------------------

To use a flag in a view, you just need ``waffle.flag_is_active``::

    import waffle

    def my_view(request):
        if waffle.flag_is_active(request, 'flag_name'):
            # Behavior if flag is active.
        else:
            # Behavior if flag is inactive.

For switches, just use the ``switch_is_active`` method::

    import waffle

    def myview(request):
        if waffle.switch_is_active('myswitch'):
            return 'switch is active'
        return 'switch is inactive'

Because it doesn't need a ``request`` object, ``switch_is_active`` can be used
anywhere.

Similarly, ``sample_is_active`` can be used anywhere, since it does not require
a ``request`` object::

    import waffle

    def myview(request):
        if waffle.sample_is_active('mysample'):
            # Some percent of requests.


Wrapping a Whole View
---------------------

You can also wrap an entire view in a flag::

    from waffle.decorators import waffle_flag

    @waffle_flag('flag_name')
    def my_view(request):
        # View only available if flag is active.

...or a switch::

    from waffle.decorators import waffle_switch

    @waffle_switch('switch_name')
    def my_view(request):
        # View only available if switch is active.

If the flag or switch is *not* active for the request, the view will be a 404.

You can reverse either decorator with an exclamation point at the start of the
flag or switch name, for example::

    @waffle_flag('!flag_name')
    def my_view(request):
        # View is only available if flag is INactive.


Global Settings
===============

There are a few global settings you can define to adjust Waffle's behavior.


``WAFFLE_COOKIE``:
    The format for the cookies Waffle sets. Must contain ``%s``. Defaults to
    ``dwf_%s``.
``WAFFLE_FLAG_DEFAULT``:
    When a Flag is undefined in the database, Waffle considers it ``False``.
    Set this to ``True`` to make Waffle consider undefined flags ``True``.
    Defaults to ``False``.
``WAFFLE_SWITCH_DEFAULT``:
    When a Switch is undefined in the database, Waffle considers it ``False``.
    Set this to ``True`` to make Waffle consider undefined switches ``True``.
    Defaults to ``False``.
``WAFFLE_SAMPLE_DEFAULT``:
    When a Sample is undefined in the database, Waffle considers it ``False``.
    Set this to ``True`` to make Waffle consider undefined samples ``True``.
    Defaults to ``False``.
``WAFFLE_MAX_AGE``:
    How long should Waffle cookies last? (Integer, in seconds.) See the
    **Cookies** section. Defaults to ``2529000`` (one month).
``WAFFLE_OVERRIDE``:
    Whether Flags can be controlled from the query string. Defaults to
    ``False``.
``WAFFLE_SECURE``:
    Whether to set the ``secure`` flag on cookies. Defaults to ``False``.
``WAFFLE_CACHE_PREFIX``:
    Waffle tries to store objects in cache pretty aggressively. If you ever
    upgrade and change the shape of the objects (for example upgrading from
    <0.7.5 to >0.7.5) you'll want to set this to something other than
    ``'waffle:'``.


Overriding Flags
================

If you turn on the ``WAFFLE_OVERRIDE`` setting, you can guarantee a flag will
be active for a request by putting it in the query string.

For example, if I use the flag ``example`` in a view that serves the URL
``/search``, then I can turn on the flag by adding ``?example=1`` to the query
string, or turn it off by adding ``?example=0``.

By default, ``WAFFLE_OVERRIDE`` is off. It may be useful for testing, automated
testing in particular.

Switches cannot be overridden at this time.


Cookies
=======

When falling back to percentage of active users, Waffle will set a cookie for
every request, setting the flag's value (on or off) for future requests.

If the cookie is set, its value is used (either True or False) and it is
re-set. Since cookies are re-set on every request (that uses the flag), you do
not need to set ``WAFFLE_MAX_AGE`` very high. Just high enough that a typical
returning user won't potentially flip back and forth between off and on.


Rollout Mode
============

**Rollout Mode** allows you to gradually enable a feature for all users. In
"normal" mode, a flag's value will be set in a cookie until ``WAFFLE_MAX_AGE``
whether the flag is active or not. In Rollout Mode, an *inactive* flag will set
a session cookie, and an *active* flag will set a longer-lived cookie.

Every time a user starts a new session, they'll have a chance (determined by
the percentage of the flag) to have the feature turned on "permanently". Once
it's on, it should stay on, unless they clear their cookies or use a different
browser (see **To Do**).

To guarantee an even rollout, it will likely be necessary to gradually increase
the flag's percentage as more and more users get stuck with the *active*
cookie.

Rollout Mode is enabled **per flag**.


Waffle in JavaScript
====================

Waffle now helps you use flags directly in JavaScript. You need to add the
``wafflejs`` view to your ``urls.py``::

    from waffle.views import wafflejs

    urlpatterns = patterns('',
        # ...
        url(r'^wafflejs$', wafflejs, name='wafflejs'),
        # ...
    )

You can then load the Waffle JavaScript in your templates::

    <script src="{% url wafflejs %}"></script>

Once you've loaded the JavaScript, you can use the global ``waffle`` object.
Just pass in a flag name. As in the Python API, if a flag or switch is
undefined, it will always be ``false``.

::

    if (waffle.flag('some_flag')) {
        // Flag is active.
    } else {
        // Flag is inactive.
    }

    if (waffle.switch('some_switch')) {
        // Switch is active.
    } else {
        // Switch is inactive.
    }

    if (waffle.sample('some_sample')) {
        // Sample is active.
    } else {
        // Sample is inactive.
    }

``waffle.sample(foo)`` will return the same value *on a given request* but
that value may not persist across multiple requests.


To Do
=====

* Keep a flag setting for a given user, regardless of browser/device.
