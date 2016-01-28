#!/usr/bin/env python
import os
import sys

SUPPORTED_ENVS = (
    'test',
    'example',
)

SETTINGS_MODULES = {
    'test': 'safety.tests.settings',
    'example': 'example.settings'
}

ENV = os.environ.get('ENV', 'test')
ENV = ENV.lower()

if ENV not in SUPPORTED_ENVS:
    raise Exception('Unsupported environment: %s' % ENV)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULES[ENV])
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
