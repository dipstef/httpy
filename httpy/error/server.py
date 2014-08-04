import socket
from .error import HttpError
from ..connection.error import SocketError, get_error


class HttpServerError(HttpError):
    pass


class HttpServerSocketError(HttpServerError, SocketError):

    def __new__(cls, request, error, *args):
        assert isinstance(error, socket.error)
        if not isinstance(error, SocketError):
            error = get_error(error)
        class_error = type(error.__class__.__name__, (cls, error.__class__), dict(cls.__dict__))

        return super(HttpServerSocketError, cls).__new__(class_error, request, error, *args)


class HttpyServerError(HttpServerSocketError):

    def __new__(cls, request, error, *args):
        if isinstance(error, socket.error):
            return HttpServerSocketError(request, error, *args)
        return HttpServerError(request, error, *args)