# coding=utf-8
from data_packer import DataPacker

def run(fields, src, dst=None):

    dst = {} if dst is None else dst
    dp = DataPacker(fields)
    dp.run(src, dst)

    return dst