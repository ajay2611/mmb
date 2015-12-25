from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError


def create_band(request):
    template = 'users/profile_form.html'
    pk = request.user.pk

    return render_to_response(template, {'form': pk}, context_instance=RequestContext(request))