# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from safety.decorators import password_reset_required


def home(request):
    return redirect(reverse('safety:session_list'))


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^security/', include('safety.urls', namespace='safety')),
    url(r'^$', password_reset_required(home)),
]
