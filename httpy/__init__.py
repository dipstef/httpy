from .http import *
from .client import requests, urllib


class HttpClient(urllib.UrllibClient):

    def __init__(self, requests=urllib.requests, default_timeout=5):
        super(HttpClient, self).__init__(requests, default_timeout)


class HttpServerRequests(requests.HttpServerRequests):
    def __init__(self, server):
        super(HttpServerRequests, self).__init__(server, httpy)

httpy = HttpClient()
requests = urllib.requests
