from django.conf import settings
from helpers import get_shopify_current_shop

def shopify_context(request):
  return {
    'shopify_current_shop': get_shopify_current_shop(),
    'SHOPIFY_APP_NAME':     settings.SHOPIFY_APP_NAME,
    'SHOPIFY_APP_API_KEY':  settings.SHOPIFY_APP_API_KEY,
    'SHOPIFY_APP_DEV_MODE': settings.SHOPIFY_APP_DEV_MODE,
  }