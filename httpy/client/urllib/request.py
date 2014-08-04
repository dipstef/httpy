import httplib
import socket
import urllib
import urllib2

from unicoder import encoded
from urlo import quote
from urlo.unicoded import unquoted

from ..requests import HttpRequests, cookie_jar
from ...http import HttpRequest, ResponseStatus
from ...connection.error import ConnectionTimeout
from ...error import HttpClientError, IncompleteRead, UnknownUrl, HttpServerSocketError, BadStatusLine, HttpStatusError


class UrlLibRequests(HttpRequests):

    def execute(self, request, timeout=None, redirect=True, **kwargs):
        request = UrllibRequest(request, redirect=redirect, timeout=timeout)
        response = _opener_request(request)
        return UrlLibResponse(request, response)


class UrllibRequest(urllib2.Request, HttpRequest):

    def __init__(self, request, redirect=True, timeout=None, *args, **kwargs):
        data = urllib.urlencode(request.data) if request.data else None
        urllib2.Request.__init__(self, quote(request.url), data, request.headers, *args, **kwargs)

        self.url = unquoted(request.url)
        self.method = request.method
        self.redirect = redirect
        self.timeout = timeout

    def get_method(self):
        return self.method

    def __unicode__(self):
        return u'%s: %s' % (self.method, self.url)

    def __str__(self):
        return encoded(unicode(self))


class UrlLibResponse(ResponseStatus):

    def __init__(self, request, response):
        super(UrlLibResponse, self).__init__(request, unquoted(response.url), response.getcode(),
                                             headers=dict(response.headers))
        self._opener_response = response
        self._read_response = _response_read(response)

    def read(self, *args, **kwargs):
        return self._read_response(self.request, *args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._opener_response, item)


class UrlLibRedirect(urllib2.HTTPErrorProcessor):

    def __init__(self):
        pass

    def http_response(self, request, response):
        if isinstance(request, UrllibRequest) and not request.redirect:
            return response
        else:
            return urllib2.HTTPErrorProcessor.http_response(self, request, response)


class RedirectHandler(urllib2.HTTPRedirectHandler):

    def __init__(self):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        if isinstance(req, UrllibRequest) and not req.redirect:
            url_info = urllib.addinfourl(fp, headers, req.get_full_url())

            url_info.status = code
            url_info.code = code
            return url_info
        else:
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


def _urlib_request(urllib_fun):
    def urlib_exec(request, *args, **kwargs):
        try:
            return urllib_fun(request, *args, **kwargs)
        except urllib2.HTTPError, e:
            raise HttpStatusError(request, e.code, e)
        except urllib2.URLError, e:
            raise _urllib_url_error(request, e)
        except httplib.BadStatusLine, e:
            raise BadStatusLine(str(request), e)
        except httplib.IncompleteRead, e:
            raise IncompleteRead(request, e)
        except httplib.HTTPException, e:
            raise HttpClientError(request, e)
        except socket.error, e:
            raise HttpServerSocketError(request, e)
    return urlib_exec

_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar), RedirectHandler)
urllib2.install_opener(_opener)


@_urlib_request
def _opener_request(request):
    if request.timeout:
        response = _opener.open(request, timeout=request.timeout)
    else:
        response = _opener.open(request)

    return response


def _response_read(response):
    @_urlib_request
    def read(request, *args, **kwargs):
        return response.read(*args, **kwargs)
    return read


def _urllib_url_error(request, url_error):
    error = _get_by_error_reason(request, url_error.reason)

    if not error:
        error = UrllibUrlError(request, url_error)

    return error


def _get_by_error_reason(request, reason):
    if hasattr(reason, 'errno') and reason.errno:
        error = HttpServerSocketError(request, reason)
    else:
        error = _get_by_message(request, reason)
    return error


def _get_by_message(request, error):
    if 'unknown url type' in str(error):
        return UnknownUrl(request, error)
    elif error.message == 'timed out':
        return HttpServerSocketError(request, ConnectionTimeout(error))


class UrllibUrlError(HttpClientError):
    def __init__(self, request, error):
        super(UrllibUrlError, self).__init__(request, type(error), error, type(error.reason), error.reason)
        self.error = error
        self.reason = error.reason