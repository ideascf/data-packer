# coding=utf-8

class OverwriteMode:
    IGNORE = 0
    OVERWRITE = 1
    RAISE = 2

class OP:
    EQ = 0  # 相等
    NE = 1  # 不等于
    GT = 2  # 大于
    GE = 3  # 大于或等于
    LT = 4  # 小于
    LE = 5  # 小宇或等于

    IN = 20
    NOT_IN = 21


class IP_VERSION:
    BOTH = 0
    IPV4 = 1
    IPV6 = 2
