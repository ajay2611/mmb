# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models

from mmb_repo.mmb_data.models import Genre, Instrument
from .app_settings import CITIES, PHONE_REG


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Profile(models.Model):
    user = models.ForeignKey(User)
    genre = models.ManyToManyField(Genre)
    instrument = models.ManyToManyField(Instrument)
    # todo - need list of all colleges if possible
    college = models.CharField(max_length=100, blank=True, null=True)
    current_city = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    following_count = models.IntegerField(default=0)
    followed_by_count = models.IntegerField(default=0)
    about_me = models.CharField(max_length=255, blank=True, null=True)
    other_link = models.CharField(max_length=255, blank=True, null=True)    #This is the link which user updates

    def __unicode__(self):
        return unicode(self.user)

    def update(self,*args,**kwargs):
        self.college = kwargs.get('college')
        self.current_city = kwargs.get('current_city')
        self.phone = kwargs.get('phone')
        self.website = kwargs.get('website')
        self.about_me = kwargs.get('about_me')
        self.save()
