# -*- coding: utf-8 -*-
from django.conf import settings


# The Python path to the login_required mixin class applied to views.
LOGIN_REQUIRED_MIXIN_CLASS = getattr(
    settings,
    'SAFETY_LOGIN_REQUIRED_MIXIN_CLASS',
    'safety.mixins.LoginRequiredMixin')


# Path to callable that handles the IP resolving.
# Takes a django.http.HttpRequest instance and returns a string.
IP_RESOLVER = getattr(
    settings,
    'SAFETY_IP_RESOLVER',
    'safety.resolvers.remote_addr_ip')


# Path to callable that handles the device resolving.
# Takes a django.http.HttpRequest instance and returns a string.
DEVICE_RESOLVER = getattr(
    settings,
    'SAFETY_DEVICE_RESOLVER',
    'safety.resolvers.device')


# Path to callable that handles the location resolving.
# Takes a django.http.HttpRequest instance and returns a string.
LOCATION_RESOLVER = getattr(
    settings,
    'SAFETY_LOCATION_RESOLVER',
    'safety.resolvers.location')


# The querystring argument to be used for redirection
REDIRECT_FIELD_NAME = getattr(
    settings,
    'SAFETY_REDIRECT_FIELD_NAME',
    'next')


# The URL name of password reset view.
PASSWORD_RESET_URL_NAME = getattr(
    settings,
    'SAFETY_PASSWORD_RESET_URL_NAME',
    'password_reset')
