# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^sessions/$',
        views.SessionListView.as_view(),
        name='session_list'),

    url(
        r'^sessions/other/delete/$',
        views.SessionDeleteOtherView.as_view(),
        name='session_delete_other'),

    url(
        r'^sessions/(?P<pk>\w+)/delete/$',
        views.SessionDeleteView.as_view(),
        name='session_delete'),

    url(
        r'^password-change/$',
        views.password_change,
        name='password_change'),

    url(
        r'^password-change/done/$',
        views.password_change_done,
        name='password_change_done'),
]
