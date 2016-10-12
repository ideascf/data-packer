# coding=utf-8
from ..checker import BaseChecker
from ..converter import BaseConverter
from ..container import BaseContainer
from .. import err, constant


class _IField(object):
    def run(self, src, dst):
        """

        :param src:
        :type src:
        :param dst:
        :type dst:
        :return:
        :rtype: bool
        :raise: err.DataPackerError
        """
        raise NotImplementedError('Implemented by yourself')

class BaseField(_IField):
    def __init__(self, src_name, dst_name, overwrite=constant.OverwriteMode.OVERWRITE,
                 checker=None, converter=None):
        """

        :param src_name: 该字段在传入数据容器中的名称
        :param dst_name: 该字段在传出数据容器中的名称
        :param overwrite: 是否覆盖已经存在的传出数据容器中的值
        :param checker: 字段的校验器，校验该字段的值是否合法
        :param converter: 字段转换器，按需转换该字段的值
        :type src_name: str
        :type dst_name: str
        :type overwrite: constant.OverwriteMode
        :type checker: BaseChecker | None
        :type converter: BaseConverter | None
        """

        self.src_name = src_name
        self.dst_name = dst_name
        self._overwrite = overwrite

        self._checker = self._valid_er(checker, BaseChecker, None, 'param(checker) must be callable or None.')
        """:type: BaseChecker"""
        self._converter = self._valid_er(converter, BaseConverter, None, 'param(converter) must be callable or None.')
        """:type: BaseConverter"""

    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def run(self, src, dst):
        """

        :param src: 传入数据容器,默认为字典
        :param dst: 传出数据容器,默认为字典
        :type src: BaseContainer
        :type dst: BaseContainer
        :return:
        :rtype: bool
        :raise: err.DataPackerError
        """

        if not all([
            isinstance(src, BaseContainer),
            isinstance(dst, BaseContainer),
        ]):
            raise err.DataPackerProgramError('src and dst must be BaseContainer')

        try:
            value = self._get_value(src)
            self._do_check(value)
            value = self._do_convert(value)
            self._set_value(value, dst)
        except err._DataPackerInterruptError:  # 内部流程中断异常，本次get操作失败
            return True
        except Exception as e:
            print e
            print 'src: ', src
            print 'dst: ', dst
            print 'field: ', self
        else:
            return True

    def _get_value(self, src):
        """
        从传入数据容器中获取value
        :param src:
        :type src: BaseContainer
        :return:
        """

        try:
            return src[self.src_name]
        except KeyError:
            raise err.DataPackerSrcKeyNotFoundError('key({}) Not found in src!'.format(self.src_name))

    def _set_value(self, value, dst):
        """
        将value设置到目的字典中
        :param value:
        :param dst:
        :type value:
        :type dst: BaseContainer
        :return:
        """

        if self.dst_name in dst:
            if self._overwrite == constant.OverwriteMode.IGNORE:
                return
            elif self._overwrite == constant.OverwriteMode.RAISE:
                raise err.DataPackerDstKeyDupError('key({}) already exist in dst'.format(self.dst_name))

        dst[self.dst_name] = value

    #### 动作函数 ####
    def _do_check(self, value):
        """
        完成对字段的校验
        :param value:
        :return:
        :rtype: bool
        :raise: err.DataPackerCheckError
        """

        if self._checker is None:  # No checker
            return True

        if self._checker.do(self.src_name, self.dst_name, value):  # pass
            return True
        else:
            raise err.DataPackerCheckError(
                'Check field({}) FAILED! src_name({}), dst_name({})'.format(
                    self, self.src_name, self.dst_name
                )
            )

    def _do_convert(self, value):
        """

        :param value:
        :return:
        """

        if self._converter is None:
            return value
        else:
            return self._converter.do(self.src_name, self.dst_name, value)

    def _do_interrupt(self, *args):
        """
        中断本field的获取, 不视为异常
        :param args:
        :type args: tuple
        :return:
        """

        raise err._DataPackerInterruptError(*args)

    def _valid_er(self, er, cls, default, errmsg):
        """
        校验各种er, checker, converter
        :param er:
        :type er:
        :param cls: 该er的基类
        :type cls:
        :param default: 默认值,如果er为None时使用
        :type default:
        :param errmsg: 类型错误消息
        :type errmsg:
        :return: er
        :rtype:
        """

        if er is None:
            er = default

        if er is not None and not isinstance(er, cls):
            raise err.DataPackerCheckError(errmsg)
        else:
            return er