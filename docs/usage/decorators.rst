.. _usage-decorators:

=======================
Decorating entire views
=======================

Waffle provides decorators to wrap an entire view in a :ref:`flag
<types-flag>` or :ref:`switch <types-switch>`. (Due to their
always-random nature, no decorator is provided for :ref:`samples
<types-sample>`.)

When the flag or switch is active, the view executes normally. When it
is inactive, the view returns a 404. Optionally, you can provide a view or URL name where the decorator can redirect to if you don't want to show a 404 page when the flag or switch is inactive.


Flags
=====

::

    from waffle.decorators import waffle_flag

    @waffle_flag('flag_name')
    def myview(request):
        pass
    
    @waffle_flag('flag_name', 'url_name_to_redirect_to')
    def myotherview(request):
        pass

Switches
========

::

    from waffle.decorators import waffle_switch

    @waffle_switch('switch_name')
    def myview(request):
        pass

    @waffle_switch('switch_name', 'url_name_to_redirect_to')
    def myotherview(request):
        pass

Inverting Decorators
====================

Both ``waffle_flag`` and ``waffle_switch`` can be reversed (i.e. they
will raise a 404 if the flag or switch is *active*, and otherwise
execute the view normally) by prepending the name of the flag or switch
with an exclamation point: ``!``.

::

    @waffle_switch('!switch_name')
    def myview(request):
        """Only runs if 'switch_name' is OFF."""
