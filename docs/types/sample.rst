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
