import sys
import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'shopify_auth',
    ),
    AUTHENTICATION_BACKENDS=(
        'shopify_auth.backends.ShopUserBackend',
    ),
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True
        }
    ],
    ROOT_URLCONF = 'shopify_auth.urls',
    SHOPIFY_APP_NAME='Test App',
    SHOPIFY_APP_API_KEY='test-api-key',
    SHOPIFY_APP_API_SECRET='test-api-secret',
    SHOPIFY_APP_API_SCOPE=['read_products'],
    SHOPIFY_APP_IS_EMBEDDED=True,
    SHOPIFY_APP_DEV_MODE=False,
)

django.setup()

from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner()
failures = test_runner.run_tests(['shopify_auth'])
if failures:
    sys.exit(failures)
