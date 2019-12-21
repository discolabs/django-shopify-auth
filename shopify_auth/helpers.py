import urllib
from collections import OrderedDict


def add_query_parameters_to_url(url, query_parameters):
    """
    Merge a dictionary of query parameters into the given URL.
    Ensures all parameters are sorted in dictionary order when returning the URL.
    """
    # Parse the given URL into parts.
    url_parts = urllib.parse.urlparse(url)

    # Parse existing parameters and add new parameters.
    qs_args = urllib.parse.parse_qs(url_parts[4])
    qs_args.update(query_parameters)

    # Sort parameters to ensure consistent order.
    sorted_qs_args = OrderedDict()
    for k in sorted(qs_args.keys()):
        sorted_qs_args[k] = qs_args[k]

    # Encode the new parameters and return the updated URL.
    new_qs = urllib.parse.urlencode(sorted_qs_args, True)
    return urllib.parse.urlunparse(list(url_parts[0:4]) + [new_qs] + list(url_parts[5:]))
