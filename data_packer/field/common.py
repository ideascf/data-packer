# coding=utf-8
from data_packer.field._base import BaseField
from data_packer import constant


class FixField(BaseField):
    """
    带固定值的字段
    @ATTENTION 一般用于打包到目的数据容器时使用, 如某些场景需要传入一些固定值
    """

    def __init__(self, fix_value, dst_name, overwrite=constant.OverwriteMode.OVERWRITE, checker=None,
                 converter=None):
        super(FixField, self).__init__('', dst_name, overwrite, checker, converter)

        self.fix_value = fix_value

    def _get_value(self, src):
        return self.fix_value


class DynamicField(BaseField):
    """
    动态生成值的字段
    @ATTENTION 一般用于打包到目的数据容器时使用, 如生成随机数等
    """

    def __init__(self, value_maker, dst_name, overwrite=constant.OverwriteMode.OVERWRITE, checker=None,
                 converter=None):
        """

        :param value_maker: 动态构建值的方法, 传入dst_name, 传出value
        :type value_maker: callable,
        :param dst_name:
        :type dst_name:
        :param overwrite:
        :type overwrite:
        :param checker:
        :type checker:
        :param converter:
        :type converter:
        """
        super(DynamicField, self).__init__('', dst_name, overwrite, checker, converter)

        self.value_maker = value_maker

    def _get_value(self, src):
        return self.value_maker(self.dst_name)

