.. _types-sample:

=======
Samples
=======

Samples are on a given percentage of the time. They do not require a
request object and can be used in other contexts, such as management
commands and tasks.

.. warning::

    Sample values are random: if you check a Sample twice, there is no
    guarantee you will get the same value both times. If you need to
    rely on the value more than once, you should store it in a variable.

    ::

        # YES
        foo_on = sample_is_active('foo')
        if foo_on:
            pass

        # ...later...
        if foo_on:
            pass

    ::

        # NO!
        if sample_is_active('foo'):
            pass

        # ...later...
        if sample_is_active('foo'):  # INDEPENDENT of the previous check
            pass


Sample Attributes
=================

Samples can be administered through the Django `admin site`_ or the
:ref:`command line <usage-cli>`. They have the following attributes:

:Name:
    The name of the Sample.
:Percent:
    A number from 0.0 to 100.0 that determines how often the Sample
    will be active.
:Note:
    Describe where the Sample is used.


.. _admin site: https://docs.djangoproject.com/en/dev/ref/contrib/admin/


.. _types-custom-sample-models:

Custom Sample Models
======================

For many cases, the default Sample model provides all the necessary functionality.
If you would like additional fields not supported by the default Sample model,
you can use a custom Sample model.

An application needs to define a ``WAFFLE_SAMPLE_MODEL`` settings. The default is ``waffle.Sample``
but can be pointed to an arbitrary object.

.. note::

    It is not possible to change the Sample model and generate working migrations. Ideally, the Sample
    model should be defined at the start of a new project. This is a limitation of the `swappable`
    Django magic. Please use magic responsibly.

The custom Sample model must inherit from `waffle.models.AbstractBaseSample`.

When using a custom Sample model, you must run Django's
``makemigrations`` before running migrations as outlined in the :ref:`installation docs
<installation-settings-migrations>`.

If you need to reference the class that is being used as the `Sample` model in your project, use the
``get_waffle_model('SAMPLE_MODEL')`` method. If you reference the Switch a lot, it may be convenient
to add ``Switch = get_waffle_model('SAMPLE_MODEL')`` right below your imports and reference the Sample
model as if it had been imported directly.

Example:

.. code-block:: python

    # settings.py
    WAFFLE_SAMPLE_MODEL = 'myapp.Sample'

    # models.py
    from waffle.models import AbstractBaseSample, CACHE_EMPTY

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


.. _types-sample-auto-create-missing:

Auto Create Missing
===================

When a sample is evaluated in code that is missing in the database the
sample returns the :ref:`WAFFLE_SAMPLE_DEFAULT <starting-configuring>`
value but does not create a sample in the database. If you'd like
waffle to create missing samples in the database whenever it
encounters a missing sample you can set
:ref:`WAFFLE_CREATE_MISSING_SAMPLES <starting-configuring>` to
``True``. If :ref:`WAFFLE_SAMPLE_DEFAULT <starting-configuring>` is ``True`` then the
``Percent`` attribute of the sample will be created as 100.0 (so that
when the sample is checked it always evaluates to
``True``). Otherwise the value will be set to 0.0 so that the sample
always evaluates to ``False``.


.. _types-sample-log-missing:

Log Missing
===================

Whether or not you enabled :ref:`Auto Create Missing Sample <types-sample-auto-create-missing>`,
it can be practical to be informed that a sample was or is missing.
If you'd like waffle to log a warning, error, ... you can set :ref:`WAFFLE_LOG_MISSING_SAMPLES
<starting-configuring>` to any level known by Python default logger.
