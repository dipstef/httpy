from .headers import HttpHeaders


class HttpRequest(object):

    def __init__(self, url, method, headers=None):
        self.url = url
        self.method = method.upper()
        self.headers = HttpHeaders(headers or {})

    def __repr__(self):
        return '%s: %s' % (self.method, self.url)