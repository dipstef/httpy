class HttpError(Exception):
    def __init__(self, request, *args, **kwargs):
        super(HttpError, self).__init__(str(request), *args, **kwargs)
        self.request = request


class HttpRequestError(HttpError):
    pass


class HttpResponseError(HttpError):
    pass


class HttpOperationTimeout(HttpResponseError):
    pass


class UnknownUrl(HttpRequestError):
    pass


class BadStatusLine(HttpResponseError):
    pass


class IncompleteRead(HttpError):
    pass