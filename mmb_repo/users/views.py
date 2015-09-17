# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError

from braces.views import LoginRequiredMixin

from .forms import UserForm, ProfileDataForm
from .models import User, Genre


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
    success = False
    template = 'users/profile_form.html'
    if request.method == 'POST':
        profile_data_form = ProfileDataForm(request.POST)
        if profile_data_form.is_valid():
            profile_data_form.save()
            success = True
    else:
        form = ProfileDataForm()
    return render_to_response(template,
                              {'form': form, 'success': success},
                              context_instance=RequestContext(request)
                              )


def view_profile(request, user_id):
    template = 'users/profile.html'
    if request.method == 'GET':
        data = User.objects.filter(id=1) #replace with user_id
    else:
        template = '404.html'
    return render_to_response(template, {'data': data})