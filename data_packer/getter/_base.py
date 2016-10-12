# coding=utf-8

class BaseGetter(object):
    def do(self, src, src_name):
        """

        :param src: 传入数据容器
        :type src: object
        :param src_name: 该字段在传入数据容器中的名称
        :type src_name: str
        :return: 该字段的传入值
        :rtype:
        """

        raise NotImplementedError('Implemented by youself')