# -*- coding: utf-8 -*-
import importlib
import re
import warnings

from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext


BROWSERS = (
    (re.compile('Chrome'), _('Chrome')),
    (re.compile('Safari'), _('Safari')),
    (re.compile('Firefox'), _('Firefox')),
    (re.compile('Opera'), _('Opera')),
    (re.compile('IE'), _('Internet Explorer')),
)

DEVICES = (
    (re.compile('Android'), _('Android')),
    (re.compile('Linux'), _('Linux')),
    (re.compile('iPhone'), _('iPhone')),
    (re.compile('iPad'), _('iPad')),
    (re.compile('(Mac OS X)'), _('OS X')),
    (re.compile('NT 5.1'), _('Windows XP')),
    (re.compile('NT 6.0'), _('Windows Vista')),
    (re.compile('NT 6.1'), _('Windows 7')),
    (re.compile('NT 6.2'), _('Windows 8')),
    (re.compile('NT 6.3'), _('Windows 8.1')),
    (re.compile('Windows'), _('Windows')),
)


def get_device(user_agent):
    """
    Transform a User Agent into a human readable text.
    """
    infos = []

    for regex, name in BROWSERS:
        if regex.search(user_agent):
            infos.append('%s' % name)
            break

    for regex, name in DEVICES:
        if regex.search(user_agent):
            infos.append('%s' % name)
            break

    return ', '.join(infos)


def get_session_store():
    mod = getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db')
    engine = importlib.import_module(mod)
    store = engine.SessionStore()
    return store
