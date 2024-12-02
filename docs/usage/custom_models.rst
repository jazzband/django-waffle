.. _usage-custom-models:

================
Custom Models
================

For many cases, the default models for flags, switches, and samples provide all the necessary functionality. However, if you need additional fields or functionality, you can use custom models.

Custom Flag Model
=================

To use a custom flag model, define a `WAFFLE_FLAG_MODEL` setting in your `settings.py`. The custom flag model must inherit from `waffle.models.AbstractBaseFlag` or `waffle.models.AbstractUserFlag`.

Example:

.. code-block:: python

    # settings.py
    WAFFLE_FLAG_MODEL = 'myapp.Flag'

    # models.py
    from waffle.models import AbstractUserFlag, CACHE_EMPTY
    from waffle.utils import get_setting, keyfmt, get_cache

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
            cache = get_cache()
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
        raw_id_fields = tuple(list(WaffleFlagAdmin.raw_id_fields) + ['companies'])
    admin.site.register(Flag, FlagAdmin)

To reference the custom flag model in your project, use the `get_waffle_flag_model` method.

.. code-block:: python

    from waffle import get_waffle_flag_model

    Flag = get_waffle_flag_model()


Custom Switch Model
===================

To use a custom switch model, define a `WAFFLE_SWITCH_MODEL` setting in your `settings.py`. The custom switch model must inherit from `waffle.models.AbstractBaseSwitch`.

Example:

.. code-block:: python

    # settings.py
    WAFFLE_SWITCH_MODEL = 'myapp.Switch'

    # models.py
    from waffle.models import AbstractBaseSwitch

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

To reference the custom switch model in your project, use the `get_waffle_switch_model` method.

.. code-block:: python

    from waffle import get_waffle_switch_model

    Switch = get_waffle_switch_model()


Custom Sample Model
===================

To use a custom sample model, define a `WAFFLE_SAMPLE_MODEL` setting in your `settings.py`. The custom sample model must inherit from `waffle.models.AbstractBaseSample`.

Example:

.. code-block:: python

    # settings.py
    WAFFLE_SAMPLE_MODEL = 'myapp.Sample'

    # models.py
    from waffle.models import AbstractBaseSample

    class Sample(AbstractBaseSample):

        owner = models.CharField(
            max_length=100,
            blank=True,
            help_text=_('The individual/team who owns this sample.'),
        )

    # admin.py
    from waffle.admin import SampleAdmin as WaffleSampleAdmin

    class SampleAdmin(WaffleSampleAdmin):
        raw_id_fields = tuple(list(WaffleSampleAdmin.raw_id_fields) + ['owner'])
    admin.site.register(Sample, SampleAdmin)

To reference the custom sample model in your project, use the `get_waffle_sample_model` method.

.. code-block:: python

    from waffle import get_waffle_sample_model

    Sample = get_waffle_sample_model()
