from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.forms.formsets import formset_factory

from allauth.socialaccount.models import SocialAccount
from config.settings.common import STATIC_URL
from mmb_repo.mmb_data.models import Genre, Instrument, Song
from .models import Band, BandMember, BandVacancy
from .forms import BandForm, BandMemberForm, BaseBandFormset, BandVacancyForm
from .utils import send_multiple_mail


def create_band(request):
    template = 'bands/create_band.html'
    pk = request.user.pk
    Memberformset = formset_factory(BandMemberForm, formset=BaseBandFormset)
    if request.method == 'POST':
        band_form = BandForm(request.POST)
        memberformset = Memberformset(request.POST)
        if band_form.is_valid() and memberformset.is_valid():
            band_name = band_form.cleaned_data['name']
            band_obj = Band.objects.create(name=band_name,
                                           location=band_form.cleaned_data['location'],
                                           label=band_form.cleaned_data['label'],
                                           year=band_form.cleaned_data['year'],
                                           desc=band_form.cleaned_data['desc'],
                                           created_by=request.user
                                           )
            for genre in band_form.cleaned_data['genre']:
                genre_obj = Genre.objects.get(genre=genre)
                band_obj.genre.add(genre_obj)

            sub = 'Join {}'.format(band_name)

            for mem in memberformset:
                to_list = []
                inst = mem.cleaned_data['instrument']
                BandMember.objects.create(band=band_obj,
                                          member=mem.cleaned_data['member'],
                                          instrument=inst,
                                          type=mem.cleaned_data['type']
                                          )
                to_list.append(SocialAccount.objects.get(user_id=mem.cleaned_data['member'].pk).extra_data['email'])
                msg = 'Hey, You are invited to join {} at MakeMyBand to play {}, Please click link to Join this band'.format(
                    band_name, inst)
                send_multiple_mail(sub, msg, '', to_list)
            return HttpResponse("Do something")
        else:
            print band_form.errors, memberformset.errors

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
        import ipdb;ipdb.set_trace()
        if vacancy_form.is_valid():
            band_obj = Band.objects.get(id=band_id)
            BandVacancy.objects.create(band=band_obj,
                                       instrument=vacancy_form.cleaned_data['instrument'],
                                       type=vacancy_form.cleaned_data['type']
                                      )
        else:
            print vacancy_form.errors

    return render_to_response(template,
                              {'form': vacancy_form},
                              context_instance=RequestContext(request)
                              )


def invite_user(request, band_id):
    pass
    # send_mail('Subject here', 'Here is the message.', 'ajay.singh1@delhivery.com', ['ajayk40@gmail.com'])

