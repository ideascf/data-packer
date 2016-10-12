# coding=utf-8
import pytest
from data_packer import constant, container, err
from data_packer import RequiredField
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

def test_overwrite():
    # 覆盖
    fields = [
        RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.OVERWRITE)
    ]
    dst = {
        'exist_name': 1,
    }
    run(fields, g_src, dst)
    assert dst['exist_name'] == g_src['b']
    assert dst['exist_name'] != 1

    # 忽略
    fields = [
        RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.IGNORE)
    ]
    dst = {
        'exist_name': 1,
    }
    run(fields, g_src, dst)
    assert dst['exist_name'] != g_src['b']
    assert dst['exist_name'] == 1

    # 抛异常
    fields = [
        RequiredField('b', 'exist_name', overwrite=constant.OverwriteMode.RAISE)
    ]
    dst = {
        'exist_name': 1,
    }

    with pytest.raises(err.DataPackerDstKeyDupError):
        run(fields, g_src, dst)
    assert dst['exist_name'] == 1
