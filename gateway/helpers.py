from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def construct_callback_url(callback_url, authority, status):
    """
    Adds Authority and status to the callback URL while preserving existing query parameters.
    """
    parsed_url = urlparse(callback_url)

    query_params = parse_qs(parsed_url.query)
    query_params['Authority'] = authority
    query_params['Status'] = status

    new_query = urlencode(query_params, doseq=True)
    modified_url = urlunparse(parsed_url._replace(query=new_query))

    return modified_url
