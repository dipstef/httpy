from .requests import HttpServerRequests as HttpRequests
from .http.response import ResponseStatus
from .requests.urllibs import UrlLibRequests
from .requests import HttpRequestDispatch


requests = UrlLibRequests()


class HttpClient(HttpRequestDispatch):
    def __init__(self, requests=requests, default_timeout=5):
        super(HttpClient, self).__init__(requests)
        self._timeout_default = default_timeout

    def _execute(self, request, **kwargs):
        timeout = kwargs.pop('timeout', self._timeout_default)

        response = super(HttpClient, self)._execute(request, timeout=timeout, **kwargs)

        return HttpResponseBody(response.request, response)


class HttpResponseBody(ResponseStatus):

    def __init__(self, request, response):
        super(HttpResponseBody, self).__init__(request, response.url, response.status, response.headers, response.date)
        self._response = response
        self._body = None

    @property
    def body(self):
        if self._body is None:
            self._body = self._response.read()
        return self._body

    def __setstate__(self, state):
        self.request = state['request']
        self.url = state['url']
        self.status = state['status']
        self.headers = state['headers']
        self._body = state['body']

    def __getstate__(self):
        return {'request': self.request, 'url': self.url, 'status': self.status, 'body': self.body,
                'headers': self.headers}


http_client = HttpClient()


class HttpServerRequests(HttpRequests):
    def __init__(self, server):
        super(HttpServerRequests, self).__init__(server, http_client)