import sys
import django
from django.conf import settings

configuration = {
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'shopify_auth',
    ],
    'AUTHENTICATION_BACKENDS': ['shopify_auth.backends.ShopUserBackend'],
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True
        }
    ],
    'ROOT_URLCONF': 'shopify_auth.tests.urls',
    'SHOPIFY_APP_NAME': 'Test App',
    'SHOPIFY_APP_API_KEY': 'test-api-key',
    'SHOPIFY_APP_API_SECRET': 'test-api-secret',
    'SHOPIFY_APP_API_VERSION': 'unstable',
    'SHOPIFY_APP_API_SCOPE': ['read_products'],
    'SHOPIFY_APP_DEV_MODE': False,
    'SHOPIFY_APP_THIRD_PARTY_COOKIE_CHECK': True,
    'SECRET_KEY': 'uq8e140t1rm3^kk&blqxi*y9h_j5yd9ghjv+fd1p%08g4%t6%i',
    'MIDDLEWARE': [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
}

settings.configure(**configuration)

django.setup()

from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner()
failures = test_runner.run_tests(['shopify_auth'])
if failures:
    sys.exit(failures)
