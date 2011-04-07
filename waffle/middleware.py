from django.conf import settings
from django.utils.encoding import smart_str

from waffle import COOKIE_NAME


class WaffleMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request, 'waffles'):
            secure = getattr(settings, 'WAFFLE_SECURE', False)
            max_age = getattr(settings, 'WAFFLE_MAX_AGE', 2592000)  # 1 month
            for k in request.waffles:
                name = smart_str(COOKIE_NAME % k)
                active, rollout = request.waffles[k]
                if rollout and not active:
                    # "Inactive" is a session cookie during rollout mode.
                    age = None
                else:
                    age = max_age
                response.set_cookie(name, value=active, max_age=age,
                                    secure=secure)
        return response
