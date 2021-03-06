#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2021, Kovid Goyal <kovid at kovidgoyal.net>

import importlib
import os
from pprint import pprint

QT_WRAPPER = 'PyQt5'

base = os.path.dirname(os.path.abspath(__file__))
module_lists = {
    'core': (
        'QtCore',
        'QtGui',
        'QtWidgets',
        'QtNetwork',
        'QtSvg',
        'QtPrintSupport',
    ),
    'webengine': (
        'QtWebEngine',
        'QtWebEngineCore',
        'QtWebEngineWidgets',
    ),
}


def scan(name):
    module_names = module_lists[name]
    name_map = {}
    types = []
    for mod_name in module_names:
        mod = importlib.import_module(f'{QT_WRAPPER}.{mod_name}')
        full_name = name_map[mod_name] = mod.__name__
        types.append(f'import {full_name}')
        for obj_name in sorted(dir(mod)):
            if not obj_name.startswith('_') and obj_name not in name_map:
                name_map[obj_name] = full_name
                types.append(f'{obj_name} = {full_name}.{obj_name}')
    with open(f'{base}/{name}.pyi', 'w') as f:
        print('# autogenerated by __main__.py do not edit', file=f)
        f.write('\n'.join(types))
    if name == 'core':
        module_names += ('sip',)
        mod = importlib.import_module(f'{QT_WRAPPER}.sip')
        name_map['sip'] = mod.__name__
        name_map['QtWin'] = f'{QT_WRAPPER}.QtWinExtras'
    with open(f'{base}/{name}_name_map.py', 'w') as f:
        print('# autogenerated by __main__.py do not edit', file=f)
        print('name_map =', end=' ', file=f)
        pprint(name_map, stream=f)
        print('module_names = frozenset(', end='', file=f)
        pprint(module_names, stream=f)
        print(')', file=f)


for name in ('core', 'webengine'):
    scan(name)
