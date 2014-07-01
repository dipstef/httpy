from datetime import datetime
from .headers import HttpHeaders, date_header


class HttpRequest(object):

    def __init__(self, method, url, headers=None, data=None):
        self.url = url
        self.method = method.upper()
        self.headers = HttpHeaders(headers or {})
        self.data = data

    def __repr__(self):
        return '%s: %s' % (self.method, self.url)


class ResponseStatus(object):

    def __init__(self, request, url, status, headers=None, date=None):
        self.request = request
        self.url = url
        self.status = status
        self.headers = HttpHeaders(headers or {})
        self.date = date or date_header(self.headers) or datetime.utcnow()

    def __repr__(self):
        return '%s: %s' % (self.url, self.status)


class HttpResponse(ResponseStatus):
    def __init__(self, request, url, status, headers=None, body='', date=None):
        super(HttpResponse, self).__init__(request, url, status, headers, date)
        self.body = body