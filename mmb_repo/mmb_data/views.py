from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError

from .forms import UserForm, ProfileDataForm, ChangePasswordForm
from .models import User, Genre, Profile

