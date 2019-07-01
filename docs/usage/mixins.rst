.. _usage-mixins:

============================
Mixins for Class Based Views
============================

Waffle provides mixins to add to Class Based Views.

When the flag or switch is active, or a sample returns True, the view executes normally.
When it is inactive, the view returns a 404.

WaffleFlagMixin
===============

.. code-block:: python

    from waffle.mixins import WaffleFlagMixin

    class MyClass(WaffleFlagMixin, View):
        waffle_flag = "my_flag"


WaffleSwitchMixin
=================

.. code-block:: python

    from waffle.mixins import WaffleSwitchMixin

    class MyClass(WaffleSwitchMixin, View):
        waffle_switch= "my_switch"


WaffleSampleMixin
=================

.. code-block:: python

    from waffle.mixins import WaffleSampleMixin

    class MyClass(WaffleSampleMixin, View):
        waffle_switch= "my_sample"