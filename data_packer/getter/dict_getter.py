# coding=utf-8
from ._base import BaseGetter
from .. import err

class DictGetter(BaseGetter):
    def do(self, src, src_name):
        """

        :param src:
        :type src: dict
        :param src_name:
        :type src_name: str
        :return:
        :rtype:
        """

        if src_name not in src:
            raise err.DataPackerSrcKeyNotFoundError('key(%s) Not found in src!')

        return src[src_name]