from django.conf import settings
import shopify

def shopify_context(request):
  return {
    'shopify_current_shop': shopify.Shop.current() if shopify.ShopifyResource.site else None,
    'shopify_app_api_key':  settings.SHOPIFY_APP_API_KEY,
  }