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


def get_resolver(request, setting):
    module_path = getattr(app_settings, setting)

    try:
        module, attribute = module_path.rsplit('.', 1)
        resolver_module = import_module(module)
        resolver = getattr(resolver_module, attribute)

    except ImportError:
        raise ImproperlyConfigured(
            "Please specify a valid %s module. "
            "Could not find %s " % (setting, module))

    except AttributeError:
        raise ImproperlyConfigured(
            "Please specify a valid %s "
            "function. Could not find %s function in module %s" %
            (setting, attribute, module))

    return resolver(request)
