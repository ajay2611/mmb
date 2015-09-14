# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.translation import ugettext_lazy as _

from mmb_repo.mmb_data.models import Genre, Instrument
from mmb_repo.mmb_data.utils import get_image_path


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Profile(models.Model):
    user = models.ForeignKey(User)
    genre = models.ForeignKey(Genre)
    instrument = models.ForeignKey(Instrument)
    # todo - need list of all colleges if possible
    college = models.CharField(blank=True, max_length=100, null=True)
    # todo - update with indian cities using inbuilt django package
    current_city = models.CharField(blank=True, max_length=255, null=True)
    phone = models.IntegerField(blank=True, null=True)
    website = models.CharField(blank=True, max_length=100, null=True)
    about_me = models.CharField(blank=True, max_length=255, null=True)
    profile_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)