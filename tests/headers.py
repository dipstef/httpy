from httpy import HttpHeaders

headers = HttpHeaders()

headers['user-agent'] = 'httpy'
assert headers['User-Agent'] == 'httpy'