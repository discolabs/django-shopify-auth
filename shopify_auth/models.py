import shopify

from django.conf import settings

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class ShopifyUserProfile(models.Model):
    myshopify_domain = models.CharField(max_length=255, unique=True, editable=False)
    token = models.CharField(
        max_length=64, editable=False, default="00000000000000000000000000000000"
    )

    def get_full_name(self):
        return self.myshopify_domain

    def get_short_name(self):
        return self.myshopify_domain

    def __str__(self):
        return self.get_full_name()

    @property
    def session(self):
        return shopify.Session.temp(
            self.myshopify_domain,
            getattr(settings, "SHOPIFY_APP_API_VERSION", "unstable"),
            self.token,
        )
