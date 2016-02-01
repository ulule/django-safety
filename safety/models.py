# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)

from django.db.models.signals import post_delete
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import app_settings
from . import utils


class SessionManager(models.Manager):
    def create_session(self, request, user):
        ip = utils.resolve(app_settings.IP_RESOLVER, request)
        device = utils.resolve(app_settings.DEVICE_RESOLVER, request)
        location = utils.resolve(app_settings.LOCATION_RESOLVER, request)

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent = user_agent[:200] if user_agent else user_agent

        return self.create(
            user=user,
            session_key=request.session.session_key,
            ip=ip,
            user_agent=user_agent,
            device=device,
            location=location,
            expiration_date=request.session.get_expiry_date())


@python_2_unicode_compatible
class Session(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), verbose_name=_('user'), null=True)
    session_key = models.CharField(verbose_name=_('session key'), max_length=40)
    ip = models.GenericIPAddressField(verbose_name=_('IP'))
    user_agent = models.CharField(verbose_name=_('user agent'), max_length=200)
    location = models.CharField(verbose_name=_('location'), max_length=255)
    device = models.CharField(verbose_name=_('device'), max_length=200, blank=True, null=True)
    expiration_date = models.DateTimeField(verbose_name=_('expiration date'), db_index=True)
    last_activity = models.DateTimeField(verbose_name=_('last activity'), auto_now=True)

    objects = SessionManager()

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def __str__(self):
        return '%s (%s)' % (self.user, self.device)


# -----------------------------------------------------------------------------
# Signals
# -----------------------------------------------------------------------------

def user_logged_in_handler(sender, request, user, **kwargs):
    Session.objects.create_session(request, user)


def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        key = request.session.session_key
        instance = Session.objects.get(user=user, session_key=key)
        instance.delete()
    except Session.DoesNotExist:
        pass


def post_delete_session_handler(sender, instance, **kwargs):
    key = instance.session_key
    store = utils.get_session_store()
    if store.exists(session_key=key):
        store.delete(session_key=key)


user_logged_in.connect(user_logged_in_handler)
user_logged_out.connect(user_logged_out_handler)
post_delete.connect(post_delete_session_handler, sender=Session)
