# coding=utf-8
from unicoder import encoded

from httpy.http.headers.content import parse_disposition, parse_file_name


def main():
    assert u'asd(foo\'s bar).jpg' == parse_file_name("asd(foo\'s bar).jpg")
    assert u'D MVC 008S.jpg' == parse_file_name('D%2520MVC%2520008S.jpg')

    assert u'foo.jpg' == parse_disposition('''inline; filename="foo.jpg"''')
    assert u'åöä.zip' == parse_disposition("inline; filename*=UTF-8''%s" % encoded(u'åöä.zip', 'utf-8'))

    assert u'åöä på nätet.rar' == parse_disposition(u'attachment; filename="åöä på nätet.rar"')
    assert u'ååååååää på nätet.rar' == parse_disposition('attachment; filename="ååååååää på nätet.rar"')

    assert u'D MVC 008S.jpg' == parse_disposition('inline; filename="D%2520MVC%2520008S.jpg"')
    assert u'foo.jpg' == parse_disposition('''inline; filename="foo.jpg"''')
    assert u'åöä.zip' == parse_disposition("inline; filename*=UTF-8''åöä.zip")
    assert u'file.zip' == parse_disposition('attachment; filename="file.zip"')

if __name__ == '__main__':
    main()