# coding=utf-8

class BaseContainer(object):
    def __str__(self):
        raise NotImplementedError('Implemented by yourself')

    def __setitem__(self, key, value):
        raise NotImplementedError('Implemented by yourself')

    def __getitem__(self, key):
        raise NotImplementedError('Implemented by yourself')

    def __delitem__(self, key):
        raise NotImplementedError('Implemented by yourself')

    def __len__(self):
        raise NotImplementedError('Implemented by yourself')

    def __contains__(self, k):
        raise NotImplementedError('Implemented by yourself')

    def clear(self):
        raise NotImplementedError('Implemented by yourself')

    def get(self, k, d=None):
        raise NotImplementedError('Implemented by yourself')

    def setdefault(self, key, default=None):
        raise NotImplementedError('Implemented by yourself')

    def raw_data(self):
        """
        获取原始数据
        :return:
        :rtype:
        """
        raise NotImplementedError('Implemented by yourself')