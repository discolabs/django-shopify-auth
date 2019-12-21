from django.contrib.auth.backends import RemoteUserBackend


class ShopUserBackend(RemoteUserBackend):
    def authenticate(self, request=None, myshopify_domain=None, token=None, **kwargs):
        if not myshopify_domain or not token or not request:
            return

        user = super(ShopUserBackend, self).authenticate(request=request, remote_user=myshopify_domain)

        if not user:
            return

        user.token = token
        user.save()
        return user
