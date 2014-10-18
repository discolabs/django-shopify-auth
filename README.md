Django Shopify Auth
===================

This Django package makes it easy to integrate Shopify authentication into your Django app. It shares some similarities
with the [shopify_django_app](https://github.com/Shopify/shopify_django_app) project, but with a couple of key
differences:


* It provides a custom Django Authentication scheme based on `AbstractBaseUser` and `RemoteUserBackend`, meaning shops
  will be authenticated as 'users' of your Django app. This makes it easier to use common Django patterns and libraries
  (such as accessing the currently authenticated store as `request.user`).

* It persists users' Shopify access tokens in the database, rather than in the Session, meaning your app will be able
  to make API calls on behalf of a user when they're not logged in.

* It supports the authentication flow for new-style 'Embedded' Shopify apps.


This project provides one package, `shopify_auth`. We'll add a demo app soon.


Requirements
------------

Django v1.7 or higher is required.

As with the original `shopify_django_app` package, you'll need a [Shopify partner account](http://shopify.com/partners)
and to have created an app in order to get an API key and secret.


Installation
------------

Add this package to your project by either cloning this repository and copying `shopify_auth` to your apps directory,
or via `pip` with:

````
pip install django-shopify-auth
````

Once you have the package installed, add `shopify_auth` to your `INSTALLED_APPS` and set the following in your
`settings.py`:

````
SHOPIFY_APP_NAME = 'Your App Name'
SHOPIFY_APP_API_KEY = get_env_setting('SHOPIFY_APP_API_KEY')
SHOPIFY_APP_API_SECRET = get_env_setting('SHOPIFY_APP_API_SECRET')
SHOPIFY_APP_API_SCOPE = ['read_products', 'read_orders']
SHOPIFY_APP_IS_EMBEDDED = True
SHOPIFY_APP_DEV_MODE = False
````

Note that in the example above, the API key and secret are pulled from environment settings, which is a best practice
for Django apps that helps avoid the accidental check-in of sensitive information to source files.

Set `SHOPIFY_APP_IS_EMBEDDED` to `True` if your app has been configured as an Embedded app (you choose this option at
the time of app creation). Setting this will make the app provide a Javascript-based redirect that breaks out of an
embedded app's `<iframe>` during the authentication flow as per [the Shopify documentation](http://docs.shopify.com/embedded-app-sdk).
If `SHOPIFY_APP_IS_EMBEDDED` is `False`, the normal authentication flow for non-Embedded apps will be used.

Setting `SHOPIFY_APP_DEV_MODE` to `True` allows you to test your apps locally by skipping the external OAuth phase for
your app. As it means you can log into your app as any store, you should obviously ***never*** set this to `True` in
production.


Questions or Problems?
----------------------

Read up on the possible API calls:
<http://api.shopify.com>

Learn how to use the `shopify_python_api` library:
<http://wiki.shopify.com/Using_the_shopify_python_api>

Ask technical questions on Stack Overflow:
<http://stackoverflow.com/questions/tagged/shopify>

Email me:
[gavin@gavinballard.com](mailto:gavin@gavinballard.com)
