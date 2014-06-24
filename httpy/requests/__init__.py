import cookielib

from urlo.unquoted import params_url, build_url

from ..http.request import HttpRequest
from ..http.headers import HttpHeaders


cookie_jar = cookielib.LWPCookieJar()

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0'

headers_default = HttpHeaders({'User-Agent':  user_agent})


class HttpRequests(object):

    def get(self, url, params=None, headers=None, **kwargs):
        return self.request('GET', url, params=params, headers=headers, **kwargs)

    def post(self, url, params=None, data=None, headers=None, **kwargs):
        return self.request('POST', url, params=params, data=data, headers=headers, **kwargs)

    def request(self, method, url, params=None, data=None, headers=None, **kwargs):
        request = HttpRequest(params_url(url, params), method.upper(), self._add_default_headers(headers), data)
        return self._execute(request, **kwargs)

    def _execute(self, request, **kwargs):
        raise NotImplementedError

    def __getattr__(self, method):
        def request(url, headers=None, **kwargs):
            return self.request(method.upper(), url, headers=headers, **kwargs)
        return request

    @staticmethod
    def _add_default_headers(headers):
        default = HttpHeaders(headers_default)

        if headers:
            default.update(headers)

        return default


class HttpRequestDispatch(HttpRequests):

    def __init__(self, request_handler):
        self._requests = request_handler

    def _execute(self, request, **kwargs):
        return self._requests._execute(request, **kwargs)


class HttpServerRequests(HttpRequestDispatch):

    def __init__(self, server, request_handler):
        super(HttpServerRequests, self).__init__(request_handler)
        self._address = server

    def request(self, method, path, params=None, data=None, headers=None, **kwargs):
        url = build_url(self._address[0], path, port=self._address[1])

        return super(HttpServerRequests, self).request(method, url, params=params, data=data, headers=headers, **kwargs)