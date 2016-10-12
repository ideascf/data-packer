# coding=utf-8
"""
单一的样例
"""
import pytest
from data_packer import DefaultField, OptionalField, PlaceholderField, RequiredField, CompositedField
from data_packer import container
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
g_src = container.DictContainer(g_src)

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


def test_composited():
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
    dst = run(fields, g_src)
    assert len(dst) == 4
    assert dst['a'] == g_src['a']
    assert dst['b'] == g_src['b']
    assert dst['c'] == g_src['c']
    assert dst['e']['e.1'] == g_src['e']['1']
    assert 'e.a' not in dst['e']
    assert 'a' not in g_src['e']
    assert dst['e']['2']['e.2.a'] == g_src['e']['2']['a']
    assert dst['e']['2']['e.2.b'] == g_src['e']['2']['b']
