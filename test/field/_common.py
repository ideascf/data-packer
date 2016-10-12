# coding=utf-8
from data_packer import DataPacker, container

def run(fields, src, dst=None):

    if dst is None:
        dst = container.DictContainer({})
    elif isinstance(dst, dict):
        dst = container.DictContainer(dst)
    else:
        raise TypeError('dst Must be dict or DictContainer')

    dp = DataPacker(fields)
    dp.run(src, dst)

    return dst.raw_data()