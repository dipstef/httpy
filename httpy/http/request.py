from .headers import HttpHeaders


class HttpRequest(object):

    def __init__(self, url, method, headers=None, data=None):
        self.url = url
        self.method = method.upper()
        self.headers = HttpHeaders(headers or {})
        self.data = data

    def __repr__(self):
        return '%s: %s' % (self.method, self.url)