from httpy import HttpHeaders

headers = HttpHeaders()

headers['user-agent'] = 'httpy'
assert headers['User-Agent'] == 'httpy'


headers['user-agent'] = ['httpy']
assert headers['User-Agent'] == 'httpy'

headers.append('referrer', 'foo')
assert headers['referrer'] == 'foo'

headers.append('referrer', 'bar')
assert headers['referrer'] == 'bar'
assert headers.get_list('referrer') == ['foo', 'bar']


headers.update({'user-agent': 'urllib'})
assert headers['User-Agent'] == 'urllib'