# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.http import JsonResponse

from safety.decorators import password_reset_required


def home(request):
    return JsonResponse({'message': 'Hello'})


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^security/', include('safety.urls', namespace='safety')),
    url(r'^$', password_reset_required(home), name='home'),
]
