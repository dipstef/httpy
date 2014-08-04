from .requests import user_agent, cookie_jar, HttpRequestDispatch


class HttpClient(HttpRequestDispatch):

    def __init__(self, request_handler, timeout=5):
        super(HttpClient, self).__init__(request_handler)
        self._timeout_default = timeout

    def _request(self, method, url, params=None, data=None, headers=None, **kwargs):
        timeout = kwargs.pop('timeout', self._timeout_default)

        return super(HttpClient, self)._request(method, url, params, data, headers, timeout=timeout, **kwargs)