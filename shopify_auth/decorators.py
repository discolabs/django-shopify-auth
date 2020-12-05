
from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.encoding import force_str
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required as django_login_required

from .helpers import add_query_parameters_to_url

def is_anonymous(user):
    return user.is_anonymous

def anonymous_required(function=None, redirect_url=None):
    """
    Decorator requiring the current user to be anonymous (not logged in).
    """
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        is_anonymous,
        login_url=redirect_url,
        redirect_field_name=None
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required(f, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator that wraps django.contrib.auth.decorators.login_required, but supports extracting Shopify's authentication
    query parameters (`shop`, `timestamp`, `signature` and `hmac`) and passing them on to the login URL (instead of just
    wrapping them up and encoding them in to the `next` parameter).

    This is useful for ensuring that users are automatically logged on when they first access a page through the Shopify
    Admin, which passes these parameters with every page request to an embedded app.
    """

    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)

        # Extract the Shopify-specific authentication parameters from the current request.
        shopify_params = {
            k: request.GET[k]
            for k in ['shop', 'timestamp', 'signature', 'hmac']
            if k in request.GET
        }

        # Get the login URL.
        resolved_login_url = force_str(resolve_url(login_url or settings.LOGIN_URL))

        # Add the Shopify authentication parameters to the login URL.
        updated_login_url = add_query_parameters_to_url(resolved_login_url, shopify_params)

        django_login_required_decorator = django_login_required(redirect_field_name=redirect_field_name,
                                                                login_url=updated_login_url)
        return django_login_required_decorator(f)(request, *args, **kwargs)

    return wrapper
