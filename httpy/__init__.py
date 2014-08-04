from .http import *
from .client import requests, urllib

HttpClient = urllib.UrllibClient

httpy = HttpClient()


class HttpServerRequests(requests.HttpServerRequests):
    def __init__(self, server):
        super(HttpServerRequests, self).__init__(server, httpy)

requests = urllib.requests
