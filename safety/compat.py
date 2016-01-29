# -*- coding: utf-8 -*-
import django


if django.VERSION >= (1, 9):
    from importlib import import_module
    from django.contrib.gis.geoip2 import GeoIP2 as GeoIP
else:
    from django.utils.importlib import import_module
    from django.contrib.gis.geoip import GeoIP
