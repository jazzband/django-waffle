from waffle.decorators import waffle_flag, waffle_switch


class WaffleFlagViewMixin(object):

    def get_flag_name(self):
        assert (
            hasattr(self, 'flag_name') and self.flag_name is not None
        ), (
            "'%s' should either include `flag_name` attribute, or "
            "override the `get_flag_name()` method."
            % self.__class__.__name__
        )
        return self.flag_name

    def get_inactive_flag_redirect_to(self):
        inactive_flag_redirect_to = getattr(
            self, 'inactive_flag_redirect_to', None)

        assert (
            inactive_flag_redirect_to is None or
            type(inactive_flag_redirect_to) == str
        ), (
            "If '%s.inactive_flag_redirect_to' is defined it should be "
            "a string."
            % self.__class__.__name__
        )

        return inactive_flag_redirect_to

    def dispatch(self, request, *args, **kwargs):
        redirect_to = self.get_inactive_flag_redirect_to()
        flag_name = self.get_flag_name()

        return waffle_flag(flag_name, redirect_to=redirect_to)(
            super(WaffleFlagViewMixin, self).dispatch
        )(request, *args, **kwargs)


class WaffleSwitchViewMixin(object):

    def get_switch_name(self):
        assert (
            hasattr(self, 'switch_name') and 
                self.switch_name is not None
        ), (
            "'%s' should either include `switch_name` attribute, or "
            "override the `get_switch_name()` method."
            % self.__class__.__name__
        )
        return self.switch_name

    def get_inactive_switch_redirect_to(self):
        inactive_switch_redirect_to = getattr(
            self, 'inactive_switch_redirect_to', None)

        assert (
            inactive_switch_redirect_to is None or 
            type(inactive_switch_redirect_to) == str
        ), (
            "If '%s.inactive_switch_redirect_to' is defined it should be "
            "a string."
            % self.__class__.__name__
        )

        return inactive_switch_redirect_to

    def dispatch(self, request, *args, **kwargs):
        redirect_to = self.get_inactive_switch_redirect_to()
        switch_name = self.get_switch_name()

        return waffle_switch(switch_name, redirect_to=redirect_to)(
            super(WaffleSwitchViewMixin, self).dispatch
        )(request, *args, **kwargs)
