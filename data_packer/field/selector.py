# coding=utf-8
from ._base import _IField
from .. import err

class SelectorField(_IField):
    def __init__(self, fields, must_one=True):
        """

        :param fields: field对象的list,只要其中任何一个field匹配即可
        :param must_one: 是否至少包含fields中的一个字段
        :type fields: list[BaseField]
        :type must_one: bool
        :return:
        """

        self.fields = fields
        self.must_one = must_one

    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def run(self, src, dst):
        for field in self.fields:
            try:
                if field.run(src, dst):
                    break
            except err.DataPackerError:
                continue
        else:  # 没有获取到一个合法的field
            if self.must_one:
                raise err.DataPackerSrcKeyNotFoundError('field({}): No anyone field be found in src!'.format(self))

        return True