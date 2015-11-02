from django.contrib import admin

from .models import Genre, Instrument, Songs
 #Band, Followers


admin.site.register(Genre)
admin.site.register(Instrument)
admin.site.register(Songs)
# admin.site.register(Band)
# admin.site.register(Followers)
