# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Yasp',
    version='1.0.0',
    description='YASP data collection tools',
    long_description=readme,
    author='Pablo Virgo',
    author_email='mailbox@pablovirgo.com',
    url='https://github.com/ptvirgo/yasp',
    license=license,
    packages=['census', 'pdp_scraper', 'webapp']
)
