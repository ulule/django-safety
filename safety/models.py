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

from . import utils
from . import managers


@python_2_unicode_compatible
class PasswordReset(models.Model):
    user = models.OneToOneField(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        verbose_name=_('user'),
        related_name='safety_password_reset')

    required = models.BooleanField(verbose_name=_('required'), db_index=True, default=False)
    last_password = models.CharField(verbose_name=_('last password'), max_length=255)
    last_reset_date = models.DateTimeField(verbose_name=_('last reset date'), null=True, blank=True)

    objects = managers.PasswordResetManager()

    class Meta:
        verbose_name = _('password reset')
        verbose_name_plural = _('password resets')

    def __str__(self):
        return '%s - %s' % (self.user, self.last_reset)


@python_2_unicode_compatible
class Session(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), verbose_name=_('user'), null=True)
    session_key = models.CharField(verbose_name=_('session key'), max_length=40, unique=True)
    ip = models.GenericIPAddressField(verbose_name=_('IP'))
    user_agent = models.CharField(verbose_name=_('user agent'), max_length=200)
    location = models.CharField(verbose_name=_('location'), max_length=255)
    device = models.CharField(verbose_name=_('device'), max_length=200)
    expiration_date = models.DateTimeField(verbose_name=_('expiration date'), db_index=True)
    last_activity = models.DateTimeField(verbose_name=_('last activity'), auto_now=True)

    objects = managers.SessionManager()

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def __str__(self):
        return '%s (%s)' % (self.user, self.device)


# -----------------------------------------------------------------------------
# Signal handlers
# -----------------------------------------------------------------------------

# Connected to user_logged_in
def create_session(sender, request, user, **kwargs):
    Session.objects.create_session(request, user)


# Connected to user_logged_in
def check_password(sender, request, user, **kwargs):
    PasswordReset.objects.check_password(user=user)


# Connected to user_logged_out
def delete_session(sender, request, user, **kwargs):
    try:
        key = request.session.session_key
        instance = Session.objects.get(user=user, session_key=key)
        instance.delete()
    except Session.DoesNotExist:
        pass


# Connected to post_delete for Session model
def post_delete_session(sender, instance, **kwargs):
    key = instance.session_key
    store = utils.get_session_store()
    if store.exists(session_key=key):
        store.delete(session_key=key)


user_logged_in.connect(create_session)
user_logged_in.connect(check_password)
user_logged_out.connect(delete_session)
post_delete.connect(post_delete_session, sender=Session)
