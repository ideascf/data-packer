# coding=utf-8
from ._base import _IField
from .single import OptionalField
from .. import err

class SelectorField(_IField):
    valid_field_cls = (OptionalField,)

    def __init__(self, fields, at_most=999999, at_least=0):
        """

        :param fields: field对象的list, 按迭代器的顺序来取字段
        :param at_most: 最多取多少个字段, 即取到at_most个字段后停止
        :param at_least: 最少多少个字段
        :type fields: list[OptionalField]
        :type at_most: int
        :type at_least: int
        :return:
        """

        self.fields = fields
        self.at_most = at_most
        self.at_least = at_least

        if at_least > at_most:
            raise err.DataPackerProgramError('at_least({}) > at_most({})'.format(at_least, at_most))

        if not all([
            isinstance(field, self.valid_field_cls)
            for field in fields
        ]):
            raise err.DataPackerProgramError('SelectorField Only consists of {}'.format(self.valid_field_cls))


    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def run(self, src, dst):
        got = 0
        for field in self.fields:
            try:
                field.run(src, dst)
                got += 1
            except err.DataPackerError:
                continue

            if got >= self.at_most:
                break

        if got < self.at_least:
            raise err.DataPackerLackFieldError('field({}): got {}, but need {}'.format(self, got, self.at_least))

        return True


class CompositedField(_IField):
    def __init__(self, fields):
        """

        :param fields: field对象的list,只要其中任何一个field匹配即可
        :param must_one: 是否至少包含fields中的一个字段
        :type fields: list[BaseField]
        :type must_one: bool
        :return:
        """

        self.fields = fields

    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def run(self, src, dst):
        for field in self.fields:
            field.run(src, dst)

        return True
