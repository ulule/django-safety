# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from safety.models import PasswordChange


def home(request):
    return render(request, 'home.html')


def update_password(request):
    if request.user.is_authenticated():
        pr, created = PasswordChange.objects.get_or_create_for_user(request.user)
        pr.required = True
        pr.save()
    return redirect(reverse('home'))


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^security/', include('safety.urls', namespace='safety')),
    url(r'^update-password/$', update_password, name='update-password'),
    url(r'^$', home, name='home'),
]
