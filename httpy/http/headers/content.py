import re
from urlo import unquote
from unicoder import force_unicode


def disposition_file_name(headers):
    content_disposition = headers.get('content-disposition')
    if content_disposition:
        file_name = parse_disposition(content_disposition)
        return file_name


_disposition_regex = re.compile("filename(?P<type>=|\*=(?P<enc>.+)'')(?P<name>.*)")


def parse_disposition(disposition_string):
    match = _disposition_regex.search(disposition_string)
    if match:
        disposition = match.groupdict()
        if not disposition['enc']:
            disposition['enc'] = 'utf-8'
        file_name = parse_file_name(disposition['name'], encoding=disposition['enc'])

        return file_name


def parse_file_name(file_name, encoding='utf-8'):
    quoted = re.match('''('|")(.+)('|");?''', file_name)
    file_name = quoted.group(2) if quoted else file_name
    file_name = unquote(force_unicode(file_name, encoding.lower()))
    return file_name


def content_length(headers):
    return int(headers.get('content-length', 0))


def accepts_ranges(headers):
    return 'bytes' == headers.get('accept-ranges', '').lower()


