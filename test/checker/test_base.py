# coding=utf-8
import pytest

from data_packer import checker
from _common import verify


class TestTypeChecker:
    def test_multi_type(self):
        ck = checker.TypeChecker((str, unicode))

        verify(ck, '1')

