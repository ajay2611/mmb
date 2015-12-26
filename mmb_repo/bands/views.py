from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from mmb_repo.mmb_data.models import Genre, Instrument, Song
from .models import Band, BandMember
from .forms import BandForm, BandMemberForm


def create_band(request):
    template = 'bands/create_band.html'
    pk = request.user.pk
    if request.method == 'POST':
        import ipdb;ipdb.set_trace()
        band_form = BandForm(request.POST)
        if band_form.is_valid():
            band_obj = Band.objects.create(name=band_form.cleaned_data['name'],
                                           location=band_form.cleaned_data['location'],
                                           label=band_form.cleaned_data['label'],
                                           year=band_form.cleaned_data['year'],
                                           about_me=band_form.cleaned_data['about_me'],
                                           created_by=request.user
                                           )

            for genre in band_form.cleaned_data['genre']:
                genre_obj = Genre.objects.get(genre=genre)
                band_obj.genre.add(genre_obj)

    else:
        band_form = BandForm()

    return render_to_response(template, {'form': band_form}, context_instance=RequestContext(request))
