# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Yasp',
    version='0.0.1',
    description='YASP data collection tools',
    long_description=readme,
    author='Pablo Virgo',
    author_email='mailbox@pablovirgo.com',
    url='https://github.com/ptvirgo/yasp',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
