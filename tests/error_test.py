import socket

from httpy.connection.error import UnresolvableHost, ServerError, ConnectionTimeout, ConnectionError
from httpy.http.request import HttpRequest

from httpy.requests.error import HttpServerError, HttpClientError, HttpServerConnectionTimeout


def main():
    request = HttpRequest('http://test.com', 'GET')

    connection_error = HttpServerError(request, UnresolvableHost())
    assert isinstance(connection_error, HttpClientError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerError(request, ConnectionTimeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpClientError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request

    connection_error = HttpServerConnectionTimeout(request, socket.timeout())
    assert isinstance(connection_error, ConnectionTimeout)
    assert isinstance(connection_error, HttpClientError)
    assert isinstance(connection_error, ConnectionError)
    assert isinstance(connection_error, ServerError)
    assert isinstance(connection_error, HttpServerError)
    assert connection_error.request == request


if __name__ == '__main__':
    main()