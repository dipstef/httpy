from ..http.error import HttpError
from ..connection.error import ConnectionTimeout, SocketError


class HttpClientError(HttpError):
    def __init__(self, request, *args, **kwargs):
        super(HttpClientError, self).__init__(request, *args, **kwargs)


class IncompleteRead(HttpClientError):
    def __init__(self, request, *args, **kwargs):
        super(IncompleteRead, self).__init__(request, *args, **kwargs)


class UnknownUrl(HttpClientError):
    def __init__(self, request, *args, **kwargs):
        super(UnknownUrl, self).__init__('Unknown url: %s' % request.url, *args, **kwargs)


class HttpServerError(HttpClientError, SocketError):
    def __init__(self, request, error, *args, **kwargs):
        super(HttpServerError, self).__init__(request, error, *args, **kwargs)
        self._error = error

    def __new__(cls, request, error, *more):
        assert isinstance(error, SocketError)
        subclass = issubclass(cls, HttpServerError) and cls != HttpServerError

        cls.__bases__ = (HttpClientError, error.__class__) + error.__class__.__bases__

        if subclass:
            cls.__bases__ = (HttpServerError, ) + cls.__bases__
        else:
            cls.__name__ = 'HttpServer' + error.__class__.__name__

        return super(HttpServerError, cls).__new__(cls, request, error, *more)


class HttpServerConnectionTimeout(HttpServerError):

    def __new__(cls, request, socket_error, *more):
        return super(HttpServerConnectionTimeout, cls).__new__(cls, request, ConnectionTimeout(socket_error), *more)