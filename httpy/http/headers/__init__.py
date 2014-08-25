import email.utils as email_utils

from collected.dict.caseless import CaseLessDict
from dated import utc
from unicoder import byte_string


class HttpHeaders(CaseLessDict):

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super(HttpHeaders, self).__init__(seq)

    def _normalize_key(self, key):
        return byte_string(key.title(), encoding=self.encoding)

    def _normalize_value(self, value):
        if hasattr(value, '__iter__'):
            value = [byte_string(x, encoding=self.encoding) for x in value]
            value = value[0] if len(value) == 1 else value
        else:
            value = byte_string(value)

        return value

    def __getitem__(self, key):
        try:
            value = super(HttpHeaders, self).__getitem__(key)
            return value if not isinstance(value, list) else value[-1]
        except IndexError:
            return None

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def get_list(self, key, def_val=None):
        try:
            return super(HttpHeaders, self).__getitem__(key)
        except KeyError:
            return self._normalize_value(def_val) if def_val is not None else None

    def append(self, key, value):
        value = self._normalize_value(value)
        existing = self.get(key)
        if existing:
            if not isinstance(existing, list):
                existing = [existing]
            if isinstance(value, list):
                existing.extend(value)
            else:
                existing.append(value)
            value = existing
        self[key] = value

    def to_string(self):
        return _headers_dict_to_raw(self)

    def __copy__(self):
        return self.__class__(self)

    copy = __copy__


def header_dict_to_lines(headers_dict):
    raw_lines = []

    for key, value in headers_dict.items():
        if isinstance(value, (str, unicode)):
            raw_lines.append('%s: %s' % (key, value))
        elif isinstance(value, (list, tuple)):
            for v in value:
                raw_lines.append('%s: %s' % (key, v))
    return raw_lines


def _headers_dict_to_raw(headers_dict):
    if headers_dict is None:
        return None

    raw_lines = header_dict_to_lines(headers_dict)

    return '\r\n'.join(raw_lines)


def header_string_to_dict(headers_raw):
    if headers_raw is None:
        return None

    header_split = (header.split(':', 1) for header in headers_raw.splitlines())
    header_items = (header_item for header_item in header_split if len(header_item) == 2)

    return HttpHeaders([(item[0].strip(), [item[1].strip()]) for item in header_items])


def date_header(headers):
    date_string = headers.get('date')
    if date_string:
        time_tuple = email_utils.parsedate(date_string)
        date = utc.from_time_tuple(time_tuple).to_datetime()
        return date