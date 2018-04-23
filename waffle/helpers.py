from waffle.callables import WaffleCallable


def waffle_flag_call(
        request, flag_name, active_callable, inactive_callable=None):
    from waffle import flag_is_active
    
    assert (
        type(active_callable) == WaffleCallable
    ), (
        'Passing a `active_callable` argument to `waffle_flag_call` is '
        'required and has to be a `WaffleCallable`'
    )

    assert (
        inactive_callable is None or type(inactive_callable) == WaffleCallable
    ), (
        'Passing a `inactive_callable` argument to `waffle_flag_call` is not '
        'required but if present it has to be a `WaffleCallable`'
    )

    if flag_name.startswith('!'):
        active = not flag_is_active(request, flag_name[1:])
    else:
        active = flag_is_active(request, flag_name)

    if active:
        return active_callable()

    if inactive_callable:
        return inactive_callable()


def waffle_switch_call(
        switch_name, active_callable, inactive_callable=None):
    from waffle import switch_is_active
    
    assert (
        type(active_callable) == WaffleCallable
    ), (
        'Passing a `active_callable` argument to `waffle_switch_call` is '
        'required and has to be a `WaffleCallable`'
    )

    assert (
        inactive_callable is None or type(inactive_callable) == WaffleCallable
    ), (
        'Passing a `inactive_callable` argument to `waffle_switch_call` is not '
        'required but if present it has to be a `WaffleCallable`'
    )

    if switch_name.startswith('!'):
        active = not switch_is_active(switch_name[1:])
    else:
        active = switch_is_active(switch_name)

    if active:
        return active_callable()

    if inactive_callable:
        return inactive_callable()
