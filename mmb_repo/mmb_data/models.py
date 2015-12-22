from django.db import models
from django.template.defaultfilters import slugify
from config.settings.common import AUTH_USER_MODEL

# from mmb_repo.users.models import User
from .app_settings import SONG_TAGS


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


# class Band(models.Model):
#     name = models.CharField(blank=True, max_length=255)
#     desc = models.CharField(blank=True, max_length=255)
#     users = models.ManyToManyField(User)
#     band_genre = models.ForeignKey(Genre)
#     #tags - can't remember
#
#
class UserFollowers(models.Model):
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='follower')
    # follower_is_user = models.BooleanField()
    following = models.ForeignKey(AUTH_USER_MODEL, related_name='following')
    # following_is_user = models.BooleanField()
    def __unicode__(self):
        return '{} - {}'.format(self.follower.username, self.following.name)


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
        return '{} - {}'.format(self.user.username, self.song.name)
