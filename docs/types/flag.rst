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
    below <types-flag-testing>`.
:Percent:
    A percentage of users for whom the flag will be active, if no other
    criteria applies to them.
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


.. note::

    Users are assigned randomly when using Percentages, so in practice
    the actual proportion of users for whom the Flag is active will
    probably differ slightly from the Percentage value.
    
    
.. _types-flag-custom-model:

Custom Flag Models
======================

For many cases, the default Flag model provides all the necessary functionality. It allows
flagging individual ``User``s and ``Group``s. If you would like flags to be applied to
different things, such as companies a User belongs to, you can use a custom flag model.

The functionality uses the same concepts as Django's custom user models, and a lot of this will
be immediately recognizable.

An application needs to define a ``WAFFLE_FLAG_MODEL`` settings. The default is ``waffle.Flag``
but can be pointed to an arbitrary object.

.. note::

    It is not possible to change the Flag model and generate working migrations. Ideally, the flag
    model should be defined at the start of a new project. This is a limitation of the `swappable`
    Django magic. Please use magic responsibly.

The custom Flag model must inherit from `waffle.models.AbstractBaseFlag`. If you want the existing
``User`` and ``Group`` based flagging and would like to add more entities to it,
you may extend `waffle.models.AbstractUserFlag`.

If you need to reference the class that is being used as the `Flag` model in your project, use the
``get_waffle_flag_model()`` method. If you reference the Flag a lot, it may be convenient to add
``Flag = get_waffle_flag_model()`` right below your imports and reference the Flag model as if it had
been imported directly.

Example:

```python
# settings.py
WAFFLE_FLAG_MODEL = 'myapp.Flag'

# models.py
class Flag(AbstractUserFlag):
    FLAG_COMPANIES_CACHE_KEY = 'FLAG_COMPANIES_CACHE_KEY'
    FLAG_COMPANIES_CACHE_KEY_DEFAULT = 'flag:%s:companies'

    companies = models.ManyToManyField(
        Company,
        blank=True,
        help_text=_('Activate this flag for these companies.'),
    )

    def get_flush_keys(self, flush_keys=None):
        flush_keys = super(Flag, self).get_flush_keys(flush_keys)
        companies_cache_key = get_setting(Flag.FLAG_COMPANIES_CACHE_KEY, Flag.FLAG_COMPANIES_CACHE_KEY_DEFAULT)
        flush_keys.append(keyfmt(companies_cache_key, self.name))
        return flush_keys

    def is_active_for_user(self, user):
        is_active = super(Flag, self).is_active_for_user(user)
        if is_active:
            return is_active

        if getattr(user, 'company_id', None):
            company_ids = self._get_company_ids()
            if user.company_id in company_ids:
                return True

    def _get_company_ids(self):
        cache_key = keyfmt(
            get_setting(Flag.FLAG_COMPANIES_CACHE_KEY, Flag.FLAG_COMPANIES_CACHE_KEY_DEFAULT),
            self.name
        )
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return set()
        if cached:
            return cached

        company_ids = set(self.companies.all().values_list('pk', flat=True))
        if not company_ids:
            cache.add(cache_key, CACHE_EMPTY)
            return set()

        cache.add(cache_key, company_ids)
        return company_ids

# admin.py
from waffle.admin import FlagAdmin as WaffleFlagAdmin

class FlagAdmin(WaffleFlagAdmin):
    raw_id_fields = tuple(list(WaffleFlagAdmin.raw_id_fields)  ['companies'])
admin.site.register(Flag, FlagAdmin)

```


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
