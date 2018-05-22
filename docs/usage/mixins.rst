.. _usage-mixins:

============================
Mixins for class based views
============================

Waffle provides mixins to check if a :ref:`flag<types-flag>` or 
:ref:`switch <types-switch>` switch is active. (Due to their
always-random nature, no mixin is provided for :ref:`samples
<types-sample>`.)

It works the same way as the :ref:`decorators <usage-decorators>` but 
you define the flag name and redirect route as view attributes 
(or by overriding the methods that get these attributes).


Flags
=====

::

    from waffle.mixins import WaffleFlagViewMixin
    from django.views.generics import View 


    class MyView(WaffleFlagViewMixin, View):
        flag_name = 'flag_name'
        inactive_flag_redirect_to = 'url_name_to_redirect_to'

        def get(self, request, *args, **kwargs):
            pass

Switches
========

::

    from waffle.mixins import WaffleFlagViewMixin
    from django.views.generics import View 


    class MyView(WaffleSwitchViewMixin, View):
        flag_name = 'flag_name'
        inactive_flag_redirect_to = 'url_name_to_redirect_to'

        def get(self, request, *args, **kwargs):
            pass

Inverting Decorators
====================

Both ``WaffleFlagViewMixin`` and ``WaffleSwitchViewMixin`` can be 
reversed the same way you can do with the decorators (i.e. they 
will raise a 404 or redirect if the flag or switch is *active*, 
and otherwise execute the view normally) by prepending the name 
of the flag or switch with an exclamation point: ``!``.

::

    from waffle.mixins import WaffleFlagViewMixin
    from django.views.generics import View 


    class MyView(WaffleSwitchViewMixin, View):
        flag_name = '!flag_name'
        inactive_flag_redirect_to = 'url_name_to_redirect_to'

        def get(self, request, *args, **kwargs):
            pass

Chose flag name and redirect url depending on the request
=========================================================

Both ``WaffleFlagViewMixin`` and ``WaffleSwitchViewMixin`` have a
``get_flag_name()`` and a ``get_inactive_flag_redirect_to()`` 
methods. If you want to use information from the request to define
which flag you want to check or the redirect route in case the 
flag is not active you can override these methods.

::

    from waffle.mixins import WaffleFlagViewMixin
    from django.views.generics import View 


    class MyView(WaffleSwitchViewMixin, View):
        flag_name = 'flag_name'

        def get_inactive_flag_redirect_to(self, request, *args, **kwargs):
            if self.request.method == 'POST':
                return 'url_name_to_redirect_to'
            else:
                return 'another_url_name_to_redirect_to'

        def get(self, request, *args, **kwargs):
            pass