from httpy.connection.error import UnresolvableHost, ServerError
from httpy.requests.error import HttpError, HttpClientError, HttpServerError
from httpy.client import http_client


def main():
    response = http_client.get('http://www.repubblica.it', timeout=10)
    assert response.status == 200
    assert response.body
    
    try:
        http_client.get('http://www.repubblica.ita', timeout=10)
    except UnresolvableHost, e:
        assert isinstance(e, HttpError)
        assert isinstance(e, HttpClientError)
        assert isinstance(e, HttpServerError)
        assert isinstance(e, ServerError)


if __name__ == '__main__':
    main()