from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
import shopify

from .helpers import add_query_parameters_to_url


class ShopifyLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin which verifies that the current shop is authenticated and app is installed in shopify.
    """
    
    def handle_no_permission(self):
        shopify_params = {
            k: self.request.GET[k]
            for k in ["shop", "timestamp", "signature", "hmac"]
            if k in self.request.GET
        }

        # Add the Shopify authentication parameters to the login URL.
        self.login_url = add_query_parameters_to_url(
            self.get_login_url(), shopify_params
        )
        return super().handle_no_permission()


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Handle mismatch between request and session
        shop_name = request.GET.get("shop", None)
        if shop_name and request.user.myshopify_domain != shop_name:
            logout(request)
            return self.handle_no_permission()

        # Initialize shop making sure we can still access it
        try:
            with request.user.session:
                self.shop = shopify.Shop.current()
        except:
            logout(request)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
