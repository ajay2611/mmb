from django.contrib import admin

from .models import Genre, Instrument, Song, SongLike, Band, BandMember

admin.site.register(Genre)
admin.site.register(Instrument)
admin.site.register(Song)
admin.site.register(SongLike)
admin.site.register(Band)
admin.site.register(BandMember)
# admin.site.register(Followers)
