# coding=utf-8
# coding=utf-8
from ._base import BaseSetter
from .. import err, constant

class DictSetter(BaseSetter):
    def do(self, dst, dst_name, value, overwrite):
        """

        :param dst:
        :type dst: dict
        :param dst_name:
        :type dst_name: str
        :param overwrite:
        :type overwrite: constant.OverwriteMode
        :return:
        :rtype:
        """

        if dst_name in dst:
            exist = True
        else:
            exist = False

        if exist:
            if overwrite == constant.OverwriteMode.IGNORE:
                return
            elif overwrite == constant.OverwriteMode.RAISE:
                raise err.DataPackerDstKeyDupError('key({}) already exist in dst'.format(dst_name))

        dst[dst_name] = value