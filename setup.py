#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from cx_Freeze import setup, Executable


BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = '1.0.{}'.format(os.environ.get('BUILD_NUMBER', 'dev'))

options = {
    'build_exe': {
        'packages': ['zen_launcher', 'tkinter'],
        'include_files': ['zen_launcher_resources',],
    },

    'bdist_mac': {
        'iconfile': os.path.join(
            BASE_DIR, 'zen_launcher_resources/icons/zen.icns'
        ),
    }
}

kwargs = {
    'base': None,
    'targetName': 'zen_launcher'
}

# Platform specific options
if sys.platform.startswith('win'):
    options['build_exe']['build_exe'] = 'build_win'
    kwargs['base'] = 'Win32GUI'
    kwargs['targetName'] += '.exe'


setup(name='Zen',
      version=VERSION,
      description='',
      options=options,
      executables=[Executable('main.py', **kwargs)])
