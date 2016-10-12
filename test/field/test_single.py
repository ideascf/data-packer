# coding=utf-8
"""
单一的样例
"""
import pytest
from data_packer import DefaultField, OptionalField, PlaceholderField, RequiredField
import data_packer
from _common import run

g_src = {
    'a': 1,
    'b': 'hello',
    'c': ['a', 'b', 'c'],
    'd': {
        '1': 1,
        '2': 2,
    },
    'e': {
        '1': ['a', 'b'],
        '2': {
            'a': 'a',
            'b': 'b'
        }
    }
}

#### 缺省值字段  ####
def test_default():
    # 有传入值
    fields = [
        DefaultField('defalut', src_name='a', dst_name='a')
    ]
    dst = run(fields, g_src)
    assert dst['a'] == g_src['a']

    # 无传入值
    fields = [
        DefaultField('default value', src_name='Not Exist', dst_name='Dst name')
    ]
    dst = run(fields, g_src)
    assert dst['Dst name'] == 'default value'


#### 可选字段  ####
def test_optional():
    # 有传入值
    fields = [
        OptionalField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst['dst name'] == g_src['b']

    # 无传入值
    fields = [
        OptionalField('Not Exist', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}

#### 占位字段  ####
def test_placeholder():
    # 有传入值
    fields = [
        PlaceholderField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}

    # 无传入值
    fields = [
        PlaceholderField('Not Exist', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}


#### 必填字段  ####
def test_required():
    # 有传入值
    fields = [
        RequiredField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst['dst name'] == g_src['b']

    # 无传入值
    fields = [
        RequiredField('Not Exist', 'dst name')
    ]
    with pytest.raises(data_packer.err.DataPackerSrcKeyNotFoundError):
        run(fields, g_src)
