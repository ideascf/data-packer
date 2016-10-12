# coding=utf-8
"""
复合字段的样例
"""

from data_packer import OptionalField
from data_packer import SelectorField, CompositedField
from data_packer import err, container
from common import demo_run


#### 多选字段  ####
# 最多选一个字段
fields = [
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
            OptionalField(src_name='b', dst_name='b'),
            OptionalField(src_name='c', dst_name='c'),
        ],
        at_most=1,
    )
]
demo_run(fields, '最多取 1 个字段的SelectorField')

# 最多选 2 个字段-足够
fields = [
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
            OptionalField(src_name='b', dst_name='b'),
            OptionalField(src_name='c', dst_name='c'),
        ],
        at_most=2,
    )
]
demo_run(fields, '最多取 2 个字段的SelectorField, 且足够')

# 最多选 2 个字段-不足够
fields = [
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
        ],
        at_most=2,
    )
]
demo_run(fields, '最多取 2 个字段的SelectorField, 且不足够')


#############################################
# 最少选 2 个字段-足够
fields = [
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
            OptionalField(src_name='b', dst_name='b'),
            OptionalField(src_name='c', dst_name='c'),
        ],
        at_least=2,
    )
]
demo_run(fields, '最少取 2 个字段的SelectorField, 且足够')

# 最少选 2 个字段-不足够
fields = [
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
        ],
        at_least=2,
    )
]
demo_run(fields, '最少取 2 个字段的SelectorField, 且不足够')


#############################################
# 非法的field定义
try:
    SelectorField(
        fields = [
            OptionalField(src_name='a', dst_name='a'),
            OptionalField(src_name='b', dst_name='b'),
            OptionalField(src_name='c', dst_name='c'),
        ],
        at_least=3,
        at_most=2,
    )
except err.DataPackerProgramError as e:
    print e


#############################################
# 组合字段
fields = [
    OptionalField(src_name='a', dst_name='a'),
    OptionalField(src_name='b', dst_name='b'),
    OptionalField(src_name='c', dst_name='c'),

    CompositedField(
        [
            OptionalField('1', 'e.1'),
            OptionalField('a', 'e.a'),
            CompositedField(
                [
                    OptionalField('a', 'e.2.a'),
                    OptionalField('b', 'e.2.b'),
                ],
                container.DictContainer,
                container.DictContainer({}),
                '2',
                '2'
            )
        ],
        container.DictContainer,
        container.DictContainer({}),
        'e',
        'e'
    )
]
demo_run(fields, '组合字段')
