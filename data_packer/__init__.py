# coding=utf-8

def run(src, dst, fields):
    """

    :param src:
    :type src:
    :param dst:
    :type dst:
    :param fields:
    :type fields: list[_IField]
    :return:
    :rtype:
    """

    for field in fields:
        field.run(src, dst)


class DataPacker(object):

    def __init__(self, fields):
        """

        :param fields:
        :type fields: list[_IField]
        """

        self.fields = fields

    def run(self, src, dst):
        run(src, dst, self.fields)
