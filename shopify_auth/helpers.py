from six.moves import urllib


def add_query_parameters_to_url(url, query_parameters):
    url_parts = urllib.parse.urlparse(url)

    qs_args = urllib.parse.parse_qs(url_parts[4])
    qs_args.update(query_parameters)

    new_qs = urllib.parse.urlencode(qs_args, True)

    return urllib.parse.urlunparse(list(url_parts[0:4]) + [new_qs] + list(url_parts[5:]))
