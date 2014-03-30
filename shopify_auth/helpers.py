from django.conf import settings
import shopify

def get_shopify_current_shop():
  if not shopify.ShopifyResource.site:
    return None

  if settings.SHOPIFY_APP_DEV_MODE:
    shop = shopify.Shop()
    shop.domain = shopify.ShopifyResource.site
    shop.myshopify_domain = shopify.ShopifyResource.site
    return shop

  return shopify.Shop.current() if shopify.ShopifyResource.site else None