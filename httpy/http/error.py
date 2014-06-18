from httplib import responses


class HttpError(Exception):
    def __init__(self, request, *args, **kwargs):
        super(HttpError, self).__init__(str(request), *args, **kwargs)
        self.request = request


class HttpOperationTimeout(HttpError):
    def __init__(self, request, *args, **kwargs):
        super(HttpOperationTimeout, self).__init__(request, *args, **kwargs)


class HttpStatusCodeError(HttpError):
    def __init__(self, request, code, *args, **kwargs):
        super(HttpStatusCodeError, self).__init__(request, code, responses.get(code, ''), *args, **kwargs)
        self.code = code
        self.message = responses.get(code, '')


class BadRequest(HttpStatusCodeError):
    def __init__(self, request, *args, **kwargs):
        super(BadRequest, self).__init__(request, 400, *args, **kwargs)


class HttpForbidden(HttpStatusCodeError):
    def __init__(self, request, *args, **kwargs):
        super(HttpForbidden, self).__init__(request, 403, *args, **kwargs)


class HttpNotFound(HttpStatusCodeError):
    def __init__(self, request, *args, **kwargs):
        super(HttpNotFound, self).__init__(request, 404, *args, **kwargs)


class InternalServerError(HttpStatusCodeError):
    def __init__(self, request, *args, **kwargs):
        super(InternalServerError, self).__init__(request, 500, *args, **kwargs)


class HttpMethodNotImplemented(HttpStatusCodeError):
    def __init__(self, request, *args, **kwargs):
        super(HttpMethodNotImplemented, self).__init__(request, 501, *args, **kwargs)


class GatewayTimeoutError(HttpStatusCodeError, HttpOperationTimeout):
    def __init__(self, request, *args, **kwargs):
        super(GatewayTimeoutError, self).__init__(request, 504, *args, **kwargs)


#server overloaded
class BadGatewayError(HttpStatusCodeError, HttpOperationTimeout):
    def __init__(self, request, *args, **kwargs):
        super(BadGatewayError, self).__init__(request, 502, *args, **kwargs)


class HttpResponseError(HttpError):
    def __init__(self, request, *args, **kwargs):
        super(HttpResponseError, self).__init__(request, *args, **kwargs)


class BadStatusLine(HttpResponseError):
    def __init__(self, request, *args, **kwargs):
        super(BadStatusLine, self).__init__(request, *args, **kwargs)


_error_codes = {
    400: BadRequest,
    403: HttpForbidden,
    404: HttpNotFound,
    500: InternalServerError,
    501: HttpMethodNotImplemented,
    502: BadGatewayError,
    504: GatewayTimeoutError
}


def http_status_error(request, response_code, *args):
    error_code_error = _error_codes.get(response_code)

    if error_code_error:
        return error_code_error(*args)

    return HttpStatusCodeError(request, response_code, *args)