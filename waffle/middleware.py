from django.conf import settings


class WaffleMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request, 'waffles'):
            secure = getattr(settings, 'WAFFLE_SECURE', False)
            max_age = getattr(settings, 'WAFFLE_MAX_AGE', 2592000)  # 1 month
            format = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
            for k in request.waffles:
                response.set_cookie(format % k, value=request.waffles[k],
                                    max_age=max_age, secure=secure)
        return response
