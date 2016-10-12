# coding=utf-8

from ._base import BaseField
from .. import err

class DefaultField(BaseField):
    def __init__(self, default_value, **kwargs):
        super(DefaultField, self).__init__(**kwargs)

        self.default_value = default_value

    def _get_value(self, src):
        try:
            return super(DefaultField, self)._get_value(src)
        except err.DataPackerSrcKeyNotFoundError:
            return self.default_value