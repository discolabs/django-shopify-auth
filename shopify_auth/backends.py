from django.contrib.auth.backends import RemoteUserBackend
from shopify_auth.models import ShopifyUserProfile


class ShopUserBackend(RemoteUserBackend):
    create_unknown_user = True

    def authenticate(self, request=None, myshopify_domain=None, token=None, **kwargs):
        """
        The username passed as ``remote_user`` is considered trusted. Return
        the ``User`` object with the given username. Create a new ``User``
        object if ``create_unknown_user`` is ``True``.

        Return None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not myshopify_domain or not token or not request:
            return

        username = self.clean_username(myshopify_domain)

        user = super(ShopUserBackend, self).authenticate(
            request=request, remote_user=myshopify_domain
        )
        if not user.shopify_user_profile:
            shopify_user_profile = ShopifyUserProfile.objects.create(
                myshopify_domain=myshopify_domain
            )
        else:
            shopify_user_profile = user.shopify_user_profile

        if not user or not self.user_can_authenticate(user):
            return

        shopify_user_profile.token = token
        user.shopify_user_profile = shopify_user_profile
        shopify_user_profile.save()
        user.save()
        return user
