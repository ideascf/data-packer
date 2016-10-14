# coding=utf-8
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import io
import sys

import data_packer


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

long_description = read('README.rst')
packages = [
    'data_packer',
    'data_packer.checker',
    'data_packer.container',
    'data_packer.converter',
    'data_packer.field',
    'data_packer.util',
]

setup(
    name='data-packer',
    version=data_packer.__version__,
    url='https://github.com/ideascf/data-packer',
    license='MIT',
    author=data_packer.__author__,
    tests_require=['pytest'],
    install_requires=[

    ],
    cmdclass={
        'test': PyTest
    },
    author_email='ideascf@163.com',
    description='A python library for check and convert src data container then set it into dst data container.',
    long_description=long_description,
    packages=packages,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    extras_require={
        'testing': ['pytest']
    },
)