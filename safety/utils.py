# -*- coding: utf-8 -*-
try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


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

    except ImportError:
        raise ImproperlyConfigured(
            "Please specify a valid %s module. "
            "Could not find %s " % (module_path, module))

    except AttributeError:
        raise ImproperlyConfigured(
            "Please specify a valid %s "
            "function. Could not find %s function in module %s" %
            (module_path, attribute, module))

    return resolver(request)
