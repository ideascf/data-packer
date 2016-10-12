# coding=utf-8
from .field._base import _IField
from .field.single import DefaultField, OptionalField, PlaceholderField, RequiredField
from .field.multi import SelectorField, CompositedField

from . import checker, converter, container, constant, err


def run(src, dst, fields):
    """

    :param src:
    :type src:
    :param dst:
    :type dst:
    :param fields:
    :type fields: list[_IField]
    :return:
    :rtype:
    """

    for field in fields:
        field.run(src, dst)


class DataPacker(object):

    def __init__(self, fields):
        """

        :param fields:
        :type fields: list[_IField]
        """

        self.fields = fields

    def run(self, src, dst):
        run(src, dst, self.fields)
