from httplib import responses

from .error import HttpError, HttpRequestError, HttpResponseError, HttpOperationTimeout


error_status = {code: message for code, message in responses.iteritems() if code >= 400}

_error_codes = {}


class HttpStatusCodeError(HttpError):
    def __init__(self, request, code, *args, **kwargs):
        super(HttpStatusCodeError, self).__init__(request, code, responses.get(code, ''), *args, **kwargs)
        self.code = code
        self.message = responses.get(code, '')


class HttpRequestStatusError(HttpStatusCodeError, HttpRequestError):
    pass


class HttpResponseStatusError(HttpStatusCodeError, HttpResponseError):
    pass


class HttpStatusMeta(type):

    def __new__(cls, class_name, bases, class_dict):
        code = class_dict.pop('__code__')
        cls = super(HttpStatusMeta, cls).__new__(cls, class_name, bases, class_dict)
        if code:
            _error_codes[code] = cls
        return cls


class HttpStatusError(HttpStatusCodeError):
    def __new__(cls, request, response_code, *args):
        error_code_error = _error_codes.get(response_code)

        if error_code_error:
            return error_code_error(request, response_code, *args)

        return HttpStatusCodeError(request, response_code, *args)


class BadRequest(HttpRequestStatusError):
    __code__ = 400
    __metaclass__ = HttpStatusMeta


class HttpForbidden(HttpStatusCodeError):
    __code__ = 403
    __metaclass__ = HttpStatusMeta


class HttpNotFound(HttpStatusCodeError):
    __code__ = 404
    __metaclass__ = HttpStatusMeta


class InvalidRangeRequest(HttpRequestStatusError):
    __code__ = 416
    __metaclass__ = HttpStatusMeta


class InternalServerError(HttpResponseStatusError):
    __code__ = 500
    __metaclass__ = HttpStatusMeta


class HttpMethodNotImplemented(HttpRequestStatusError):
    __code__ = 501
    __metaclass__ = HttpStatusMeta


#server overloaded
class SiteOverloaded(HttpResponseStatusError, HttpOperationTimeout):
    __code__ = 502
    __metaclass__ = HttpStatusMeta


class GatewayTimeoutError(HttpResponseStatusError, HttpOperationTimeout):
    __code__ = 504
    __metaclass__ = HttpStatusMeta