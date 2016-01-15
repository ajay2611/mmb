from django.contrib import admin

from .models import Band, BandMember, BandVacancy

admin.site.register(Band)
admin.site.register(BandMember)
admin.site.register(BandVacancy)
