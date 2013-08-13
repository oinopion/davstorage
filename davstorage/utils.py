def trim_trailing_slash(url):
    if url.endswith('/'):
        return url[:-1]
    return url