from dated.normalized import utc
from .headers import Headers
from .headers import date_header


class ResponseStatus(object):

    def __init__(self, request, url, status, headers=None, date=None):
        self.request = request
        self.url = url
        self.status = status
        self.headers = Headers(headers or {})
        self.date = date or date_header(self.headers) or utc.now()

    def __repr__(self):
        return '%s: %s' % (self.url, self.status)


class HttpResponse(ResponseStatus):
    def __init__(self, request, url, status, headers=None, body='', date=None):
        super(HttpResponse, self).__init__(request, url, status, headers, date)
        self.body = body