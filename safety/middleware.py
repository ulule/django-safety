# -*- coding: utf-8 -*-
from .decorators import password_change_required


class PasswordChangeMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        return password_change_required(view_func)(request, *view_args, **view_kwargs)
