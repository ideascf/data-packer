# coding=utf-8
"""
单一的样例
"""
import pytest
from data_packer import DefaultField, OptionalField, PlaceholderField, RequiredField, MagicField
from data_packer import container, err, constant, checker, converter
import data_packer
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

#### 缺省值字段  ####
def test_default():
    # 有传入值
    fields = [
        DefaultField('defalut', src_name='a', dst_name='a')
    ]
    dst = run(fields, g_src)
    assert dst['a'] == g_src['a']

    # 无传入值
    fields = [
        DefaultField('default value', src_name='Not Exist', dst_name='Dst name')
    ]
    dst = run(fields, g_src)
    assert dst['Dst name'] == 'default value'


#### 可选字段  ####
def test_optional():
    # 有传入值
    fields = [
        OptionalField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst['dst name'] == g_src['b']

    # 无传入值
    fields = [
        OptionalField('Not Exist', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}

#### 占位字段  ####
def test_placeholder():
    # 有传入值
    fields = [
        PlaceholderField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}

    # 无传入值
    fields = [
        PlaceholderField('Not Exist', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst == {}


#### 必填字段  ####
def test_required():
    # 有传入值
    fields = [
        RequiredField('b', 'dst name')
    ]
    dst = run(fields, g_src)
    assert dst['dst name'] == g_src['b']

    # 无传入值
    fields = [
        RequiredField('Not Exist', 'dst name')
    ]
    with pytest.raises(data_packer.err.DataPackerSrcKeyNotFoundError):
        run(fields, g_src)


class TestMagicField:
    def setup_method(self, test_method):
        self.field = MagicField('src_name', 'dst_name',
                                constant.OverwriteMode.OVERWRITE,
                                checker=checker.NullChecker(), converter=converter.NullConverter())

    def test_call_directly(self):
        field = MagicField('src_name')
        with pytest.raises(err.DataPackerProgramError):
            field.run(None, None)

    def test_r(self):
        r = self.field.r()

        # 只改变字段的类型,不改变属性
        assert isinstance(r, RequiredField)
        assert r.src_name == self.field.src_name
        assert r.dst_name == self.field.dst_name
        assert r._overwrite == self.field._overwrite
        assert r._checker_list == self.field._checker_list
        assert r._converter_list == self.field._converter_list


        # 改变字段的类型,且改变字段的属性
        r = self.field.r(src_name='xyz', dst_name='zyx',
                         overwrite=constant.OverwriteMode.RAISE, checker=None, converter=None)
        assert isinstance(r, RequiredField)
        assert r.src_name == 'xyz' and r.src_name != self.field.src_name
        assert r.dst_name == 'zyx' and r.src_name != self.field.dst_name
        assert r._overwrite == constant.OverwriteMode.RAISE and r._overwrite != self.field._overwrite
        assert r._checker_list == None and r._checker_list != self.field._checker_list
        assert r._converter_list == None and r._converter_list != self.field._converter_list

    def test_o(self):
        o = self.field.o()

        # 只改变字段的类型,不改变属性
        assert isinstance(o, OptionalField)
        assert o.src_name == self.field.src_name
        assert o.dst_name == self.field.dst_name
        assert o._overwrite == self.field._overwrite
        assert o._checker_list == self.field._checker_list
        assert o._converter_list == self.field._converter_list

        # 改变字段的类型,且改变字段的属性
        o = self.field.o(src_name='xyz', dst_name='zyx',
                         overwrite=constant.OverwriteMode.RAISE, checker=None, converter=None)
        assert isinstance(o, OptionalField)
        assert o.src_name == 'xyz' and o.src_name != self.field.src_name
        assert o.dst_name == 'zyx' and o.src_name != self.field.dst_name
        assert o._overwrite == constant.OverwriteMode.RAISE and o._overwrite != self.field._overwrite
        assert o._checker_list == None and o._checker_list != self.field._checker_list
        assert o._converter_list == None and o._converter_list != self.field._converter_list

    def test_d(self):
        import uuid
        default_value = uuid.uuid4().hex

        # 只改变字段的类型,不改变属性
        d = self.field.d(default_value)
        assert isinstance(d, DefaultField)
        assert d.src_name == self.field.src_name
        assert d.dst_name == self.field.dst_name
        assert d._overwrite == self.field._overwrite
        assert d._checker_list == self.field._checker_list
        assert d._converter_list == self.field._converter_list
        assert d.default_value == default_value


        # 改变字段的类型,且改变字段的属性
        d = self.field.d(default_value, src_name='xyz', dst_name='zyx',
                         overwrite=constant.OverwriteMode.RAISE, checker=None, converter=None)
        assert isinstance(d, DefaultField)
        assert d.default_value == default_value
        assert d.src_name == 'xyz' and d.src_name != self.field.src_name
        assert d.dst_name == 'zyx' and d.src_name != self.field.dst_name
        assert d._overwrite == constant.OverwriteMode.RAISE and d._overwrite != self.field._overwrite
        assert d._checker_list == None and d._checker_list != self.field._checker_list
        assert d._converter_list == None and d._converter_list != self.field._converter_list
