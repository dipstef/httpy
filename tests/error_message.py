from httpy import HttpRequest
from httpy.error import HttpError, HttpStatusError

request = HttpRequest('GET', 'http://test.com')
print HttpError(request)
print HttpStatusError(request, 404)
print HttpStatusError(request, 403)
print HttpStatusError(request, 500)