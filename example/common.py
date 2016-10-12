# coding=utf-8
from data_packer import err, DataPacker, container


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
    },
    'f': '0x123',
    'g': 'longlonglonglonglong',
    'h': 2,
}
g_src = container.DictContainer(g_src)


def demo_run(fields, msg, dst=None):
    print ''
    print msg

    if dst is None:
        dst = container.DictContainer({})
    elif isinstance(dst, dict):
        dst = container.DictContainer(dst)
    else:
        raise TypeError('dst Must be dict or DictContainer')

    dp = DataPacker(fields)
    try:
        dp.run(g_src, dst)
    except err.DataPackerError as e:
        print '抛出了异常: ', type(e), e

    print dst

