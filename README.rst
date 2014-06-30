Httpy
=====

``requests`` like http client with extensive error reporting.

Features
========

Http domain and error classes and http-header parsing.

Extensive and detailed http errors reporting.

Connection control.

Base for ``keepon`` http://github.com/dipstef/keepon , an http-client that allows request to be repeated
handling different classes of errors such timeouts, disconnections, overloaded host or temporary down.


Usage
=====
Same interface as the ``requests` library

.. code-block:: python

    from httpy import httpy

    >>> response = httpy.get('http://www.google.com', timeout=10)
    assert response.status == 200
    assert response.body

    >>> response = httpy.get('http://www.google.com', params=dict(search='foo'))


.. code-block:: python

    from httpy import HttpRequest

    >>> httpy.post('http://site.com/blog/dipstef', data=dict(message='hello'))
    >>> httpy.delete('http://site.com/shop/basket', data=dict(product_id='123'))
    >>> httpy.greet('http://site.com/users/dipstef', data=dict(msg='hello'))
    >>> httpy.execute(HttpRequest('GREET', 'http://site.com/users/dipstef'))


Errors

Error classes for common http errors and status codes

.. code-block:: python

    try:
        httpy.get('http://www.google.com/foo', timeout=10)
    except HttpNotFound, e:
        assert isinstance(e, HttpStatusCodeError)
        assert e.code == 404

    >>> httpy.get('http://www.google.ita', timeout=10)
        HttpServerUnresolvableHost("[Errno GET: http://www.google.ita]")


Connection control, checks you are connected to the internet when an host is unresolvable.

.. code-block:: python

    #Assuming you are disconnected

    >>> httpy.get('http://www.google.com', timeout=10)
        NotConnected("[Errno GET: http://www.google.com]")

Header
======

.. code-block:: python

    from httpy import HttpHeaders

    headers = HttpHeaders()

    headers['user-agent'] = 'httpy'
    assert headers['User-Agent'] == 'httpy'

Parsing content disposition

.. code-block:: python

    from httpy.http.headers.content import parse_disposition

    assert u'D MVC 008S.jpg' == parse_disposition('inline; filename="D%2520MVC%2520008S.jpg"')

    assert u'foo.jpg' == parse_disposition('''inline; filename="foo.jpg"''')
    assert u'åöä.zip' == parse_disposition("inline; filename*=UTF-8''åöä.zip")
    assert u'file.zip' == parse_disposition('attachment; filename="file.zip"')


Details
=======
``httpy`` uses ``urllib2`` for request dispatching, however it should soon be ported to ``urllib3``
or ``requests``.