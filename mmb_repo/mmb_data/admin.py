from django.contrib import admin

from .models import Genre, Instrument, Song

admin.site.register(Genre)
admin.site.register(Instrument)
admin.site.register(Song)
# admin.site.register(Followers)
