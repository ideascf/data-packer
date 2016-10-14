# coding=utf-8

from ._base import BaseField
from .. import err, constant

class DefaultField(BaseField):
    def __init__(self, default_value, src_name, dst_name=None, overwrite=constant.OverwriteMode.OVERWRITE,
                  checker=None, converter=None):
        """

        :param default_value: 字段默认值
        :param src_name: 该字段在传入数据容器中的名称
        :param dst_name: 该字段在传出数据容器中的名称
        :param overwrite: 是否覆盖已经存在的传出数据容器中的值
        :param checker: 字段的校验器，校验该字段的值是否合法
        :param converter: 字段转换器，按需转换该字段的值
        :type default_value:
        :type src_name: str
        :type dst_name: str
        :type overwrite: constant.OverwriteMode
        :type checker: BaseChecker
        :type converter: BaseConverter
        """

        super(DefaultField, self).__init__(src_name, dst_name, overwrite, checker, converter)

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
            raise err._DataPackerInterruptError('Ignore not exist optional field({})'.format(self))


class PlaceholderField(BaseField):
    def run(self, src, dst):
        return True


class RequiredField(BaseField):
    pass


_unchanged = object()


class MagicField(BaseField):
    def r(self, src_name=_unchanged, dst_name=_unchanged, overwrite=_unchanged, checker=_unchanged, converter=_unchanged):
        """
        使用MagicField初始化时的值,创建RequiredField
        :return:
        :rtype: RequiredField
        """

        if src_name is _unchanged:
            src_name = self.src_name
        if dst_name is _unchanged:
            dst_name = self.dst_name
        if overwrite is _unchanged:
            overwrite = self._overwrite
        if checker is _unchanged:
            checker = self._checker_list
        if converter is _unchanged:
            converter = self._converter_list

        return RequiredField(src_name, dst_name, overwrite, checker, converter)

    def o(self, src_name=_unchanged, dst_name=_unchanged, overwrite=_unchanged, checker=_unchanged, converter=_unchanged):
        """
        使用MagicField初始化时的值,创建OptionalField
        :return:
        :rtype: OptionalField
        """

        if src_name is _unchanged:
            src_name = self.src_name
        if dst_name is _unchanged:
            dst_name = self.dst_name
        if overwrite is _unchanged:
            overwrite = self._overwrite
        if checker is _unchanged:
            checker = self._checker_list
        if converter is _unchanged:
            converter = self._converter_list

        return OptionalField(src_name, dst_name, overwrite, checker, converter)

    def d(self, default_value, src_name=_unchanged, dst_name=_unchanged, overwrite=_unchanged, checker=_unchanged, converter=_unchanged):
        """
        使用MagicField初始化时的值,创建DefaultField
        :param default_value: 该字段的默认值
        :return:
        :rtype: DefaultField
        """

        if src_name is _unchanged:
            src_name = self.src_name
        if dst_name is _unchanged:
            dst_name = self.dst_name
        if overwrite is _unchanged:
            overwrite = self._overwrite
        if checker is _unchanged:
            checker = self._checker_list
        if converter is _unchanged:
            converter = self._converter_list

        return DefaultField(default_value, src_name, dst_name, overwrite, checker, converter)

    def run(self, src, dst):
        raise err.DataPackerProgramError("Don't call MagicField directly, call d()/o()/r() instead.")

