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

        try:
            user_shopify_profile = ShopifyUserProfile.objects.get_by_natural_key(username)
        except ShopifyUserProfile.DoesNotExist:
            return

        user = user_shopify_profile.user

        if not self.user_can_authenticate(user):
            return

        user.token = token
        user.save()
        return user

