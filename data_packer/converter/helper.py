# coding=utf-8
from ._base import BaseConverter

class TypeConverter(BaseConverter):
    def __init__(self, tp):
        super(TypeConverter, self).__init__()
        self.tp = tp

    def convert(self, src_name, dst_name, value):
        return self.tp(value)

