
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from braces.views import LoginRequiredMixin

from .forms import UserForm, ProfileDataForm
from .models import User, Genre


def edit_profile(request):
    success = False
    template = 'users/profile_form.html'
    if request.method == 'POST':
        form = ProfileDataForm(request.POST)
        # pk = request.user.pk
        if form.is_valid():
            username = form.cleaned_data['username']
            get_user_model().objects.create_user(username=username)

            return HttpResponseRedirect('//'('show_profile'))
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

