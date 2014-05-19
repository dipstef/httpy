from collections import namedtuple


ContentTypeMime = namedtuple('ContentTypeMime', ['header_type', 'main_type', 'sub_type', 'parameters'])


def parse_content_type(content_type):
    if content_type is None:
        content_type = 'text/plain'
    return _parse_content_type(content_type)


def _parse_content_type(content_type):
    content_type, parameters_list_text = _split_type_parameters_text(content_type)

    fields = [field.strip().lower() for field in content_type.split('/')]

    header_type, main_type, sub_type = '/'.join(fields), fields[0], '/'.join(fields[1:])

    return ContentTypeMime(header_type, main_type, sub_type, parameters_list_text)


def _split_type_parameters_text(content_type):
    if ';' in content_type:
        i = content_type.index(';')
        parameters_list_text = content_type[i:]
        content_type = content_type[:i]
    else:
        parameters_list_text = ''

    return content_type, parameters_list_text


def get_content_type_main(headers):
    content_type = parse_content_type(headers.get('content-type', 'unknown'))
    return content_type.main_type


def main():
    print _parse_content_type('image/jpg;foo')

if __name__ == '__main__':
    main()