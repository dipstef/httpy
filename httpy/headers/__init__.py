import email.utils as email_utils

from collected.dict.caseless import CaseLessDict
from dated import utc


class Headers(CaseLessDict):

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super(Headers, self).__init__(seq)

    def _normalize_key(self, key):
        if isinstance(key, unicode):
            return key.title().encode(self.encoding)
        return key.title()

    def _normalize_value(self, value):
        if not hasattr(value, '__iter__'):
            value = [value]

        return [x.encode(self.encoding) if isinstance(x, unicode) else x for x in value]

    def __getitem__(self, key):
        try:
            return super(Headers, self).__getitem__(key)[-1]
        except IndexError:
            return None

    def get(self, key, def_val=None):
        try:
            return super(Headers, self).get(key, def_val)[-1]
        except IndexError:
            return None

    def getlist(self, key, def_val=None):
        try:
            return super(Headers, self).__getitem__(key)
        except KeyError:
            if def_val is not None:
                return self.normalize_value(def_val)
            return []

    def setlist(self, key, list_):
        self[key] = list_

    def setlistdefault(self, key, default_list=()):
        return self.setdefault(key, default_list)

    def appendlist(self, key, value):
        lst = self.getlist(key)
        lst.extend(self.normalize_value(value))
        self[key] = lst

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((k, self.getlist(k)) for k in self.keys())

    def values(self):
        return [self[k] for k in self.keys()]

    def to_string(self):
        return _headers_dict_to_raw(self)

    def __copy__(self):
        return self.__class__(self)

    copy = __copy__


def _headers_dict_to_raw(headers_dict):
    if headers_dict is None:
        return None

    raw_lines = []

    for key, value in headers_dict.items():
        if isinstance(value, (str, unicode)):
            raw_lines.append("%s: %s" % (key, value))
        elif isinstance(value, (list, tuple)):
            for v in value:
                raw_lines.append("%s: %s" % (key, v))

    return '\r\n'.join(raw_lines)


def headers_raw_to_dict(headers_raw):
    if headers_raw is None:
        return None

    header_split = (header.split(':', 1) for header in headers_raw.splitlines())
    header_items = (header_item for header_item in header_split if len(header_item) == 2)

    return dict([(item[0].strip(), [item[1].strip()]) for item in header_items])


def date_header(headers):
    date_string = headers.get('date')
    if date_string:
        date = utc.from_timestamp(email_utils.parsedate(date_string))
        return date