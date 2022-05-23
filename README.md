Django Shopify Auth
===================

[![PyPI version](https://badge.fury.io/py/django-shopify-auth.svg)](http://badge.fury.io/py/django-shopify-auth)
![example workflow](https://github.com/discolabs/django-shopify-auth/actions/workflows/ci.yml/badge.svg)

This Django package makes it easy to integrate Shopify authentication into your Django app.

* It provides a custom Django Authentication scheme based on `AbstractBaseUser` and `RemoteUserBackend`, meaning shops
  will be authenticated as "users" of your Django app. This makes it easier to use common Django patterns and libraries
  (such as accessing the currently authenticated store as `request.user`).

* It persists users' Shopify access tokens in the database, rather than in the Session, meaning your app will be able
  to make API calls on behalf of a user when they're not logged in.

* It supports the token-based authentication flow for Embedded Shopify apps.

Embedded vs Standalone apps
--------------

Session token-based authentication is now required for embedded apps. Support for it is implemented in [separate app](shopify_auth/session_tokens/). Read [this](https://shopify.dev/apps/getting-started/app-types#embedded-apps) if you're not sure what approach to use.

Requirements
------------
Tests are run against Django versions defined in `.github/workflows/ci.yml`. This package may work for
other Django versions but it's not guaranteed.

You'll need a [Shopify partner account](http://shopify.com/partners) and to have created an app in order to get an API key and secret.


Package Installation and Setup - Standalone app
------------------------------
There are a few moving parts to set up, but hopefully the following instructions will make things straightforward.

We're assuming in this setup that you're using a standard Django project layout (the sort that's created with the
`django-admin.py startproject` command). We're also assuming that our project is called `auth_demo` and that the primary
Django app inside our project is going to be called `auth_app`.


### 1. Install package
Installation is super easy via `pip`:

```shell
> pip install django-shopify-auth
```

Once you have the package installed, add `shopify_auth` to your `INSTALLED_APPS`.


### 2. Add custom user model
Because `shopify_auth` makes use of Django's authentication system, it provides a custom authentication backend
(`shopify_auth.backends.ShopUserBackend`) which allows authentication through Shopify's OAuth flow.

This backend requires that the user model for your app (specified by `AUTH_USER_MODEL` in your `settings.py`) inherits
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
SHOPIFY_APP_IS_EMBEDDED = False
SHOPIFY_APP_DEV_MODE = False

# Use the Shopify Auth authentication backend as the sole authentication backend.
AUTHENTICATION_BACKENDS = (
    'shopify_auth.backends.ShopUserBackend',
)

# Add the Shopify Auth template context processor to the list of processors.
# Note that this assumes you've defined TEMPLATE_CONTEXT_PROCESSORS earlier in your settings.
TEMPLATE_CONTEXT_PROCESSORS += (
    'shopify_auth.context_processors.shopify_auth',
)

# Use the Shopify Auth user model.
AUTH_USER_MODEL = 'auth_app.AuthAppShopUser'

# Set the login redirect URL to the "home" page for your app (where to go after logging on).
LOGIN_REDIRECT_URL = '/'

# Set secure proxy header to allow proper detection of secure URLs behind a proxy.
# This ensures that correct 'https' URLs are generated when our Django app is running behind a proxy like nginx, or is
# being tunneled (by ngrok, for example).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Note that in the example above, the application API key and API secret are pulled from environment settings, which is a
best practice for Django apps that helps avoid the accidental check-in of sensitive information to source files.

Setting `SHOPIFY_APP_DEV_MODE` to `True` allows you to test your apps locally by skipping the external OAuth phase for
your app. As it means you can log into your app as any store, you should obviously ***never*** set this to `True` in
production.

Now that all of the settings are configured, you can run `migrate` to set up the database for your new user model:

```shell
> python manage.py migrate
```


### 4. Configure URL mappings

Include `shopify_auth` URLs in your project's `urls.py`:

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path('login/', include('shopify_auth.urls')),

    # ... remaining configuration here ...
]
```

### 5. Create application views
Now that you've gotten the configuration out of the way, you can start building your application.

All views inside your application should be decorated with `@login_required`.
This decorator will check that a user has authenticated through the Shopify OAuth flow.
If they haven't, they'll be redirected to the login screen.

```python
from django.shortcuts import render
from shopify_auth.decorators import login_required

@login_required
def home(request, *args, **kwargs):
    return render(request, "my_app/home.html")
```

### 6. Making Shopify API calls
To make Shopify API calls on behalf of a user, we can use the user's `session` property inside a `with` statement:

```python
def view(request, *args, **kwargs):

    # Get a list of the user's products.
    with request.user.session:
        products = shopify.Product.find()

    # ... remaining view code ...
```

Behind the scenes, using `with request.user.session` sets up a temporary Shopify API session using the OAuth token we
obtained for that specific user during authentication.

All code wrapped within the `with` statement is executed in the context of the specified user. You should always wrap
calls to the Shopify API using this pattern.


Partner Application Setup
-------------------------
In addition to getting the package up and running in your local Django project, you'll need to configure your
application via the Shopify Partner dashboard.

To avoid getting an OAuth error while customers try to install your application, make sure your application's settings
include the absolute URL to `/login/finalize/` (including the trailing slash) in their whitelisted URLs. For example,
if your application resides at `https://myapp.example.com`, then you should include
`https://myapp.example.com/login/finalize/` in the "Redirection URL" section of your application settings.


Questions or Problems?
----------------------

Read up on the possible API calls:
<https://shopify.dev/>

Ask technical questions on Stack Overflow:
<https://stackoverflow.com/questions/tagged/shopify>


Release History
---------------

Refer to the [change log](https://github.com/discolabs/django-shopify-auth/blob/master/CHANGELOG.md) for a full list of changes.

Special Thanks
--------------

A big shout-out to [Josef Rousek](https://github.com/stlk) for his contributions and help maintaining this package.

Work with us!
------------------

If you want to work with Django and maybe even React, the current maintainer [Digismoothie.com is hiring](https://www.digismoothie.com/company/careers).
