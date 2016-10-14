# coding=utf-8
from data_packer import checker


def verify(ck, value):
    """

    :param ck:
    :type ck: checker.BaseChecker
    :param value:
    :type value:
    :return:
    :rtype:
    """

    ck.verify('', '', value)