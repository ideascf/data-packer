# coding=utf-8
import pytest
from data_packer import SelectorField, OptionalField, CompositedField
from data_packer import err, container
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

def test_selector():
    # 最多选一个字段
    fields = [
        SelectorField(
            fields=[
                OptionalField(src_name='a', dst_name='a'),
                OptionalField(src_name='b', dst_name='b'),
                OptionalField(src_name='c', dst_name='c'),
            ],
            at_most=1,
        )
    ]
    dst = run(fields, g_src)
    assert len(dst) == 1
    assert dst['a'] == g_src['a']


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
    dst = run(fields, g_src)
    assert len(dst) == 2
    assert dst['a'] == g_src['a']
    assert dst['b'] == g_src['b']
    assert 'c' not in dst
    assert 'c' in g_src


    # 最多选 2 个字段-不足够
    fields = [
        SelectorField(
            fields = [
                OptionalField(src_name='a', dst_name='a'),
            ],
            at_most=2,
        )
    ]
    dst = run(fields, g_src)
    assert len(dst) == 1
    assert dst['a'] == g_src['a']


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
    dst = run(fields, g_src)
    assert len(dst) == 3
    assert dst['a'] == g_src['a']
    assert dst['b'] == g_src['b']
    assert dst['c'] == g_src['c']

    # 最少选 2 个字段-不足够
    fields = [
        SelectorField(
            fields = [
                OptionalField(src_name='a', dst_name='a'),
            ],
            at_least=2,
        )
    ]
    with pytest.raises(err.DataPackerLackFieldError):
        dst = run(fields, g_src)


def test_invalid_define():
    # 非法的field定义
    with pytest.raises(err.DataPackerProgramError):
        SelectorField(
            fields = [
                OptionalField(src_name='a', dst_name='a'),
                OptionalField(src_name='b', dst_name='b'),
                OptionalField(src_name='c', dst_name='c'),
            ],
            at_least=3,
            at_most=2,
        )
