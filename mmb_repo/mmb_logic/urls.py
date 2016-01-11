# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import *

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^api/get-user-category/$',
        view=category_search,
        name='category_search'
    ),
    url(
        regex=r'^api/get_location/$',
        view=get_location,
        name='get_location'
    ),
    url(
        regex=r'^api/inc-likes/$',
        view=inc_likes,
        name='inc_likes'
    ),
    url(
        regex=r'^api/change-profile/$',
        view=change_profile,
        name='change_profile'
    ),
]
