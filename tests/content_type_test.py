from httpy.headers.content_type import parse_content_type


def main():
    content_type = parse_content_type('image/jpg;foo')
    assert content_type.main_type == 'image'

    content_type = parse_content_type('text/main')
    assert content_type.main_type == 'text'

if __name__ == '__main__':
    main()