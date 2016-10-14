# coding=utf-8
import re
from functools import partial
from .. import err, constant
from .. import err

class BaseChecker(object):

    def __str__(self):
        return 'cls_name: {cls_name}property: {property}'.format(
            cls_name=self.__class__,
            property=self.__dict__
        )

    def verify(self, src_name, dst_name, value):
        """
        检查该字段的值是否合法
        :param src_name: 字段在传入容器中的名称
        :type src_name: str
        :param dst_name: 字段再传出容器中的名称
        :type dst_name: str
        :param value: 从传入容器中取出的该字段的值
        :type value:
        :raise: err.DataPackerCheckError
        """

        raise NotImplementedError('Implemented by yourself')


class ReChecker(BaseChecker):
    """
    正则表达式校验器
    """

    def __init__(self, pattern, flags=0):
        super(ReChecker, self).__init__()

        self.pat = re.compile(pattern, flags)
        self._pattern_str = pattern

    def verify(self, src_name, dst_name, value):
        if self.pat.match(value) is None:
            raise err.DataPackerCheckError(src_name, dst_name, value, self)


class TypeChecker(BaseChecker):
    """
    类型校验器
    """
    def __init__(self, tp):
        """

        :param tp:
        :type tp: type(tp) | tuple(type(tp))
        """
        super(TypeChecker, self).__init__()
        self.tp = tp

    def verify(self, src_name, dst_name, value):
        if not isinstance(value, self.tp):
            raise err.DataPackerCheckError(src_name, dst_name, value, self)


class LenChecker(BaseChecker):
    def __init__(self, min_len=None, max_len=None):
        """

        :param min_len:
        :type min_len: int | None
        :param max_len:
        :type max_len: int | None
        """
        super(LenChecker, self).__init__()

        if min_len is not None \
                and max_len is not None \
                and min_len > max_len:
            raise err.DataPackerProgramError('min_len({}) > max_len({})'.format(min_len, max_len))

        self.min_len = min_len
        self.max_len = max_len

    def verify(self, src_name, dst_name, value):
        l = len(value)

        if self.min_len is not None\
            and l < self.min_len:
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                "Value's len({}) is too short than min_len({})".format(l, self.min_len)
            )

        if self.max_len is not None\
            and l > self.max_len:
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                "Value's len({}) is too long than max_len({})".format(l, self.max_len)
            )


class ValueChecker(BaseChecker):
    """
    操作符校验器
    """

    OP2FUNC = {
        constant.OP.EQ: lambda a,b: a == b,
        constant.OP.NE: lambda a,b: a != b,
        constant.OP.GT: lambda a,b: a > b,
        constant.OP.GE: lambda a,b: a >= b,
        constant.OP.LT: lambda a,b: a < b,
        constant.OP.LE: lambda a,b: a <= b,

        constant.OP.IN: lambda a,b: a in b,
        constant.OP.NOT_IN: lambda a,b: a not in b,
    }

    def __init__(self, op_wrapper_list):
        """

        :param op_wrapper_list: 形如: [(constant.OP.GT, 1), (constant.OP.LE, 10)]
        :type op_wrapper_list: list[tuple]
        """
        super(ValueChecker, self).__init__()

        self.op_wrapper_list = op_wrapper_list

    def verify(self, src_name, dst_name, value):
        map(partial(self._op_checker, src_name, dst_name, value), self.op_wrapper_list)

    def _op_checker(self, src_name, dst_name, value, op_wrapper):
        op = op_wrapper[0]
        d_value = op_wrapper[1]

        func = self.OP2FUNC.get(op)
        if func is None:
            raise err.DataPackerProgramError('Invalid op({})'.format(op))

        if not func(value, d_value):
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self,
                "FAILED op_wrapper is: {}".format(op_wrapper)
            )


class NullChecker(BaseChecker):
    def verify(self, src_name, dst_name, value):
        pass


class CheckerWrapper(BaseChecker):
    """
    校验函数包装器, 将校验函数包装为checker对象
    """

    def __init__(self, func):
        super(CheckerWrapper, self).__init__()
        if not callable(func):
            raise err.DataPackerProgramError('func({}) must be callable'.format(func))

        self.func = func

    def verify(self, src_name, dst_name, value):
        if not self.func(src_name, dst_name, value):
            raise err.DataPackerCheckError(
                src_name, dst_name, value, self
            )