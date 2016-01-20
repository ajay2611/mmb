from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _

from mmb_repo.mmb_data.models import Genre, Instrument
from config.settings.common import AUTH_USER_MODEL
from .app_settings import CITIES, YEAR_CHOICES, MEMBER_TYPE


class Band(models.Model):
    name = models.CharField(unique=True, max_length=255)
    genre = models.ManyToManyField(Genre)
    member = models.ManyToManyField(AUTH_USER_MODEL, through='BandMember')
    # vacancy = models.ManyToManyField(Instrument)
    location = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
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
    type = models.CharField(max_length=4, choices=MEMBER_TYPE, default='perm')

    def __unicode__(self):
        return '{} - {}'.format(self.band, self.member)


class BandVacancy(models.Model):
    band = models.ForeignKey(Band)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=4, choices=MEMBER_TYPE, default='perm')

    class Meta:
        verbose_name_plural = 'Band vacancies'

    def __unicode__(self):
        return '{} - {}'.format(self.band, self.instrument)