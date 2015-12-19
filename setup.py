from setuptools import setup, find_packages

version = __import__('shopify_auth').__version__

setup(
    name='django-shopify-auth',
    version=version,
    description='A simple package for adding Shopify authentication to Django apps.',
    long_description=open('README.md').read(),
    author='Gavin Ballard',
    author_email='gavin@discolabs.com',
    url='https://github.com/discolabs/django-shopify-auth',
    license='MIT',

    packages=find_packages(),
    package_data={
        'shopify_auth': ['*.html']
    },

    install_requires=[
        'django >=1.7',
        'ShopifyAPI >=2.1.5',
        'setuptools >=5.7',
        'six >=1.9.0',
    ],

    tests_require=[
        'model_mommy >=1.2.1',
    ],

    zip_safe=False,
    include_package_data=True,
    classifiers=[],
)
