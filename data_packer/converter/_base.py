# coding=utf-8
from data_packer import err


class BaseConverter(object):
    def convert(self, src_name, dst_name, value):
        """
        按需转换该字段的值
        :param src_name: 字段在传入容器中的名称
        :type src_name: object
        :param dst_name: 字段再传出容器中的名称
        :type dst_name: object
        :param value: 从传入容器中取出的该字段的值
        :type value:
        :return: 处理后的字段值
        :rtype:
        """

        raise NotImplementedError('Implemented by yourself')


class TypeConverter(BaseConverter):
    def __init__(self, tp):
        super(TypeConverter, self).__init__()
        self.tp = tp

    def convert(self, src_name, dst_name, value):
        return self.tp(value)


class NullConverter(BaseConverter):
    def convert(self, src_name, dst_name, value):
        pass


class ConverterWrapper(BaseConverter):
    """
    转换函数包装器, 将转换函数包装为converter对象
    """

    def __init__(self, func):
        super(ConverterWrapper, self).__init__()
        if not callable(func):
            raise err.DataPackerProgramError('func({}) must be callable'.format(func))

        self.func = func

    def convert(self, src_name, dst_name, value):
        return self.func(src_name, dst_name, value)