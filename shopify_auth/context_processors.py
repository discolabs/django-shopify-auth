from django.conf import settings


def shopify_auth(request):
    return {
        'SHOPIFY_APP_NAME': getattr(settings, 'SHOPIFY_APP_NAME'),
        'SHOPIFY_APP_API_KEY': getattr(settings, 'SHOPIFY_APP_API_KEY'),
        'SHOPIFY_APP_IS_EMBEDDED': getattr(settings, 'SHOPIFY_APP_IS_EMBEDDED'),
        'SHOPIFY_APP_DEV_MODE': getattr(settings, 'SHOPIFY_APP_DEV_MODE'),
    }
