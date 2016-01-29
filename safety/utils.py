# -*- coding: utf-8 -*-
from django.conf import settings

from .compat import import_module


def get_session_store():
    mod = getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db')
    engine = import_module(mod)
    store = engine.SessionStore()
    return store


def resolve(path, request):
    obj = import_from_path(path)
    return obj(request)


def import_from_path(path):
    try:
        module_path, attr = path.rsplit('.', 1)
        module = import_module(module_path)
        obj = getattr(module, attr)
    except Exception as e:
        raise e
    return obj
