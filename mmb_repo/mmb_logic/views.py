import json

from django.http import *
from functools import wraps
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader

from mmb_repo.users.models import *
from mmb_repo.mmb_data.models import *


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        result = json.dumps({'not_authenticated': True})
        return HttpResponse(result, 'application/json')

    return wrapper


def category_search(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_location(request):
    data = None
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=q)[:20]
        print "query result "
        print users
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username

            results.append(user_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@ajax_login_required
def inc_likes(request):
    success = False
    mimetype = 'application/json'
    print request.POST.get('song_id')
    if request.is_ajax():
        song_id = request.GET.get('song_id').split('_')[1]
        song_obj = Song.objects.get(id=song_id)
        song_obj.likes += 1
        song_obj.save()
        SongLike.objects.create(user=request.user, song=song_obj)
        success = True

    return HttpResponse(json.dumps({'success': success, 'like_count': song_obj.likes}), mimetype)
