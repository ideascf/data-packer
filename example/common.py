# coding=utf-8
from data_packer import DataPackerError, DataPacker


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


def demo_run(fields, msg, dst=None):
    print ''
    print msg

    dst = {} if dst is None else dst
    dp = DataPacker(fields)
    try:
        dp.run(g_src, dst)
    except DataPackerError as e:
        print '抛出了异常: ', type(e), e

    print dst

