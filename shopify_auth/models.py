import shopify

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class ShopUserManager(BaseUserManager):

    def create_user(self, myshopify_domain, password=None):
        """
        Creates and saves a ShopUser with the given domain and password.
        """
        if not myshopify_domain:
            raise ValueError('ShopUsers must have a myshopify domain')

        user = self.model(myshopify_domain=myshopify_domain)

        # Never want to be able to log on externally.
        # Authentication will be taken care of by Shopify OAuth.
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, myshopify_domain, password):
        """
        Creates and saves a ShopUser with the given domains and password.
        """
        return self.create_user(myshopify_domain, password)


class AbstractShopUser(AbstractBaseUser):
    myshopify_domain = models.CharField(max_length=255, unique=True, editable=False)
    token = models.CharField(max_length=64, editable=False, default='00000000000000000000000000000000')

    objects = ShopUserManager()

    USERNAME_FIELD = 'myshopify_domain'

    @property
    def session(self):
        return shopify.Session.temp(self.myshopify_domain, getattr(settings, 'SHOPIFY_APP_API_VERSION', 'unstable'), self.token)

    def get_full_name(self):
        return self.myshopify_domain

    def get_short_name(self):
        return self.myshopify_domain

    def __str__(self):
        return self.get_full_name()

    class Meta:
        abstract = True
