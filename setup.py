from distutils.core import setup

version=__import__('shopify_auth').__version__

setup(
    name='django-shopify-auth',
    version=version,
    description='An simple package for adding Shopify authentication to Django apps.',
    long_description=open('README.md').read(),
    author='Gavin Ballard',
    author_email='gavin@gavinballard.com',
    url='https://github.com/gavinballard/django-shopify-auth',
    license='MIT',

    packages=['shopify_auth'],
    package_dir={
        'shopify_auth': 'shopify_auth',
    },

    requires=['Django (>=1.3)',],
    install_requires=['Django>=1.3',],

    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
