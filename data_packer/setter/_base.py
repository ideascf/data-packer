# coding=utf-8

class BaseSetter(object):
    def do(self, dst, dst_name, value, overwrite):
        """

        :param dst:
        :type dst: 传出数据容器
        :param dst_name:
        :type dst_name: str
        :param overwrite: 是否覆盖已有的值
        :type overwrite:
        """

        raise NotImplementedError('Implemented by youself')