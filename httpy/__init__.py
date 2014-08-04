from .http import *
from .client import urllib
from .client.requests import HttpyRequest, HttpServerRequests as ServerRequests

HttpClient = urllib.UrllibClient

httpy = HttpClient()


class HttpServerRequests(ServerRequests):
    def __init__(self, server):
        super(HttpServerRequests, self).__init__(server, httpy)

requests = urllib.requests
