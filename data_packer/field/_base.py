# coding=utf-8
from ..checker import BaseChecker
from ..getter import BaseGetter, DictGetter
from ..setter import BaseSetter, DictSetter
from ..converter import BaseConverter
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
        raise NotImplementedError('Implemented by youself')

class BaseField(_IField):
    def __init__(self, src_name, dst_name, overwrite=constant.OverwriteMode.OVERWRITE,
                 getter=None, checker=None, converter=None, setter=None):
        """

        :param src_name: 该字段在传入数据容器中的名称
        :param dst_name: 该字段在传出数据容器中的名称
        :param overwrite: 是否覆盖已经存在的传出数据容器中的值
        :param getter: 字段的获取器，从传入容器中获取数据
        :param checker: 字段的校验器，校验该字段的值是否合法
        :param converter: 字段转换器，按需转换该字段的值
        :param setter: 字段的设置器，将转换后的该字段的值设置到传出数据容器中
        :type src_name: str
        :type dst_name: str
        :type overwrite: constant.OverwriteMode
        :type getter: BaseGetter
        :type checker: BaseChecker
        :type converter: BaseConverter
        :type setter: BaseSetter
        """

        self.src_name = src_name
        self.dst_name = dst_name
        self._overwrite = overwrite

        self._getter = self._valid_er(getter, BaseGetter, DictGetter(), 'param(getter) must be callable or None.')
        """:type: BaseGetter"""
        self._checker = self._valid_er(checker, BaseChecker, None, 'param(checker) must be callable or None.')
        """:type: BaseChecker"""
        self._converter = self._valid_er(converter, BaseConverter, None, 'param(converter) must be callable or None.')
        """:type: BaseConverter"""
        self._setter = self._valid_er(setter, BaseSetter, DictSetter(), 'param(setter) must be callable or None.')
        """:type: BaseSetter"""

    def __str__(self):
        return '{cls_name}: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def run(self, src, dst):
        """

        :param src: 传入数据容器,默认为字典
        :param dst: 传出数据容器,默认为字典
        :return:
        :rtype: bool
        :raise: err.DataPackerError
        """


        try:
            value = self._get_value(src)
            self._do_check(value)
            value = self._do_convert(value)
            self._set_value(value, dst)
        except err._DataPackerInterruptError:  # 内部流程中断异常，本次get操作失败
            return True
        else:
            return True

    def _get_value(self, src):
        """
        从传入数据容器中获取value
        :param src:
        :return:
        """

        return self._getter.do(src, self.src_name)

    def _set_value(self, value, dst):
        """
        将value设置到目的字典中
        :param value:
        :param dst:
        :type value:
        :type dst: dict
        :return:
        """

        return self._setter.do(dst, self.dst_name, value, self._overwrite)

    #### 动作函数 ####
    def _do_check(self, value):
        """
        完成对字段的校验
        :param value:
        :return:
        :rtype: bool
        :raise: err.JsonGetterCheckError
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
        校验各种er, getter, checker, converter, setter
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