import urllib
import urlparse


def add_query_parameters_to_url(url, query_parameters):
    url_parts = urlparse.urlparse(url)

    qs_args = urlparse.parse_qs(url_parts[4])
    qs_args.update(query_parameters)

    new_qs = urllib.urlencode(qs_args, True)

    return urlparse.urlunparse(list(url_parts[0:4]) + [new_qs] + list(url_parts[5:]))
