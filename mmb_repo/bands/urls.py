# __author__ = 'delhivery'
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(regex=r'^create/$', view=create_band, name='create_band'),
]
