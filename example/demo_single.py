# coding=utf-8
"""
单一的样例
"""

from data_packer import DefaultField, OptionalField, PlaceholderField, RequiredField
from common import demo_run

######################################################################################################

#### 缺省值字段  ####
# 有传入值
fields = [
    DefaultField('defalut', src_name='a', dst_name='a')
]
demo_run(fields, '有传入值时的DefaultField')

# 无传入值
fields = [
    DefaultField('default value', src_name='Not Exist', dst_name='Dst name')
]
demo_run(fields, '无传入值时的DefaultField')


#### 可选字段  ####
# 有传入值
fields = [
    OptionalField('b', 'dst name')
]
demo_run(fields, '有传入值时的OptionalField')

# 无传入值
fields = [
    OptionalField('Not Exist', 'dst name')
]
demo_run(fields, '无传入值时的OptionalField')


#### 占位字段  ####
# 有传入值
fields = [
    PlaceholderField('b', 'dst name')
]
demo_run(fields, '有传入值时的PlaceholderField')

# 无传入值
fields = [
    PlaceholderField('Not Exist', 'dst name')
]
demo_run(fields, '无传入值时的PlaceholderField')


#### 必填字段  ####
# 有传入值
fields = [
    RequiredField('b', 'dst name')
]
demo_run(fields, '有传入值时的RequiredField')

# 无传入值
fields = [
    RequiredField('Not Exist', 'dst name')
]
demo_run(fields, '无传入值时的RequiredField')
