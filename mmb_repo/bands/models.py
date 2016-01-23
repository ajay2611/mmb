from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from mmb_repo.mmb_data.models import Genre, Instrument
from config.settings.common import AUTH_USER_MODEL
from .app_settings import CITIES, YEAR_CHOICES, MEMBER_TYPE, SONG_TAGS


def get_upload_file_name(instance, filename):
    return 'audio/{0}_{1}/{2}'.format(slugify(instance.user_id), instance.user.username, filename)


class Band(models.Model):
    name = models.CharField(unique=True, max_length=255)
    genre = models.ManyToManyField(Genre)
    member = models.ManyToManyField(AUTH_USER_MODEL, through='BandMember')
    # vacancy = models.ManyToManyField(Instrument)
    location = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    follower_count = models.IntegerField(default=0)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.now().year)
    desc = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='band_admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class BandMember(models.Model):
    band = models.ForeignKey(Band)
    member = models.ForeignKey(AUTH_USER_MODEL)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')

    def __unicode__(self):
        return '{} - {}'.format(self.band, self.member)


class BandVacancy(models.Model):
    band = models.ForeignKey(Band)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')

    class Meta:
        verbose_name_plural = 'Band vacancies'

    def __unicode__(self):
        return '{} - {}'.format(self.band, self.instrument)


class BandFollowers(models.Model):
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='band_follower')
    following_band = models.ForeignKey(Band, related_name='band_following')

    def __unicode__(self):
        return '{} - {}'.format(self.follower.username, self.following.name)


# class BandSong(models.Model):
#     # type = models.CharField(choices=SONG_TYPES, default='Audio')
#     band = models.ForeignKey(Band)
#     user = models.ForeignKey(AUTH_USER_MODEL)
#     name = models.CharField(max_length=255)
#     tags = models.CharField(choices=SONG_TAGS, max_length=255)
#     likes = models.IntegerField(default=0)
#     upload = models.FileField(upload_to=get_upload_file_name)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     # singer = models.CharField(blank=True, max_length=255)
#     # label = models.CharField(blank=True, max_length=255)
#
#     def __unicode__(self):
#         return '{}'.format(self.name)
#
#
# class BandSongLike(models.Model):
#     band = models.ForeignKey(Band)
#     song = models.ForeignKey(BandSong)
#
#     def __unicode__(self):
#         return '{} - {}'.format(self.band.name, self.song.name)
