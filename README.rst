Httpy
=====

``requests`` like http client interface.
It is based on python ``urllib2`` however this ideally should be a wrapper of ``requests``.

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

Headers
=======

parse content disposition

.. code-block:: python

    assert u'asd(foo\'s bar).jpg' == parse_file_name("asd(foo\'s bar).jpg")
    assert u'D MVC 008S.jpg' == parse_file_name('D%2520MVC%2520008S.jpg')

    assert u'foo.jpg' == parse_disposition('''inline; filename="foo.jpg"''')
    assert u'åöä.zip' == parse_disposition("inline; filename*=UTF-8''%s" % encoded(u'åöä.zip', 'utf-8'))
    assert 'file.zip' == parse_disposition('attachment; filename="file.zip"')
