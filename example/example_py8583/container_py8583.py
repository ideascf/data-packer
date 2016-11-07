# coding=utf-8
from data_packer import container
from py8583.py8583 import Py8583
from py8583.err import Py8583BitNotExistError


class Py8583Container(container.BaseContainer):

    def __init__(self, data):
        super(Py8583Container, self).__init__()

        self._data = data
        """:type: Py8583"""

    def __contains__(self, k):
        """

        :param k: filed index, 8583的第几域
        :type k: int
        :return:
        :rtype: bool
        """

        return k in self._data.bitmap

    def __delitem__(self, key):
        """

        :param key: 需要清除的8583第几域
        :type key: int
        :return:
        :rtype:
        """

        return self._data.clear_bit(key)

    def __len__(self):
        """
        返回是64或128, 代表是64域的8583还是128域的8583.
        :return:
        :rtype: int
        """

        return self._data._bitmap_len()

    def __getitem__(self, key):
        try:
            return self._data.get_bit(key)
        except Py8583BitNotExistError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        return self._data.set_bit(key, value)

    def __str__(self):
        return self._data.bitmap_info() + '\n' + self._data.field_info()

    def raw_data(self):
        return self._data

    def clear(self):
        return self._data.reset()

    def get(self, k, d=None):
        try:
            return self._data.get_bit(k)
        except Py8583BitNotExistError:
            return d

    def setdefault(self, key, default=None):
        if key not in self:
            self._data.set_bit(key, default)
