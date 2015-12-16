from django.contrib.auth.backends import RemoteUserBackend


class ShopUserBackend(RemoteUserBackend):

    def authenticate(self, myshopify_domain=None, token=None, **kwargs):
        if not myshopify_domain or not token:
            return

        user = super(ShopUserBackend, self).authenticate(remote_user=myshopify_domain)
        if not user:
            return

        user.token = token
        user.save(update_fields=['token'])
        return user
