from unicoder import byte_string


class HttpError(Exception):

    def __init__(self, request, *args, **kwargs):
        super(HttpError, self).__init__(request, *args, **kwargs)
        self.request = request

        message = '%s on: %s' % (self.__class__.__name__, byte_string(request))
        if args:
            message += ':\n %s' % ', '.join([byte_string(arg) for arg in args])
        if kwargs:
            message += ':\n %s' % ', '.join(['%s=%s' % (item, byte_string(arg)) for item, arg in kwargs.iteritems()])

        self.message = message

    def __str__(self):
        return self.message


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