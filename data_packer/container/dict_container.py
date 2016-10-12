# coding=utf-8
from ._base import BaseContainer

class DictContainer(BaseContainer):
    def __init__(self, data):
        """

        :param data:
        :type data: dict
        """
        self._data = data

    def __str__(self):
        return self._data.__str__()

    def __len__(self):
        return self._data.__len__()

    def __contains__(self, k):
        return self._data.__contains__(k)

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        return self._data.__delitem__(key)

    def clear(self):
        return self._data.clear()

    def setdefault(self, key, default=None):
        return self._data.setdefault(key, default)

    def get(self, k, d=None):
        return self._data.get(k, d)

    def raw_data(self):
        return self._data