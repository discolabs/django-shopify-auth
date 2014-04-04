from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from .authorization import UserOwnedModelAuthorization


class UserOwnedModelResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        authorization = UserOwnedModelAuthorization()