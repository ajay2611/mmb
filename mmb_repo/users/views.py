# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from braces.views import LoginRequiredMixin
from .forms import UserForm, ProfileDataForm, ChangePasswordForm
from .models import User,Profile
from mmb_repo.mmb_data.models import Genre, Instrument
from config.settings.common import STATIC_URL



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
    user = request.user
    try:
        instance = Profile.objects.get(user__id = pk)
    except:
        instance = None

    if request.method == 'POST':
        form= ProfileDataForm(request.POST,instance=instance)
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
            kwargs = {'college':college, 'website':website, 'phone':phone, \
                      'about_me':about_me, 'current_city':current_city}
            if instance:
                instance.genre.clear()
                instance.instrument.clear()
                instance.update(**kwargs)
                for i in genres:
                    obj=Genre.objects.get(genre=i)
                    instance.genre.add(obj)
                for i in instruments:
                    it=Instrument.objects.get(instrument=i)
                    instance.instrument.add(it)
            else:

                profile_obj=Profile(user=user,website=website,phone=phone,\
                                    about_me=about_me,college=college,current_city=current_city)
                profile_obj.save()
                for i in genres:
                    obj=Genre.objects.get(genre=i)
                    profile_obj.genre.add(obj)
                for i in instruments:
                    it=Instrument.objects.get(instrument=i)
                    profile_obj.instrument.add(it)

            user.username = username
            user.save()

            return HttpResponseRedirect('/users/profile/'+str(username))

    else:

        if instance:
            form = ProfileDataForm(initial={'username':instance.user.username,
                                            'instrument':instance.instrument.get_queryset(),
                                            'genre':instance.genre.get_queryset(),
                                            'website':instance.website,
                                            'about_me':instance.about_me,
                                            'phone':instance.phone,
                                            'college':instance.college,
                                            'current_city':instance.current_city})
        else:
            form= ProfileDataForm()


    return render_to_response(template,
                              {'form': form, 'edit_profile': "active"},
                              context_instance=RequestContext(request)
                              )


def view_profile(request, username):
    template = 'users/profile.html'
    if request.method == 'GET':
        user = User.objects.get(username=username)
        details = Profile.objects.get(user__id = user.id)
    else:
        template = '404.html'
    return render_to_response(template, {'my_audio':"active", 'user': user ,\
                                         'details':details, 'STATIC_URL':STATIC_URL})


def change_password(request):
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
            return HttpResponseRedirect('/users/profile/'+str(username))
    else:
        form = ChangePasswordForm()

    return render_to_response(template,
                              {'form': form, 'change_password': "active"},
                              context_instance=RequestContext(request)
                              )




# def show_audio(request):
#     template = 'users/profile.html'
#     return render_to_response(template, {'STATIC_URL':STATIC_URL})

