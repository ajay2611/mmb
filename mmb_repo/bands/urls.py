# __author__ = 'delhivery'
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(regex=r'^create/$', view=create_band, name='create_band'),
    url(regex=r'^profile/(?P<band_id>[0-9]+)/$', view=view_band, name='view_band'),
    url(regex=r'^upload/song/(?P<band_id>[0-9]+)/$', view=band_upload_song, name='band_upload_song'),
    url(regex=r'^(?P<band_id>[0-9]+)/vacancy/$', view=create_vacancy, name='create_vacancy'),
    url(regex=r'^(?P<band_id>[0-9]+)/invite-user/$', view=invite_user, name='invite_user'),
    # url(regex=r'^profile/upload/songs/(?P<band_id>[\d])/$', view=band_upload_song, name='band_upload_song'),
]
