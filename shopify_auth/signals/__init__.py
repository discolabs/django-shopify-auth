import django.dispatch

oauth_finalize = django.dispatch.Signal(providing_args=["shop"])
