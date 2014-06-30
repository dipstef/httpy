import errno
import socket
from . import is_disconnected


class SocketError(socket.error):
    def __init__(self, *args, **kwargs):
        super(SocketError, self).__init__(*args, **kwargs)


class ServerError(SocketError):

    def __init__(self, *args, **kwargs):
        super(ServerError, self).__init__(*args, **kwargs)


class UnresolvableHost(ServerError):
    def __init__(self, *args, **kwargs):
        super(UnresolvableHost, self).__init__(*args, **kwargs)


class NoRouteToHost(ServerError):
    def __init__(self, *args, **kwargs):
        super(NoRouteToHost, self).__init__(*args, **kwargs)


class NameServiceNotKnow(ServerError):
    def __init__(self, *args, **kwargs):
        super(NameServiceNotKnow, self).__init__(*args, **kwargs)


class ConnectionError(ServerError):
    def __init__(self, *args, **kwargs):
        super(ConnectionError, self).__init__(*args, **kwargs)


class ConnectionTimeout(ConnectionError):
    def __init__(self, *args, **kwargs):
        super(ConnectionTimeout, self).__init__(*args, **kwargs)


class ConnectionRefused(ConnectionError):
    def __init__(self, *args, **kwargs):
        super(ConnectionRefused, self).__init__(*args, **kwargs)


class NotConnected(SocketError):
    def __init__(self, *args, **kwargs):
        super(NotConnected, self).__init__(*args, **kwargs)


class ConnectionResetByPeer(ConnectionError):
    def __init__(self, *args, **kwargs):
        super(ConnectionResetByPeer, self).__init__(*args, **kwargs)


class BrokenPipe(ConnectionError):
    def __init__(self, *args, **kwargs):
        super(BrokenPipe, self).__init__(*args, **kwargs)


class OperationNowInProgress(ServerError):
    def __init__(self, *args, **kwargs):
        super(OperationNowInProgress, self).__init__(*args, **kwargs)


class SocketTimeout(ConnectionTimeout):
    def __init__(self, *args, **kwargs):
        super(SocketTimeout, self).__init__(*args, **kwargs)


class UnresolvableOrNotConnected(ConnectionError):
    def __new__(cls, *more):
        error_class = NotConnected if is_disconnected() else UnresolvableHost

        return error_class.__new__(error_class, *more)


_socket_errors = {
    errno.ENETUNREACH: NotConnected,
    errno.ETIMEDOUT: SocketTimeout,
    errno.EHOSTUNREACH: NoRouteToHost,
    errno.ECONNREFUSED: ConnectionRefused,
    errno.ECONNRESET: ConnectionResetByPeer,
    errno.EPIPE: BrokenPipe,
    errno.EINPROGRESS: OperationNowInProgress,
    -2: NameServiceNotKnow
}


def get_error_by_errno(error_number):
    return _socket_errors.get(error_number)


_error_message = {
    'nodename nor servname provided, or not known': UnresolvableOrNotConnected,
    'No route to host': NoRouteToHost
}


def get_error_by_strerror(strerror):
    return _error_message.get(strerror)


def error_class(socket_error):
    if socket_error.errno == errno.ENOEXEC:
        class_error = get_error_by_strerror(socket_error.strerror)
    else:
        class_error = get_error_by_errno(socket_error.errno)
    if not class_error:
        class_error = SocketError
    return class_error


def get_error(socket_error):
    class_error = error_class(socket_error)

    return class_error(socket_error)