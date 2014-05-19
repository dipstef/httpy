from httplib import responses
from connected.error import ConnectionError, ConnectionTimeout


class HttpError(Exception):
    def __init__(self, *args, **kwargs):
        super(HttpError, self).__init__(*args, **kwargs)


class HttpServerConnectionError(HttpError, ConnectionError):
    def __init__(self, *args, **kwargs):
        super(HttpServerConnectionError, self).__init__(*args, **kwargs)


class HttpTimeout(HttpServerConnectionError, ConnectionTimeout):
    def __init__(self, *args, **kwargs):
        super(HttpTimeout, self).__init__(*args, **kwargs)


class HttpOperationTimeout(HttpTimeout):
    def __init__(self, *args, **kwargs):
        super(HttpOperationTimeout, self).__init__(*args, **kwargs)


class HttpStatusCodeError(HttpError):
    def __init__(self, code, *args, **kwargs):
        super(HttpStatusCodeError, self).__init__(code, responses.get(code, ''), *args, **kwargs)
        self.code = code
        self.message = responses.get(code, '')


class BadRequest(HttpStatusCodeError):
    def __init__(self, *args, **kwargs):
        super(BadRequest, self).__init__(400, *args, **kwargs)


class HttpForbidden(HttpStatusCodeError):
    def __init__(self, *args, **kwargs):
        super(HttpForbidden, self).__init__(403, *args, **kwargs)


class HttpNotFound(HttpStatusCodeError):
    def __init__(self, *args, **kwargs):
        super(HttpNotFound, self).__init__(404, *args, **kwargs)


class InternalServerError(HttpStatusCodeError):
    def __init__(self, *args, **kwargs):
        super(InternalServerError, self).__init__(500, *args, **kwargs)


class HttpMethodNotImplemented(HttpStatusCodeError):
    def __init__(self, *args, **kwargs):
        super(HttpMethodNotImplemented, self).__init__(501, *args, **kwargs)


class GatewayTimeoutError(HttpStatusCodeError, HttpOperationTimeout):
    def __init__(self, *args, **kwargs):
        super(GatewayTimeoutError, self).__init__(504, *args, **kwargs)


#server overloaded
class BadGatewayError(HttpStatusCodeError, HttpOperationTimeout):
    def __init__(self, *args, **kwargs):
        super(BadGatewayError, self).__init__(502, *args, **kwargs)


class HttpResponseError(HttpError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseError, self).__init__(*args, **kwargs)


class BadStatusLine(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(BadStatusLine, self).__init__(*args, **kwargs)


_error_codes = {
    400: BadRequest,
    403: HttpForbidden,
    404: HttpNotFound,
    500: InternalServerError,
    501: HttpMethodNotImplemented,
    502: BadGatewayError,
    504: GatewayTimeoutError
}


def http_status_error(response_code, *args):
    error_code_error = _error_codes.get(response_code)

    if error_code_error:
        return error_code_error(*args)
    return HttpStatusCodeError(response_code, *args)