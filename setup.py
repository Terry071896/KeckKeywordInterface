# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.

import sys
import os
import glob

from setuptools import setup

# Get some values from the setup.cfg
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

conf = ConfigParser()
conf.read(['setup.cfg'])
#metadata = dict(conf.items('metadata'))

NAME = 'KeckKeywordInterface'
VERSION = '1.0'
RELEASE = 'dev' not in VERSION

scripts = [fname for fname in glob.glob(os.path.join('scripts', '*'))
           if os.path.basename(fname) != 'README.md']
scripts = []
# Define entry points for command-line scripts
entry_points = {
    'console_scripts': []}


setup(name=NAME,
      provides=NAME,
      version=VERSION,
      license='BSD3',
      description='Keck Keyword Interface',
      long_description=open('README.md').read(),
      author='Terry Cox',
      author_email='tfcox1703@gmail.com',
      packages=['KeckKeywordInterface',],
      scripts=scripts,
      )




