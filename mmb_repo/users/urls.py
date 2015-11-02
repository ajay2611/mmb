# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(regex=r'^edit-profile/$', view=views.edit_profile, name='edit_profile'),
    url(regex=r'^profile/(?P<username>[\w.@+-]+)/$', view=views.view_profile, name='view_profile'),
    url(regex=r'^profile/upload/songs/(?P<username>[\w.@+-]+)/$', view=views.upload_song, name='upload_song'),
    url(regex=r'^change-password/$', view=views.change_password, name='change_password'),

    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
]