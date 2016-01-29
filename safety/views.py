# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView, View
from django.views.generic.edit import DeletionMixin

from . import app_settings
from . import utils
from .models import Session


# Mixins
# -----------------------------------------------------------------------------
class SessionMixin(object):
    def get_queryset(self):
        return (Session.objects.filter(expire_date__gt=now())
                               .order_by('-last_activity'))


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


# Views
# -----------------------------------------------------------------------------
class SessionListView(SessionMixin, ListView):
    pass


class SessionDeleteView(SessionMixin, DeleteView):
    def get_success_url(self):
        return str(reverse_lazy('safety:session_list'))


class SessionDeleteOtherView(SessionMixin, DeletionMixin, View):
    def get_object(self):
        qs = super(SessionDeleteOtherView, self).get_queryset()
        qs = qs.exclude(session_key=self.request.session.session_key)
        return qs

    def get_success_url(self):
        return str(reverse_lazy('safety:session_list'))


def wrap_views():
    login_required_class = utils.import_from_path(
        app_settings.LOGIN_REQUIRED_MIXIN_CLASS)

    views = (
        SessionListView,
        SessionDeleteView,
        SessionDeleteOtherView,
    )

    for view in views:
        view.__bases__ = (login_required_class,) + view.__bases__

wrap_views()
