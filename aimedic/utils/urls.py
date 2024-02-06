from django.urls import URLPattern, URLResolver, reverse


def list_urls(lis, acc=None):
    """
    gets all urls so it can be printed from the command line
    """
    if acc is None:
        acc = []

    if not lis:
        return

    url = lis[0]

    if isinstance(url, URLPattern):
        yield acc + [str(url.pattern)]

    elif isinstance(url, URLResolver):
        yield from list_urls(url.url_patterns, acc + [str(url.pattern)])

    yield from list_urls(lis[1:], acc)


def get_url(request, path_str: None, default: None, args=()):
    """
    generates full url using the app urls pattern e.g.
    get_url(request, 'admin:index')
    >>> http://localhost:8000/admin/index/

    get_url(request, 'product:detail', [1])
    >>> http://localhost:8000/product/1/
    """
    domain = request.get_host().strip("/")
    default = default.lstrip("/")
    scheme = request.scheme
    path = default or reverse(path_str, args=args).strip("/")
    return f"{scheme}://{domain}/{path}"
