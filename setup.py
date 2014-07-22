from distutils.core import setup

version = __import__('shopify_auth').__version__

setup(
    name = 'django-shopify-auth',
    version = version,
    description = 'An simple package for adding Shopify authentication to Django apps.',
    long_description = open('README.md').read(),
    author = 'Gavin Ballard',
    author_email = 'gavin@discolabs.com',
    url = 'https://github.com/discolabs/django-shopify-auth',
    license = 'MIT',

    packages = [
        'shopify_auth'
    ],

    package_dir = {
        'shopify_auth': 'shopify_auth',
    },

    requires = [
        'django',
        'shopify',
    ],

    install_requires = [
        'django',
        'shopify',
    ],

    zip_safe = True,
    classifiers = [],
)