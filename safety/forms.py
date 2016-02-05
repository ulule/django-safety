# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import PasswordChange


class PasswordChangeForm(BasePasswordChangeForm):
    error_messages = dict(BasePasswordChangeForm.error_messages, **{
        'same_password': _("Your old password and the new one are the same. You must use a different password."),
    })

    def clean_new_password2(self):
        password2 = super(PasswordChangeForm, self).clean_new_password2()

        if self.user.check_password(password2):
            raise forms.ValidationError(
                self.error_messages['same_password'],
                code='same_password')

        return password2

    def save(self, *args, **kwargs):
        pc, created = PasswordChange.objects.get_or_create_for_user(self.user)
        pc.required = False
        pc.save()
        super(PasswordChangeForm, self).save(*args, **kwargs)
