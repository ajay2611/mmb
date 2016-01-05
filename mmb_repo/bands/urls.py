# __author__ = 'delhivery'
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(regex=r'^create/$', view=create_band, name='create_band'),
    url(regex=r'^profile/(?P<band_id>[\d])/$', view=view_band, name='view_band'),
]
