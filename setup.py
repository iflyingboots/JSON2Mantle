# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='JSON2Mantle',
    version='0.0.1',
    description='Generate Mantle models using JSON files',
    long_description=readme,
    author='Xin Wang',
    author_email='i@wangx.in',
    url='https://github.com/sutar/JSON2Mantle',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

