# coding=utf-8
import pytest

from data_packer import checker

def verify(ck, value):
    ck.verify('', '', value)


class TestTypeChecker:
    def test_multi_type(self):
        ck = checker.TypeChecker((str, unicode))

        verify(ck, '1')

