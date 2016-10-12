# coding=utf-8
from data_packer import RequiredField
from data_packer import checker, DataPacker, container, converter
import data_packer

busicd = RequiredField(
    src_name='busicd',
    dst_name='busicd',
    checker=[
        checker.TypeChecker(str),
        checker.LenChecker(min_len=6, max_len=6),
    ],
    converter=converter.TypeConverter(int)
)
businm = RequiredField(
    src_name='businm',
    dst_name='busixxx',
    checker=[
        checker.TypeChecker(str),
    ]
)
yyy = RequiredField(
    src_name='yyy',
    dst_name='yyy',
    checker=[
        checker.ReChecker(r'\d')
    ]
)

q = {
    'busicd': '800101',
    'businm': 'alipay_query',
    'yyy': '234234'
}
d = {}

alipay_query = DataPacker([busicd, businm, yyy])
try:
    alipay_query.run(container.DictContainer(q), container.DictContainer(d))
except Exception as e:
    print e
print d
