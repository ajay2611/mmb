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
]

