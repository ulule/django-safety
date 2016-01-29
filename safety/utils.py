# -*- coding: utf-8 -*-
from django.conf import settings

from .compat import import_module


def get_session_store():
    mod = getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db')
    engine = import_module(mod)
    store = engine.SessionStore()
    return store


def resolve(module_path, request):
    try:
        module, attribute = module_path.rsplit('.', 1)
        resolver_module = import_module(module)
        resolver = getattr(resolver_module, attribute)
    except Exception as e:
        raise e
    return resolver(request)
