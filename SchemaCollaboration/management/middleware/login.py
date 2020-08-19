# Partially copied from https://github.com/CleitonDeLima/django-login-required-middleware/blob/master/login_required/middleware.py
# (MIT license)

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'The LoginRequiredMiddleware requires authentication middleware '
            'to be installed. Edit your MIDDLEWARE setting to insert before '
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        if request.path.startswith(settings.LOGIN_REDIRECT_URL) and not request.user.is_active:
            return redirect_to_login(request.path)
