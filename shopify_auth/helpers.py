from django.conf import settings
from urlparse import urlparse
import shopify

def get_shopify_current_shop(get_shopify_dev_shop = get_shopify_dev_shop):
  """
  Get the Shopify Shop being used for the current session.
  Checks the SHOPIFY_APP_DEV_MODE flag.
  """
  if not shopify.ShopifyResource.site:
    return None

  # If in dev mode, we don't actually use the Shopify API to fetch the
  # current shop. Instead, we create a skeleton Shop object with the
  # 'site' attribute from the current setting being used to populate
  # the myshopify_domain attribute.
  #
  # The get_shopify_current_shop() method can be called with an optional
  # 'get_shopify_dev_shop' keyword argument, which points to a method
  # that takes a shop as a parameter, performs any initialisation, and
  # returns the shop.
  #
  # This can be useful to use an existing database of shop information
  # to populate the returned Shop object.
  if settings.SHOPIFY_APP_DEV_MODE:
    shop = shopify.Shop()
    shop.myshopify_domain = urlparse(shopify.ShopifyResource.site).netloc
    return get_shopify_dev_shop(shop)

  # Not in dev mode - just use the Shopify API to return the current shop.
  return shopify.Shop.current()

def get_shopify_dev_shop(shop):
  """
  The default method used to populate the Shopify Shop object when in dev
  mode.
  """
  return shop