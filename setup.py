#!/usr/bin/env python3
from setuptools import setup

setup(
    name='clipw',
    version='1.1',
    packages=['lib'],
    scripts=['bin/clipw_cli.py', 'bin/clipw'],
    url='https://github.com/darkerego/clipw',
    license='GPL Whatever Just Credit Me',
    author='darkerego',
    author_email='xelectron@protonmail.com',
    description='CLI Password Manager'
)
