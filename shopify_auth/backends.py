from django.contrib.auth.backends import RemoteUserBackend


class ShopUserBackend(RemoteUserBackend):
    def authenticate(self, request=None, myshopify_domain=None, token=None, **kwargs):
        if not myshopify_domain or not token or not request:
            return

        try:
            user = super(ShopUserBackend, self).authenticate(request=request, remote_user=myshopify_domain)
        except TypeError:
            #  Django < 1.11 does not have request as a mandatory parameter for RemoteUserBackend
            user = super(ShopUserBackend, self).authenticate(remote_user=myshopify_domain)

        if not user:
            return

        user.token = token
        user.save(update_fields=['token'])
        return user
