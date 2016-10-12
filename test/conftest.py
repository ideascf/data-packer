# coding=utf-8
import logging
import sys
import time

import os


def pytest_configure(*args):
    _setup_syspath()
    _install_log()


def _setup_syspath():
    p = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(p))
    sys.path.append(root)


def _install_log():
    log = logging.getLogger()
    hdlr = logging.FileHandler('./test.log')
    log.addHandler(hdlr)
    log.setLevel('DEBUG')

