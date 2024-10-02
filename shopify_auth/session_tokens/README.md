# Authenticate an embedded app using session tokens

Session token based authentication comes with significant changes requried. I recommend you to follow this [article](https://shopify.dev/tutorials/authenticate-your-app-using-session-tokens).

This app takes care of the installation and provides middleware that adds a user to a request based on a request header.

I created a [demo app](https://github.com/digismoothie/django-session-token-auth-demo) that uses Hotwire, successor of Turbolinks.

> [!NOTE]  
> Managed installation is much more involved because there's no speficic install entrypoint. The main entrypoint is used instead. For now you can use managed_install.py and session_token_bounce view.

### Instalation

### 1. Install package
Installation is super easy via `pip`:

```shell
> pip install django-shopify-auth
```

Once you have the package installed, add `shopify_auth` to your `INSTALLED_APPS`.


### 2. Add custom user model

This package requires that the user model for your app (specified by `AUTH_USER_MODEL` in your `settings.py`) inherits
from `shopify_auth.models.AbstractShopUser`. To do this, just add something like this to the `models.py` for your
Django app:

```python
# auth_demo/auth_app/models.py
from shopify_auth.models import AbstractShopUser

class AuthAppShopUser(AbstractShopUser):
    pass
```

Before moving forward, ensure this model has been added to the database by running
```
python manage.py makemigrations
python manage.py migrate
```

Then make sure that you have the following line or similar in `settings.py`:

```python
AUTH_USER_MODEL = 'auth_app.AuthAppShopUser'
```


### 3. Configure settings
In addition to setting `AUTH_USER_MODEL`, there are a few more required additions to `settings.py`:

```python
# Configure Shopify Application settings
SHOPIFY_APP_NAME = 'Your App Name'
SHOPIFY_APP_API_KEY = os.environ.get('SHOPIFY_APP_API_KEY')
SHOPIFY_APP_API_SECRET = os.environ.get('SHOPIFY_APP_API_SECRET')
SHOPIFY_APP_API_SCOPE = ['read_products', 'read_orders']
# Find API version to pin at https://help.shopify.com/en/api/versioning
SHOPIFY_APP_API_VERSION = "0000-00"

# Add the Shopify Auth template context processor to the list of processors.
# Note that this assumes you've defined TEMPLATE_CONTEXT_PROCESSORS earlier in your settings.
TEMPLATE_CONTEXT_PROCESSORS += (
    'shopify_auth.session_tokens.context_processors.shopify_auth',
)

# Use the Shopify Auth user model.
AUTH_USER_MODEL = 'auth_app.AuthAppShopUser'

# Set secure proxy header to allow proper detection of secure URLs behind a proxy.
# This ensures that correct 'https' URLs are generated when our Django app is running behind a proxy like nginx, or is
# being tunneled (by ngrok, for example).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Note that in the example above, the application API key and API secret are pulled from environment settings, which is a
best practice for Django apps that helps avoid the accidental check-in of sensitive information to source files.

Now that all of the settings are configured, you can run `migrate` to set up the database for your new user model:

```shell
> python manage.py migrate
```

### 4. Configure authentication based on what Views are you using.

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

### 5. Configure URL mappings

Include `shopify_auth.session_tokens` URLs in your project's `urls.py`:

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("auth/", include("shopify_auth.session_tokens.urls", namespace="session_tokens")),

    # ... remaining configuration here ...
]
```

### 6. Create view that supports unauthenticated requests.


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
        encoded_host = request.GET.get("host") # New in App Bridge 2.0

        if not myshopify_domain:
            return HttpResponse("Shop parameter missing.")
        try:
            shop = get_user_model().objects.get(myshopify_domain=myshopify_domain)
        except get_user_model().DoesNotExist:
            return get_scope_permission(request, myshopify_domain)

        with shop.session:
            try:
                shopify_shop = shopify.Shop.current()
                # Do your billing logic here
            except UnauthorizedAccess:
                shop.uninstall()
                return get_scope_permission(request, myshopify_domain)

        if not encoded_host:
            return redirect(f"https://{myshopify_domain}/admin/apps/{settings.SHOPIFY_APP_API_KEY}")

        user_logged_in.send(sender=shop.__class__, request=request, user=shop)

        return render(
            request,
            self.template_name,
            {
                "data": {
                    "shopOrigin": shop.myshopify_domain,
                    "apiKey": getattr(settings, "SHOPIFY_APP_API_KEY"),
                    "encodedHost": encoded_host,
                }
            },
        )
```