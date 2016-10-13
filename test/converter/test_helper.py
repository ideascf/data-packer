# coding=utf-8
from data_packer import converter, err


def test_TypeConverter():
    cvt = converter.TypeConverter(int)
    assert cvt.convert('', '', '123') == 123


def test_StrConverter():
    cvt = converter.StrConverter('utf-8')
    assert cvt.convert('', '', 123) == '123'
    assert cvt.convert('', '', u'你好') == '你好'
    assert cvt.convert('', '', '你好') == '你好'

    cvt = converter.StrConverter('GBK')
    assert cvt.convert('', '', 123) == '123'.decode('utf-8').encode('GBK')
    assert cvt.convert('', '', u'你好') == '你好'.decode('utf-8').encode('GBK')
    assert cvt.convert('', '', '你好') == '你好'

def test_UnicodeConverter():
    cvt = converter.UnicodeConverter('utf-8')
    assert cvt.convert('', '', 123) == u'123'
    assert cvt.convert('', '', '你好') == u'你好'
    assert cvt.convert('', '', u'你好') == u'你好'

    cvt = converter.UnicodeConverter('GBK')
    assert cvt.convert('', '', 123) == '123'.decode('GBK')
    assert cvt.convert('', '', '你好') == '你好'.decode('GBK')
    assert cvt.convert('', '', u'你好') == u'你好'