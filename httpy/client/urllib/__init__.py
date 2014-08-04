from .request import UrlLibRequests
from .. import HttpClient
from ... import ResponseStatus

requests = UrlLibRequests()


class UrllibClient(HttpClient):

    def __init__(self, requests=requests, timeout=5):
        super(UrllibClient, self).__init__(requests, timeout)

    def execute(self, request, **kwargs):
        response = super(UrllibClient, self).execute(request, **kwargs)

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


client = UrllibClient()