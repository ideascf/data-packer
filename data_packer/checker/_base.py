# coding=utf-8
from .. import err

class BaseChecker(object):
    def do(self, src_name, dst_name, value):
        """
        检查该字段的值是否合法
        :param src_name: 字段在传入容器中的名称
        :type src_name: str
        :param dst_name: 字段再传出容器中的名称
        :type dst_name: str
        :param value: 从传入容器中取出的该字段的值
        :type value:
        :return: 通过返回True, 否则返回False或抛出异常
        :rtype: bool
        :raise: err.DataPackerCheckError
        """

        raise NotImplementedError('Implemented by yourself')