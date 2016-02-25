# -*- coding: utf-8 -*-
from django.db import models, transaction, IntegrityError
from django.utils.timezone import now

from . import app_settings
from . import utils


class PasswordChangeManager(models.Manager):
    def get_or_create_for_user(self, user):
        return self.get_or_create(user=user)

    def is_required_for_user(self, user):
        obj, created = self.get_or_create_for_user(user=user)
        return obj.required


class SessionManager(models.Manager):
    def active(self, user=None):
        qs = self.filter(expiration_date__gt=now())
        if user is not None:
            qs = qs.filter(user=user)
        return qs.order_by('-last_activity')

    def create_session(self, request, user):
        ip = utils.resolve(app_settings.IP_RESOLVER, request)
        device = utils.resolve(app_settings.DEVICE_RESOLVER, request)
        location = utils.resolve(app_settings.LOCATION_RESOLVER, request)

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent = user_agent[:200] if user_agent else user_agent

        try:
            with transaction.atomic():
                obj = self.create(
                    user=user,
                    session_key=request.session.session_key,
                    ip=ip,
                    user_agent=user_agent,
                    device=device,
                    location=location,
                    expiration_date=request.session.get_expiry_date(),
                    last_activity=now())
        except IntegrityError:
            obj = self.get(
                user=user,
                session_key=request.session.session_key)
            obj.last_activity = now()
            obj.save()

        return obj
