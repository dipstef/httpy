import socket

from httpy import HttpRequest
from httpy.connection.error import UnresolvableHost, ServerError, ConnectionTimeout, ConnectionError
from httpy.error import HttpServerError, HttpError, HttpServerConnectionTimeout


def main():
    request = HttpRequest('GET', 'http://test.com')

    connection_error = HttpServerError(request, UnresolvableHost())
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerError(request, ConnectionTimeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerConnectionTimeout(request, socket.timeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request


if __name__ == '__main__':
    main()