# -*- coding: utf-8 -*-
from functools import wraps

from .models import PasswordReset
from .views import redirect_to_password_reset


def password_reset_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            obj = PasswordReset.objects.get_for_user(user=request.user)
            if obj.reset_required:
                return redirect_to_password_reset(request.get_full_path())
        return func(request, *args, **kwargs)
    return inner
