# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # pragma: no cover
    # Python 2 fallback
    from urlparse import urlparse, urlunparse  # noqa

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, DeleteView, View
from django.views.generic.edit import DeletionMixin

from . import app_settings
from . import forms
from . import utils

from .mixins import SessionMixin


LoginRequiredMixin = utils.import_from_path(
    app_settings.LOGIN_REQUIRED_MIXIN_CLASS)


# -----------------------------------------------------------------------------
# Sessions
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Password Change
# -----------------------------------------------------------------------------

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request):
    return auth_views.password_change(
        request=request,
        template_name='safety/password_change/form.html',
        post_change_redirect=reverse('safety:password_change_done'),
        password_change_form=forms.PasswordChangeForm)


@login_required
def password_change_done(request):
    return auth_views.password_change_done(
        request=request,
        template_name='safety/password_change/done.html')
