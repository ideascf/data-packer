# coding=utf-8
from ._base import BaseConverter, TypeConverter


class StrConverter(TypeConverter):
    def __init__(self, encoding):
        super(StrConverter, self).__init__(str)
        self.encoding = encoding

    def convert(self, src_name, dst_name, value):
        if isinstance(value, unicode):
            value = value.encode(self.encoding)


        return super(StrConverter, self).convert(src_name, dst_name, value)

class UnicodeConverter(TypeConverter):
    def __init__(self, encoding):
        super(UnicodeConverter, self).__init__(unicode)
        self.encoding = encoding

    def convert(self, src_name, dst_name, value):
        if not isinstance(value, basestring):
            value = str(value)

        if isinstance(value, str):
            value = value.decode(self.encoding)

        return super(UnicodeConverter, self).convert(src_name, dst_name, value)