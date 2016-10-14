# coding=utf-8
import json

import data_packer.checker._base
from data_packer import RequiredField, CompositedField, OptionalField, DefaultField
from data_packer import checker, DataPacker, container, converter
from data_packer.checker import text_checker, LenChecker, TypeChecker
from data_packer.converter import TypeConverter
import data_packer

busicd = RequiredField(
    src_name='busicd',
    dst_name='busicd',
    checker=[
        data_packer.checker._base.TypeChecker(str),
        data_packer.checker._base.LenChecker(min_len=6, max_len=6),
    ],
    converter=converter.TypeConverter(int)
)
businm = OptionalField(
    src_name='businm',
    dst_name='busixxx',
    checker=[
        data_packer.checker._base.TypeChecker(str),
    ]
)
yyy = RequiredField(
    src_name='yyy',
    dst_name='yyy',
    checker=[
        data_packer.checker._base.ReChecker(r'\d')
    ]
)

cli_dtm = OptionalField(
    src_name='cli_dtm'
)

pay_method = DefaultField(
    default_value='alipay',
    src_name='pay_method',
)

location = CompositedField(
    fields=[
        RequiredField('lng', checker=TypeChecker((float, str, unicode)), converter=TypeConverter(float)),
        RequiredField('lat', checker=TypeChecker((float, str, unicode)), converter=TypeConverter(float)),
        DefaultField('china', 'country', checker=[text_checker, LenChecker(1, 20)]),
        OptionalField('city', checker=[text_checker, LenChecker(1, 20)]),
    ],
    src_sub_container_cls=container.DictContainer,
    dst_sub_container=container.DictContainer({}),
    src_name='location'
)

q = {
    'busicd': '800101',
    'businm': 'alipay_query',
    'yyy': '234234',
    'location': {
        'lng': '1.0',
        'lat': 9.9
    }
}
d = {}

alipay_query_fields = [busicd, businm, yyy, cli_dtm, pay_method, location]
try:
    alipay_query = DataPacker(alipay_query_fields)
    alipay_query.run(container.DictContainer(q), container.DictContainer(d))
except Exception as e:
    print e

print json.dumps(d, indent=4)
