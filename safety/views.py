# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # pragma: no cover
    # Python 2 fallback
    from urlparse import urlparse, urlunparse  # noqa

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, QueryDict
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


def redirect_to_password_reset(next_url):
    """
    Redirects the user to the password reset page,
    passing the given 'next' page.
    """
    url_parts = list(urlparse(reverse(app_settings.PASSWORD_RESET_URL_NAME)))
    querystring = QueryDict(url_parts[4], mutable=True)
    querystring[app_settings.REDIRECT_FIELD_NAME] = next_url
    url_parts[4] = querystring.urlencode(safe='/')
    return HttpResponseRedirect(urlunparse(url_parts))
