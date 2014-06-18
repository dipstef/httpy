import re
from urlo import unquoted


def disposition_file_name(headers):
    content_disposition = headers.get('content-disposition')
    if content_disposition:
        file_name = _disposition_file_name(content_disposition)
        return file_name


_disposition_regex = re.compile("filename(?P<type>=|\*=(?P<enc>.+)'')(?P<name>.*)")


def _disposition_file_name(disposition_string):
    match = _disposition_regex.search(disposition_string)
    if match:
        disposition = match.groupdict()
        if not disposition['enc']:
            disposition['enc'] = 'utf-8'
        file_name = _unquote_disposition_file(disposition['name'], encoding=disposition['enc'])

        return file_name


def _unquote_disposition_file(file_name, encoding='utf-8'):
    quoted = re.match('''('|")(.+)('|");?''', file_name)
    file_name = quoted.group(2) if quoted else file_name
    file_name = unquoted(file_name, encoding.lower())
    return file_name


def content_length(headers):
    return int(headers.get('content-length', 0))




