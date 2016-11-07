# coding=utf-8
from data_packer import RequiredField, constant, converter
from common import demo_run


cvt = converter.TypeConverter(str)
fields = [
    RequiredField('a', 'a', converter=cvt)
]
demo_run(fields, '类型转换为str')
