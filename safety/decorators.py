# -*- coding: utf-8 -*-
from functools import wraps

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import (
    PasswordChange,
    Session,
)


def password_change_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return func(request, *args, **kwargs)

        required = PasswordChange.objects.is_required_for_user(request.user)
        url = reverse('safety:password_change')
        is_excluded_url = request.path.startswith(url)

        if required and not is_excluded_url:
            return redirect(url)

        return func(request, *args, **kwargs)
    return inner
