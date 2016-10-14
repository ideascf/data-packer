# coding=utf-8
from __future__ import print_function
from data_packer import RequiredField, constant
from common import demo_run

#### 测试overwrite ####
# 覆盖
fields = [
    RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.OVERWRITE)
]
dst = {
    'exist_name': 1,
}
demo_run(fields, '测试overwrite-覆盖: \n\t BEFORE dst: {}'.format(dst), dst)
print('\t AFTER dst: ', dst)

# 忽略
fields = [
    RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.IGNORE)
]
dst = {
    'exist_name': 1,
}
demo_run(fields, '测试overwrite-忽略: \n\t BEFORE dst: {}'.format(dst), dst)
print('\t AFTER dst: ', dst)

# 抛异常
fields = [
    RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.RAISE)
]
dst = {
    'exist_name': 1,
}
demo_run(fields, '测试overwrite-抛异常: \n\t BEFORE dst: {}'.format(dst), dst)
print('\t AFTER dst: ', dst)