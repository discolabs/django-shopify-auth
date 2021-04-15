# Authenticate an embedded app using session tokens

Session token based authentication comes with significant changes requried. I recommend you to follow this [article](https://shopify.dev/tutorials/authenticate-your-app-using-session-tokens).

This app takes care of the installation and provides middleware that adds a user to a request based on a request header.

I created a [demo app](https://github.com/digismoothie/django-session-token-auth-demo) that uses Hotwire, successor of Turbolinks.

### Instalation

1. Add `shopify_auth` to `INSTALLED_APPS`.

myproject/settings.py
```python
INSTALLED_APPS = [
    ...
    "shopify_auth",
    ...
]
```

2. Configure authentication based on what Views are you using.

#### Plain Django views

myproject/settings.py
```python
MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "shopify_auth.session_tokens.middleware.SessionTokensAuthMiddleware", # This middleware has to be after django.contrib.auth.middleware.AuthenticationMiddleware.
    ...
]
```

#### Django REST Framework

myproject/settings.py
```python
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["shopify_auth.session_tokens.authentication.ShopifyTokenAuthentication"]}
```

3. Add `path("auth/", include("shopify_auth.session_tokens.urls", namespace="session_tokens")),` to your project's `urls.py`.

4. Create view that supports unauthenticated requests.


```python
import shopify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from pyactiveresource.connection import UnauthorizedAccess
from shopify_auth.session_tokens.views import get_scope_permission


class DashboardView(generic.View):
    template_name = "myapp/dashboard.html"

    def get(self, request):
        myshopify_domain = request.GET.get("shop")

        if not myshopify_domain:
            return HttpResponse("Shop parameter missing.")
        try:
            shop = get_user_model().objects.get(myshopify_domain=myshopify_domain)
        except get_user_model().DoesNotExist:
            return get_scope_permission(request, myshopify_domain)

        with shop.session:
            try:
                shopify_shop = shopify.Shop.current()
            except UnauthorizedAccess:
                shop.uninstall()
                return get_scope_permission(request, myshopify_domain)

        user_logged_in.send(sender=shop.__class__, request=request, user=shop)

        return render(
            request,
            self.template_name,
            {
                "data": {
                    "shopOrigin": shop.myshopify_domain,
                    "apiKey": getattr(settings, "SHOPIFY_APP_API_KEY"),
                }
            },
        )
```