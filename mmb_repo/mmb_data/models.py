from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from config.settings.common import AUTH_USER_MODEL
from .app_settings import SONG_TAGS, CITIES, YEAR_CHOICES, MEMBER_TYPE


def get_upload_file_name(instance, filename):
    return 'audio/{0}_{1}/{2}'.format(slugify(instance.user_id), instance.user.username, filename)


class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __unicode__(self):
        return '{}'.format(self.genre)


class Instrument(models.Model):
    instrument = models.CharField(max_length=30)
    # level = models.CharField(choices=SKILL_LEVEL, default='Beginner')

    def __unicode__(self):
        return '{}'.format(self.instrument)


class Band(models.Model):
    name = models.CharField(unique=True, max_length=255)
    genre = models.ManyToManyField(Genre)
    vacancy = models.ManyToManyField(Instrument)
    location = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.now().year)
    about_me = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class BandMember(models.Model):
    band = models.ForeignKey(Band)
    member = models.ManyToManyField(AUTH_USER_MODEL)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=4, choices=MEMBER_TYPE, default='temp')

    def __unicode__(self):
        return '{} - {}'.format(self.band, self.instrument)


# class Followers(models.Model):
#     follower = models.ForeignKey(User)
#     follower_is_user = models.BooleanField()
#     following = models.ForeignKey(User)
#     following_is_user = models.BooleanField()


class Song(models.Model):
    # type = models.CharField(choices=SONG_TYPES, default='Audio')
    user = models.ForeignKey(AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    tags = models.CharField(choices=SONG_TAGS, max_length=255)
    likes = models.IntegerField(default=0)
    upload = models.FileField(upload_to=get_upload_file_name)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    # singer = models.CharField(blank=True, max_length=255)
    # label = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return '{}'.format(self.name)


class SongLike(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    song = models.ForeignKey(Song)

    def __unicode__(self):
        return '{} - {}'.format(self.user, self.song.name)