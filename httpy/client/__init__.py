from abc import abstractmethod
from .requests import user_agent, cookie_jar, HttpRequests, HttpyRequest


class HttpClient(HttpRequests):

    def __init__(self, timeout=5):
        self._timeout_default = timeout

    def _request(self, method, url, params=None, data=None, headers=None, **kwargs):
        timeout = kwargs.pop('timeout', self._timeout_default)

        return super(HttpClient, self)._request(method, url, params, data, headers, timeout=timeout, **kwargs)

    @abstractmethod
    def execute(self, request, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._close()

    def _close(self):
        pass