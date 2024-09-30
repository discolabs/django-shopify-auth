from django.core.checks import Error, register
from django.conf import settings

@register()
def check_shopify_auth_bounce_page_url(app_configs, **kwargs):
    errors = []
    if not hasattr(settings, 'SHOPIFY_AUTH_BOUNCE_PAGE_URL'):
        errors.append(
            Error(
                'SHOPIFY_AUTH_BOUNCE_PAGE_URL is not set in settings.',
                hint='Set SHOPIFY_AUTH_BOUNCE_PAGE_URL in your settings file or environment variables.',
                id='shopify_auth.E001',
            )
        )
    elif not settings.SHOPIFY_AUTH_BOUNCE_PAGE_URL:
        errors.append(
            Error(
                'SHOPIFY_AUTH_BOUNCE_PAGE_URL is empty.',
                hint='Provide a valid URL for SHOPIFY_AUTH_BOUNCE_PAGE_URL in your settings file or environment variables.',
                id='shopify_auth.E002',
            )
        )
    return errors