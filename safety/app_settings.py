# -*- coding: utf-8 -*-
from django.conf import settings


IP_RESOLVER = getattr(
    settings,
    'SAFETY_IP_RESOLVER',
    'safety.resolvers.remote_addr_ip')


DEVICE_RESOLVER = getattr(
    settings,
    'SAFETY_DEVICE_RESOLVER',
    'safety.resolvers.device')
