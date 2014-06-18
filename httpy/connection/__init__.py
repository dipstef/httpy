from collections import defaultdict
import os
import socket

import random

from urlo.domain import get_sub_domain


_hosts = ['www.google.com',
          'www.yahoo.com',
          'www.facebook.com',
          'www.youtube.com',
          'www.archive.org',
          'www.wikipedia.org',
          'www.twitter.com',
          'www.amazon.com',
          'www.blogger.com',
          'www.wordpress.com',
          'www.ebay.com',
          'www.cnn.com',
          'www.repubblica.it',
          'www.dn.se',
          'www.blocket.se']


#caches host resolutions to avoid resolving a server everytime we check the connection is up
_resolutions = defaultdict(set)


def is_disconnected():
    server = random.choice(_hosts)

    server_ips = _resolutions[server]

    previous_resolution = random.choice(list(server_ips)) if server_ips else None

    host_up = None
    if previous_resolution and _is_connecting_host(previous_resolution):
        host_up = previous_resolution

    if not host_up:
        host_up = _server_host_up(server)

    if host_up:
        server_ips.add(host_up)

    if previous_resolution and host_up != previous_resolution:
        #an ip previously resolved is down
        server_ips.remove(previous_resolution)

    return not host_up


def _server_host_up(server, port=80):
    try:
        # see if we can resolve the host name -- tells us if there is a DNS listening
        host = socket.gethostbyname(server)
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection((host, port), timeout=2)

        return host
    except:
        pass


def _is_connecting_host(host, port=80):
    try:
        socket.create_connection((host, port), timeout=2)
        return True
    except:
        return False


def host_is_down(host):
    return not _server_host_up(host)


def _ping_host(host):
    response = os.system('ping -c 1  %s > /dev/null 2>&1' % host)
    return response == 0


def site_is_down(url):
    return host_is_down(get_sub_domain(url))