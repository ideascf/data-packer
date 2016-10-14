# coding=utf-8
"""
单一的样例
"""

from data_packer import DefaultField, OptionalField, PlaceholderField, RequiredField, MagicField
from data_packer import checker
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


#### 魔法字段 ####
mf = MagicField('src_name', 'dst_name', checker=checker.NullChecker())

# 在场景1时, 该字段是可选的,所以需要设置该字段为可选字段
of = mf.o()   # 即可通过mf,创建一个可选字段
print type(of)
# 在场景2时, 该字段是待默认值的,所以需要设置该字段为默认字段
df = mf.d('default_value_xxxxxx')  # 即可通过mf,创建一个带默认值的默认值字段
print type(df)
# 在场景3时, 该字段是必需传递的,所以需要设置该字段为必传
rf = mf.r()  # 即可通过mf,创建一个必传字段
print type(rf)

# 在场景4时, 该字段的源字段名是 'guest', 所以需要更改mf的源字段名
f = mf.r(src_name='guest')
print f.src_name
# 在场景5时, 该字段没有checker, 所以需要去掉该字段的checker
f = mf.r(checker=None)
print f._checker_list