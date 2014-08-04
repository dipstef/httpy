from httpy import httpy
from httpy.connection.error import UnresolvableHost, ServerError
from httpy.error import HttpError, HttpClientError, HttpServerError, HttpNotFound, HttpStatusCodeError


def main():
    response = httpy.get('http://www.google.com', timeout=10)
    assert response.status == 200
    assert response.body

    try:
        httpy.get('http://www.google.ita', timeout=10)
    except UnresolvableHost, e:
        assert isinstance(e, HttpError)
        assert isinstance(e, HttpServerError)
        assert isinstance(e, ServerError)

    try:
        httpy.get('http://www.google.com/foo', timeout=10)
    except HttpNotFound, e:
        assert isinstance(e, HttpStatusCodeError)
        assert e.code == 404

if __name__ == '__main__':
    main()