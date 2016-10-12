# coding=utf-8

from ._base import BaseField
from .. import err, constant

class DefaultField(BaseField):
    def __init__(self, default_value, src_name, dst_name, overwrite=constant.OverwriteMode.OVERWRITE,
                 getter=None, checker=None, converter=None, setter=None):
        """

        :param default_value: 字段默认值
        :param src_name: 该字段在传入数据容器中的名称
        :param dst_name: 该字段在传出数据容器中的名称
        :param overwrite: 是否覆盖已经存在的传出数据容器中的值
        :param getter: 字段的获取器，从传入容器中获取数据
        :param checker: 字段的校验器，校验该字段的值是否合法
        :param converter: 字段转换器，按需转换该字段的值
        :param setter: 字段的设置器，将转换后的该字段的值设置到传出数据容器中
        :type default_value:
        :type src_name: str
        :type dst_name: str
        :type overwrite: constant.OverwriteMode
        :type getter: BaseGetter
        :type checker: BaseChecker
        :type converter: BaseConverter
        :type setter: BaseSetter
        """

        super(DefaultField, self).__init__(src_name, dst_name, overwrite, getter, checker, converter, setter)

        self.default_value = default_value

    def _get_value(self, src):
        try:
            return super(DefaultField, self)._get_value(src)
        except err.DataPackerSrcKeyNotFoundError:
            return self.default_value


class OptionalField(BaseField):
    def _get_value(self, src):
        try:
            return super(OptionalField, self)._get_value(src)
        except err.DataPackerSrcKeyNotFoundError:
            raise err._DataPackerInterruptError('Ignore not exist optional fields({})'.format(self))


class PlaceholderField(BaseField):
    def run(self, src, dst):
        return True


class RequiredField(BaseField):
    pass