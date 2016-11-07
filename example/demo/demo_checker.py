# coding=utf-8
from functools import partial
import data_packer.checker._base
from data_packer import RequiredField, constant, checker
from common import demo_run

###################################
ck = data_packer.checker._base.ReChecker(r'\d')
# 正则表达式校验通过
fields = [
    RequiredField('f', 'f', checker=ck)
]
demo_run(fields, '正则表达式校验-pass')

# 正则表达式校验失败
fields = [
    RequiredField('b', 'b', checker=ck)
]
demo_run(fields, '正则表达式校验-failed')


###################################
ck = data_packer.checker._base.TypeChecker(int)
# 类型校验通过
fields = [
    RequiredField('a', 'a', checker=ck)
]
demo_run(fields, '类型校验-pass')

# 类型校验失败
fields = [
    RequiredField('b', 'b', checker=ck)
]
demo_run(fields, '类型校验-failed')


###################################
ck = data_packer.checker._base.LenChecker(1, 10)
# 长度校验通过
fields = [
    RequiredField('b', 'b', checker=ck)
]
demo_run(fields, '长度校验-pass')

# 长度校验失败
fields = [
    RequiredField('g', 'g', checker=ck)
]
demo_run(fields, '长度校验-failed')


###################################
ck = data_packer.checker._base.ValueChecker([
    (constant.OP.EQ, 1),
    (constant.OP.NE, 2),
    (constant.OP.LT, 10),
    (constant.OP.LE, 1),
    (constant.OP.GT, 0),
    (constant.OP.GE, 1),

    (constant.OP.IN, (1, 2, 3)),
    (constant.OP.NOT_IN, ('a', 'b')),
])
# 值校验通过
fields = [
    RequiredField('a', 'a', checker=ck)
]
demo_run(fields, '值校验-pass')

# 值校验失败
fields = [
    RequiredField('h', 'h', checker=ck)
]
demo_run(fields, '值校验-failed')


###################################
ck = data_packer.checker._base.CheckerWrapper(lambda src_name, dst_name, value: isinstance(value, dict))
# 校验器包装器校验通过
fields = [
    RequiredField('e', 'e', checker=ck)
]
demo_run(fields, '校验器包装器校验-pass')

# 校验器包装器校验失败
fields = [
    RequiredField('a', 'a', checker=ck)
]
demo_run(fields, '校验器包装器校验-failed')


###################################
fields = [
    RequiredField('ip', 'ip', checker=checker.ipv4_checker)
]
demo_run(fields, '测试ipv4校验', src={'ip': '192.168.1.1'})


###################################
fields = [
    RequiredField('url', 'url', checker=checker.url_checker)
]
urls = [
    'http://192.168.0.1',
    'https://192.168.0.1',
    'ftp://192.168.0.1',
    'ftps://192.168.0.1',
]
for url in urls:
    demo_run(fields, '测试URL校验', src={'url': url})