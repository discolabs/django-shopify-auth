from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ShopUserManager(BaseUserManager):

    def create_user(self, myshopify_domain, domain, password = None):
        """
        Creates and saves a ShopUser with the given domains and password.
        """
        if not myshopify_domain:
            raise ValueError('ShopUsers must have a myshopify domain')

        user = self.model(
            myshopify_domain = myshopify_domain,
            domain = domain,
        )

        # Never want to be able to log on externally.
        # Authentication will be taken care of by Shopify OAuth.
        user.set_unusable_password()
        user.save(using = self._db)
        return user

    def create_superuser(self, myshopify_domain, domain, password):
        """
        Creates and saves a ShopUser with the given domains and password.
        """
        return self.create_user(myshopify_domain, domain, password)


class AbstractShopUser(AbstractBaseUser):
    myshopify_domain  = models.CharField(max_length = 255, unique = True)
    token             = models.CharField(max_length = 32)

    objects = ShopUserManager()

    USERNAME_FIELD  = 'myshopify_domain'

    def get_full_name(self):
        return self.myshopify_domain

    def get_short_name(self):
        return self.myshopify_domain

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        abstract = True


class UserOwnedModelManager(models.Manager):

    def filter_for_user(self, user):
        return super(UserOwnedModelManager, self).get_queryset().filter(user = user)


class UserOwnedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable = False)

    objects = UserOwnedModelManager()

    class Meta:
        abstract = True