from django.db import models

from mmb_repo.users.models import User


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
    name = models.CharField(blank=True, max_length=255)
    desc = models.CharField(blank=True, max_length=255)
    users = models.ManyToManyField(User)
    band_genre = models.ForeignKey(Genre)
    #tags - can't remember


class Followers(models.Model):
    follower = models.ForeignKey(User)
    follower_is_user = models.BooleanField()
    following = models.ForeignKey(User)
    following_is_user = models.BooleanField()

class Songs(models.Model):
    # type = models.CharField(choices=SONG_TYPES, default='Audio')
    # tags = models.CharField(choices=SONG_TAGS)
    uploaded_by = models.CharField(max_length=255)
    singer = models.CharField(blank=True, max_length=255)
    lebel = models.CharField(blank=True, max_length=255)