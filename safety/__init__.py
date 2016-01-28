# -*- coding: utf-8 -*-
version = (0, 1, 0)

__version__ = '.'.join(map(str, version))

default_app_config = 'safety.apps.SafetyConfig'

__all__ = [
    'default_app_config',
    'version',
]
