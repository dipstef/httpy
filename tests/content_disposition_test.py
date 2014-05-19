# coding=utf-8
from unicoder import encoded
from httpy.headers.content import _disposition_file_name, _unquote_disposition_file


def main():
    assert u'asd(foo\'s bar).jpg' == _unquote_disposition_file("asd(foo\'s bar).jpg")
    assert u'D MVC 008S.jpg' == _unquote_disposition_file('D%2520MVC%2520008S.jpg')

    assert u'foo.jpg' == _disposition_file_name('''inline; filename="foo.jpg"''')
    assert u'åöä.jpg' == _disposition_file_name("inline; filename*=UTF-8''%s" % encoded(u'åöä.jpg', 'utf-8'))

    assert u'åöä på nätet.rar' == _disposition_file_name(u'attachment; filename="åöä på nätet.rar"')
    assert u'ååååååää på nätet.rar' == _disposition_file_name('attachment; filename="ååååååää på nätet.rar"')

if __name__ == '__main__':
    main()