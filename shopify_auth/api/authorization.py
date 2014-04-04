from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


def all_owned_by_user(object_list, user):
    """
    Helper method to check whether all objects is the given list
    are owned by the given user. This all or nothing approach is
    taken because there are never situations where users should
    be able to even read a list of objects they don't have
    permissions over.
    """
    for object in object_list:
        if object.user != user:
            return False
    return True


class UserOwnedModelAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(user = bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        if not all_owned_by_user(object_list, bundle.request.user):
            raise Unauthorized()
        return object_list

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        if not all_owned_by_user(object_list, bundle.request.user):
            raise Unauthorized()
        return object_list

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user