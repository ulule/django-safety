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

from . import managers


@python_2_unicode_compatible
class PasswordChange(models.Model):
    user = models.OneToOneField(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        verbose_name=_('user'),
        related_name='safety_password_change')

    required = models.BooleanField(verbose_name=_('required'), db_index=True, default=False)
    last_change_date = models.DateTimeField(verbose_name=_('last change date'), null=True, blank=True)

    objects = managers.PasswordChangeManager()

    class Meta:
        verbose_name = _('password change')
        verbose_name_plural = _('password changes')

    def __str__(self):
        return '%s - %s' % (self.user, self.last_change_date)


@python_2_unicode_compatible
class Session(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), verbose_name=_('user'), null=True)
    session_key = models.CharField(verbose_name=_('session key'), max_length=40, unique=True)
    ip = models.GenericIPAddressField(verbose_name=_('IP'))
    user_agent = models.CharField(verbose_name=_('user agent'), max_length=200)
    location = models.CharField(verbose_name=_('location'), max_length=255)
    device = models.CharField(verbose_name=_('device'), max_length=200)
    expiration_date = models.DateTimeField(verbose_name=_('expiration date'), db_index=True)
    last_activity = models.DateTimeField(verbose_name=_('last activity'))
    active = models.BooleanField(default=True)

    objects = managers.SessionManager()

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')

    def __str__(self):
        return '%s (%s)' % (self.user, self.device)

    def delete_store_session(self):
        from .utils import get_session_store

        store = get_session_store()

        if store.exists(session_key=self.session_key):
            store.delete(session_key=self.session_key)


# -----------------------------------------------------------------------------
# Signal handlers
# -----------------------------------------------------------------------------

# Connected to user_logged_in
def create_session(sender, request, user, **kwargs):
    Session.objects.create_session(request, user)


# Connected to user_logged_out
def deactivate_session(sender, request, user, **kwargs):
    try:
        key = request.session.session_key
        instance = Session.objects.get(user=user, session_key=key)
        instance.active = False
        instance.save()
    except Session.DoesNotExist:
        pass


# Connected to post_delete for Session model
def post_delete_session(sender, instance, **kwargs):
    instance.delete_store_session()


user_logged_in.connect(create_session)
user_logged_out.connect(deactivate_session)
post_delete.connect(post_delete_session, sender=Session)
