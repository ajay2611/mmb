# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import urllib

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from braces.views import LoginRequiredMixin
from django.core.exceptions import ValidationError

from mmb_repo.mmb_data.models import Genre, Instrument
from config.settings.common import STATIC_URL
from allauth.socialaccount.models import SocialAccount
from mmb_repo.mmb_data.models import Genre, Instrument, Song

from .forms import UserForm, ProfileDataForm, ChangePasswordForm, UploadSongForm
from .models import User, Profile
from .utils import handle_uploaded_file


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


def edit_profile(request):
    template = 'users/profile_form.html'
    pk = request.user.pk
    socialaccount_obj = SocialAccount.objects.filter(user_id=pk)
    picture_url = None
    try:
        picture_url = socialaccount_obj[0].get_provider_account().get_avatar_url()
    except:
        pass
    try:
        urllib.urlretrieve(picture_url, 'mmb_repo/static/images/profile/' + str(pk))
    except:
        pass

    try:
        instance = Profile.objects.get(user__id=pk)
    except:
        instance = None

    if request.method == 'POST':
        form = ProfileDataForm(request.POST, instance=instance)
        if form.is_valid():
            user = get_user_model().objects.get(id=pk)
            username = form.cleaned_data['username']
            website = form.cleaned_data['website']
            phone = form.cleaned_data['phone']
            about_me = form.cleaned_data['about_me']
            college = form.cleaned_data['college']
            current_city = form.cleaned_data['current_city']
            instruments = form.cleaned_data['instrument']
            genres = form.cleaned_data['genre']
            following_count = 0
            followed_by_count = 0
            import ipdb;ipdb.set_trace()
            kwargs = {'college': college, 'website': website, 'phone': phone, \
                      'about_me': about_me, 'current_city': current_city}
            if instance:
                instance.genre.clear()
                instance.instrument.clear()
                instance.update(**kwargs)
                for i in genres:
                    obj = Genre.objects.get(genre=i)
                    instance.genre.add(obj)
                for i in instruments:
                    it = Instrument.objects.get(instrument=i)
                    instance.instrument.add(it)
            else:

                profile_obj = Profile(user=user, website=website, phone=phone, \
                                      about_me=about_me, college=college, current_city=current_city,
                                      )
                profile_obj.save()
                for i in genres:
                    obj = Genre.objects.get(genre=i)
                    profile_obj.genre.add(obj)
                for i in instruments:
                    it = Instrument.objects.get(instrument=i)
                    profile_obj.instrument.add(it)

            user.username = username
            user.save()

            return HttpResponseRedirect('/users/profile/' + str(username))

    else:

        if instance:
            form = ProfileDataForm(initial={'username': instance.user.username,
                                            'instrument': instance.instrument.get_queryset(),
                                            'genre': instance.genre.get_queryset(),
                                            'website': instance.website,
                                            'about_me': instance.about_me,
                                            'phone': instance.phone,
                                            'college': instance.college,
                                            'current_city': instance.current_city})
        else:
            form = ProfileDataForm()

    return render_to_response(template,
                              {'form': form, 'edit_profile': "active"},
                              context_instance=RequestContext(request)
                              )


def view_profile(request, username):
    template = 'users/profile.html'
    if request.method == 'GET':
        user = User.objects.get(username=username)
        details = Profile.objects.get(user__id=user.id)
        try:
            playlist = Song.objects.filter(user__id=user.id)
        except:
            playlist = None
    else:
        template = '404.html'
    # import ipdb;ipdb.set_trace()
    return render_to_response(template,
                              {'my_audio': "active", 'user': user, 'playlist': playlist, \
                               'details': details, 'STATIC_URL': STATIC_URL},
                              context_instance=RequestContext(request)
                              )


def change_password(request):
    """
    :param request:
    :return:
    """
    template = 'users/profile_form.html'
    form = ChangePasswordForm()

    if request.method == 'POST':
        pk = request.user.pk
        if form.is_valid():
            password = form.cleaned_data['passwrord']
            user = get_user_model().objects.get(id=pk)
            username = user.username
            user.set_password = password
            user.save()
            return HttpResponseRedirect('/users/profile/' + str(username))

    else:
        form = ChangePasswordForm()

    return render_to_response(template,
                              {'form': form, 'change_password': "active"},
                              context_instance=RequestContext(request)
                              )


@csrf_exempt
def upload_song(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    template = 'users/profile.html'
    user = User.objects.get(username=username)
    details = Profile.objects.get(user__id=user.id)

    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            return HttpResponseRedirect('/users/profile/' + str(username))

    else:
        form = UploadSongForm()

    return render_to_response(template, {'form': form, 'upload_song': "active", 'user': user, \
                                         'details': details, 'STATIC_URL': STATIC_URL},
                              context_instance=RequestContext(request))
