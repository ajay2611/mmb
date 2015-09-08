# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __unicode__(self):
        return '{}'.format(self.genre)


class Instrument(models.Model):
    instrument = models.CharField(max_length=30)

    def __unicode__(self):
        return '{}'.format(self.instrument)


class Profile(models.Model):
    genre = models.ForeignKey(Genre)
    instrument = models.ForeignKey(Instrument)
    # todo - need list of all colleges if possible
    school = models.CharField(blank=True, max_length=100, null=True)
    # todo - update with indian cities using inbuilt django package
    current_city = models.CharField(blank=True, max_length=255, null=True)
    phone = models.IntegerField(blank=True, null=True)
    website = models.CharField(blank=True, max_length=100, null=True)
    about_me = models.CharField(blank=True, max_length=255, null=True)

