# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.timezone import now

from .models import (
    PasswordReset,
    Session,
)


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_reset', 'reset_required')
    raw_id_fields = ('user',)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'last_activity', 'location', 'device', 'is_valid')
    raw_id_fields = ('user',)

    def is_valid(self, obj):
        return obj.expiration_date > now()
    is_valid.boolean = True


admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(Session, SessionAdmin)
