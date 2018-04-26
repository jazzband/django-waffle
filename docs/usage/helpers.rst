.. _helpers:

=============================
Helpers for flags based logic
=============================

Django Waffle provide some helpers and decorators to make easy to adapt
your logic to be based on flags/switches status, and also make easy to 
remove these flags/switched from code after the feature is accepted or
rejected.   


Waffle callables
================

The best way to make a feature flip is by modularizing your code, so
the active and inactive states logic don't get mixed. This way is 
easier to read the code and to remove the feature flag/switch after.

Django Waffle provides a ``@waffle_callable`` decorator to mark
functions to be called or not by the helpers depending on the 
flag/switch state at the moment.

Eg.::
    
    from waffle.decorators import waffle_callable

    @waffle_callable
    def my_great_function(a, b, c):
        return [a, b, c]


Flags
=====

There is a ``waffle_flag_call()`` helper to branch logic depending on 
flag state. It receives the request, the flag name, the active state
waffle_callable and the inactive waffle_callable (optional).

It checks whether the flag is active and calls the proper 
``waffle_callable``::

    waffle_flag_call(
        request, 'my-flag', my_great_function(1, 2, 3), 
        my_inactve_function())

If you want to check if the feature is inactive to run your 
waffle_callable, you can add an exclamation point before your flag 
name::

    from waffle import waffle_flag_call

    waffle_flag_call(
        request, '!my-flag', my_inactve_function())

Switches
========

The logic is the same as for flags. There's a ``waffle_switch_call()``
helper to branch logic depending on the flag  state. It receives the 
the flag name, the active state waffle_callable and the inactive 
waffle_callable (optional).

It checks whether the flag is active and calls the proper 
``waffle_callable``::

    from waffle import waffle_switch_call

    waffle_switch_call(
        'my-switch', my_great_function(1, 2, 3), my_inactve_function())

If you want to check if the feature is inactive to run your 
waffle_callable, you can add an exclamation point before your switch 
name::

    waffle_switch_call('!my-switch', my_inactve_function())
