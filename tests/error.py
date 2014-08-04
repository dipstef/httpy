import socket

from httpy import HttpRequest
from httpy.connection.error import UnresolvableHost, ServerError, ConnectionTimeout, ConnectionError, SocketTimeout
from httpy.error import HttpServerError, HttpServerSocketError, HttpyServerError, HttpStatusCodeError, HttpStatusError,\
    HttpNotFound, HttpError


class HttpServerSocketTimeout(HttpServerSocketError):

    def __init__(self, request, socket_error):
        assert isinstance(socket_error, socket.timeout)
        super(HttpServerSocketTimeout, self).__init__(request, socket_error)


class HttpServerConnectionTimeout(HttpServerError, ConnectionTimeout):

    def __init__(self, request):
        super(HttpServerConnectionTimeout, self).__init__(request, socket.timeout())


def main():
    request = HttpRequest('GET', 'http://test.com')

    connection_error = HttpServerSocketError(request, UnresolvableHost())
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert isinstance(connection_error, HttpServerSocketError)

    assert connection_error.request == request

    connection_error = HttpServerSocketError(request, ConnectionTimeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert isinstance(connection_error, HttpServerSocketError)
    assert connection_error.request == request

    connection_error = HttpServerSocketError(request, socket.timeout())
    assert isinstance(connection_error, socket.timeout)
    assert isinstance(connection_error, SocketTimeout)
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerSocketTimeout(request, socket.timeout())
    assert isinstance(connection_error, socket.timeout)
    assert isinstance(connection_error, SocketTimeout)
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerConnectionTimeout(request)
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpyServerError(request, ConnectionTimeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert isinstance(connection_error, HttpServerSocketError)
    assert connection_error.request == request

    connection_error = HttpyServerError(request, Exception())
    assert isinstance(connection_error, HttpServerError)
    assert not isinstance(connection_error, HttpServerSocketError)
    assert connection_error.request == request

    error = HttpStatusError(request, 404)
    assert isinstance(error, HttpStatusCodeError)
    assert isinstance(error, HttpNotFound)

    try:
        raise HttpStatusError(request, 404)
    except HttpNotFound:
        pass

if __name__ == '__main__':
    main()