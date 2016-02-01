# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now

from .models import Session


class SessionMixin(object):
    def get_queryset(self):
        qs = Session.objects.filter(expiration_date__gt=now(), user=self.request.user)
        qs = qs.order_by('-last_activity')
        return qs


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
