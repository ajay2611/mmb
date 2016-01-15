from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.forms.formsets import formset_factory
from django.core.mail import send_mail

from config.settings.common import STATIC_URL
from mmb_repo.mmb_data.models import Genre, Instrument, Song
from .models import Band, BandMember, BandVacancy
from .forms import BandForm, BandMemberForm, BaseBandFormset, BandVacancyForm


def create_band(request):
    template = 'bands/create_band.html'
    pk = request.user.pk
    Memberformset = formset_factory(BandMemberForm, formset=BaseBandFormset)
    # members = Band.objects.get
    if request.method == 'POST':
        import ipdb;ipdb.set_trace()
        band_form = BandForm(request.POST)
        memberformset = Memberformset(request.POST)
        if band_form.is_valid() and memberformset.is_valid():
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
            # for mem in memberformset:
            #     mem_obj =
        return HttpResponse("Do something")

    else:
        band_form = BandForm()

    return render_to_response(template, {'form': band_form, 'memberformset': Memberformset, 'STATIC_URL': STATIC_URL}, context_instance=RequestContext(request))


def view_band(request, band_id):
    template = 'bands/band_profile.html'
    if request.method == 'GET':
        band = Band.objects.get(id=band_id)
        band_members = BandMember.objects.get(band=band_id)
    else:
        template = '404.html'

    return render_to_response(template,
                              {'band': band, 'band_members': band_members},
                              context_instance=RequestContext(request))


def create_vacancy(request, band_id):
    template = 'bands/create_vacancy.html'
    if request.method == 'GET':
        vacancy_form = BandVacancyForm()
        # band = Band.objects.get(id=band_id)
    else:
        vacancy_form = BandVacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy_obj = BandVacancy.objects.create(name=band_id,
                                                     instrument=vacancy_form.cleaned_data['instrument'],
                                                     type=vacancy_form.cleaned_data['type']
                                                     )
            vacancy_obj.save()

    return render_to_response(template,
                              {'form': vacancy_form},
                              context_instance=RequestContext(request)
                              )


def invite_user(request, band_id):
    send_mail('Subject here', 'Here is the message.', 'ajay.singh1@delhivery.com', ['ajayk40@gmail.com'])