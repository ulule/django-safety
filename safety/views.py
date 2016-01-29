# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DeleteView, View
from django.views.generic.edit import DeletionMixin

from . import app_settings
from . import utils

from .mixins import SessionMixin


LoginRequiredMixin = utils.import_from_path(
    app_settings.LOGIN_REQUIRED_MIXIN_CLASS)


class SessionListView(LoginRequiredMixin, SessionMixin, ListView):
    pass


class SessionDeleteView(LoginRequiredMixin, SessionMixin, DeleteView):
    def get_success_url(self):
        return str(reverse_lazy('safety:session_list'))


class SessionDeleteOtherView(LoginRequiredMixin, SessionMixin, DeletionMixin, View):
    def get_object(self):
        qs = super(SessionDeleteOtherView, self).get_queryset()
        qs = qs.exclude(session_key=self.request.session.session_key)
        return qs

    def get_success_url(self):
        return str(reverse_lazy('safety:session_list'))
