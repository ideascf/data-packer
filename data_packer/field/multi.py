# coding=utf-8
from ._base import _IField, BaseField
from .single import OptionalField
from ..container import BaseContainer
from .. import err, constant

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


class CompositedField(BaseField):
    def __init__(self, fields, src_sub_container_cls, dst_sub_container, src_name, dst_name=None, overwrite=constant.OverwriteMode.OVERWRITE):
        """

        :param fields:
        :type fields:
        :param src_sub_container_cls:
        :type src_sub_container_cls: type(BaseContainer)
        :param dst_sub_container:
        :type dst_sub_container: BaseContainer
        :param src_name:
        :type src_name: str
        :param dst_name:
        :type dst_name: str
        :param overwrite:
        :type overwrite:
        """

        super(CompositedField, self).__init__(src_name, dst_name, overwrite, None, None)
        self.fields = fields
        self.src_sub_container_cls = src_sub_container_cls
        self.dst_sub_container = dst_sub_container

    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def _get_value(self, src):
        src_raw_data = super(CompositedField, self)._get_value(src)
        src_sub_container = self.src_sub_container_cls(src_raw_data)

        for field in self.fields:
            field.run(src_sub_container, self.dst_sub_container)

        return self.dst_sub_container.raw_data()
