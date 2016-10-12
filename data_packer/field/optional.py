# coding=utf-8

from ._base import BaseField
from .. import err


class OptionalField(BaseField):
    def _get_value(self, src):
        try:
            return super(OptionalField, self)._get_value(src)
        except err.DataPackerSrcKeyNotFoundError:
            raise err._DataPackerInterruptError('Ignore not exist optional fields({})'.format(self))