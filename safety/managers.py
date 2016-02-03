# -*- coding: utf-8 -*-
from django.db import models, transaction, IntegrityError
from django.utils.timezone import now

from . import app_settings
from . import utils


class PasswordResetManager(models.Manager):
    def get_or_create_for_user(self, user):
        return self.get_or_create(
            user=user,
            defaults={'last_password': user.password})

    def is_required_for_user(self, user):
        obj, created = self.get_or_create_for_user(user=user)
        return obj.required

    def check_password(self, user):
        obj, created = self.get_or_create_for_user(user=user)
        if obj.last_password != user.password:
            obj.last_password = user.password
            obj.last_reset_date = now()
            obj.required = False
            obj.save()


class SessionManager(models.Manager):
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
                    expiration_date=request.session.get_expiry_date())
        except IntegrityError:
            obj = self.get(
                user=user,
                session_key=request.session.session_key)

        return obj
