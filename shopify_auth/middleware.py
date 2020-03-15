from django.contrib.auth import get_user_model
from shopify_auth.decorators import is_authenticated
from django.contrib.auth import authenticate, login


class VerifyRequestMiddleware:
    """ Login again if user changed. """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_authenticated(request.user):
            query_shop = request.GET.get('shop', request.POST.get('shop'))

            if query_shop is not None and query_shop != request.user.myshopify_domain:
                user = get_user_model().objects.get(myshopify_domain=query_shop)
                user = authenticate(request=request, myshopify_domain=user.myshopify_domain, token=user.token)
                if user is not None:
                    login(request, user)

        response = self.get_response(request)
        return response
