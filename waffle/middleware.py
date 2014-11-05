from django.utils.encoding import smart_str

from . import settings


class WaffleMiddleware(object):
    def process_response(self, request, response):
        secure = settings.SECURE
        max_age = settings.MAX_AGE

        if hasattr(request, 'waffles'):
            for k in request.waffles:
                name = smart_str(settings.COOKIE_NAME % k)
                active, rollout = request.waffles[k]
                if rollout and not active:
                    # "Inactive" is a session cookie during rollout mode.
                    age = None
                else:
                    age = max_age
                response.set_cookie(name, value=active, max_age=age,
                                    secure=secure)
        if hasattr(request, 'waffle_tests'):
            for k in request.waffle_tests:
                name = smart_str(settings.TEST_COOKIE_NAME % k)
                value = request.waffle_tests[k]
                response.set_cookie(name, value=value)

        return response
