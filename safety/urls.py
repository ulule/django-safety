# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    SessionListView,
    SessionDeleteView,
    SessionDeleteOtherView
)


urlpatterns = [
    url(
        regex=r'^sessions/$',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    url(
        regex=r'^sessions/other/delete/$',
        view=SessionDeleteOtherView.as_view(),
        name='session_delete_other',
    ),
    url(
        regex=r'^sessions/(?P<pk>\w+)/delete/$',
        view=SessionDeleteView.as_view(),
        name='session_delete',
    ),
]
