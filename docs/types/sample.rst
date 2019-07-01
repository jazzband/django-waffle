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

Wether or not you enabled :ref:`Auto Create Missing Sample <types-sample-auto-create-missing>`,
it can be practical to be informed that a sample was or is missing.
If you'd like waffle to log a warning, error, ... you can set :ref:`WAFFLE_LOG_MISSING_SAMPLES
<starting-configuring>` to any level known by Python default logger.
